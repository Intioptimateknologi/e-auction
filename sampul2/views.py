from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import tables
from . import forms
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from adm_lelang import utils
from smra.models import undangan_smra_cca
from userman.models import tim_lelang, bidder_perwakilan, bidder, bidder_user
from adm_lelang.models import auctioner_lelang, bidder_lelang, item_lelang, detail_itemlelang, jadwal_seleksi
from persiapan.models import p_dokumen, berita_acara_persiapan
from persiapan.forms import DokumenForm,BeritaAcaraForm
from persiapan.tables import p_dokumensTable,berita_acara_persiapanTable
from django.utils import timezone
from datetime import datetime, timedelta

@login_required
def home (request):
    
    return render(request, 'index_sampul2.html')

def evaluasi_penawaran(request,pk):
    if request.user.is_authenticated:
        url = "/sampul2/evaluasi_penawaran/"    
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"],pk)
            context.update(tabs)
            return render(request, 'index_evaluasi_sampul2_auctioneer.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"],pk)
            context.update(tabs)
            return render(request, 'index_evaluasi_sampul2_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"],pk)
            context.update(tabs)
            return render(request, 'index_evaluasi_sampul2_auctioneer.html', context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"],pk)
            context.update(tabs)
            return render(request, 'index_evaluasi_sampul2_auctioneer.html', context)
        else:  
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')


    
def penawaran(request,pk):
    url = "/sampul2/penawaran/"    
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"],pk)
            context.update(tabs)
            return render(request, 'index_sampul2_auctioneer.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"],pk)
            context.update(tabs)
            return render(request, 'index_sampul2_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"],pk)
            context.update(tabs)
            return render(request, 'index_sampul2_auctioneer.html', context)  
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"],pk)
            context.update(tabs)
            return render(request, 'index_sampul2_auctioneer.html', context)  
        else:  
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')

def setting(request,pk):
    if request.user.is_authenticated:
        url = "/sampul2/setting/"    
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"],pk)
            context.update(tabs)
            return render(request, 'setting_sampul2.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"],pk)
            context.update(tabs)
            return render(request, 'setting_sampul2.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"],pk)
            context.update(tabs)
            return render(request, 'setting_sampul2.html', context)  
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewer(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'setting_sampul2.html', context)  
        else:  
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')

# pengumuman seleksi
class PenawaranCreateView(BSModalCreateView):
    template_name = 'modal_penyampaian_penawaran.html'
    form_class = forms.PenawaranForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item": self.kwargs["pk"]}

class PenawaranUpdateView(BSModalUpdateView):
    template_name = 'modal_penyampaian_penawaran.html'
    form_class = forms.PenawaranForm
    model = models.penawaran
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial

class EvaluasiPenawaranCreateView(BSModalCreateView):
    template_name = 'modal_evaluasi_penawaran.html'
    form_class = forms.EvaluasiPenawaranForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item": self.kwargs["pk"]}

class EvaluasiPenawaranUpdateView(BSModalUpdateView):
    template_name = 'modal_evaluasi_penawaran.html'
    form_class = forms.EvaluasiPenawaranForm
    model = models.evaluasi_penawaran
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial

class ObyekSeleksiCreateView(BSModalCreateView):
    template_name = 'obyek_seleksi_sampul2.html'
    form_class = forms.obyek_seleksiForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item": self.kwargs["pk"]}

class ObyekSeleksiUpdateView(BSModalUpdateView):
    template_name = 'obyek_seleksi_sampul2.html'
    form_class = forms.obyek_seleksiForm
    model = models.obyek_seleksi_sampul2
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial


class obselListView(SingleTableMixin, generic.ListView):
    model = models.obyek_seleksi_sampul2
    table_class = tables.obyek_seleksiTable
    template_name = 'table_p_penawaran.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.obyek_seleksi_sampul2.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])


class verifikasiPenawaranUpdateView(BSModalUpdateView):
    template_name = 'modal_verifikasi_penawaran.html'
    form_class = forms.verifikasi_penawaranForm
    model = models.penawaran
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    
class penawaranListView(SingleTableMixin, generic.ListView):
    model = models.penawaran
    table_class = tables.penawaranTable
    template_name = 'table_p_penawaran.html'
    def get_table_class(self):
        if self.request.user.user_type == "B":
            return tables.penawaran2Table
        else:
            return tables.penawaranTable
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type == 'B':
            return models.penawaran.objects.all().filter(item__item_lelang__id=self.kwargs['pk'], bidder__users__id=self.request.user.id)
        else:
            return models.penawaran.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])

class hasil_pemasukanPenawaranListView(SingleTableMixin, generic.ListView):
    model = models.penawaran
    table_class = tables.hasil_penawaranTable
    template_name = 'table_p_penawaran.html'

    def get_table_class(self):
        if self.request.user.user_type == "B":
            return tables.hasil_penawaran2Table
        else:
            return tables.hasil_penawaranTable

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type == 'B':
            return models.penawaran.objects.all().filter(item__item_lelang__id=self.kwargs['pk'], bidder__users__id=self.request.user.id)
        else:
            return models.penawaran.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])


class evaluasiPenawaranListView(SingleTableMixin, generic.ListView):
    model = models.evaluasi_penawaran
    table_class = tables.evaluasi_penawaranTable
    template_name = 'table_p_penawaran.html'
    def get_table_class(self):
        if self.request.user.user_type == "B":
            return tables.evaluasi_penawaran2Table
        else:
            return tables.evaluasi_penawaranTable
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type == 'B':
            return models.evaluasi_penawaran.objects.all().filter(penawaran__item__item_lelang__id=self.kwargs['pk'], penawaran__bidder__users__id=self.request.user.id)
        else:
            return models.evaluasi_penawaran.objects.all().filter(penawaran__item__item_lelang__id=self.kwargs['pk'])
            
    
class hasil_sampul2ListView(SingleTableMixin, generic.ListView):
    model = models.hasil_sampul2
    table_class = tables.hasil_sampul2Table
    template_name = 'table_p_penawaran.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if  self.request.user.user_type == 'C':
            return models.hasil_sampul2.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).order_by('item','ranking')
        #penambahan untuk bidder karna tidak ada
        else:
            return models.hasil_sampul2.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).order_by('item','ranking')