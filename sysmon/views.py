from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from django.db import connection, transaction
from django_tables2 import SingleTableMixin

import requests
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
import json
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.shortcuts import render,redirect, get_object_or_404
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django_renderpdf.views import PDFView
from django.utils import timezone
from collections import namedtuple
from django.contrib.humanize.templatetags.humanize import intcomma
from userman.models import Users
from django.contrib.sessions.models import Session
from psutil import AccessDenied

def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return Users.objects.filter(id__in=uid_list)

cpuTuple = namedtuple('cpuTuple',
                      'core, used')

memTuple = namedtuple('memTuple',
                      'total, used')

diskPartTuple = namedtuple('diskPartTuple',
                           'device, mountpoint, fstype, total, percent')

networkTuple = namedtuple('networkTuple',
                          'device, sent, recv, pkg_sent, pkg_recv')

processTuple = namedtuple('processTuple',
                          'pid, name, status, user, memory')


def bytes2human(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

def tofloat(value):
    try:
        return float(value)
    except ValueError:
        return 0

@login_required
def dashboard(request):
    context = {}
    try:
        import psutil as pu
    except:
        context['error_psutil'] = 'not_found'
        return render(request, "dashboard_monitoring.html", context)

    # cpu
    #print(pu)
    cpu_info = cpuTuple(
        core=pu.cpu_count(),
        used=intcomma(pu.cpu_percent(), use_l10n=False))

    # memory
    mem_info = memTuple(
        total=bytes2human(pu.virtual_memory().total),
        used=intcomma(pu.virtual_memory().percent, use_l10n=False))

    # disk
    partitions = list()
    for part in pu.disk_partitions():
        partitions.append(
            diskPartTuple(
                device=part.device,
                mountpoint=part.mountpoint,
                fstype=part.fstype,
                total=bytes2human(
                    pu.disk_usage(part.mountpoint).total),
                percent=intcomma(pu.disk_usage(part.mountpoint).percent,
                                    use_l10n=False)
            )
        )

    # network
    networks = list()
    for k, v in pu.net_io_counters(pernic=True).items():
        # Skip loopback interface
        if k == 'lo':
            continue

        networks.append(
            networkTuple(
                device=k,
                sent=bytes2human(v.bytes_sent),
                recv=bytes2human(v.bytes_recv),
                pkg_sent=v.packets_sent,
                pkg_recv=v.packets_recv))

    # processes

    all_stats = {
        'cpu_info': cpu_info,
        'mem_info': mem_info,
        'partitions': partitions,
        'networks': networks,
        'users': get_all_logged_in_users,
    }
    context = all_stats
    print(context)
    return render(request, "dashboard_monitoring.html", context)
