from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from . import tables
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_tables2 import SingleTableMixin,MultiTableMixin
from django.urls import reverse_lazy
from django_filters.views import FilterView
from userman.models import tim_lelang, bidder_perwakilan, bidder, bidder_user
from adm_lelang.models import auctioner_lelang, bidder_lelang, item_lelang, detail_itemlelang, jadwal_seleksi, pengumuman
from adm_lelang.forms import pengumumanForm
from persiapan.models import p_dokumen, berita_acara_persiapan
from persiapan.forms import DokumenForm,BeritaAcaraForm
from persiapan.tables import p_dokumensTable,berita_acara_persiapanTable
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils import timezone
from adm_lelang import utils
from django.views.generic.base import TemplateView
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django_renderpdf.views import PDFView
import json



# Create your views here.

@login_required
def home(request):
    return render(request, 'index_kelengkapan.html')



class form_pemeriksaan_kView(SingleTableMixin, generic.ListView):
    model = models.form_pemeriksaan
    table_class = tables.form_pemeriksaanTable
    template_name = 'tabel_form_pemeriksaan.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.form_pemeriksaan.objects.all().filter(item_lelang=self.kwargs['pk'])

class berita_acara_allView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_administrasi
    table_class = tables.berita_acaraTable
    template_name = 'tabel_berita_acara_ba.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_administrasi.objects.all().filter(item_lelang=self.kwargs['pk'])
    
class pkeikutsertaan_allView(SingleTableMixin, generic.ListView):
    model = models.permohonan_keikutsertaan
    table_class = tables.p_keikutsertaanTable
    template_name = 'tabel_p_keikutsertaan.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.permohonan_keikutsertaan.objects.all().filter(item_lelang=self.kwargs['pk'])


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def permohonan(request):
    url = "/administrasi/keikutsertaan/"
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_keikutsertaan_auctioneer.html',context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_keikutsertaan_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            #print(context)
            return render(request, 'index_keikutsertaan_auctioneer.html',context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            #print(context)
            return render(request, 'index_keikutsertaan_auctioneer.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    
    
def pemeriksaan(request):
    url = "/administrasi/kelengkapan/"
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_kelengkapan_auctioneer.html',context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_kelengkapan_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_kelengkapan_auctioneer.html',context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            #print(context)
            return render(request, 'index_kelengkapan_auctioneer.html', context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')    
    
def verifikasi(request):
    url = "/administrasi/verifikasi/"
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_verifikasi_auctioneer.html',context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_verifikasi_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_verifikasi_auctioneer.html',context)
            
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_verifikasi_auctioneer.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')        
    
def hasil_evaluasi(request):
    url = "/administrasi/evaluasi/"
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_hasil_evaluasi_auctioneer.html',context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_hasil_evaluasi_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_hasil_evaluasi_auctioneer.html',context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_hasil_evaluasi_auctioneer.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')      
    
def sanggahan(request):
    url = "/administrasi/sanggahan/"
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_sanggahan_auctioneer.html',context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_sanggahan_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_sanggahan_auctioneer.html',context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_sanggahan_auctioneer.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')       

def pengumuman(request):
    url = "/administrasi/pengumuman/"
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pengumuman_hasil_evaluasi_auctioneer.html',context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pengumuman_hasil_evaluasi_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pengumuman_hasil_evaluasi_auctioneer.html',context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pengumuman_hasil_evaluasi_auctioneer.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html') 

def akun_lelang(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            return render(request, 'index_akun_lelang_auctionner.html',context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            return render(request, 'index_akun_lelang_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            return render(request, 'index_akun_lelang_auctioneer.html',context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            return render(request, 'index_akun_lelang_auctioneer.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')    

#### TABLE-TABLE #####

    
# form pemeriksaan
class form_pemeriksaanListView(SingleTableMixin, generic.ListView):
    model = models.form_pemeriksaan 
    form_class = forms.FormPemeriksaanForm
    table_class = tables.form_pemeriksaanTable
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.form_pemeriksaan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
class form_pemeriksaan2ListView(SingleTableMixin, generic.ListView):
    model = models.form_pemeriksaan 
    form_class = forms.FormPemeriksaanForm
    table_class = tables.form_pemeriksaan2Table
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.form_pemeriksaan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
    
# form verifikasi
class form_verifikasiListView(SingleTableMixin, generic.ListView):
    model = models.form_verifikasi 
    form_class = forms.FormVerifikasiForm
    table_class = tables.form_verifikasiTable
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.form_verifikasi.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
class form_verifikasi2ListView(SingleTableMixin, generic.ListView):
    model = models.form_verifikasi 
    form_class = forms.FormVerifikasiForm
    table_class = tables.form_verifikasi2Table
    template_name = 'tabel_undangan_kelengkapan.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type =='B':
            bdr_user = bidder_user.objects.get(users = self.request.user)
            user = self.request.user
            return models.form_verifikasi.objects.all().filter(item_lelang=self.kwargs['pk'], bidder = bdr_user)
        else:
            return models.form_verifikasi.objects.all().filter(item_lelang=self.kwargs['pk'])
            
    
    
# form evaluasi
class form_evaluasiListView(SingleTableMixin, generic.ListView):
    model = models.form_evaluasi 
    form_class = forms.FormEvaluasiForm
    table_class = tables.form_evaluasiTable
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.form_evaluasi.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
class form_evaluasi2ListView(SingleTableMixin, generic.ListView):
    model = models.form_evaluasi 
    form_class = forms.FormEvaluasiForm
    table_class = tables.form_evaluasi2Table
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.form_evaluasi.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
    
# form sanggahan
class form_sanggahanListView(SingleTableMixin, generic.ListView):
    model = models.form_sanggahan 
    form_class = forms.FormSanggahanForm
    table_class = tables.form_sanggahanTable
    template_name = 'tabel_form_sanggahan.html'
    def get_queryset(self, **kwargs):
        try:
            itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
            # qs = super().get_queryset(**kwargs)
            if self.request.user.user_type =='B':
                bdr_user = bidder_user.objects.get(users = self.request.user)
            
                return models.form_sanggahan.objects.all().filter(item_lelang=itm_lelang, bidder = bdr_user).order_by('-id')
            else:
                return models.form_sanggahan.objects.all().filter(item_lelang=itm_lelang).order_by('-id')
        except:
            return []
        # return models.form_sanggahan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
class form_sanggahan2ListView(SingleTableMixin, generic.ListView):
    model = models.form_sanggahan 
    form_class = forms.FormSanggahanForm
    table_class = tables.form_sanggahan2Table
    template_name = 'tabel_form_sanggahan.html'
    def get_queryset(self, **kwargs):
        try:
            itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
            # qs = super().get_queryset(**kwargs)
            # return models.form_sanggahan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
            if self.request.user.user_type =='B':
                bdr_user = bidder_user.objects.get(users = self.request.user)
                bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
                return models.form_sanggahan.objects.all().filter(item_lelang=itm_lelang, bidder = bdr_user).order_by('-id')
            else:
                return models.form_sanggahan.objects.all().filter(item_lelang=itm_lelang).order_by('-id')
        except:
            return []
    
    
# peermohonan keikutsertaan
class permohonan_keikutsertaanListView(SingleTableMixin, generic.ListView):
    model = models.permohonan_keikutsertaan 
    form_class = forms.PermohonanKeikutsertaanForm
    table_class = tables.p_keikutsertaanTable
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_table_class(self):
        if self.request.user.user_type =='B':
            return tables.p_keikutsertaanTable
        else:
            return tables.p_keikutsertaan2Table

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        try:
            itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
            #dokumen = models.permohonan_keikutsertaan.objects.all.filter(item_lelang = itm_lelang)
            if self.request.user.user_type =='B':
                bdr_user = bidder_user.objects.get(users = self.request.user)
                bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
                return models.permohonan_keikutsertaan.objects.all().filter(item_lelang=itm_lelang, perwakilan__in = bdr_wakil).order_by('-id')
            else:
                return models.permohonan_keikutsertaan.objects.all().filter(item_lelang=itm_lelang).order_by('-id')
        except:
            return []

class permohonan_keikutsertaan2ListView(SingleTableMixin, generic.ListView):
    model = models.permohonan_keikutsertaan 
    form_class = forms.PermohonanKeikutsertaanForm
    table_class = tables.p_keikutsertaan2Table
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        try:
            itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
            #dokumen = models.permohonan_keikutsertaan.objects.all.filter(item_lelang = itm_lelang)
            if self.request.user.user_type =='B':
                bdr_user = bidder_user.objects.get(users = self.request.user)
                bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
                return models.permohonan_keikutsertaan.objects.all().filter(item_lelang=itm_lelang, perwakilan__in = bdr_wakil).order_by('-id')
            else:
                return models.permohonan_keikutsertaan.objects.all().filter(item_lelang=itm_lelang).order_by('-id')
        except:
            return []
#        return models.permohonan_keikutsertaan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
class permohonan_keikutsertaan3ListView(SingleTableMixin, generic.ListView):
    model = models.permohonan_keikutsertaan 
    form_class = forms.PermohonanKeikutsertaanForm
    table_class = tables.p_keikutsertaan3Table
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_queryset(self, **kwargs):
        itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
        if self.request.user.user_type =='B':
            bdr_user = bidder_user.objects.get(users = self.request.user)
            bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
     #       return models.permohonan_keikutsertaan.objects.all().filter(item_lelang=itm_lelang, bidder__in = bdr_wakil).exclude(pernyataan = "TIDAK_MENGIKUTI").order_by('-id')
     #   else:
     #       return models.permohonan_keikutsertaan.objects.all().filter(item_lelang=itm_lelang).order_by('-id').exclude(pernyataan = "TIDAK_MENGIKUTI").order_by('-id')
            return models.permohonan_keikutsertaan.objects.all().filter(item_lelang=itm_lelang, perwakilan__in = bdr_wakil)
        else:
            return models.permohonan_keikutsertaan.objects.all().filter(item_lelang=itm_lelang).order_by('-id')
    
# hasil evaluasi
class hasil_evaluasiListView(SingleTableMixin, generic.ListView):
    model = pengumuman
    table_class = tables.evaluasi_hasilTable
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_table_class(self):
        if self.request.user.user_type =='C':
            return tables.evaluasi_hasilTable
        else:
            return tables.evaluasi_hasilTable2
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
        #dokumen = models.hasil_evaluasi.objects.get(item_lelang = itm_lelang)
        return pengumuman.objects.all().filter(item_lelang=itm_lelang).order_by('-id')    


    
class hasil_evaluasi2ListView(SingleTableMixin, generic.ListView):
    model = models.hasil_kesimpulan
    table_class = tables.hasil_kesimpulanTable3
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type =='B':
            bdr_user = bidder_user.objects.get(users = self.request.user)
            user = self.request.user
            return models.hasil_kesimpulan.objects.all().filter(item_lelang=self.kwargs['pk'], bidder = bdr_user)
        else:
            coba = models.hasil_kesimpulan.objects.all().filter(item_lelang=self.kwargs['pk'], hasil_pemeriksaan=True)
            #print(coba)
            return models.hasil_kesimpulan.objects.all().filter(item_lelang=self.kwargs['pk'], hasil_pemeriksaan=True)
    
class hasil_evaluasi3ListView(SingleTableMixin, generic.ListView):
    model = models.hasil_kesimpulan
    table_class = tables.hasil_kesimpulanTable
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.hasil_kesimpulan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
        #return models.form_evaluasi.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')

class hasil_evaluasi4ListView(SingleTableMixin, generic.ListView):
    model = models.hasil_kesimpulan
    #model = models.form_evaluasi
    table_class = tables.hasil_kesimpulanTable3
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.hasil_kesimpulan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
#        return models.hasil_sementara.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
        #models.form_evaluasi.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')

class pengumuman_hasil_evaluasiListView(SingleTableMixin, generic.ListView):
    model = pengumuman
    table_class = tables.evaluasi_hasilTable
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_table_class(self):
        if self.request.user.user_type =='C':
            return tables.evaluasi_hasilTable
        else:
            return tables.evaluasi_hasilTable2
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
        #dokumen = models.hasil_evaluasi.objects.get(item_lelang = itm_lelang)
        return pengumuman.objects.all().filter(item_lelang=itm_lelang).order_by('-id')   
    
# ba Administrasi
class ba_administrasiListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_administrasi 
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acaraTable
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_administrasi.objects.all().filter(item_lelang=self.kwargs['pk'], owner=self.kwargs['code']).order_by('-id')
    
class ba_administrasi2ListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_administrasi 
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara2Table
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_administrasi.objects.all().filter(item_lelang=self.kwargs['pk'], owner=self.kwargs['code']).order_by('-id')

# Jawaban Sanggahan
class jawaban_sanggahanListView(SingleTableMixin, generic.ListView):
    model = models.jawaban_sanggahan 
    form_class = forms.JawabanSanggahanForm
    table_class = tables.jawaban_sanggahanTable
    template_name = 'tabel_jawaban_sanggahan.html'
    def get_table_class(self):
        if self.request.user.user_type =='C':
            return tables.jawaban_sanggahanTable
        elif self.request.user.user_type =='A':
            return tables.jawaban_sanggahanTable
        else:
            return tables.jawaban_sanggahan2Table
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        # itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
        #dokumen = models.permohonan_keikutsertaan.objects.all.filter(item_lelang = itm_lelang)
        # if self.request.user.user_type =='B':
        #     bdr_user = bidder_user.objects.get(users = self.request.user)
        #     bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
        #     return models.jawaban_sanggahan.objects.all().filter(item_lelang=itm_lelang, bidder = bdr_user.bidder).order_by('-id')
        # else:
        #     return models.jawaban_sanggahan.objects.all().filter(item_lelang=itm_lelang).order_by('-id')
        return models.jawaban_sanggahan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
class jawaban_sanggahan2ListView(SingleTableMixin, generic.ListView):
    model = models.jawaban_sanggahan 
    form_class = forms.JawabanSanggahanForm
    table_class = tables.jawaban_sanggahan2Table
    template_name = 'tabel_jawaban_sanggahan.html'
    def get_queryset(self, **kwargs):
        # qs = super().get_queryset(**kwargs)
        itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
        # bdr_user = bidder_user.objects.get(users = self.request.user)
        # bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
        # return models.jawaban_sanggahan.objects.all().filter(item_lelang=itm_lelang).order_by('-id')
        #dokumen = models.permohonan_keikutsertaan.objects.all.filter(item_lelang = itm_lelang)
        if self.request.user.user_type =='B':
            bdr_user = bidder_user.objects.get(users = self.request.user)
            #print(itm_lelang.id)
            #print(bdr_user.bidder.id)
            # bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
            return models.jawaban_sanggahan.objects.all().filter(item_lelang=itm_lelang, bidder = bdr_user.id).order_by('-id')
        else:
            return models.jawaban_sanggahan.objects.all().filter(item_lelang=itm_lelang).order_by('-id')

        # if self.request.user.user_type =='B':
        #     bdr_user = bidder_user.objects.get(users = self.request.user)
        #     bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
        #     return models.form_sanggahan.objects.all().filter(item_lelang=itm_lelang, bidder__in = bdr_wakil).order_by('-id')
        # else:
        #     return models.form_sanggahan.objects.all().filter(item_lelang=itm_lelang).order_by('-id')


# FORM SECTION #
class form_pemeriksaanCreateView(BSModalCreateView):

    template_name = 'modal_form_penyerahan_dan_pemeriksaan_kelengkapan.html'
    form_class = forms.FormPemeriksaanForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            "item_lelang": self.kwargs["pk"],
        })        
        return initial
    
class form_verifikasiCreateView(BSModalCreateView):

    template_name = 'modal_form_verifikasi_permohonan.html'
    form_class = forms.FormVerifikasiForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class form_evaluasiCreateView(BSModalCreateView):

    template_name = 'modal_form_evaluasi_permohonan.html'
    form_class = forms.FormEvaluasiForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {
            "item_lelang": self.kwargs["pk"],
        }
    
class form_sanggahanCreateView(BSModalCreateView):

    template_name = 'modal_form_sanggahan.html'
    form_class = forms.FormSanggahanForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        user = self.request.user
        bdr = bidder_user.objects.get(users__id = user.id)
        # return {"item_lelang": self.kwargs["pk"]}
        initial = ({
            'item_lelang': self.kwargs["pk"],
            # 'bidder': self.request.user.id,
            'bidder': bdr,
            # 'bdr': bdr,
        })
        return initial
#END SECTION #

# api
def api_check_keikutsertaan(request, pk):
    if request.user.is_authenticated:
        if request.method == 'GET':
            itm_lelang = item_lelang.objects.get(pk = pk)
            bdr_user = bidder_user.objects.get(users = request.user)
            bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
            count = models.permohonan_keikutsertaan.objects.filter(item_lelang=itm_lelang, perwakilan__in=bdr_wakil).count()

            return JsonResponse(count, safe=False)
# 

def api_check_sanggahan(request, pk):
    if request.user.is_authenticated:
        if request.method == 'GET':
            itm_lelang = item_lelang.objects.get(pk = pk)
            bdr_user = bidder_user.objects.get(users = request.user.id)
           
            count= models.form_sanggahan.objects.values("bidder").filter(item_lelang=itm_lelang, bidder = bdr_user).count()
            #count =  models.form_verifikasi.objects.all().filter(item_lelang=itm_lelang, bidder=bdr_user).count()
            
            return JsonResponse(count, safe=False)
# 
# OTHER SECTION #
class jawaban_sanggahanCreateView(BSModalCreateView):

    template_name = 'modal_jawaban_sanggahan.html'
    form_class = forms.JawabanSanggahanForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class permohonan_keikutsertaanCreateView(BSModalCreateView):

    template_name = 'modal_permohonan_keikutsertaan.html'
    form_class = forms.PermohonanKeikutsertaanForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        user = self.request.user
        bdr = bidder_user.objects.get(users__id = user.id)
        # return {"item_lelang": self.kwargs["pk"]}
        initial = ({
            'item_lelang': self.kwargs["pk"],
            'bidder': bdr,
        })
        return initial
    
class hasil_evaluasiCreateView(BSModalCreateView):

    template_name = 'modal_upload_pengumuman_hasil_evaluasi.html'
    form_class = pengumumanForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
# END SECTION #

# BA SECTION # 
class ba_penyerahanCreateView(BSModalCreateView):

    template_name = 'modal_ba_penyerahan_dan_pemeriksaan_kelengkapan.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class ba_permohonan_keikutsertaanCreateView(BSModalCreateView):

    template_name = 'modal_ba_permohonan_keikutsertaan.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class ba_verifikasi_permohonanCreateView(BSModalCreateView):

    template_name = 'modal_ba_verifikasi_permohonan.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
class ba_sanggahanCreateView(BSModalCreateView):

    template_name = 'modal_ba_sanggahan_evaluasi_administrasi.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class ba_hasil_evaluasiCreateView(BSModalCreateView):

    template_name = 'modal_ba_hasil_evaluasi_administrasi.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class ba_evaluasiCreateView(BSModalCreateView):

    template_name = 'modal_ba_evaluasi_permohonan.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
# END SECTION #


#### UPDATE-UPDATE #####
# UNDANGAN SECTION #
class JawabanSanggahanUpdateView(BSModalUpdateView):
    template_name = 'modal_jawaban_sanggahan.html'
    form_class = forms.JawabanSanggahanForm
    model = models.jawaban_sanggahan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    

    
# FORM SECTION 
class FormPemeriksaanUpdateView(BSModalUpdateView):
    template_name = 'modal_form_penyerahan_dan_pemeriksaan_kelengkapan.html'
    form_class = forms.FormPemeriksaanForm
    model = models.form_pemeriksaan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    
class FormVerifikasiUpdateView(BSModalUpdateView):
    template_name = 'modal_form_verifikasi_permohonan.html'
    form_class = forms.FormVerifikasiForm
    model = models.form_verifikasi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial

from django.template.loader import render_to_string

class FormEvaluasiUpdateView(BSModalUpdateView):
    template_name = 'modal_form_evaluasi_permohonan.html'
    form_class = forms.FormEvaluasiForm
    model = models.form_evaluasi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fe = models.form_evaluasi.objects.get(pk=self.kwargs['pk'])
        bidder = fe.bidder
        itm_llg = fe.item_lelang
        frm = models.hasil_kesimpulan.objects.filter(bidder=bidder, item_lelang=itm_llg)
        tbls = tables.hasil_kesimpulanTable3(frm)
        print(tbls)
        html = render_to_string("evaluasi_tables.html",{"table":tbls})
        context['html'] = html
        return context
    
class FormSanggahanUpdateView(BSModalUpdateView):
    template_name = 'modal_form_sanggahan.html'
    form_class = forms.FormSanggahanForm
    model = models.form_sanggahan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
# END SECTION

# OTHER SECTION #
class PermohonanKeikutsertaanUpdateView(BSModalUpdateView):
    template_name = 'modal_permohonan_keikutsertaan2.html'
    form_class = forms.PermohonanKeikutsertaanForm
    model = models.permohonan_keikutsertaan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    
class hasil_evaluasiUpdateView(BSModalUpdateView):
    template_name = 'modal_upload_pengumuman_hasil_evaluasi.html'
    form_class = pengumumanForm
    model = pengumuman
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
# END SECTION #  

# BA SECTION #
class ba_penyerahanUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_penyerahan_dan_pemeriksaan_kelengkapan.html'
    form_class = forms.BeritaAcaraForm
    model = models.berita_acara_administrasi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class ba_permohonan_keikutsertaanUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_permohonan_keikutsertaan.html'
    form_class = forms.BeritaAcaraForm
    model = models.berita_acara_administrasi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class ba_verifikasi_permohonanUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_verifikasi_permohonan.html'
    form_class = forms.BeritaAcaraForm
    model = models.berita_acara_administrasi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class ba_sanggahanUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_sanggahan_evaluasi_administrasi.html'
    form_class = forms.BeritaAcaraForm
    model = models.berita_acara_administrasi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class ba_hasil_evaluasiUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_hasil_evaluasi_administrasi.html'
    form_class = forms.BeritaAcaraForm
    model = models.berita_acara_administrasi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class ba_evaluasiUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_evaluasi_permohonan.html'
    form_class = forms.BeritaAcaraForm
    model = models.berita_acara_administrasi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'item_lelang': self.kwargs['id'],
        })

        return initial
# END SECTION #

# pdf  permohonan keikutsertaan
class PdfsView_keikutsertaan(PDFView):

    template_name = 'bukti_pengambilan_permohonan.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context = {}
        try:
            dokumen = models.permohonan_keikutsertaan.objects.get(pk=kwargs['pk'])
            if dokumen:
                context['tanggal']= dokumen.created
                context['bidder']= dokumen.perwakilan
                context['perusahaan']= dokumen.bidder
                itm_lelang = item_lelang.objects.get(pk=dokumen.item_lelang.id)
                context['seleksi'] = itm_lelang.nama_lelang
            return context
        except:
            context['tanggal']= ''
            context['bidder']= {}
            context['perusahaan']= {}
            context['seleksi'] = ''
            return context
