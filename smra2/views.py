from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from . import tables
#from smra.models import round_schedule_smra
from userman.models import tim_lelang, bidder_perwakilan, bidder, bidder_user, viewers
from adm_lelang.models import jadwal_seleksi, auctioner_lelang, bidder_lelang, item_lelang, detail_itemlelang
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
from django_tables2 import SingleTableMixin, MultiTableMixin
from django.views.generic.base import TemplateView
from django_filters.views import FilterView
from adm_lelang import utils
from django_pivot.pivot import pivot
import django_tables2
from django_renderpdf.views import PDFView
from terbilang import Terbilang
import locale
from django.db.models import Max
from django.utils import timezone
from django.http import FileResponse
from django_pandas.io import read_frame
from django.http import JsonResponse
import pygal
from pygal.style import DefaultStyle
from pygal.style import RedBlueStyle
from pygal.style import TurquoiseStyle
from django.conf import settings as SETTINGS
from datetime import datetime, timedelta
from . import tasks
from .utils import ws_publish

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home(request):
    if request.user.is_authenticated:
        url = "/smra2/manajemen_smra/"    
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_smra2.html',context)
        if request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_smra2.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_smra2.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_smra2.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')   

def settings(request):
    if request.user.is_authenticated:
        url = "/smra2/settings/"    
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'settings_smra2.html',context)
            
        if request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'settings_smra2.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'settings_smra2.html',context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'settings_smra2.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')   


def dashboard_bidder(request):
    url = "/smra2/dashboard_bidder/"    
    if request.user.is_authenticated:
        if request.user.user_type == "B":
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            bdr = bidder_user.objects.get(users__id = request.user.id)
            perwakilan = bidder_perwakilan.objects.all().filter(bidder = bdr, profil_peruri__isnull  = False, peruri_ttd__isnull=False)
            context['perwakilan'] = perwakilan
            context['bidder_id'] = bdr.id
            context.update(tabs)
            return render(request, 'dash_bidder_smra2.html',context)

            """            url = '/smra2/dashboard_bidder/'
            context = {}
            user = request.user
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            bdr = bidder_user.objects.get(users__id = request.user.id)
            perwakilan = bidder_perwakilan.objects.all().filter(bidder = bdr)
            context['perwakilan'] = perwakilan
            context.update(tabs)
            return render(request, 'dash_bidder_smra2.html', context)"""
        elif request.user.user_type == "A":
            #print(request.user.user_type)
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'dash_auctioner_smra2.html',context)

            """            context = {}
            user = request.user
            context = utils.get_judul_context_admin(request)
            vauctioner1 = tim_lelang.objects.all().filter(users = user.id)
            if vauctioner1:
                auctioner_id = vauctioner1[0].id
                if request.GET.get("id"):
                    vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id, item_lelang=request.GET.get("id"))
                else:
                    vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id).order_by('created')
                context["auctioner"] = vauctioner[0]
                context["item_lelang"] = auctioner_lelang.objects.all().filter(auctioner = auctioner_id)
                context['user_type'] = request.user.user_type
                return render(request, 'dash_auctioner_smra2.html', context) 
            else:
                return redirect("/")"""
        elif request.user.user_type == "C":
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            """            vauctioner1 = tim_lelang.objects.all().filter(users = request.user.id)
            if vauctioner1:
                auctioner_id = vauctioner1[0].id
                if request.GET.get("id"):
                    vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id, item_lelang=request.GET.get("id"))
                else:
                    vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id).order_by('created')
                context["auctioner"] = vauctioner[0]
                context["item_lelang"] = auctioner_lelang.objects.all().filter(auctioner = auctioner_id)
                context['user_type'] = request.user.user_type"""
            return render(request, 'dash_auctioner_smra2.html', context)    

            """            context = {}
            user = request.user
            context = utils.get_judul_context_auctioneer(request)
            vauctioner1 = tim_lelang.objects.all().filter(users = user.id)
            if vauctioner1:
                auctioner_id = vauctioner1[0].id
                if request.GET.get("id"):
                    vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id, item_lelang=request.GET.get("id"))
                else:
                    vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id).order_by('created')
                context["auctioner"] = vauctioner[0]
                context["item_lelang"] = auctioner_lelang.objects.all().filter(auctioner = auctioner_id)
                context['user_type'] = request.user.user_type
                return render(request, 'dash_auctioner_smra2.html', context)    
            else:
                return  redirect("/")"""
        #elif request.user.user_type == "V":
        #    context = {}
        #    user = request.user
        #    vwr = viewers.objects.all().filter(users = user.id)
        #    if vauctioner1:
        #        auctioner_id = vauctioner1[0].id
        #        if request.GET.get("id"):
        #            vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id, item_lelang=request.GET.get("id"))
        #        else:
        #            vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id).order_by('created')
        #        context["auctioner"] = vauctioner[0]
        #       context["item_lelang"] = auctioner_lelang.objects.all().filter(auctioner = auctioner_id)
        #        context['user_type'] = request.user.user_type
        #        return render(request, 'dash_viewer_smra2.html', context)        
        elif request.user.user_type == "V":
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url,context["item_lelang"])
            context.update(tabs)
            return render(request, 'dash_viewer_smra2.html', context)    
        
        else:
            return redirect("/")
    else:
        return redirect("/")

def hasil_putaran_bidder(request):
    if request.user.is_authenticated:
        # check company
        context = {}
        user = request.user
        vbidder_perwakilan = bidder_perwakilan.objects.all().filter(users_id = user.id)
        if vbidder_perwakilan:
            bidder_id = vbidder_perwakilan[0].bidder_id
            vbidder = bidder.objects.all().filter(id = bidder_id)
            context["bidder"] = vbidder
            if request.GET.get("id"):
                vbidder_lelang = bidder_lelang.objects.all().filter(bidder = bidder_id, item_lelang=request.GET.get("id"))
            else:
                vbidder_lelang = bidder_lelang.objects.all().filter(bidder = bidder_id).order_by('created')
            dt = timezone.now()
            tahapan = jadwal_seleksi.objects.all().filter(item_lelang=vbidder_lelang[0].item_lelang).filter(tanggal_akhir__gte=dt).filter(tanggal_awal__lte=dt)
            context["bidder_lelang"] = vbidder_lelang[0]
            context["bidder_id"] = bidder_id
            context["ip_address"] = get_client_ip(request)
            context["item_lelang"] = bidder_lelang.objects.all().filter(bidder = bidder_id)
            return render(request, 'hasil_bidder_smra2.html', context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def hasil_putaran_auctioneer(request):
    if request.user.is_authenticated:
        url = "/smra2/hasil_putaran_auctioneer/"    
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'hasil_auctioner_smra2.html',context)
        if request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'hasil_auctioner_smra2.html',context)
        if request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'hasil_auctioner_smra2.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context2(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'hasil_auctioner_smra2.html',context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
    else:
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')   

def dashboard_auctioner(request):
    if request.user.is_authenticated:
        # check company
        context = {}
        user = request.user
        vauctioner1 = tim_lelang.objects.all().filter(users = user.id)
        if vauctioner1:
            auctioner_id = vauctioner1[0].id
            if request.GET.get("id"):
                vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id, item_lelang=request.GET.get("id"))
            else:
                vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id).order_by('created')
            context["auctioner"] = vauctioner[0]
            context["item_lelang"] = auctioner_lelang.objects.all().filter(auctioner = auctioner_id)
            context['user_type'] = request.user.user_type
            return render(request, 'dash_auctioner_smra2.html', context)
        else:
            return redirect("/")
    else:
        return redirect("/")

def dashboard_auctioner2(request):
    if request.user.is_authenticated:
        # check company
        context = {}
        user = request.user
        vauctioner1 = tim_lelang.objects.all().filter(users = user.id)
        if vauctioner1:
            auctioner_id = vauctioner1[0].id
            if request.GET.get("id"):
                vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id, item_lelang=request.GET.get("id"))
            else:
                vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id).order_by('created')
            context["auctioner"] = vauctioner[0]
            context["item_lelang"] = auctioner_lelang.objects.all().filter(auctioner = auctioner_id)
            context['user_type'] = request.user.user_type
            return render(request, 'dash_auctioner_smra3.html', context)
        else:
            return redirect("/")
    else:
        return redirect("/")

def dashboard(request):
    #check hasil di SMRA;
    # url = "/smra2/dashboard/"
    # itm_lelang = models.auctioner_hasil.objects.all().distinct('item_lelang')
    # context = utils.get_judul_context_admin(request)
    # tabs = utils.get_tab_context2(request,url, context["item_lelang"])
    # context = {}
    # context["item_lelang"] = itm_lelang
    # context.update(tabs)
    # return render(request, 'dashboard.html', context)
    
    #check hasil di SMRA;
    if request.user.is_authenticated:
        itm_lelang = models.auctioner_hasil.objects.all().distinct('item_lelang')
        context = {}
        context["item_lelang"] = itm_lelang
        return render(request, 'dashboard.html', context)

def create_schedule(request, pk=None):
    if request.user.is_authenticated:
        itm = item_lelang.objects.get(pk = pk)
        dt = timezone.localtime()
        td = timezone.localtime().today().isoweekday()
        today_weekday = dt.today().weekday()
        #today_weekday = today.weekday()
        hari = request.GET.get("hari")
        jam = request.GET.get("waktu_mulai")
        lama = request.GET.get("lama_putaran")
        jeda = request.GET.get("jeda_putaran")
        putaran = int(request.GET.get("jumlah_putaran"))
        days_ahead = (int(hari) - today_weekday) % 7
        print(days_ahead,hari,today_weekday)
        future_date = datetime.today() + timedelta(days=days_ahead)
        waktu_mulai = datetime.strptime(future_date.strftime("%d/%m/%Y") + " " + jam,"%d/%m/%Y %H:%M")
        for i in range(putaran):
            waktu_selesai = waktu_mulai + timedelta(minutes=int(lama))
            mulai_berikutnya = waktu_selesai + timedelta(minutes=int(jeda))
            selesai_berikutnya = mulai_berikutnya + timedelta(minutes=int(lama))
            data = models.round_schedule_smra2(hari = hari, item=itm, mulai= waktu_mulai, selesai= waktu_selesai, dibuat_oleh=request.user)
            data.save()
            tasks.mulai(itm.id, extra_param={'next': str(mulai_berikutnya), 'end': str(selesai_berikutnya),'id_round_scheduler': data.id, 'lama': int(lama) },verbose_name="Memulai Putaran", schedule=waktu_mulai, creator=data)
            waktu_mulai = waktu_selesai + timedelta(minutes=int(jeda))
            tasks.selesai(itm.id, extra_param={'next_mulai': str(mulai_berikutnya), 'next_selesai':str(selesai_berikutnya), "id_round_scheduler": data.id},verbose_name="Mengakhiri Putaran", schedule=waktu_selesai, creator=data)
    return JsonResponse({"statuss":"OK"})

def clear_schedule(request, pk=None):
    if request.user.is_authenticated:
        vtasks = BTask.objects.filter(creator_object_id = pk).delete()
        data = models.round_schedule_smra2.objects.filter(item__id=pk)
        id = []
        for d in data:
            id.append(d.id)
        vtasks = BTask.objects.filter(creator_object_id__in = id).delete()
        data.delete()        
    return JsonResponse({"statuss":"OK"})

def clear_schedulebg(request, pk=None):
    if request.user.is_authenticated:
        BTask.objects.filter(run_at__date= timezone.localtime().today()).delete()
    return JsonResponse({"statuss":"OK"})

def push_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ws_publish(data)

def run_schedule(request, pk=None):
    ptr = []
    if request.user.is_authenticated:
        dt = timezone.localtime()
        td = timezone.localtime().today()
        itm = detail_itemlelang.objects.get(pk = pk)
        hari = str(timezone.localtime().today().isoweekday())
        putaran = round_schedule_smra2.objects.filter(item=itm.item_lelang, hari=hari, mulai__gte = datetime.strptime(dt.strftime("%H:%M"),"%H:%M"))
        for r in putaran:
            mulai = datetime.strptime(td.strftime("%d/%m/%Y") + " " + r.mulai.strftime("%H:%M:00+07:00"),"%d/%m/%Y %H:%M:00+07:00")
            ptr.append(mulai)
            akhir = schedule=datetime.strptime(td.strftime("%d/%m/%Y") + " " + r.selesai.strftime("%H:%M:00+07:00"),"%d/%m/%Y %H:%M:00+07:00")
            tasks.mulai(pk,hari, mulai.strftime("%d/%m/%Y %H:%M:00"), akhir.strftime("%d/%m/%Y %H:%M:00"), verbose_name="Memulai Putaran", schedule=mulai)
            tasks.selesai(pk,hari, mulai.strftime("%d/%m/%Y %H:%M:00"), akhir.strftime("%d/%m/%Y %H:%M:00"), verbose_name="Mengakhiri Putaran", schedule=akhir)
    return JsonResponse({"status":ptr})

def docxview(request, pk, bidder):
    from docx import Document
    from htmldocx import HtmlToDocx

    template_name = 'ba_putaran.html'
    document = Document()
    new_parser = HtmlToDocx()
    strhtml = render_to_string(template_name)
    new_parser.add_html_to_document(strhtml, document)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=download.docx'
    document.save(response)
    return response

class PdfsView(PDFView):
    template_name = 'ba_putaran.html'

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
        bdr = bidder.objects.get(pk=45)

        vbidder_perwakilan = bidder_perwakilan.objects.all().filter(users_id = user.id)
        if vbidder_perwakilan:
            bidder_id = vbidder_perwakilan[0].bidder_id
            vbidder = bidder.objects.all().filter(id = bidder_id)
            context["bidder"] = vbidder
            vbidder_lelang = bidder_lelang.objects.all().filter(bidder = bidder_id)
            context["bidder_lelang"] = vbidder_lelang
            context["bidder_id"] = bidder_id
            context["harga"] = harga
            context["terbilang"] = t.parse(str(harga)).getresult()
            context["wakil"] = vbidder_perwakilan[0].nama_lengkap
            context["tahun"] = item_llg.item_lelang.tahun
            context["seleksi"] = item_llg.item_lelang.nama_lelang
            context["block"] = block
            context["block_t"] = t.parse(block).getresult()
            context["putaran"] = putaran
            context["putaran_t"] = t.parse(putaran).getresult()
            context["terbilang"] = t.parse(harga).getresult()   
        return context


def hasil_chart(request, pk):
    from pygal.style import Style
    #locale.setlocale( locale.LC_ALL, 'id_ID.UTF-8' )
    custom_style = Style(
        transition='400ms ease-in',
        title_font_size = 24,
        label_font_size = 24,
        major_label_font_size = 24,
    )    
    item_llg = detail_itemlelang.objects.all().get(id=pk)
    judul = item_lelang.objects.all().get(id = item_llg.item_lelang.id)
    m = models.auctioner_hasil.objects.all().filter(item=pk).order_by('round')
    if m:
        df = read_frame(m)
        df['increase'] = (df['harga'].pct_change())*100
        min = df['harga'].min()/1000000
        max = df['harga'].max()/1000000
        bar_chart = pygal.StackedLine(height=300, fill=True, interpolate='cubic', style=RedBlueStyle)
        #bar_chart.title = 'Grafik 2 Kenaikan Total Penawaran\n' + judul.nama_lelang + ' band ' + item_llg.band + "\n(dalam jutaan Rupiah)"
        bar_chart.zero = min-1/100*min
        bar_chart.x_labels = df['round']
        bar_chart.add('', df['harga']/1000000)
        bar_chart.range=(min, max+1/100*max)
        #bar_chart.value_formatter = lambda y: locale.currency(y, grouping=True)
        #bar_chart.value_formatter = lambda y: y
        context = {}
        return bar_chart.render_django_response(is_unicode=True)
    else:
        bar_chart = pygal.StackedLine(height=300, fill=True, interpolate='cubic', style=RedBlueStyle)
        #bar_chart.title = 'Grafik Kenaikan Total Penawaran \n' + judul.nama_lelang 
        context = {}
        return bar_chart.render_django_response(is_unicode=True)

def hasil_chart_maxmin(request, pk):
    from pygal.style import Style
    #locale.setlocale( locale.LC_ALL, 'id_ID.UTF-8' )
    custom_style = Style(
        transition='400ms ease-in',
        title_font_size = 24,
        label_font_size = 36,
        major_label_font_size = 24,
        plot_background = '#343a40',
        foreground_subtle='#630C0D',
        
        background='transparent',
        opacity='.8',
        foreground_strong='#53A0E8',
        foreground='#ffffff',
        value_font_size=25, 
        value_colors=('white','white',),
    )    
    #item_llg = detail_itemlelang.objects.all().get(id=pk)
    #judul = item_lelang.objects.all().get(id = item_llg.item_lelang.id)
    rsmra = models.round_smra2.objects.all().filter(item=pk).order_by("-round")[0]
    maxround=rsmra.round

    m = models.hasil_auctioner_maxmin.objects.all().filter(item=pk).order_by('round')
   
    if m:
        df = read_frame(m)
        #min = df['harga_min'].min()/1000000
        max = df['harga_max'].max()/1000000
        ran = df['harga_minimal'].min()/1000000

        #dt1 = list()
        dt2 = list()
        dl = list()
        
        for i in range (0, maxround) :
            #dt1.append(0)
            dt2.append(0)
            dl.append(i+1)
         
        i=0
        
        for a in m :
            #dt1[i] = a.harga_min/1000000
            dt2[i] = a.harga_max/1000000
            i = i +1
        

        bar_chart = pygal.Bar(height=350,legend_at_bottom=True, show_y_labels=False, print_values=True, print_values_position='top', style=custom_style)
        #bar_chart.title = 'Grafik Kenaikan Total Penawaran (Max-Min)\n' + judul.nama_lelang + ' band ' + item_llg.band + "\n(dalam jutaan Rupiah)"
        bar_chart.range=(0, max+1/100*max)
        bar_chart.zero = 0
        bar_chart.x_labels = dl

        #bar_chart.add('Min (jt rp)', dt1)
        bar_chart.add('Max (jt rp)', dt2)
        #bar_chart.value_formatter = lambda y: locale.currency(y, grouping=True)
        #bar_chart.value_formatter = lambda y: y
        context = {}
        return bar_chart.render_django_response(is_unicode=True)
    else:
        bar_chart = pygal.StackedLine(height=300, fill=True, interpolate='cubic', style=RedBlueStyle)
        #bar_chart.title = 'Grafik Kenaikan Total Penawaran \n' + judul.nama_lelang 
        context = {}
        return bar_chart.render_django_response(is_unicode=True)

def hasil_persen(request, pk):
    from pygal.style import Style
    #locale.setlocale( locale.LC_ALL, 'id_ID.UTF-8' )
    custom_style = Style(
        transition='400ms ease-in',
        title_font_size = 24,
        label_font_size = 36,
        major_label_font_size = 24,
        plot_background = '#343a40',
        foreground_subtle='#630C0D',
        colors=('#fbec5d','#fbec5d','#fbec5d','#9e6ffe'),
        background='transparent',
        opacity='.8',
        foreground_strong='#53A0E8',
        foreground='#ffffff',
        stroke_width = 10.0,
        value_font_size=25, 
        value_colors=('white',),
    )    
    #item_llg = detail_itemlelang.objects.all().get(id=pk)
    #judul = item_lelang.objects.all().get(id = item_llg.item_lelang.id)
    rsmra = models.round_smra2.objects.all().filter(item_lelang=pk).order_by("-round")[0]
    maxround=rsmra.round
    m = models.hasil_auctioner_maxmin.objects.all().filter(item_lelang=pk).order_by('round')
    print(str(m))
    if m:
        df = read_frame(m)
        max = df['persen1'].max()
        dt = list()
        dl = list()
        
        for i in range (0, maxround) :
            dt.append(0)
            dl.append(i+1)
        i=0

        for a in m :
            dt[i] = round(a.persen1,2)
            i = i +1

        for i in range (0, maxround) :
            if (dt[i]== 0 and i>0):
                 dt[i]=dt[i-1]

        #label
        bar_chart = pygal.Line(dots_size=20, height=350,  legend_at_bottom=True, print_values=True, print_values_position='top', show_x_labels=True, show_y_labels=False, style=custom_style)
        bar_chart.range=(0, max+1/100*max)
        bar_chart.zero = 0
        bar_chart.x_labels = dl

        bar_chart.add('% kenaikan', dt)
        #bar_chart.add('Max', df['harga_max']/1000000)
        #bar_chart.value_formatter = lambda y: locale.currency(y, grouping=True)
        #bar_chart.value_formatter = lambda y: y
        context = {}
        return bar_chart.render_django_response(is_unicode=True)
        
    else:
        bar_chart = pygal.StackedLine(height=300, fill=True, interpolate='cubic', style=RedBlueStyle)
        #bar_chart.title = 'Grafik Kenaikan Total Penawaran \n' + judul.nama_lelang 
        context = {}
        return bar_chart.render_django_response(is_unicode=True)

def hasil_peserta(request, pk):
    from pygal.style import Style
    #locale.setlocale( locale.LC_ALL, 'id_ID.UTF-8' )
    custom_style = Style(
        transition='400ms ease-in',
        title_font_size = 24,
        label_font_size = 36,
        major_label_font_size = 24,
        plot_background = '#343a40',
        foreground_subtle='#630C0D',
        colors=('#9e6ffe','#9e6ffe','#9e6ffe','#9e6ffe'),
        background='transparent',
        opacity='.8',
        foreground_strong='#53A0E8',
        foreground='#ffffff',
        value_font_size=25, 
        value_colors=('white',),
    )    
    #item_llg = detail_itemlelang.objects.all().get(id=pk)
    #judul = item_lelang.objects.all().get(id = item_llg.item_lelang.id)
    rsmra = models.round_smra2.objects.all().filter(item_lelang=pk).order_by("-round")[0]
    maxround=rsmra.round
    m = models.auctioner_hasil.objects.all().filter(item_lelang__id=pk).order_by('round')
    if m:
        df = read_frame(m)
        max = df['peserta'].max()
        dt = list()
        dl = list()
        
        for i in range (0, maxround) :
            dt.append(0)
            dl.append(i+1)
        i=0

        for a in m :
            dt[i] = a.peserta
            i = i +1

        
       
        bar_chart = pygal.Bar(height=350, fill=True, show_minor_y_labels=False, show_y_labels=False, print_values=True, legend_at_bottom=True, print_values_position='top', style=custom_style)
        #bar_chart.title = 'Grafik 2 Kenaikan Total Penawaran\n' + judul.nama_lelang + ' band ' + item_llg.band + "\n(dalam jutaan Rupiah)"
        bar_chart.zero = 0
        bar_chart.x_labels = dl
        bar_chart.add('bidder', dt)
        bar_chart.range=(0, max)
        #bar_chart.value_formatter = lambda y: locale.currency(y, grouping=True)
        #bar_chart.value_formatter = lambda y: y
        context = {}
        return bar_chart.render_django_response(is_unicode=True)
    else:
        bar_chart = pygal.StackedLine(height=300, fill=True,  style=RedBlueStyle)
        #bar_chart.title = 'Grafik Kenaikan Total Penawaran \n' + judul.nama_lelang 
        context = {}
        return bar_chart.render_django_response(is_unicode=True)

def hasil_block(request, pk):
    from pygal.style import Style
    #locale.setlocale( locale.LC_ALL, 'id_ID.UTF-8' )
    custom_style = Style(
       transition='400ms ease-in',
        title_font_size = 24,
        label_font_size = 36,
        major_label_font_size = 24,
        plot_background = '#343a40',
        foreground_subtle='#630C0D',
        colors=('#99EDc3','#99EDc3','#fbec5d','#9e6ffe'),
        background='transparent',
        opacity='.8',
        foreground_strong='#53A0E8',
        foreground='#ffffff',
        value_font_size=25, 
        value_colors=('white',),
        
    )    
    #item_llg = detail_itemlelang.objects.all().get(id=pk)
    #judul = item_lelang.objects.all().get(id = item_llg.item_lelang.id)
    rsmra = models.round_smra2.objects.all().filter(item_lelang=pk).order_by("-round")[0]
    maxround=rsmra.round
    m = models.auctioner_hasil.objects.all().filter(item_lelang__id=pk).order_by('round')
    if m:
        df = read_frame(m)
        max = df['block'].max()
        dt = list()
        dl = list()
        
        for i in range (0, maxround) :
            dt.append(0)
            dl.append(i+1)
        i=0

        for a in m :
            dt[i] = a.block
            i = i +1

       
        bar_chart = pygal.StackedLine(height=350, fill=True, legend_at_bottom=True, print_values=True, print_values_position='top' ,  show_y_labels=False,  style=custom_style)
        #bar_chart.title = 'Grafik 2 Kenaikan Total Penawaran\n' + judul.nama_lelang + ' band ' + item_llg.band + "\n(dalam jutaan Rupiah)"
        bar_chart.zero = 0
        bar_chart.x_labels = dl
        bar_chart.add('permintaan', dt)
        bar_chart.range=(0, max)
        #bar_chart.value_formatter = lambda y: locale.currency(y, grouping=True)
        #bar_chart.value_formatter = lambda y: y
        context = {}
        return bar_chart.render_django_response(is_unicode=True)
    else:
        bar_chart = pygal.StackedLine(height=300, fill=True,  style=RedBlueStyle)
        #bar_chart.title = 'Grafik Kenaikan Total Penawaran \n' + judul.nama_lelang 
        context = {}
        return bar_chart.render_django_response(is_unicode=True)

class hasil_smra2ListView(SingleTableMixin, generic.ListView):
    model = models.hasil_smra2
    table_class = tables.hasil_smra2Table
    template_name = 'table_detail_itemlelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        item_llg = item_lelang.objects.all().filter(id=self.kwargs['pk'])[0]
        bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)[0]
        return models.hasil_smra2.objects.all().filter(item_lelang=item_llg.id,bidder=bdr, valid=True).order_by('-round')


class hasil2_smra2ListView(MultiTableMixin, TemplateView):
    model = models.hasil2_smra
    table_class = tables.hasil2_smra2Table
    template_name = 'table_hasil_valid.html'
    def get_tables(self):
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        
        
        #item_llg = models.hasil2_smra.objects.all().filter(item_lelang=self.kwargs['pk'])
        tbls = []
        
        
        for i in item_llg:
            if self.request.user.user_type=="B":
                bdr = bidder_user.objects.filter(users__id = self.request.user.id)[0]
                # bdr = bidder_user.objects.filter(users__id = self.request.user.id).first()
                filtered_data = models.hasil2_smra.objects.filter(item=i, bidder=bdr, valid=True).order_by('round','ranking_putaran')
                cek_data = []
                for d in filtered_data:
                    cek_data.append({
                        'round': d.round,
                        'price': d.price,
                        'penawaran': d.penawaran,
                        'valid': d.valid
                    })
                tbls.append(tables.hasil2_smra2Table2(filtered_data))
            else:
                filtered_data = models.hasil2_smra.objects.all().filter(item=i,valid=True).order_by('round','ranking_putaran')
                tbls.append(tables.hasil2_smra2_auctioneerTable2(filtered_data))
        
        return tbls

    def get_context_data(self, **kwargs):
        context = super(hasil2_smra2ListView, self).get_context_data(**kwargs)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        tabs = []
        for i in item_llg:
            tabs.append(i)
        context['tabs'] = tabs
        return context


class hasil3_smra2ListView(MultiTableMixin, TemplateView):
    model = models.hasil2_smra
    table_class = tables.hasil2_smra2Table
    template_name = 'price_increase2_table.html'
    def get_tables(self):
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        tbls = []
        for i in item_llg:
            if self.request.user.user_type=="B":
                bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)[0]
                permintaan = models.hasil_smra2.objects.all().filter(item=i, bidder=bdr, valid=False).order_by("-round").first()
                if permintaan:
                    batas = permintaan.block
                else:
                    batas = 1
                tbls.append(tables.hasil2_smra2Table(models.hasil2_smra.objects.all().filter(item=i,bidder=bdr, valid=False).order_by('ranking')[:batas]))
            else:
                sum_penawaran = models.detail_itemlelang.objects.all().get(id=i.id)
                max_block = sum_penawaran.max_block
                tbls.append(tables.hasil2_smra2Table2(models.hasil2_smra.objects.all().filter(item=i,valid=False).order_by('ranking')[:max_block]))
        return tbls

    def get_context_data(self, **kwargs):
        context = super(hasil3_smra2ListView, self).get_context_data(**kwargs)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        tabs = []
        for i in item_llg:
            tabs.append(i)
        context['tabs'] = tabs
        return context

class hasil4_smra2ListView(MultiTableMixin, TemplateView):
    model = models.hasil2_smra
    table_class = tables.hasil5_smra2Table
    template_name = 'price_increase2_table.html'
    def get_tables(self):
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        tbls = []
        for i in item_llg:
            """
            if self.request.user.user_type=="B":
                bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)[0]
                if permintaan:
                    batas = max_block
                else:
                    batas = 1
                tbls.append(tables.hasil2_smra2Table(models.hasil2_smra.objects.all().filter(item=i,bidder=bdr, valid=True,ranking__isnull=False, berlaku=True).order_by('ranking')[:batas]))
            else:
            """
            sum_penawaran = models.detail_itemlelang.objects.all().get(id=i.id)
            max_block = sum_penawaran.max_block
            tbls.append(tables.hasil5_smra2Table(models.hasil2_smra.objects.all().filter(item=i,valid=True,ranking__gt=0, berlaku=True).order_by('ranking')[:max_block]))
        return tbls

    def get_context_data(self, **kwargs):
        context = super(hasil4_smra2ListView, self).get_context_data(**kwargs)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'],disabled=False).order_by('id')
        tabs = []
        for i in item_llg:
            tabs.append(i)
        context['tabs'] = tabs
        return context

class hasil5_smra2ListView(MultiTableMixin, TemplateView):
    model = models.hasil_smra2
    table_class = tables.hasilvalid_smra2Table
    template_name = 'price_increase2_table.html'
    def get_tables(self):
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        tbls = []
        for i in item_llg:
            if self.request.user.user_type=="B":
                bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)[0]
                permintaan = models.hasil_smra2.objects.all().filter(item=i, bidder=bdr, valid=True).order_by("-round").first()
                if permintaan:
                    batas = permintaan.block
                else:
                    batas = 1
                tbls.append(tables.hasilvalid_smra2Table(models.hasil_smra2.objects.all().filter(item=i,bidder=bdr, valid=True).order_by("-round")))
            else:
                sum_penawaran = models.detail_itemlelang.objects.all().get(id=i.id)
                max_block = sum_penawaran.max_block
                tbls.append(tables.hasilvalid_smra2Table(models.hasil_smra2.objects.all().filter(item=i,valid=True)))
        return tbls

    def get_context_data(self, **kwargs):
        context = super(hasil5_smra2ListView, self).get_context_data(**kwargs)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        tabs = []
        for i in item_llg:
            tabs.append(i)
        context['tabs'] = tabs
        return context

class hasil_smra2_auctionerListView(SingleTableMixin, generic.ListView):
    model = models.hasil_smra2
    table_class = tables.hasil_smra2_auctionerTable
    template_name = 'table_detail_itemlelang.html'
    table_pagination = False

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        item_llg = item_lelang.objects.all().filter(id=self.kwargs['pk'], disabled=False)[0]
        m = models.hasil_smra2.objects.all().filter(item_lelang=item_llg.id,valid=True).order_by('-round','-price')
        df = read_frame(m)
        df2=df.loc[df.index.repeat(df['block'])].reset_index()
        b = df2.to_dict('records')
        return b

class hasil_akhir_auctionerListView(MultiTableMixin, TemplateView):
    model = models.hasil_smra2
    template_name = 'price_increase_table.html'

    def get_tables(self):
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk']).order_by('id')
        tbls = []
        for i in item_llg:
            sum_penawaran = models.detail_itemlelang.objects.all().get(id=i.id)
            max_block = sum_penawaran.max_block
            m = models.hasil_smra2.objects.all().filter(item__id=i.id,valid=True).order_by('-round','-price','submit')
            df = read_frame(m)
            df2=df.loc[df.index.repeat(df['block'])].reset_index()
            df2['row_number'] = df2.reset_index().index
            b = df2.head(max_block).to_dict('records')

            tbls.append(tables.hasil_smra2_auctionerTable(b))

        return tbls

    def get_context_data(self, **kwargs):
        context = super(hasil_akhir_auctionerListView, self).get_context_data(**kwargs)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        tabs = []
        for i in item_llg:
            tabs.append(i)
        context['tabs'] = tabs
        return context

class auctioner_hasilListView(MultiTableMixin, TemplateView):
    model = models.auctioner_hasil
    table_class = tables.auctioner_hasilTable
    template_name = 'price_increase_table.html'

    def get_tables(self):
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk']).order_by('id')
        tbls = []
        for i in item_llg:
            m = models.hasil_smra2.objects.all().filter(item__id=i.id,valid=True).order_by('-round','-price','submit')
            df = read_frame(m)
            df2=df.loc[df.index.repeat(df['block'])].reset_index()
            df2['row_number'] = df2.reset_index().index
            b = df2.to_dict('records')
            tbls.append(tables.hasil_smra2_auctionerTable(b))

        return tbls

    def get_context_data(self, **kwargs):
        context = super(auctioner_hasilListView, self).get_context_data(**kwargs)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=True).order_by('id')
        tabs = []
        for i in item_llg:
            tabs.append(i)
        context['tabs'] = tabs
        return context

class auctioner_hasil_maxminListView(SingleTableMixin, generic.ListView):
    model = models.hasil_auctioner_maxmin
    table_class = tables.auctioner_hasil_maxminTable
    template_name = 'table_detail_itemlelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        m = models.hasil_auctioner_maxmin.objects.all().filter(item=self.kwargs['pk']).order_by('round')
        df = read_frame(m)
        b = df.to_dict('records')
        return b

class auctioner_highestListView(SingleTableMixin, generic.ListView):
    model = models.hasil_highest
    table_class = tables.auctioner_highestTable
    template_name = 'table_detail_itemlelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        item_llg = item_lelang.objects.all().filter(id=self.kwargs['pk'])[0]
        return models.hasil_highest.objects.all().filter(item_lelang=item_llg.id).order_by('item','-price')


class price_increaseListView(MultiTableMixin, TemplateView):
    template_name = 'price_increase2_table.html'

    def get_tables(self):
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        tbls = []
        for i in item_llg:
            tbls.append(tables.price_increaseTable(models.price_increase.objects.all().filter(detail_item=i)))

        return tbls

    def get_context_data(self, **kwargs):
        context = super(price_increaseListView, self).get_context_data(**kwargs)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        tabs = []
        for i in item_llg:
            tabs.append(i)
        context['tabs'] = tabs
        return context


class round_smraPivotView(SingleTableMixin, generic.ListView):
    model = models.hasil_smra2
    table_class = tables.hasil_smra2PivotTable
    template_name = 'table_detail_itemlelang.html'

    def get_table(self, **kwargs):
        pivot_table = pivot(models.hasil_smra2, ["bidder","item_id","block"],"round", "price")
        cols = [(k, django_tables2.Column()) for k,v in pivot_table[0].items()]
        return tables.hasil_smra2PivotTable(data=pivot_table, extra_columns=cols)
    
class obyek_seleksiGroupView(MultiTableMixin, generic.ListView):
    model = models.obyek_seleksi_smra
    template_name = 'obyek_seleksi_group.html'
    #table_class = tables.obyek_seleksi_groupTable
    def get_tables(self):
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
        tbls = []
        for i in item_llg:
            tbls.append(tables.obyek_seleksiTable(models.obyek_seleksi_smra.objects.all().filter(item=i)))

        return tbls

    def get_context_data(self, **kwargs):
        context = super(obyek_seleksiGroupView, self).get_context_data(**kwargs)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'],disabled=False).order_by('id')
        tabs = []
        for i in item_llg:
            tabs.append(i)
        context['tabs'] = tabs
        return context

class obyek_seleksiView(SingleTableMixin, generic.ListView):
    model = models.obyek_seleksi_smra
#    table_class = tables.obyek_seleksiTable
    template_name = 'table_detail_itemlelang.html'
    table_pagination = False

    def get_table_class(self):
        if self.request.user.user_type =='B':
            return tables.obyek_seleksi2Table
        else:
            return tables.obyek_seleksiTable

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type == "B":
            bdr_user = bidder_user.objects.all().get(users__id = self.request.user.id)
            obj =  models.obyek_seleksi_smra.objects.all().filter(bidder_user = bdr_user, item__item_lelang=self.kwargs['pk'])
        else:
            item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'], disabled=False).order_by('id')
            tbls = []
            for i in item_llg:
                tbls.append(i)
            obj = models.obyek_seleksi_smra.objects.all().filter(item__in=tbls)
        return obj
 
class bidSMRA2CreateView(BSModalUpdateView):
    template_name = 'modal_bid_smra2.html'
    form_class = forms.bidSMRA2
    model = models.round_smra2
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item": self.kwargs["pk"], "bidder":self.kwargs["bidder"]}

    def get_object(self, queryset=None):
        obj = self.model.objects.get(item=self.kwargs["pk"], bidder=self.kwargs["bidder"])
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
    model = models.price_increase
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')

    def get_initial(self):
        return {"id": self.kwargs["pk"]}

class obyek_seleksiCreateView(BSModalCreateView):
    template_name = 'modal_obyek_seleksi_smra.html'
    form_class = forms.obyek_seleksiForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')

    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class obyek_seleksiUpdateView(BSModalUpdateView):
    template_name = 'modal_obyek_seleksi_smra_update.html'
    form_class = forms.obyek_seleksiForm
    model = models.obyek_seleksi_smra
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')

    def get_initial(self):
        return {"id": self.kwargs["pk"]}

class detail_itemlelangListView(SingleTableMixin, generic.ListView):
    model = models.detail_itemlelang
    #form_class = forms.detail_itemlelangForm
    table_class = tables.item_lelang_detailTable
    template_name = 'table_detail_itemlelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.detail_itemlelang.objects.all().filter(item_lelang=self.kwargs['pk'], disabled=False).order_by('urutan')
        
class detail_itemlelangCreateView(BSModalCreateView):
    template_name = 'modal_obyeklelang2.html'
    form_class = forms.obyekSeleksi2Form
    #model = models.price_increase
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')

    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class detail_itemlelangUpdateView(BSModalUpdateView):
    template_name = 'modal_obyeklelang2.html'
    form_class = forms.obyekSeleksi2Form
    model = detail_itemlelang
    success_message = 'Success: Book was created.'
    success_url = "/"

    def get_initial(self):
        return {"id": self.kwargs["pk"]}

from background_task.models import Task as BTask
import json
from adm_lelang.models import detail_itemlelang
class scheduler_smra2ListView(SingleTableMixin, generic.ListView):
    model = BTask
    table_class = tables.scheduler_smra2Table
    template_name = 'table_detail_itemlelang.html'
    table_pagination = False

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        harike = {'1':'Senin','2':'Selasa','3':'Rabu','4':'Kamis','5':'Jumat','6':'Sabtu','0':'Minggu'}
        b_task = BTask.objects.filter(creator_object_id = self.kwargs['pk'] )
        b = []
        for bt in b_task:
            #param = json.loads(bt.task_params)[1]
            vb = bt.verbose_name
            ra = bt.run_at
            id_detail = bt.creator_object_id
            di = item_lelang.objects.get(pk=id_detail)
            hari = ra.strftime("%A")
            b.append({'verbose_name':vb, 'hari': hari,'run_at': ra, 'seleksi': di.nama_lelang + "/" + di.tahun})
        return b

class round_scheduleListView(SingleTableMixin, generic.ListView):
    model = models.round_schedule_smra2
    table_class = tables.round_scheduleTable
    template_name = 'table_detail_itemlelang.html'
    table_pagination = False

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
#        dt = timezone.now()
        dt = timezone.localtime()
        hari = str(timezone.localtime().today().isoweekday())
        return models.round_schedule_smra2.objects.all().filter(item=self.kwargs['pk']).order_by('hari')
        #.filter(mulai__gte=dt).order_by('mulai')

class round_schedule2ListView(SingleTableMixin, generic.ListView):
    model = models.round_schedule_smra2
    table_class = tables.round_scheduleTable2
    template_name = 'table_detail_itemlelang.html'
    table_pagination = False
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        dt = timezone.localtime()
        hari = str(timezone.localtime().today().isoweekday())
        return models.round_schedule_smra2.objects.all().filter(item=self.kwargs['pk']).order_by('hari')
#        dt = timezone.now()
#        return models.round_schedule_smra2.objects.all().filter(item=self.kwargs['pk'], hari=hari, mulai__gte = datetime.strptime(dt.strftime("%H:%M"),"%H:%M")).order_by('hari')

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
    model = models.round_schedule_smra2
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"id": self.kwargs["pk"]}