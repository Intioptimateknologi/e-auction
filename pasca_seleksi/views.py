from django.shortcuts import render, get_object_or_404
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django_tables2 import SingleTableMixin
from django.urls import reverse_lazy
from django.views import generic
from . import models
from . import forms
from . import tables
from adm_lelang import utils
from userman.models import tim_lelang, bidder_perwakilan, bidder, bidder_user
from adm_lelang.models import auctioner_lelang, bidder_lelang, item_lelang, detail_itemlelang, jadwal_seleksi
from persiapan.models import p_dokumen, berita_acara_persiapan
from persiapan.forms import DokumenForm,BeritaAcaraForm
from persiapan.tables import p_dokumensTable,berita_acara_persiapanTable
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.humanize.templatetags.humanize import intcomma


# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def pemilihan_blok(request):
    if request.user.is_authenticated:
        url = "/pasca_seleksi/pemilihan_blok/"    
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pemilihan_block_auctioneer.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pemilihan_block_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pemilihan_block_auctioneer.html',context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pemilihan_block_auctioneer.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')   
    
    
def hasil_seleksi(request):
    if request.user.is_authenticated:
        url = "/pasca_seleksi/hasil_seleksi/"  
        if request.user.is_superuser:
            return render(request, 'index_hasil_seleksi_auctioneer.html')
        elif request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_hasil_seleksi_auctioneer.html', context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_hasil_seleksi_auctioneer.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_hasil_seleksi_bidder.html', context)
        elif request.user.user_type == 'C':
            # context = {}
            # user = request.user
            # vauctioner1 = tim_lelang.objects.all().filter(users = user.id)
            # if (vauctioner1):
            #     auctioner_id = vauctioner1[0].id
            #     if request.GET.get("id"):
            #         vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id, item_lelang=request.GET.get("id"))
            #     else:
            #         vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id).order_by('created')
            #     context["auctioner"] = vauctioner[0]
            #     context["item_lelang"] = auctioner_lelang.objects.all().filter(auctioner = auctioner_id)
            #     context['user_type'] = request.user.user_type
            #     print(context)
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_hasil_seleksi_auctioneer.html', context)  
        else:  
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')           
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    
    
def sanggahan(request):
    url = "/pasca_seleksi/sanggahan/" 
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'index_sanggahan_pc_auctioneer.html')
        elif request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request,)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_sanggahan_pc_auctioneer.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_sanggahan_pc_bidder.html', context)
        elif request.user.user_type == 'C':
                context = utils.get_judul_context_auctioneer(request)
                tabs = utils.get_tab_context2(request,url, context["item_lelang"])
                context.update(tabs)
                return render(request, 'index_sanggahan_pc_auctioneer.html', context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_sanggahan_pc_auctioneer.html',context)  
        else:  
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')           
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')


def penetapan_pemenang(request):
    url = "/pasca_seleksi/penetapan_pemenang/" 
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request,)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)            
            return render(request, 'index_penetapan_pemenang_auctioneer.html', context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)            
            return render(request, 'index_penetapan_pemenang_auctioneer.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_penetapan_pemenang_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_penetapan_pemenang_auctioneer.html', context)  
        else:  
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')           
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    
def settings(request):
    if request.user.is_authenticated:
        url = "/pasca_seleksi/settings/"    
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'setting_pemilihan_blok.html',context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'setting_pemilihan_blok.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'setting_pemilihan_blok.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'setting_pemilihan_blok.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')   

# TABLE-TABLE
class ps_u_p_blokListView(SingleTableMixin, generic.ListView):
    model = models.blok
    form_class = forms.u_pemilihan_blokForm
    table_class = tables.bloknyaTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.blok.objects.all().filter(item_lelang=self.kwargs['pk'])
    
class ps_u_p_blok2ListView(SingleTableMixin, generic.ListView):
    model = models.blok
    form_class = forms.u_pemilihan_blokForm
    table_class = tables.bloknya2Table
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.blok.objects.all().filter(item_lelang=self.kwargs['pk'], users=self.kwargs['code'])
    
    
# pemilihan blok   


class blok_pasca_seleksiListView(SingleTableMixin, generic.ListView):
    model = models.blok_pasca_seleksi
    table_class = tables.blok_pasca_seleksiTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.blok_pasca_seleksi.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])


class ps_pemilihan_blokListView(SingleTableMixin, generic.ListView):
    model = models.pemilihan_blok_pasca_seleksi
    form_class = forms.pemilihan_blok_psForm
    table_class = tables.pemilihan_bloknyaTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        pk = self.kwargs['pk']
        qs = super().get_queryset(**kwargs)
        itm_lelang = item_lelang.objects.get(pk=pk)
        return models.pemilihan_blok_pasca_seleksi.objects.all().filter(item_lelang=pk, pilih_blok=True)
    
class ps_pemilihan_blok2ListView(SingleTableMixin, generic.ListView):
    model = models.pemilihan_blok_pasca_seleksi
    form_class = forms.pemilihan_blok_psForm
    table_class = tables.pemilihan_bloknya2Table
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.pemilihan_blok_pasca_seleksi.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).order_by('item','ranking')

class ps_pemilihan_blok3ListView(SingleTableMixin, generic.ListView):
    #print('sini')
    model = models.pemilihan_blok_pasca_seleksi
    form_class = forms.pemilihan_blok_psForm
    table_class = tables.pemilihan_bloknya3Table
    template_name = 'tabel_pasca_seleksi.html'
    def get_table_class(self):
        if self.request.user.user_type=="B":
            return tables.pemilihan_bloknya4Table
        else:
            return tables.pemilihan_bloknya3Table            
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type=="B":
            b = bidder_user.objects.get(users__id = self.request.user.id)    
            hasil =  models.pemilihan_blok_pasca_seleksi.objects.all().filter(item__item_lelang__id=self.kwargs['pk'], bidder=b, pilih_blok=True).order_by('ranking')
            print(hasil)
            return hasil
        else:
            return models.pemilihan_blok_pasca_seleksi.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).order_by('ranking')

#seleksi    
class ps_seleksiListView(SingleTableMixin, generic.ListView):
    model = models.seleksi
    form_class = forms.seleksinyaForm
    table_class = tables.hasilseleksinyaTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.seleksi.objects.all().filter(item_lelang=self.kwargs['pk'])
    
class ps_seleksi2ListView(SingleTableMixin, generic.ListView):
    model = models.seleksi
    form_class = forms.seleksinyaForm
    table_class = tables.hasilseleksinya2Table
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.seleksi.objects.all().filter(item_lelang=self.kwargs['pk'])
    
    
    
#sanggahan
class ps_sanggahanListView(SingleTableMixin, generic.ListView):
    model = models.sanggahan
    form_class = forms.sanggahannyaForm
    table_class = tables.sanggahannyaTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.sanggahan.objects.all().filter(item_lelang=self.kwargs['pk'])
    
class ps_sanggahan2ListView(SingleTableMixin, generic.ListView):
    model = models.sanggahan
    form_class = forms.sanggahannyaForm
    table_class = tables.sanggahannya2Table
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.sanggahan.objects.all().filter(item_lelang=self.kwargs['pk'])
    
    
    
#sanggahan Jawaban 
class ps_sanggahan_jawabanListView(SingleTableMixin, generic.ListView):
    model = models.sanggahan_jawaban
    form_class = forms.sanggahan_jawabForm
    table_class = tables.s_jawabanTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.sanggahan_jawaban.objects.all().filter(item_lelang=self.kwargs['pk'])
    
class ps_sanggahan_jawaban2ListView(SingleTableMixin, generic.ListView):
    model = models.sanggahan_jawaban
    form_class = forms.sanggahan_jawabForm
    table_class = tables.s_jawaban2Table
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.sanggahan_jawaban.objects.all().filter(item_lelang=self.kwargs['pk'])
    
    
    
#jawaban atas sanggahan 
class ps_j_a_sanggahanListView(SingleTableMixin, generic.ListView):
    model = models.jawaban_atas_sanggahan
    form_class = forms.jawab_atas_sanggahForm
    table_class = tables.jawaban_atas_sTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.jawaban_atas_sanggahan.objects.all().filter(item_lelang=self.kwargs['pk'])
    
class ps_j_a_sanggahan2ListView(SingleTableMixin, generic.ListView):
    model = models.jawaban_atas_sanggahan
    form_class = forms.jawab_atas_sanggahForm
    table_class = tables.jawaban_atas_s2Table
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.jawaban_atas_sanggahan.objects.all().filter(item_lelang=self.kwargs['pk'], bidder=self.kwargs['code'])
    
    
#Pemenang 
class ps_pemenangListView(SingleTableMixin, generic.ListView):
    model = models.pemenang
    form_class = forms.pemenangnyaForm
    table_class = tables.pemenangnyaTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.pemenang.objects.all().filter(item_lelang=self.kwargs['pk'])
    
class ps_pemenang2ListView(SingleTableMixin, generic.ListView):
    model = models.pemenang
    form_class = forms.pemenangnyaForm
    table_class = tables.pemenangnya2Table
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type =='B':
            bdr_user = bidder_user.objects.get(users = self.request.user)
            return models.pemenang.objects.all().filter(item_lelang=self.kwargs['pk'], bidder = bdr_user).order_by('-id')
        elif self.request.user.user_type=='C':
            return models.pemenang.objects.all().filter(item_lelang=self.kwargs['pk'], auctioneer__users__id = self.request.user.id).order_by('-id')
            #if ba:
            #    auc = ba[0].auctioneer.all().filter(users= self.request.user)
            #    if auc:
            #        return models.undangan.objects.all().filter(item_lelang=self.kwargs['item_lelang'], auctioneer=auc[0],tahapan=self.kwargs['current_step'])
            #return models.undangan.objects.none()
        elif self.request.user.user_type=='V':
            return models.pemenang.objects.all().filter(item_lelang=self.kwargs['pk'], viewer__users__id = self.request.user.id).order_by('-id')
            #print(ba)
            #if ba:
            #    vwr = ba[0].viewer.all().filter(users= self.request.user)
            #    if vwr:
            #        return models.undangan.objects.all().filter(item_lelang=self.kwargs['item_lelang'], viewer=vwr[0],tahapan=self.kwargs['current_step'])
            #return models.undangan.objects.none()
        elif self.request.user.user_type=='A':            
            return models.pemenang.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
        else:
            return models.pemenang.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
        # return models.pemenang.objects.all().filter(item_lelang=self.kwargs['pk'])
    
    
    
#Pengumuman pemenang 
class ps_p_pemenangListView(SingleTableMixin, generic.ListView):
    model = models.pengumuman_pemenang
    form_class = forms.pengumuman_pForms
    table_class = tables.pemenang_pengumumanTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.pengumuman_pemenang.objects.all().filter(item_lelang=self.kwargs['pk'])
    
class ps_p_pemenang2ListView(SingleTableMixin, generic.ListView):
    model = models.pengumuman_pemenang
    form_class = forms.pengumuman_pForms
    table_class = tables.pemenang_pengumuman2Table
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.pengumuman_pemenang.objects.all().filter(item_lelang=self.kwargs['pk'])
    
    
#Berita-Acara
class ps_berita_acaraListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_pasca_seleksi
    form_class = forms.ba_pasca_seleksiForm
    table_class = tables.berita_acara_pasca_seleksiTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_pasca_seleksi.objects.all().filter(item_lelang=self.kwargs['pk'], owner=self.kwargs['code'])
    
class ps_berita_acara2ListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_pasca_seleksi
    form_class = forms.ba_pasca_seleksiForm
    table_class = tables.berita_acara_pasca_seleksi2Table
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_pasca_seleksi.objects.all().filter(item_lelang=self.kwargs['pk'], owner=self.kwargs['code'])
    
    
#update form,undangan,jawaban tanggal 13    
class ps_form_sanggahannewListView(SingleTableMixin, generic.ListView):
    model = models.form_ps_sanggahan
    form_class = forms.ps_sanggahannya_jawabForm
    table_class = tables.form_pasca_sanggahannyaTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
        # qs = super().get_queryset(**kwargs)
        if self.request.user.user_type =='B':
            bdr_user = bidder_user.objects.get(users = self.request.user)
           #bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
            return models.form_ps_sanggahan.objects.all().filter(item_lelang=itm_lelang, bidder = bdr_user).order_by('-id')
        else:
            return models.form_ps_sanggahan.objects.all().filter(item_lelang=itm_lelang).order_by('-id')
    
class ps_form_sanggahannew2ListView(SingleTableMixin, generic.ListView):
    model = models.form_ps_sanggahan
    form_class = forms.ps_sanggahannya_jawabForm
    table_class = tables.form_pasca_sanggahannyaTable2
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        # qs = super().get_queryset(**kwargs)
        itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
        if self.request.user.user_type =='B':
            bdr_user = bidder_user.objects.get(users = self.request.user)
            #bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
            return models.form_ps_sanggahan.objects.all().filter(item_lelang=itm_lelang, bidder=bdr_user).order_by('-id')
        else:
            return models.form_ps_sanggahan.objects.all().filter(item_lelang=itm_lelang).order_by('-id')
    
class ps_undg_sanggahannewListView(SingleTableMixin, generic.ListView):
    model = models.undangan_ps_sanggahan
    form_class = forms.ps_sanggahannya_jawabForm
    table_class = tables.undg_ps_sanggahannyaTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.undangan_ps_sanggahan.objects.all().filter(item_lelang=self.kwargs['pk'])
    
class ps_undg_sanggahannew2ListView(SingleTableMixin, generic.ListView):
    model = models.undangan_ps_sanggahan
    form_class = forms.ps_sanggahannya_jawabForm
    table_class = tables.undg_ps_sanggahannyaTable2
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.undangan_ps_sanggahan.objects.all().filter(item_lelang=self.kwargs['pk'])
    
class ps_jawaban_sanggahannewListView(SingleTableMixin, generic.ListView):
    model = models.jawaban_ps_sanggahan
    form_class = forms.jawab_sanggahan_psForm
    table_class = tables.pasca_jawaban_sanggahannyaTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_table_class(self):
        if self.request.user.user_type =='C':
            return tables.pasca_jawaban_sanggahannyaTable
        elif self.request.user.user_type =='A':
            return tables.pasca_jawaban_sanggahannyaTable
        else:
            return tables.pasca_jawaban_sanggahannyaTable2
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.jawaban_ps_sanggahan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
class ps_jawaban_sanggahannew2ListView(SingleTableMixin, generic.ListView):
    model = models.jawaban_ps_sanggahan
    form_class = forms.jawab_sanggahan_psForm
    table_class = tables.pasca_jawaban_sanggahannyaTable2
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        # qs = super().get_queryset(**kwargs)
        itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
        if self.request.user.user_type =='B':
            bdr_user = bidder_user.objects.get(users = self.request.user)
            #print(itm_lelang.id)
            #print(bdr_user.bidder.id)
            # bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
            return models.jawaban_ps_sanggahan.objects.all().filter(item_lelang=itm_lelang, bidder = bdr_user.bidder.id).order_by('-id')
        else:
            return models.jawaban_ps_sanggahan.objects.all().filter(item_lelang=itm_lelang).order_by('-id')
    
    
# MODAL-MODAL
class ps_pemilihan_blokCreateView(BSModalCreateView):

    template_name = 'modal_form_pemilihan_blok.html'
    form_class = forms.pemilihan_blok_psForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class pemilihan_blokUpdateView(BSModalUpdateView):

    template_name = 'modal_form_pemilihan_blok.html'
    form_class = forms.pemilihan_blok_psForm
    model = models.pemilihan_blok_pasca_seleksi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"id": self.kwargs["pk"]}

class ps_undangan_p_blokCreateView(BSModalCreateView):

    template_name = 'modal_undangan_pemilihan_blok.html'
    form_class = forms.u_pemilihan_blokForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class ps_seleksiCreateView(BSModalCreateView):

    template_name = 'modal_pengumuman_hasil_seleksi.html'
    form_class = forms.seleksinyaForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class ps_sanggahanCreateView(BSModalCreateView):

    template_name = 'modal_kirim_sanggahan.html'
    form_class = forms.sanggahannyaForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class ps_sanggahanjawabanCreateView(BSModalCreateView):

    template_name = 'modal_sanggahan_jawaban.html'
    form_class = forms.jawab_sanggahan_psForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class ps_jawaban_atas_sanggahanCreateView(BSModalCreateView):

    template_name = 'modal_form_jawab_sanggahan.html'
    form_class = forms.jawab_atas_sanggahForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class ps_pemenangCreateView(BSModalCreateView):

    template_name = 'modal_form_penetapan_pemenang.html'
    form_class = forms.pemenangnyaForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class ps_p_pemenangCreateView(BSModalCreateView):

    template_name = 'modal_pengumuman_penetapan_pemenang.html'
    form_class = forms.pengumuman_pForms
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class ps_berita_acaraCreateView(BSModalCreateView):

    template_name = 'modal_ba_pemilihan_blok.html'
    form_class = forms.ba_pasca_seleksiForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class ps_berita_acara_hasil_seleksiCreateView(BSModalCreateView):

    template_name = 'modal_ba_hasil_seleksi.html'
    form_class = forms.ba_pasca_seleksiForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class ps_berita_acara_sanggahanCreateView(BSModalCreateView):

    template_name = 'modal_ba_sanggahan.html'
    form_class = forms.ba_pasca_seleksiForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    

class blok_paska_seleksiCreateView(BSModalCreateView):

    template_name = 'modal_blok_paska_seleksi.html'
    form_class = forms.blok_paska_seleksiForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"id":None, "item_lelang": self.kwargs["pk"]}

class blok_paska_seleksiUpdateView(BSModalUpdateView):

    template_name = 'modal_blok_paska_seleksi.html'
    form_class = forms.blok_paska_seleksiForm
    model = models.blok_pasca_seleksi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"id": self.kwargs["pk"]}
    

#tambah form,undangan,jawaban tanggal 13    
    
class form_ps_sanggahanCreateView(BSModalCreateView):

    template_name = 'modal_ps_sanggahan.html'
    form_class = forms.ps_sanggahannya_jawabForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"],'bidder': self.request.user.id,}
    
class kirim_undg_sanggahanCreateView(BSModalCreateView):

    template_name = 'modal_kirim_undangan_sanggahan_jawaban.html'
    form_class = forms.kirim_undg_sanggahan_jawabForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
    
class jawab_pasca_sanggahanCreateView(BSModalCreateView):

    template_name = 'modal_sanggahan_jawaban.html'
    form_class = forms.jawab_sanggahan_psForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
    

    

    





# # UPDATE-UPDATE
#pemilihan
class ps_pemilihan_blokUpdateView(BSModalUpdateView):
    template_name = 'modal_form_pemilihan_blok.html'
    form_class = forms.pemilihan_blok_psForm
    model = models.pemilihan_blok_pasca_seleksi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial

#undangan_blok
class ps_undangan_blokUpdateView(BSModalUpdateView):
    template_name = 'modal_undangan_pemilihan_blok.html'
    form_class = forms.u_pemilihan_blokForm
    model = models.blok
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial

#seleksi
class ps_seleksiUpdateView(BSModalUpdateView):
    template_name = 'modal_pengumuman_hasil_seleksi.html'
    form_class = forms.seleksinyaForm
    model = models.seleksi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial

#sanggahan
class ps_sanggahanUpdateView(BSModalUpdateView):
    template_name = 'modal_kirim_sanggahan.html'
    form_class = forms.sanggahannyaForm
    model = models.sanggahan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial

#sanggahanjawaban    
class ps_sanggahan_jawabanUpdateView(BSModalUpdateView):
    template_name = 'modal_sanggahan_jawaban.html'
    form_class = forms.sanggahan_jawabForm
    model = models.sanggahan_jawaban
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
#jawaban_atas_sanggahan
class ps_jawaban_atas_sanggahanUpdateView(BSModalUpdateView):
    template_name = 'modal_form_jawab_sanggahan.html'
    form_class = forms.jawab_atas_sanggahForm
    model = models.jawaban_atas_sanggahan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })
        
        return initial

#pemenang
class ps_pemenangUpdateView(BSModalUpdateView):
    template_name = 'modal_form_penetapan_pemenang.html'
    form_class = forms.pemenangnyaForm
    model = models.pemenang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    
class ps_pengumuman_pemenangUpdateView(BSModalUpdateView):
    template_name = 'modal_pengumuman_penetapan_pemenang.html'
    form_class = forms.pengumuman_pForms
    model = models.pengumuman_pemenang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class ps_berita_acaraUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_pemilihan_blok.html'
    form_class = forms.ba_pasca_seleksiForm
    model = models.berita_acara_pasca_seleksi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class ps_berita_acara_hasil_seleksiUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_hasil_seleksi.html'
    form_class = forms.ba_pasca_seleksiForm
    model = models.berita_acara_pasca_seleksi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class ps_berita_acara_sanggahanUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_sanggahan.html'
    form_class = forms.ba_pasca_seleksiForm
    model = models.berita_acara_pasca_seleksi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
    
#update form,undangan,jawaban tanggal 13    

class ps_form_sanggahanUpdateView(BSModalUpdateView):
    template_name = 'modal_ps_sanggahan.html'
    form_class = forms.ps_sanggahannya_jawabForm
    model = models.form_ps_sanggahan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            
        })

        return initial
    
class ps_undg_sanggahanUpdateView(BSModalUpdateView):
    template_name = 'modal_kirim_undangan_sanggahan_jawaban.html'
    form_class = forms.kirim_undg_sanggahan_jawabForm
    model = models.undangan_ps_sanggahan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    
class ps_jawab_sanggahanUpdateView(BSModalUpdateView):
    template_name = 'modal_sanggahan_jawaban.html'
    form_class = forms.jawab_sanggahan_psForm
    model = models.jawaban_ps_sanggahan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial

# api
def api_check_ps_sanggahan(request, pk):
    if request.user.is_authenticated:
        if request.method == 'GET':
            itm_lelang = item_lelang.objects.get(pk = pk)
            bdr_user = bidder_user.objects.get(pk = request.user.id)
           
            count= models.form_ps_sanggahan.objects.values("bidder").filter(item_lelang=itm_lelang, bidder = bdr_user).count()

            return JsonResponse(count, safe=False)
# 
class pemenang_blok_pasca_seleksiListView(SingleTableMixin, generic.ListView):
    model = models.pemilihan_blok_pasca_seleksi
    table_class = tables.pemenang_bloknyaTable
    template_name = 'tabel_pasca_seleksi.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.pemilihan_blok_pasca_seleksi.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])

class pemenang_blok_paska_seleksiCreateView(BSModalCreateView):

    template_name = 'modal_pemenang_blok_paska_seleksi.html'
    form_class = forms.pemenang_blok_paska_seleksiForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"id":None, "item_lelang": self.kwargs["pk"]}

class pemenang_blok_paska_seleksiUpdateView(BSModalUpdateView):

    template_name = 'modal_pemenang_blok_paska_seleksi.html'
    form_class = forms.pemenang_blok_paska_seleksiForm
    model = models.pemilihan_blok_pasca_seleksi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"id": self.kwargs["pk"]}
    