from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from . import tables
from userman.models import tim_lelang, bidder_perwakilan, bidder
from adm_lelang.models import auctioner_lelang, bidder_lelang, item_lelang
from adm_lelang import utils
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db import connection
from django.template.loader import render_to_string
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.utils import timezone
from persiapan.models import p_dokumen
from persiapan.forms import DokumenForm
from persiapan.tables import p_dokumensTable
from datetime import datetime


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            return render(request, 'index_smra.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            return render(request, 'index_smra_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            return render(request, 'index_smra.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')   

def dashboard_bidder(request):
    if request.user.is_authenticated:
        # check company
        context = {}
        user = request.user
        vbidder_perwakilan = bidder_perwakilan.objects.all().filter(users_id = user.id)
        if vbidder_perwakilan:
            bidder_id = vbidder_perwakilan[0].bidder_id
            vbidder = bidder.objects.all().filter(id = bidder_id)
            context["bidder"] = vbidder
            vbidder_lelang = bidder_lelang.objects.all().filter(bidder = bidder_id)
            context["bidder_lelang"] = vbidder_lelang
            context["bidder_id"] = bidder_id
            context["ip_address"] = get_client_ip(request)
            print(context)
            return render(request, 'dash_bidder_smra.html', context)
        else:
            return redirect( '/')
    else:
        return redirect( '/')

def dashboard_auctioner(request):
    if request.user.is_authenticated:
        # check company
        context = {}
        user = request.user
        vauctioner1 = tim_lelang.objects.all().filter(users = user.id)
        if vauctioner1:
            auctioner_id = vauctioner1[0].id
            vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id)
            context["auctioner"] = vauctioner
            print(context)
            return render(request, 'dash_auctioner_smra.html', context)
        else:
            return redirect( '/')
    else:
        return redirect( '/')

def jadwal(request):
    context ={}
    if request.user.is_authenticated:
        if request.GET.get("id"):
            id = request.GET.get("id")
            if request.GET.get("edit"):
                data = get_object_or_404(models.round_schedule_smra, item = id)
                form = forms.jadwalSMRAForm(instance=data)
                context["form"] = form
                #print(render_to_string("smra_jadwal_form.html", context))
                return render(request, "smra_jadwal_form.html", context)
            else:
                form = forms.jadwalSMRAForm({"item":id})
                return render(request, "smra_jadwal_form.html", {"form": form})        
    else:
        return redirect( '/')


class bidderLelangCreateView(BSModalCreateView):
    template_name = 'modal_bidderlelang.html'
    form_class = forms.bidderLelangForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}


class auctionerLelangCreateView(BSModalCreateView):
    template_name = 'modal_auctionerlelang.html'
    form_class = forms.auctionerLelangForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class viewerLelangCreateView(BSModalCreateView):
    template_name = 'modal_viewerlelang.html'
    form_class = forms.viewerLelangForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class round_scheduleListView(SingleTableMixin, generic.ListView):
    model = models.round_schedule_smra
    table_class = tables.round_scheduleTable
    template_name = 'table_detail_itemlelang.html'
    table_pagination = False

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
#        dt = timezone.now()
        dt = timezone.localtime()
        hari = str(timezone.localtime().today().isoweekday())
        return models.round_schedule_smra.objects.all().filter(item=self.kwargs['pk'],hari=hari, mulai__gte = datetime.strptime(dt.strftime("%H:%M"),"%H:%M")).order_by('hari')
        #.filter(mulai__gte=dt).order_by('mulai')

class round_schedule2ListView(SingleTableMixin, generic.ListView):
    model = models.round_schedule_smra
    table_class = tables.round_scheduleTable2
    template_name = 'table_detail_itemlelang.html'
    table_pagination = False
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        dt = timezone.localtime()
        hari = str(timezone.localtime().today().isoweekday())

#        dt = timezone.now()
        return models.round_schedule_smra.objects.all().filter(item=self.kwargs['pk'], hari=hari, mulai__gte = datetime.strptime(dt.strftime("%H:%M"),"%H:%M")).order_by('hari')

class round_scheduleCreateView(BSModalCreateView):
    template_name = 'modal_round_schedule.html'
    form_class = forms.jadwalSMRAForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item": self.kwargs["pk"]}

class round_scheduleUpdateView(BSModalUpdateView):
    template_name = 'modal_round_schedule.html'
    form_class = forms.jadwalSMRAForm
    model = models.round_schedule_smra
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"id": self.kwargs["pk"]}

# undangan

    #model = models.p_dokumen 
    #form_class = forms.DokumenForm
    #table_class = tables.p_dokumensTable
    #template_name = 'tabel_persiapan.html'
    #def get_queryset(self, **kwargs):
    #    qs = super().get_queryset(**kwargs)
    #    return p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'],tahapan=4).order_by('-id')

class undangan_smra_ccaListView(SingleTableMixin, generic.ListView):
    model = p_dokumen 
    form_class = DokumenForm
    table_class = p_dokumensTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'],tahapan=64).order_by('-id')
    
class undangan_smra_cca2ListView(SingleTableMixin, generic.ListView):
    model = models.undangan_smra_cca
    table_class = tables.smra_cca_Tabel2
    template_name = 'tabel_undangan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.undangan_smra_cca.objects.all().filter(item_lelang=self.kwargs['pk'], owner=self.kwargs['code'],  bidder=self.kwargs['id'])
    
class undangan_smra_ccabidListView(SingleTableMixin, generic.ListView):
    model = models.undangan_smra_cca
    table_class = tables.smra_cca_Tabel2
    template_name = 'tabel_undangan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.undangan_smra_cca.objects.all().filter(item_lelang=self.kwargs['pk'], owner=self.kwargs['code'], bidder=self.kwargs['id'])

class undangan_smra_ccaaucListView(SingleTableMixin, generic.ListView):
    model = models.undangan_smra_cca
    table_class = tables.smra_cca_Tabel2
    template_name = 'tabel_undangan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.undangan_smra_cca.objects.all().filter(item_lelang=self.kwargs['pk'], owner=self.kwargs['code'], auctioneer=self.kwargs['id'])
    
# smra
class undangan_smraCreateView(BSModalCreateView):

    template_name = 'modal_undangan_pengambilan_dokumen.html'
    form_class = DokumenForm
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"], "tahapan": 64}
    
class undangan_smraUpdateView(BSModalUpdateView):
    template_name = 'modal_undangan_smra.html'
    form_class = forms.undangan_smra_ccaForm
    model = models.undangan_smra_cca
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial