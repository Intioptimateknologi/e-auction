from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from . import tables
from userman.models import tim_lelang, bidder_perwakilan, bidder, bidder_user
from smra.forms import undangan_smra_ccaForm
from smra.models import undangan_smra_cca
from adm_lelang.models import auctioner_lelang, bidder_lelang, item_lelang, detail_itemlelang, jadwal_seleksi
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
from django_tables2 import SingleTableMixin,MultiTableMixin
from django.views.generic.base import TemplateView
from django_filters.views import FilterView
from django_renderpdf.views import PDFView
from terbilang import Terbilang
from django.db.models import Max
from django.utils import timezone
from persiapan.models import p_dokumen, berita_acara_persiapan
from persiapan.forms import DokumenForm,BeritaAcaraForm
from persiapan.tables import p_dokumensTable,berita_acara_persiapanTable
from adm_lelang import utils
import locale
from django.http import FileResponse
from django_pandas.io import read_frame
from django.http import JsonResponse
import pygal
from pygal.style import DefaultStyle
from django.conf import settings as SETTINGS

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def settings(request):
    if request.user.is_authenticated:
        url = "/cca/settings/"    
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'settings_cca.html',context)
        if request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'settings_cca.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'settings_cca.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'settings_cca.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')   

def cr(request):
    if request.user.is_authenticated:
        url = "/cca/cr/"    
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_cr.html',context)
        if request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_cr.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_cr.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_cr.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')   

def putaran_cr(request):
    if request.user.is_authenticated:
        url = "/cca/putaran_cr/"
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_putaran_cr_auctioner.html',context)
        if request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_putaran_cr_auctioner.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            bdr = bidder_user.objects.get(users_id = request.user.id)
            perwakilan = bidder_perwakilan.objects.all().filter(bidder = bdr)
            context['perwakilan'] = perwakilan
            context['centrifugo']  = SETTINGS.CENTRIFUGO_WS
            context.update(tabs)
            return render(request, 'dash_bidder_cca.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context['centrifugo']  = SETTINGS.CENTRIFUGO_WS
            context.update(tabs)
            print(context)
            return render(request, 'dash_auctioner_cca.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')   

def putaran_sr(request):
    if request.user.is_authenticated:
        url = "/cca/putaran_cr/"    
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_putaran_sr.html',context)
        if request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_putaran_sr.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            bdr = bidder_user.objects.get(users_id = request.user.id)
            perwakilan = bidder_perwakilan.objects.all().filter(bidder = bdr)
            context['perwakilan'] = perwakilan
            context['centrifugo']  = SETTINGS.CENTRIFUGO_WS
            context.update(tabs)
            return render(request, 'cca_putaran_sr.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_putaran_sr_auctioner.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')   

def putaran_ar(request):
    if request.user.is_authenticated:
        url = "/cca/putaran_cr/"    
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_putaran_ar.html',context)
        if request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_putaran_ar.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            bdr = bidder_user.objects.get(users_id = request.user.id)
            perwakilan = bidder_perwakilan.objects.all().filter(bidder = bdr)
            context['perwakilan'] = perwakilan
            context['centrifugo']  = SETTINGS.CENTRIFUGO_WS
            context.update(tabs)
            return render(request, 'cca_putaran_ar.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_putaran_ar_auctioner.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')   

def sr(request):
    if request.user.is_authenticated:
        url = "/cca/sr/"    
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_sr.html',context)
        if request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_sr.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_sr.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_sr.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')   

def ar(request):
    if request.user.is_authenticated:
        url = "/cca/ar/"    
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_ar.html',context)
        if request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_ar.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_ar.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'cca_ar.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')   

def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'B':
            context = {}
            user = request.user
            vbidder_user = bidder_user.objects.get(users_id = user.id)
            bidder_id = vbidder_user.bidder_id
            vbidder = bidder.objects.all().filter(id = bidder_id)
            context["bidder"] = vbidder[0]
            if request.GET.get("id"):
                vbidder_lelang = bidder_lelang.objects.all().filter(bidder = vbidder_user, item_lelang=request.GET.get("id"))
            else:
                vbidder_lelang = bidder_lelang.objects.all().filter(bidder = vbidder_user).order_by('created')
            context["bidder_lelang"] = vbidder_lelang[0]
            context["bidder_id"] = bidder_id
            context["ip_address"] = get_client_ip(request)
            context["item_lelang"] = bidder_lelang.objects.all().filter(bidder = bidder_id)
            dt = timezone.now()
            tahapan = jadwal_seleksi.objects.all().filter(item_lelang=vbidder_lelang[0].item_lelang).filter(tanggal_akhir__gte=dt).filter(tanggal_awal__lte=dt)
            if tahapan:
                context["tahapan"]  = tahapan[0]
            else:
                context["tahapan"]  = None
            context['user_type'] = request.user.user_type
            print(context)
            return render(request, 'index_cca_bidder.html',context)
        elif request.user.user_type == 'C':
            context = {}
            user = request.user
            auc = tim_lelang.objects.all().filter(users_id = request.user.id)
            if (auc):
                context['auctioner'] = auc[0]
                if request.GET.get("id"):
                    context["item_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) #bidder_lelang.objects.all().filter(bidder = bidder_id)
                else:
                    context["item_lelang"] = item_lelang.objects.all()[0] #bidder_lelang.objects.all().filter(bidder = bidder_id)
                context['user_type'] = request.user.user_type
                return render(request, 'index_cca.html', context)
            return render(request, 'index.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')


def dashboard_bidder(request):
    if request.user.is_authenticated:
        # check company
        context = {}
        user = request.user
        vbidder_perwakilan = bidder_perwakilan.objects.all().filter(users_id = user.id)
        bidder_id = vbidder_perwakilan[0].bidder_id
        vbidder = bidder.objects.all().filter(id = bidder_id)
        context["bidder"] = vbidder
        ttd = signature2.objects.all().filter(bidder=bidder_id)
        if ttd:
            context["signature"] = ttd[0].ttd
            context["signature_id"] = ttd[0].id
        else:
            context["signature"] = None
            context["signature_id"] = None
        if request.GET.get("id"):
            vbidder_lelang = bidder_lelang.objects.all().filter(bidder = bidder_id, item_lelang=request.GET.get("id"))
        else:
            vbidder_lelang = bidder_lelang.objects.all().filter(bidder = bidder_id).order_by('created')
        context["bidder_lelang"] = vbidder_lelang[0]
        context["bidder_id"] = bidder_id
        context["ip_address"] = get_client_ip(request)
        context["item_lelang"] = bidder_lelang.objects.all().filter(bidder = bidder_id)
        dt = timezone.now()
        tahapan = jadwal_seleksi.objects.all().filter(item_lelang=vbidder_lelang[0].item_lelang).filter(tanggal_akhir__gte=dt).filter(tanggal_awal__lte=dt)
        if tahapan:
            context["tahapan"]  = tahapan[0]
        else:
            context["tahapan"]  = None
        context['user_type'] = request.user.user_type
        print(context)
        return render(request, 'dash_bidder_cca.html', context)
    else:
        return render(request, 'index.html')

def dashboard_auctioner(request):
    if request.user.is_authenticated:
        # check company
        context = {}
        user = request.user
        vauctioner1 = tim_lelang.objects.all().filter(users = user.id)
        if (vauctioner1):
            auctioner_id = vauctioner1[0].id
            if request.GET.get("id"):
                vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id, item_lelang=request.GET.get("id"))
            else:
                vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id).order_by('created')
            context["auctioner"] = vauctioner[0]
            context["item_lelang"] = auctioner_lelang.objects.all().filter(auctioner = auctioner_id)
            print(context)
            return render(request, 'dash_auctioner_cca.html', context)
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def jadwal(request):
    context ={}
    if request.user.is_authenticated:
        if request.GET.get("id"):
            id = request.GET.get("id")
            if request.GET.get("edit"):
                data = get_object_or_404(models.round_schedule_cca, item = id)
                form = forms.jadwalCCAForm(instance=data)
                context["form"] = form
                #print(render_to_string("smra_jadwal_form.html", context))
                return render(request, "cca_jadwal_form.html", context)
            else:
                form = forms.jadwalCCAForm({"item":id})
                return render(request, "smra_jadwal_form.html", {"form": form})        
    else:
        return render(request, 'index.html')


class hasil_ccaListView(MultiTableMixin, TemplateView):
    model = models.hasil_cca
    table_class = tables.hasil_ccaTable
    template_name = 'hasil_cca_tabs.html'
    table_pagination = False
    def get_tables(self):
#        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk']).order_by('id')
        hasil = models.hasil_cca.objects.filter(item_lelang = self.kwargs['pk'], valid=True).distinct('round').order_by('round')
        tbls = []
        if self.request.user.user_type=="B":
            bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)[0]
        for i in hasil:
            if self.request.user.user_type=="B":
                item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
                id = []
                for j in item_llg:
                    id.append(j.id)
                tbls.append(tables.hasil_ccaTable(models.hasil2_detail_cca.objects.all().filter(item__in=id,parent__bidder=bdr, parent__round=i.round, parent__valid=True).order_by('-parent__round')))
            else:
                tbls.append(tables.auctioner_hasilTable(models.hasil2_detail_cca.objects.all().filter(parent__item_lelang = self.kwargs['pk'],parent__round=i.round,parent__valid=True).order_by('-parent__round','ranking')))
        return tbls

    def get_context_data(self, **kwargs):
        context = super(hasil_ccaListView, self).get_context_data(**kwargs)
        hasil = models.hasil_cca.objects.filter(item_lelang = self.kwargs['pk'], valid=True).distinct('round').order_by('round')

#        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        tabs = []
        for i in hasil:
            tabs.append(i)
        context['tabs'] = tabs
        return context

def dashboard(request):
    #check hasil di SMRA;
    itm_lelang = models.hasil_cca.objects.all().distinct('item_lelang')
    context = {}
    id = []
    for i in itm_lelang:
        id.append(i.item_lelang)
    i_lelang = item_lelang.objects.filter(id__in = id)
    context["item_lelang"] = i_lelang
    return render(request, 'dashboard_cca.html', context)

def hasil_chart(request, pk):
    from pygal.style import Style
    locale.setlocale( locale.LC_ALL, 'id_ID.UTF-8' )
    custom_style = Style(
        transition='400ms ease-in',
        title_font_size = 24,
        label_font_size = 24,
        major_label_font_size = 24,
    )    
    item_llg = detail_itemlelang.objects.all().get(id=pk)
    judul = item_lelang.objects.all().get(id = item_llg.item_lelang.id)
    m = models.auctioner_hasil_cca.objects.all().filter(item=pk).order_by('round')
    if m:
        df = read_frame(m)
        df['increase'] = (df['harga'].pct_change())*100
    #    b = df.to_dict(orient="records")
        min = df['harga'].min()/1000000
        max = df['harga'].max()/1000000
        bar_chart = pygal.Bar(show_legend=False,style=custom_style)
        bar_chart.title = 'Grafik Kenaikan Total Penawaran\n' + judul.nama_lelang + ' band ' + item_llg.band + "\n(dalam jutaan Rupiah)"
        bar_chart.zero = min-1/100*min
        bar_chart.x_labels = df['round']
        bar_chart.add('', df['harga']/1000000)
        bar_chart.range=(min, max+1/100*max)
        bar_chart.value_formatter = lambda y: locale.currency(y, grouping=True)
        context = {}
        return bar_chart.render_django_response(is_unicode=True)
    else:
        bar_chart = pygal.Bar(show_legend=False,style=custom_style)
        bar_chart.title = 'Grafik Kenaikan Total Penawaran \n' + judul.nama_lelang 
        context = {}
        return bar_chart.render_django_response(is_unicode=True)

def hasil_chart_maxmin(request, pk):
    from pygal.style import Style
    locale.setlocale( locale.LC_ALL, 'id_ID.UTF-8' )
    custom_style = Style(
        transition='400ms ease-in',
        title_font_size = 24,
        label_font_size = 24,
        major_label_font_size = 24,
    )    
    item_llg = detail_itemlelang.objects.all().get(id=pk)
    judul = item_lelang.objects.all().get(id = item_llg.item_lelang.id)
    m = models.hasil_auctioner_maxmin_cca.objects.all().filter(item=pk).order_by('round')
    if m:
        df = read_frame(m)
        print(df)
        min = df['harga_min'].min()/1000000
        max = df['harga_max'].max()/1000000
        bar_chart = pygal.Bar(style=custom_style)
        bar_chart.title = 'Grafik Kenaikan Total Penawaran (Max-Min)\n' + judul.nama_lelang + ' band ' + item_llg.band + "\n(dalam jutaan Rupiah)"
        bar_chart.range=(min, max+1/100*max)
        bar_chart.zero = min-1/100*min
        bar_chart.x_labels = df['round']

        bar_chart.add('Min', df['harga_min']/1000000)
        bar_chart.add('Max', df['harga_max']/1000000)
        bar_chart.value_formatter = lambda y: locale.currency(y, grouping=True)
        context = {}
        return bar_chart.render_django_response(is_unicode=True)
    else:
        bar_chart = pygal.Bar(show_legend=False,style=custom_style)
        bar_chart.title = 'Grafik Kenaikan Total Penawaran \n' + judul.nama_lelang 
        context = {}
        return bar_chart.render_django_response(is_unicode=True)

class hasil_invalidccaListView(MultiTableMixin, TemplateView):
    model = models.hasil_cca
    table_class = tables.hasil_ccaTable
    template_name = 'hasil_cca_tabs_invalid.html'
    def get_tables(self):
#        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk']).order_by('id')
        hasil = models.hasil_cca.objects.filter(item_lelang = self.kwargs['pk']).distinct('round').order_by('round')
        tbls = []
        if self.request.user.user_type=="B":
            bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)[0]
        for i in hasil:
            if self.request.user.user_type=="B":
                item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
                id = []
                for j in item_llg:
                    id.append(j.id)
                tbls.append(tables.hasil_ccaTable(models.hasil2_detail_cca.objects.all().filter(item__in=id,parent__bidder=bdr, parent__round=i.round, parent__valid=False).order_by('-parent__round')))
            else:
                tbls.append(tables.auctioner_hasilTable(models.hasil2_detail_cca.objects.all().filter(parent__item_lelang = self.kwargs['pk'],parent__round=i.round, parent__valid=False).order_by('-parent__round','ranking')))
        return tbls

    def get_context_data(self, **kwargs):
        context = super(hasil_invalidccaListView, self).get_context_data(**kwargs)
        hasil = models.hasil_cca.objects.filter(item_lelang = self.kwargs['pk']).distinct('round').order_by('round')

#        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        tabs = []
        for i in hasil:
            tabs.append(i)
        context['tabs'] = tabs
        return context

class matirx_hasil_crListView(MultiTableMixin, TemplateView):
    model = models.matrix2_cr
    table_class = tables.matrix_hasil_crTable
    template_name = 'matrix_cca_tabs.html'
    def get_tables(self):
#        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk']).order_by('id')
        tbls = []
        if self.request.user.user_type=="B":
            bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)[0]
            hasil = models.matrix2_cr.objects.filter(parent__item_lelang = self.kwargs['pk'], parent__bidder = bdr).distinct('kombinasi').order_by('kombinasi','-parent__round')
        else:
            hasil = models.hasil_cca.objects.filter(item_lelang = self.kwargs['pk']).distinct('round').order_by('round')
        for i in hasil:
            if self.request.user.user_type=="B":
                tbls.append(tables.matrix_hasil_crTable(models.matrix2_cr.objects.all().filter(parent=i.parent).distinct('kombinasi').order_by('kombinasi')))
            else:
                tbls.append(tables.matrix_hasil_crTable(models.matrix2_cr.objects.all().filter(item=i).order_by('-parent__round')))
        return tbls

    def get_context_data(self, **kwargs):
        context = super(matirx_hasil_crListView, self).get_context_data(**kwargs)
        if self.request.user.user_type=="B":
            bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)[0]
            hasil = models.matrix2_cr.objects.filter(parent__item_lelang = self.kwargs['pk'], parent__bidder = bdr).distinct('kombinasi').order_by('kombinasi','-parent__round')
        else:
            hasil = models.hasil_cca.objects.filter(item_lelang = self.kwargs['pk']).distinct('round').order_by('round')

#        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        tabs = []
        for i in hasil:
            tabs.append(i)
        context['tabs'] = tabs
        return context
        
class auctioner_hasilListView(SingleTableMixin, generic.ListView):
    model = models.auctioner_hasil_cca
    table_class = tables.auctioner_hasilTable
    template_name = 'table_detail_itemlelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        item_llg = item_lelang.objects.all().filter(id=self.kwargs['pk'])[0]
        return models.auctioner_hasil_cca.objects.all().filter(item_lelang=item_llg.id).order_by('round')


class round_ccsListView(SingleTableMixin, generic.ListView):
    model = models.round_cca
    table_class = tables.round_ccaTable
    template_name = 'table_detail_itemlelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        item_llg = item_lelang.objects.all().filter(id=self.kwargs['pk'])[0]
        bdr = bidder.objects.all().filter(id=self.kwargs['bidder'])[0]
        return models.round_cca.objects.all().filter(item_lelang=item_llg.id).filter(bidder=bdr)

class round_detail_ccsListView(SingleTableMixin, generic.ListView):
    model = models.round_detail_cca
    table_class = tables.round_detail_ccaTable
    template_name = 'table_detail_itemlelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        item_llg = item_lelang.objects.all().filter(id=self.kwargs['pk'])[0]
        bdr = bidder_user.objects.all().filter(id=self.kwargs['bidder'])[0]
        return models.round_detail_cca.objects.all().filter(parent__item_lelang=item_llg.id).filter(parent__bidder=bdr).order_by('item__urutan')

class price_increaseListView(MultiTableMixin, TemplateView):
    #model = models.price_increase
    #table_class = tables.price_increaseTable
    template_name = 'price_increase2_table.html'

    def get_tables(self):
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk']).order_by('id')
        tbls = []
        for i in item_llg:
            tbls.append(tables.price_increaseTable(models.cca_price_increase.objects.all().filter(detail_item=i)))

        return tbls

    #def get_queryset(self, **kwargs):
    #    qs = super().get_queryset(**kwargs)
    #    item_llg = item_lelang.objects.all().filter(id=self.kwargs['pk'])[0]
    #    return models.price_increase.objects.all().filter(item=item_llg.id)

    def get_context_data(self, **kwargs):
        context = super(price_increaseListView, self).get_context_data(**kwargs)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk']).order_by('id')
        tabs = []
        for i in item_llg:
            tabs.append(i)
        context['tabs'] = tabs
        return context


class obyek_seleksiCreateView(BSModalCreateView):
    template_name = 'obyek_seleksi_cca.html'
    form_class = forms.obyek_seleksiForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')

    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class obyek_seleksiUpdateView(BSModalUpdateView):
    template_name = 'obyek_seleksi_cca.html'
    form_class = forms.obyek_seleksiForm
    model = models.obyek_seleksi_cca
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')

    def get_initial(self):
        return {"id": self.kwargs["pk"]}

class obyek_seleksiGroupView(MultiTableMixin, generic.ListView):
    model = models.obyek_seleksi_cca
    template_name = 'obyek_seleksi_group.html'
    #table_class = tables.obyek_seleksi_groupTable
    def get_tables(self):
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk']).order_by('id')
        tbls = []
        for i in item_llg:
            tbls.append(tables.obyek_seleksiTable(models.obyek_seleksi_cca.objects.all().filter(item=i)))

        return tbls

    def get_context_data(self, **kwargs):
        context = super(obyek_seleksiGroupView, self).get_context_data(**kwargs)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk']).order_by('id')
        tabs = []
        for i in item_llg:
            tabs.append(i)
        context['tabs'] = tabs
        return context

class obyek_seleksiView(SingleTableMixin, generic.ListView):
    model = models.obyek_seleksi_cca
#    table_class = tables.obyek_seleksiTable
    template_name = 'table_detail_itemlelang.html'

    def get_table_class(self):
        if self.request.user.user_type =='B':
            return tables.obyek_seleksi2Table
        else:
            return tables.obyek_seleksiTable

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type == "B":
            bdr_user = bidder_user.objects.all().get(users__id = self.request.user.id)
            obj =  models.obyek_seleksi_cca.objects.all().filter(bidder_user = bdr_user, item__id=self.kwargs['pk'])
        else:
            obj =  models.obyek_seleksi_cca.objects.all().filter(item__id=self.kwargs['pk'])
        return obj

class price_increaseCreateView(BSModalCreateView):
    template_name = 'modal_price_increase.html'
    form_class = forms.price_increaseForm
    #model = models.price_increase
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')

    def get_initial(self):
        return {"item": self.kwargs["pk"]}

class price_increaseUpdateView(BSModalUpdateView):
    template_name = 'modal_price_increase.html'
    form_class = forms.price_increaseForm
    model = models.cca_price_increase
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')

    def get_initial(self):
        return {"id": self.kwargs["pk"]}


class PdfsView(PDFView):
    template_name = 'ba_putaran_cca.html'

    def get_context_data(self, *args, **kwargs):
        t = Terbilang()
        context = super().get_context_data(*args, **kwargs)
        context = {}
        user = self.request.user
        harga = 100000000000
        block = 1
        putaran = 1
        seleksi = "Lelang"
        tahun = "2022"
        item_llg = detail_itemlelang.objects.get(pk=1)
        b = 45
        i = 1
        bdr = bidder.objects.get(pk=b)
        data= [
                {
                    "id": 136,
                    "price": 320,
                    "block": 1,
                    "bidder": 46,
                    "item": 1,
                    "item_lelang": 1,
                    "prev_price": 320,
                    "prev_block": 1,
                    "min_price": 300,
                    "status_round": "CLOSED",
                    "mulai": "2023-07-26T21:00:00+07:00",
                    "selesai": "2023-07-26T21:30:00+07:00",
                    "round": 2,
                    "band": "700 MHz",
                    "max_block": 3,
                    "spectrum_cap": 2,
                    "lock": True,
                    "penawaran": 0,
                    "jenis": "CLOCK",
                    "status_sah": False,
                    "eli_point": 30,
                    "activity": 30
                },
                {
                    "id": 137,
                    "price": 220,
                    "block": 1,
                    "bidder": 46,
                    "item": 3,
                    "item_lelang": 1,
                    "prev_price": 220,
                    "prev_block": 1,
                    "min_price": 200,
                    "status_round": "CLOSED",
                    "mulai": "2023-07-26T21:00:00+07:00",
                    "selesai": "2023-07-26T21:30:00+07:00",
                    "round": 2,
                    "band": "2600 MHz",
                    "max_block": 2,
                    "spectrum_cap": 1,
                    "lock": True,
                    "penawaran": 0,
                    "jenis": "CLOCK",
                    "status_sah": False,
                    "eli_point": 20,
                    "activity": 20
                },
                {
                    "id": 138,
                    "price": 170,
                    "block": 1,
                    "bidder": 46,
                    "item": 11,
                    "item_lelang": 1,
                    "prev_price": 17,
                    "prev_block": 1,
                    "min_price": 150,
                    "status_round": "CLOSED",
                    "mulai": "2023-07-26T21:00:00+07:00",
                    "selesai": "2023-07-26T21:30:00+07:00",
                    "round": 2,
                    "band": "3500 MHz",
                    "max_block": 2,
                    "spectrum_cap": 1,
                    "lock": True,
                    "penawaran": 0,
                    "jenis": "CLOCK",
                    "status_sah": False,
                    "eli_point": 15,
                    "activity": 15
                },
                {
                    "id": 139,
                    "price": 180,
                    "block": 1,
                    "bidder": 46,
                    "item": 15,
                    "item_lelang": 1,
                    "prev_price": 18,
                    "prev_block": 1,
                    "min_price": 100,
                    "status_round": "CLOSED",
                    "mulai": "2023-07-26T21:00:00+07:00",
                    "selesai": "2023-07-26T21:30:00+07:00",
                    "round": 2,
                    "band": "26 GHz",
                    "max_block": 4,
                    "spectrum_cap": 2,
                    "lock": True,
                    "penawaran": 0,
                    "jenis": "CLOCK",
                    "status_sah": False,
                    "eli_point": 10,
                    "activity": 10
                },
                {
                    "id": 140,
                    "price": 0,
                    "block": 0,
                    "bidder": 46,
                    "item": 18,
                    "item_lelang": 1,
                    "prev_price": 0,
                    "prev_block": 0,
                    "min_price": 120000000,
                    "status_round": "CLOSED",
                    "mulai": "2023-07-26T21:00:00+07:00",
                    "selesai": "2023-07-26T21:30:00+07:00",
                    "round": 2,
                    "band": "120",
                    "max_block": 0,
                    "spectrum_cap": 0,
                    "lock": True,
                    "penawaran": 0,
                    "jenis": "CLOCK",
                    "status_sah": False,
                    "eli_point": 120,
                    "activity": 0
                }
            ]
        data_template = []
        total = 0
        putaran = 1
        for d in data:
            item_llg = detail_itemlelang.objects.get(pk=d['item'])
            putaran = int(d['round'])
            total = total + float(d['price'])
            data_template.append({
                'price':float(d['price']),
                'block':int(d['block']),
                'putaran':putaran, 
                'band':item_llg.band,
                'tblock': t.parse(int(d['block'])).getresult(),
                'tputaran': t.parse(putaran).getresult(),
            })

        vbidder_perwakilan = bidder_perwakilan.objects.all().filter(users_id = user.id)
        if vbidder_perwakilan:
            bidder_id = vbidder_perwakilan[0].bidder_id
            vbidder = bidder.objects.all().filter(id = bidder_id)
            context["bidder"] = vbidder
            vbidder_lelang = bidder_lelang.objects.all().filter(bidder = bidder_id)
            context["bidder_lelang"] = vbidder_lelang
            context["bidder_id"] = bidder_id
            context["wakil"] = vbidder_perwakilan[0].nama_lengkap
            context["tahun"] = item_llg.item_lelang.tahun
            context["seleksi"] = item_llg.item_lelang.nama_lelang
            context["obyek"] = data_template
            context["total"] = total
            context["ttotal"] = t.parse(int(total)).getresult(),
            context["putaran"] = putaran
            context["tputaran"] = t.parse(int(putaran)).getresult(),


        return context

class detail_itemlelangListView(SingleTableMixin, generic.ListView):
    model = models.detail_itemlelang
    #form_class = forms.detail_itemlelangForm
    table_class = tables.item_lelang_detailTable
    template_name = 'table_detail_itemlelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.detail_itemlelang.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('urutan')
        
class detail_itemlelangCreateView(BSModalCreateView):
    template_name = 'modal_obyeklelang_cca.html'
    form_class = forms.obyekSeleksi2Form
    #model = models.price_increase
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')

    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class detail_itemlelangUpdateView(BSModalUpdateView):
    template_name = 'modal_obyeklelang_cca.html'
    form_class = forms.obyekSeleksi2Form
    model = detail_itemlelang
    success_message = 'Success: Book was created.'
    success_url = "/"

    def get_initial(self):
        return {"id": self.kwargs["pk"]}