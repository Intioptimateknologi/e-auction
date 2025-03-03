from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from . import tables
from django.urls import reverse_lazy
from django.views import generic
from django_tables2 import SingleTableMixin
from userman.models import tim_lelang, bidder_perwakilan, bidder, UserMenu, Users, UserMenuGroup, bidder_user
from userman.serializers import UserMenu2Serializer
from adm_lelang.models import auctioner_lelang, bidder_lelang, jadwal_seleksi, item_lelang, pengumuman, berita_acara
from adm_lelang import utils
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from datetime import datetime, timedelta
from django.utils import timezone
from django_renderpdf.views import PDFView
from docxtpl import DocxTemplate
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models import Min
from django.http import JsonResponse



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_tabs(request):
    url = '/persiapan/dokumen_seleksi/'
    menu = UserMenu.objects.all().filter(link=url)
    nodes = menu[0].get_leafnodes()
    user = Users.objects.get(pk=request.user.id)
    grp = []
    for g in user.customGroup.all():
        grp.append(g.id)
    #for p in nodes:
        #print(p.id)

    menugroup = UserMenuGroup.objects.all().filter(menu__in=nodes).filter(group__in=grp).distinct('menu')

    context = {
        'tabs': nodes,
        'menu_group': menugroup,
        'user': request.user
    }
    #print(context)
    return render(request, 'tabs_pembukaan.html',context)

def pembukaan(request):
    url = "/persiapan/pembukaan/"
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pembukaan_admin.html',context)
        elif request.user.user_type == 'B':
            user = request.user
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pembukaan_admin.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pembukaan_admin.html',context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pembukaan_admin.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    
    
def aanwizing_doksel(request):
    url = "/persiapan/aanwizing/"
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_aanwizing_auctioneer.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_aanwizing_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_aanwizing_auctioneer.html',context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_aanwizing_auctioneer.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    
def addendum(request):
    url = "/persiapan/addendum_doksel/"
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_addendum_doksel_auctioneer.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_addendum_doksel_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_addendum_doksel_auctioneer.html',context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_addendum_doksel_auctioneer.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    
def simulasi(request):
    url = "/persiapan/simulasi/"
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_simulasi_auctioneer.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_simulasi_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_simulasi_auctioneer.html', context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_simulasi_auctioneer.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    
def dokumen_seleksi(request):
    url = "/persiapan/dokumen_seleksi/"
    if request.user.is_authenticated:
        context = {}
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_dokumen_seleksi_auctioneer.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_dokumen_seleksi_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            #print(context)
            return render(request, 'index_dokumen_seleksi_auctioneer.html', context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            #print(context)
            return render(request, 'index_dokumen_seleksi.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    
def pertanyaan(request):
    url = "/persiapan/pertanyaan/"
    #print(request.path)
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pertanyaan_auctioneer.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pertanyaan_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pertanyaan_auctioneer.html', context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_pertanyaan_auctioneer.html',context)
        return render(request, 'index_dokumen_seleksi_auctioneer.html', context)
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')

# Table-table
class pengambilan_dokselListView(SingleTableMixin, generic.ListView):
    model = models.pengambilan_dokumen_seleksi 
    table_class = tables.status_dokumen_seleksinyaTable
    template_name = 'tabel_persiapan.html'
    def get_table_class(self):
        
        if self.request.user.user_type =='B':
            return tables.status_dokumen_seleksinya2Table
        else:
            return tables.status_dokumen_seleksinyaTable

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
        docs = models.dokumen_seleksi.objects.filter(item_lelang = itm_lelang)
        if docs.exists():
            dokumen = docs[0]
            if self.request.user.user_type =='B':
                bdr_user = bidder_user.objects.get(users = self.request.user)
                bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
                # max_year = models.pengambilan_dokumen_seleksi.objects.filter(dokumen_seleksi=dokumen, bidder_perwakilan__in = bdr_wakil).order_by("tgl_download")[0].tgl_download
                # d = models.pengambilan_dokumen_seleksi.objects.all().filter(dokumen_seleksi=dokumen, bidder_perwakilan__in = bdr_wakil, tgl_download=max_year)
                d = models.pengambilan_dokumen_seleksi.objects.all().filter(dokumen_seleksi=dokumen, bidder_perwakilan__in = bdr_wakil).order_by('-id')
                return d
            else:
                return models.pengambilan_dokumen_seleksi.objects.filter(dokumen_seleksi=dokumen, bidder_perwakilan__isnull = False).order_by('-id')
                # return models.pengambilan_dokumen_seleksi.objects.filter(dokumen_seleksi=dokumen, bidder_perwakilan__isnull = False).order_by("bidder_perwakilan__id","tgl_download").distinct("bidder_perwakilan")
                #return models.pengambilan_dokumen_seleksi.objects.all().filter(dokumen_seleksi=dokumen).order_by('-id')
        else:
            return []


class pengambilan_addendumListView(SingleTableMixin, generic.ListView):
    model = models.pengambilan_dokumen_addendum
    table_class = tables.pengambilan_addendum_dokselTable
    template_name = 'tabel_persiapan.html'
    def get_table_class(self):
        if self.request.user.user_type =='B':
            return tables.pengambilan_addendum_dokselTable
        else:
            return tables.pengambilan_addendum_doksel2Table

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
        docs = models.p_addendum.objects.filter(item_lelang = itm_lelang)
        if docs.exists():
            dokumen = docs[0]
            if self.request.user.user_type =='B':
                bdr_user = bidder_user.objects.get(users = self.request.user)
                bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
                return models.pengambilan_dokumen_addendum.objects.all().filter(dokumen_addendum=dokumen, bidder_perwakilan__in = bdr_wakil).order_by('-id')
            else:
                return models.pengambilan_dokumen_addendum.objects.all().filter(dokumen_addendum=dokumen).order_by('-id')
        else:
            return []

def api_check_addendum(request, pk):
    if request.user.is_authenticated:
        if request.method == 'GET':
            itm_lelang = item_lelang.objects.get(pk = pk)
            dokumen = models.p_addendum.objects.filter(item_lelang = itm_lelang)
            if (dokumen.exists()):
                bdr_user = bidder_user.objects.get(users = request.user)
                bdr_wakil = bidder_perwakilan.objects.all().filter(bidder  = bdr_user)
                count = models.pengambilan_dokumen_addendum.objects.filter(dokumen_addendum=dokumen[0], bidder_perwakilan__in=bdr_wakil).count()

                return JsonResponse(count, safe=False)
            else:
                return JsonResponse({"count":0})

class pengambilan_doksel2ListView(SingleTableMixin, generic.ListView):
    model = models.pengambilan_dokumen_seleksi 
    table_class = tables.status_dokumen_seleksinya2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        itm_lelang = item_lelang.objects.get(pk = self.kwargs['pk'])
        try:
            dokumen = models.dokumen_seleksi.objects.get(item_lelang = itm_lelang)
            return models.pengambilan_dokumen_seleksi.objects.all().filter(dokumen_seleksi=dokumen).order_by('-id')
        except:
            return []

class p_dokumenListView(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumensTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'],tahapan=4).order_by('-id')
    
class p_dokumenList2View(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumens2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'], bidder__id=self.kwargs['code'], tahapan=4).order_by('-id')
    
class p_dokumenListauctioneer2View(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumens2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'], auctioneer=self.kwargs['auctioneer'],tahapan=4).order_by('-id')
    
    
# Penyusun jawab      
class penyusunan_jawabanListView(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumensTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'],tahapan=15).order_by('-id')
    
class penyusunan_jawaban2ListView(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumensTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'],tahapan=15).order_by('-id')
    
class penyusunan_jawaban3ListView(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumensTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'], auctioneer=self.kwargs['code'],tahapan=15).order_by('-id')
    
    
# Aanwizing    
class aanwizingListView(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumensTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'],tahapan=17).order_by('-id')

class aanwizing2ListView(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumensTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'], bidder=self.kwargs['code'], tahapan=17).order_by('-id')
    
class aanwizing3ListView(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumensTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'], auctioneer=self.kwargs['code'], tahapan=17).order_by('-id')
    
    
# Simulasi    
class simulasiListView(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumensTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'], tahapan=21).order_by('-id')
    
class simulasi2ListView(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumensTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'], auctioneer=self.kwargs['code'], tahapan=21).order_by('-id')
    
class simulasi3ListView(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumensTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['pk'], bidder=self.kwargs['code'], tahapan=21).order_by('-id')
    
    
# addendum      
class p_addendumListView(SingleTableMixin, generic.ListView):
    model = models.p_addendum 
    form_class = forms.DokumenForm
    table_class = tables.addendumTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_addendum.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
class p_addendum2ListView(SingleTableMixin, generic.ListView):
    model = models.p_addendum 
    form_class = forms.PersiapanAddendumForm
    table_class = tables.addendum2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_addendum.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
class p_addendumauctioneer2ListView(SingleTableMixin, generic.ListView):
    model = models.p_addendum 
    form_class = forms.PersiapanAddendumForm
    table_class = tables.addendum2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_addendum.objects.all().filter(item_lelang=self.kwargs['pk'], auctioneer=self.kwargs['code'], tahapan=26).order_by('-id')
    
#dokumen
class p_dokumen_seleksiListView(SingleTableMixin, generic.ListView):
    model = models.dokumen_seleksi 
    form_class = forms.DokumenSeleksiForm
    table_class = tables.dokumen_seleksinyaTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.dokumen_seleksi.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
class p_dokumen_seleksi2ListView(SingleTableMixin, generic.ListView):
    model = models.dokumen_seleksi 
    form_class = forms.DokumenSeleksiForm
    table_class = tables.dokumen_seleksinya2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        #return models.dokumen_seleksi.objects.all().filter(item_lelang=self.kwargs['pk']).annotate(earliest_created=Min('created')).order_by('-id')
        return models.dokumen_seleksi.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
class p_dokumen_seleksi3ListView(SingleTableMixin, generic.ListView):
    model = models.dokumen_seleksi 
    form_class = forms.DokumenSeleksiForm
    table_class = tables.dokumen_seleksinya3Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.dokumen_seleksi.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
    
#pertanyaan    
class p_pertanyaanListView(SingleTableMixin, generic.ListView):
    model = models.p_pertanyaan 
    form_class = forms.PertanyaanForm
    table_class = tables.p_pertanyaanTable
    template_name = 'tabel_persiapan.html'

    def get_table_class(self):
        if self.request.user.user_type =='B':
            return tables.p_pertanyaanTable
        else:
            return tables.p_pertanyaan3Table

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type =='B':
            bdr_user = bidder_user.objects.get(users = self.request.user)
            return models.p_pertanyaan.objects.all().filter(item_lelang=self.kwargs['pk'], bidder = bdr_user).order_by('-last_updated')
        else:
            return models.p_pertanyaan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-last_updated')

class p_pertanyaanvListView(SingleTableMixin, generic.ListView):
    model = models.p_pertanyaan 
    form_class = forms.PertanyaanForm
    table_class = tables.p_pertanyaanTable
    template_name = 'tabel_persiapan.html'

    def get_table_class(self):
        if self.request.user.user_type =='B':
            return tables.p_pertanyaan4Table
        else:
            return tables.p_pertanyaan3Table

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type =='B':
            bdr_user = bidder_user.objects.get(users = self.request.user)
            return models.p_pertanyaan.objects.all().filter(item_lelang=self.kwargs['pk'], bidder = bdr_user).order_by('-last_updated')
        else:
            return models.p_pertanyaan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-last_updated')

class p_pertanyaan2ListView(SingleTableMixin, generic.ListView):
    model = models.p_pertanyaan 
    form_class = forms.PertanyaanForm
    table_class = tables.p_pertanyaan2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        # return models.p_pertanyaan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')
        if self.request.user.user_type =='B':
            bdr_user = bidder_user.objects.get(users = self.request.user)
            return models.p_pertanyaan.objects.all().filter(item_lelang=self.kwargs['pk'], bidder = bdr_user).order_by('-last_updated')
        else:
            return models.p_pertanyaan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-last_updated')
    
class p_pertanyaan3ListView(SingleTableMixin, generic.ListView):
    model = models.p_pertanyaan 
    form_class = forms.PertanyaanForm
    table_class = tables.p_pertanyaanTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_pertanyaan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-last_updated')

#berita acara    
class berita_acara_persiapanListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_persiapan
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_persiapanTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['pk'],tahapan=8).order_by('-id')

class berita_acara_persiapan2ListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_persiapan
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_persiapan2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['pk'], tahapan=8).order_by('-id')

class berita_acara_persiapan2ListAuctioneerView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_persiapan 
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_persiapan2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['pk'], tahapan=8).order_by('-id')

class berita_acara_persiapan_simulasiListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_persiapan
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_persiapanTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')

class berita_acara_persiapan_simulasi2ListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_persiapan
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_persiapan2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['pk'], tahapan=23).order_by('-id')

class berita_acara_persiapan_simulasiAuctioneerListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_persiapan 
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_persiapan2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['pk'], auctioneer=self.kwargs['auctioneer'],tahapan=23).order_by('-id')

class berita_acara_persiapanaddendumbidder2ListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_persiapan
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_persiapan2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['pk'],  bidder=self.kwargs['bidder']).order_by('-id')
     
class berita_acara_persiapanaddendumauctioneer2ListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_persiapan
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_persiapan2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['pk'], auctioneer=self.kwargs['auctioneer']).order_by('-id') 


class berita_acara_pertanyaanListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_persiapan
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_persiapanTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['pk'],tahapan=13).order_by('-id')

class berita_acara_pertanyaan2ListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_persiapan
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_persiapan2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['pk'], bidder=self.kwargs['bidder'], tahapan=13).order_by('-id')

class berita_acara_pertanyaan2ListAuctioneerView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_persiapan 
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_persiapan2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['pk'], auctioneer=self.kwargs['auctioneer'],tahapan=13).order_by('-id')

# daftar hadir
class daftar_hadirListView(SingleTableMixin, generic.ListView):
    model = models.daftar_hadir 
    table_class = tables.daftar_hadirTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.daftar_hadir.objects.all().filter(item_lelang=self.kwargs['pk'], tahapan=self.kwargs["tahapan"]).order_by('-id')
    
class daftar_hadirListView2(SingleTableMixin, generic.ListView):
    model = models.daftar_hadir 
    table_class = tables.daftar_hadirTable2
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.daftar_hadir.objects.all().filter(item_lelang=self.kwargs['pk'], tahapan=self.kwargs["tahapan"]).order_by('-id')
    
class daftar_hadirCreateView(BSModalCreateView):
    
    template_name = 'modal_daftar_hadir.html'
    form_class = forms.DaftarHadirForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"], "tahapan": self.kwargs["tahapan"]}
    
class daftar_hadirUpdatedView(BSModalUpdateView):
    template_name = 'modal_daftar_hadir.html'
    form_class = forms.DaftarHadirForm
    model = models.daftar_hadir
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'], "tahapan": self.kwargs["tahapan"]
        })
        return initial

#templatetags
class modalUpdateUndangan(BSModalUpdateView):
    template_name = 'modal_undangan_pengambilan_dokumen.html'
    form_class = forms.DokumenForm
    model = models.p_dokumen
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['item_lelang'],
        })
        return initial

class modalCreateUndangan(BSModalCreateView):

    template_name = 'modal_undangan_pengambilan_dokumen.html'
    form_class = forms.DokumenForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"], "tahapan": self.kwargs["tahapan"]}
    
class undanganBidderListView(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumens2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['item_lelang'], bidder__id=self.kwargs['bidder'], tahapan=self.kwargs['current_step']).order_by('-id')
    
class undanganAuctionerListView(SingleTableMixin, generic.ListView):
    model = models.p_dokumen 
    form_class = forms.DokumenForm
    table_class = tables.p_dokumensTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.p_dokumen.objects.all().filter(item_lelang=self.kwargs['item_lelang'], auctioneer__id=self.kwargs['auctioner'],tahapan=self.kwargs['current_step']).order_by('-id')

class modalUpdateBA(BSModalUpdateView):
    template_name = 'modal_ba_dokumen_seleksi.html'
    form_class = forms.BeritaAcaraForm
    model = models.berita_acara_persiapan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['item_lelang'],
        })
        return initial

class modalCreateBA(BSModalCreateView):

    template_name = 'modal_ba_dokumen_seleksi.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"], "tahapan": self.kwargs["tahapan"]}
    
class BABidderListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_persiapan 
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_persiapan2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['item_lelang'], bidder__id=self.kwargs['bidder'], tahapan=self.kwargs['current_step']).order_by('-id')
    
class BAAuctionerListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara_persiapan 
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_persiapanTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['item_lelang'], auctioneer__id=self.kwargs['auctioner'],tahapan=self.kwargs['current_step']).order_by('-id')

# Modal-modal
class p_dokumenCreateView(BSModalCreateView):

    template_name = 'modal_undangan_pengambilan_dokumen.html'
    form_class = forms.DokumenForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"], "tahapan": 4, "judul_undangan": "Pengambilan Dokumen Seleksi"}
    
class penyusunan_jawabanCreateView(BSModalCreateView):

    template_name = 'modal_undangan_pengambilan_dokumen.html'
    form_class = forms.DokumenForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"], "tahapan": 15, "judul_undangan": "Pengambilan Dokumen Seleksi"}
    
class aanwizingCreateView(BSModalCreateView):
    
    template_name = 'modal_undangan_pengambilan_dokumen.html'
    form_class = forms.DokumenForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"], "tahapan": 17}

class simulasiCreateView(BSModalCreateView):
    
    template_name = 'modal_undangan_pengambilan_dokumen.html'
    form_class = forms.DokumenForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"], "tahapan": 21}
    
    
class p_addendumCreateView(BSModalCreateView):
    
    template_name = 'modal_adendum_doksel.html'
    form_class = forms.PersiapanAddendumForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"], "tahapan": 26}
    
class p_dokumen_seleksiCreateView(BSModalCreateView):
    
    template_name = 'modal_dokumen_seleksi.html'
    form_class = forms.DokumenSeleksiForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class p_pertanyaanCreateView(BSModalCreateView):
    
    template_name = 'modal_pertanyaan.html'
    form_class = forms.PertanyaanForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class berita_acara_dokumen_seleksiCreateView(BSModalCreateView):
    
    template_name = 'modal_ba_dokumen_seleksi.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"], "tahapan": 8 }
    
class berita_acara_simulasiCreateView(BSModalCreateView):
    
    template_name = 'modal_ba_simulasi.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class berita_acara_pertanyaanCreateView(BSModalCreateView):
    
    template_name = 'modal_ba_pertanyaan.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class berita_acara_addendumCreateView(BSModalCreateView):
    
    template_name = 'modal_ba_addendum.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
class berita_acara_aanwizingCreateView(BSModalCreateView):
    
    template_name = 'modal_ba_aanwizing.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

#Update-update    
class p_dokumenUpdateView(BSModalUpdateView):
    template_name = 'modal_undangan_pengambilan_dokumen.html'
    form_class = forms.DokumenForm
    model = models.p_dokumen
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class penyusunan_jawabanUpdateView(BSModalUpdateView):
    template_name = 'modal_undangan_pengambilan_dokumen.html'
    form_class = forms.DokumenForm
    model = models.p_dokumen
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class aanwizingUpdateView(BSModalUpdateView):
    template_name = 'modal_undangan_pengambilan_dokumen.html'
    form_class = forms.DokumenForm
    model = models.p_dokumen
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class simulasiUpdateView(BSModalUpdateView):
    template_name = 'modal_undangan_pengambilan_dokumen.html'
    form_class = forms.DokumenForm
    model = models.p_dokumen
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class p_addendumUpdateView(BSModalUpdateView):
    template_name = 'modal_adendum_doksel.html'
    form_class = forms.PersiapanAddendumForm
    model = models.p_addendum
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    
class p_dokumen_seleksiUpdateView(BSModalUpdateView):
    template_name = 'modal_dokumen_seleksi.html'
    form_class = forms.DokumenSeleksiForm
    model = models.dokumen_seleksi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            # 'item_lelang': self.kwargs['pk'],
        })

        return initial
    
class p_pertanyaanUpdateView(BSModalUpdateView):
    template_name = 'modal_pertanyaan.html'
    form_class = forms.PertanyaanForm
    model = models.p_pertanyaan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    
class berita_acara_dokumen_seleksiUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_dokumen_seleksi.html'
    form_class = forms.BeritaAcaraForm
    model = models.berita_acara_persiapan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class berita_acara_simulasiUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_simulasi.html'
    form_class = forms.BeritaAcaraForm
    model = models.berita_acara_persiapan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class berita_acara_pertanyaanUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_pertanyaan_update.html'
    form_class = forms.BeritaAcaraForm
    model = models.berita_acara_persiapan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial

# class berita_acara_pertanyaanUpdateView(BSModalUpdateView):
#     template_name = 'modal_ba_pertanyaan.html'
#     form_class = forms.BeritaAcaraForm
#     model = models.berita_acara_persiapan
#     success_message = 'Success: Data was created.'
#     success_url = reverse_lazy('index')
#     def get_initial(self):
#         initial = ({
#             'id': self.kwargs['pk'],
#             'item_lelang': self.kwargs['id'],
#         })

#         return initial
    
class berita_acara_addendumUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_addendum_update.html'
    form_class = forms.BeritaAcaraForm
    model = models.berita_acara_persiapan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
class berita_acara_aanwizingUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_aanwizing_update.html'
    form_class = forms.BeritaAcaraForm
    model = models.berita_acara_persiapan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial

class pengambilan_dokumen_seleksiView(BSModalCreateView):
    template_name = 'modal_pengambilan_doksel.html'
    form_class = forms.PengambilanDokumenSeleksiForm
    model = models.pengambilan_dokumen_seleksi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        user = self.request.user
        if user.user_type == 'B':
            bdr = bidder_user.objects.get(users__id = user.id)
            #print(self.kwargs)
            initial = ({
                'dokumen_seleksi': self.kwargs['dokumen'],
                'bdr': bdr,
            })
        else:
            initial = ({
                'dokumen_seleksi': self.kwargs['dokumen'],
                'bdr': None,
                'bidder_perwakilan': None,
            })
            
            
        
        return initial

class pengambilan_dokumen_addendumView(BSModalCreateView):
    template_name = 'modal_pengambilan_addendum.html'
    form_class = forms.PengambilanAddendumDokumenSeleksiForm
    model = models.pengambilan_dokumen_addendum
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        user = self.request.user
        if user.user_type == 'B':
            bdr = bidder_user.objects.get(users__id = user.id)
            #print(self.kwargs)
            initial = ({
                'dokumen_addendum': self.kwargs['dokumen'],
                'bdr': bdr,
            })
        else:
            initial = ({
                'dokumen_addendum': self.kwargs['dokumen'],
                'bdr': None,
                'bidder_perwakilan': None,
            })
            
            
        
        return initial
    # def get_initial(self):
    #     user = self.request.user
    #     bdr = bidder_user.objects.get(users__id = user.id)
    #     print(self.kwargs)
    #     initial = ({
    #         'dokumen_addendum': self.kwargs['dokumen'],
    #         'bdr': bdr,
    #     })
    #     return initial


def docxview(request, pk):
    from docx import Document
    from htmldocx import HtmlToDocx

    docs = berita_acara.objects.filter(pk=pk)
    context = {}
    if docs.exists():
        dokumen = docs[0]
        context['nomor']=dokumen.nomor
        context['judul']=dokumen.judul
        context['tanggal']=dokumen.tanggal
        itm_lelang = item_lelang.objects.get(pk=dokumen.item_lelang.id)
        pumum = pengumuman.objects.all().filter(item_lelang=dokumen.item_lelang.id)[0]
        doksel = models.dokumen_seleksi.objects.all().filter(item_lelang=dokumen.item_lelang.id)
        pansel = auctioner_lelang.objects.all().filter(item_lelang=dokumen.item_lelang.id)
        ketua_pansel = auctioner_lelang.objects.all().filter(item_lelang=dokumen.item_lelang.id).filter(auctioner__jabatan_dalam_tim="ketua")
        context['seleksi'] = itm_lelang.nama_lelang
        context['tahun'] = itm_lelang.tahun
        context['judul_pengumuman'] = pumum.judul
        context['nomor_pengumuman'] = pumum.nomor
        context['doksel'] = doksel
        context['pansel'] = pansel
        context['ketua_pansel'] = ketua_pansel[0].auctioner.users.nama_lengkap

        template_name = 'berita_acara/ba_pengambilan_doksel.html'
        document = Document()
        new_parser = HtmlToDocx()
        strhtml = render_to_string(template_name, context)
        new_parser.add_html_to_document(strhtml, document)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename=berita_acara.docx'
        document.save(response)
        return response


class PdfsView(PDFView):

    template_name = 'bukti_pengambilan.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        docs = models.pengambilan_dokumen_seleksi.objects.filter(pk=kwargs['pk'])
        context = {}
        if docs.exists():
            dokumen = docs[0]
            context['nomor']=dokumen.dokumen_seleksi.nomor
            context['judul']=dokumen.dokumen_seleksi.judul
            context['tanggal']=dokumen.created
            context['bidder']=dokumen.bidder_perwakilan

            itm_lelang = item_lelang.objects.get(pk=dokumen.dokumen_seleksi.item_lelang.id)
            # pumum = pengumuman.objects.all().filter(item_lelang=dokumen.dokumen_seleksi.item_lelang.id)[0]  
            doksel = models.dokumen_seleksi.objects.all().filter(item_lelang=dokumen.dokumen_seleksi.item_lelang.id)
            pansel = auctioner_lelang.objects.all().filter(item_lelang=dokumen.dokumen_seleksi.item_lelang.id)
            ketua_pansel = auctioner_lelang.objects.all().filter(item_lelang=dokumen.dokumen_seleksi.item_lelang.id).filter(auctioner__jabatan_dalam_tim="ketua")
            context['seleksi'] = itm_lelang.nama_lelang
            context['tahun'] = itm_lelang.tahun
            # context['judul_pengumuman'] = pumum.judul
            # context['nomor_pengumuman'] = pumum.nomor
            context['doksel'] = doksel
            context['pansel'] = pansel
            if ketua_pansel:
                context['ketua_pansel'] = ketua_pansel[0].auctioner.users.nama_lengkap  
            else:
                context['ketua_pansel'] = "Ketua Tim"
        return context
    

# pdf  permohonan keikutsertaan
class PdfsView_addendum(PDFView):

    template_name = 'bukti_pengambilan_addendum.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        dokumen = models.pengambilan_dokumen_addendum.objects.filter(pk=kwargs['pk'])
        context = {}
        if dokumen.exists():
            #context['tanggal']= datetime.now()
            context['tanggal']= dokumen[0].tgl_download
            context['bidder']= dokumen[0].bidder_perwakilan
            context['perusahaan']= dokumen[0].bidder_perwakilan
            itm_lelang = item_lelang.objects.get(pk=dokumen[0].dokumen_addendum.item_lelang.id)
            context['seleksi'] = itm_lelang.nama_lelang
        return context

