from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from . import models
from . import forms
from . import utils
from userman.models import tim_lelang, bidder_perwakilan, bidder
from adm_lelang.models import auctioner_lelang, bidder_lelang, item_lelang
#from smra.models import bidding_round_smra, round_schedule_smra
from adm_lelang.models import bidder_lelang, item_lelang, detail_itemlelang
from django.utils import timezone
import json
from django.conf import settings
from xhtml2pdf import pisa
from django_eventstream import send_event
import requests

def ws_publish2(data):
    json_data = json.dumps(data)
    response = requests.post("https://simulasi.spectrum-eauctions.id/smra2/push_message/", data=json_data)

def ws_publish(data):
    send_event("bidder", "message", data)
    send_event("auctioneer", "message", data)

def ws_publish_bidder(item, data):
    
    send_event("bidder_" + str(item), "message", data)

def ws_publish_auctioneer(data):
# def ws_publish_auctioneer(item, data):
    # send_event("auctioneer_" + str(item), "message", data)
    
    send_event("auctioneer", "message", data)

def rebuild_hasil(item, round, mulai_selesai):
    skip = False
    if mulai==None:
        skip = True

    m = models.hasil2_smra.objects.all().filter(item=item, round = round, valid=True, berlaku=True).order_by("-price", "submit")
    i = 1
    for a in m:
        a.ranking_putaran = i
        if not skip:
            a.mulai = mulai
            a.selesai = selesai
        a.save()
        i = i + 1

def rebuild_hasil1(item, round, mulai, selesai):
    skip = False
    if mulai==None:
        skip = True

    m = models.hasil2_smra.objects.all().filter(item=item, round = round, valid=True, berlaku=True).order_by("-price", "submit")
    i = 1
    for a in m:
        a.ranking_putaran = i
        if not skip:
            a.mulai = mulai
            a.selesai = selesai
        a.save()
        i = i + 1

def rebuild_hasil_akhir(item):
    m = models.hasil2_smra.objects.all().filter(item=item, valid=True, berlaku=True).order_by("-price", "submit")
    i = 1
    for a in m:
        a.ranking = i
        a.save()
        i = i + 1


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
