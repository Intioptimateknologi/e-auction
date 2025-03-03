from collections import defaultdict
from django.views import generic
from django.urls import reverse_lazy
import pytz
from . import models
from . import forms
from . import tables
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from rencana_seleksi.models import jadwal_seleksinya, rencana_seleksinya
from rencana_seleksi.forms import RencanaSeleksiForm
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django.conf import settings
from django.core.mail import send_mail
from adm_lelang import utils
from django_renderpdf.views import PDFView
from docxtpl import DocxTemplate
from django.template.loader import render_to_string
from django.http import HttpResponse,HttpResponseNotFound, JsonResponse, Http404
from userman.models import bidder_user, bidder_perwakilan, Notifikasi, tim_lelang
from smra2.models import obyek_seleksi_smra
from adm_lelang import models as adm_lelangmodels
from persiapan.models import pengambilan_dokumen_seleksi, dokumen_seleksi,p_pertanyaan,daftar_hadir,simulasi,p_addendum,pengambilan_dokumen_addendum,aanwizing
from administrasi.models import permohonan_keikutsertaan,form_pemeriksaan,form_verifikasi,form_evaluasi,form_sanggahan,jawaban_sanggahan, hasil_kesimpulan
from smra2 import models as smra2models
from rencana_seleksi import models as rencanaseleksimodels
from pasca_seleksi import models as pascaseleksimodels
from portal import models as portalmodels
from datetime import datetime, timedelta,date
from persiapan.models import p_dokumen
from userman.models import Notifikasi
from django.db.models import Avg, Max, Min
import mimetypes

from django.utils import timezone


@login_required
def home(request):
    item_lelang = models.item_lelang.objects.all().filter(tayang=True)
    url = "/persiapan/pembukaan/"

    if request.user.is_authenticated:
        if  request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            context["item"] = item_lelang
            return render(request, 'index_adm_lelang.html',context)
        elif request.user.user_type == 'B':
            return render(request, 'index_adm_lelang_bidder.html',context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            context["item"] = item_lelang
            return render(request, 'index_adm_lelang.html', context)
    else:
        return render(request, 'index.html')

    # return render(request, 'index_adm_lelang.html', {"item": item_lelang})
    
@login_required
def create_jadwal_seleksi(request,pk,tgl_awal):
    item_llg = models.item_lelang.objects.all().filter(id=pk)[0]
    #hapus dulu jadwal yang ada
    jadwal_lama = models.jadwal_seleksi.objects.all().filter(item_lelang = item_llg)
    jadwal_lama.delete()

    jadwal = models.template_jadwal_seleksi.objects.all()
    user = request.user
    t_awal = datetime.strptime(tgl_awal, "%Y-%m-%d").date()
    for j in jadwal:
        selisih = j.tanggal_akhir - j.tanggal_awal
        newjadwaL = models.jadwal_seleksi(tahap=j.tahap, tanggal_awal = t_awal, tanggal_akhir=j.tanggal_awal + timedelta(selisih.days), item_lelang = item_llg, dibuat_oleh = user )
        newjadwaL.save()
    return JsonResponse({"response":"Ok"})

def info_seleksi(request, pk):
    if request.user.is_authenticated:
        id = pk
        item_llg = models.item_lelang.objects.all().filter(id=pk)[0]
        detail = models.detail_itemlelang.objects.all().filter(item_lelang = item_llg).order_by('urutan')
        jadwal = models.jadwal_seleksi.objects.all().filter(item_lelang = item_llg)
        dasar = models.dasar_hukum.objects.all().filter(item_lelang = item_llg)
        pengumuman = models.pengumuman.objects.all().filter(item_lelang = item_llg)
        tim_lelang = models.penangung_jawab_seleksi.objects.all().filter(item_lelang = item_llg)
        panitia = models.alamat_panitia.objects.all().filter(item_lelang = item_llg)
        pengumuman = models.pengumuman.objects.all().filter(item_lelang = item_llg)
        persyaratan_lelang = models.persyaratan_lelang.objects.all().filter(item_lelang = item_llg)
        context = {"item":item_llg, "detail":detail, "jadwal": jadwal, "dasar": dasar,'tim':tim_lelang,
            'pengumuman': pengumuman, 'panitia': panitia, 'persyaratan': persyaratan_lelang, 'pengumuman':pengumuman}
        return render(request, 'info_adm_lelang.html', context)
    else:
        return render(request, 'index.html')

def judul_lelang(request, pk):
    if request.user.is_authenticated:
        id = pk
        item_llg = models.item_lelang.objects.all().filter(id=pk)[0]

    return render(request, 'judul_lelang.html', context)

def rekap_manajemen(request):
    url = "/adm_lelang/rekapitulasi/"
    if request.user.is_authenticated:
        if request.user.is_superuser:
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            semua_undangan = models.undangan.objects.all()
            context['semua_undangan'] = semua_undangan
             
            semua_pengumuman = models.pengumuman.objects.all()
            context['semua_pengumuman'] = semua_pengumuman
             
            semua_berita_acara = models.berita_acara.objects.all()
            context['semua_berita'] = semua_berita_acara
            
            semua_notifikasi = Notifikasi.objects.all()
            context['semua_notifikasi'] = semua_notifikasi
            
            return render(request, 'index_rekapitulasi.html', context)
        elif request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            semua_undangan = models.undangan.objects.all()
            context['semua_undangan'] = semua_undangan
             
            semua_pengumuman = models.pengumuman.objects.all()
            context['semua_pengumuman'] = semua_pengumuman
             
            semua_berita_acara = models.berita_acara.objects.all()
            context['semua_berita'] = semua_berita_acara
            
            semua_notifikasi = Notifikasi.objects.all()
            context['semua_notifikasi'] = semua_notifikasi
            
            return render(request, 'index_rekapitulasi.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            semua_undangan = models.undangan.objects.all()
            context['semua_undangan'] = semua_undangan
            
            semua_pengumuman = models.pengumuman.objects.all()
            context['semua_pengumuman'] = semua_pengumuman
            
            semua_berita_acara = models.berita_acara.objects.all()
            context['semua_berita'] = semua_berita_acara
            return render(request, 'index_rekapitulasi.html', context)
        elif request.user.user_type == 'C':
             #context = {}
             #user = request.user
             #auc = tim_lelang.objects.all().filter(users_id = request.user.id)
             #if (auc):
             #    context['auctioner'] = auc[0]
             #   if request.GET.get("id"):
              #       context["item_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) #bidder_lelang.objects.all().filter(bidder = bidder_id)
              #   else:
             #        context["item_lelang"] = item_lelang.objects.all()[0] #bidder_lelang.objects.all().filter(bidder = bidder_id)
             #    context['user_type'] = request.user.user_type
             context = utils.get_judul_context_auctioneer(request)
             tabs = utils.get_tab_context(request,url, context["item_lelang"])
             context.update(tabs)
             semua_undangan = models.undangan.objects.all()
             context['semua_undangan'] = semua_undangan
             
             semua_pengumuman = models.pengumuman.objects.all()
             context['semua_pengumuman'] = semua_pengumuman
             
             semua_berita_acara = models.berita_acara.objects.all()
             context['semua_berita'] = semua_berita_acara
             return render(request, 'index_rekapitulasi.html', context)    
        else:            
            return render(request, 'index_rekapitulasi.html')
    else:
        return render(request, 'index_rekapitulasi.html')

class itemLelangCreateView(BSModalCreateView):
    template_name = 'modal_itemlelang.html'
    form_class = forms.itemLelangForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')

class itemlelangUpdateView(BSModalUpdateView):
    template_name = 'modal_itemlelang.html'
    form_class = forms.itemLelangForm
    model = models.item_lelang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"id": self.kwargs["pk"]}


class pengumumanCreateView(BSModalCreateView):
    template_name = 'modal_pengumuman.html'
    form_class = forms.pengumumanForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {
        "item_lelang": self.kwargs["pk"],
        'tahapan': self.kwargs['tahapan']
        }
class pengumumanUpdateView(BSModalUpdateView):
    template_name = 'modal_pengumuman.html'
    form_class = forms.pengumumanForm
    success_message = 'Success: Book was created.'
    model = models.pengumuman
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {
        "id": self.kwargs["pk"],
        }

class dasarHukumUpdateView(BSModalUpdateView):
    template_name = 'modal_dasar_hukum.html'
    form_class = forms.dasarHukumForm
    model = models.dasar_hukum
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
       #print({"id": self.kwargs["id"], "item": self.kwargs["pk"]})
       return {"id": self.kwargs["pk"], "item": self.kwargs["id"]}

class dasarHukumCreateView(BSModalCreateView):
    template_name = 'modal_dasar_hukum.html'
    form_class = forms.dasarHukumForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

# objek seleksi
class objekSeleksiCreateView(BSModalCreateView):
    template_name = 'modal_obyek_seleksi.html'
    form_class = forms.detail_itemlelangForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class objekSeleksiUpdateView(BSModalUpdateView):
    template_name = 'modal_obyek_seleksi.html'
    form_class = forms.detail_itemlelangForm
    model = models.detail_itemlelang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
# 
class alamatPanitiaCreateView(BSModalCreateView):
    template_name = 'modal_alamat_panitia.html'
    form_class = forms.alamatPanitiaForm
    success_message = 'Success: Data was created.'
    #success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class alamatPanitiaUpdateView(BSModalUpdateView):
    template_name = 'modal_alamat_panitia.html'
    form_class = forms.alamatPanitiaForm
    model = models.alamat_panitia
    success_message = 'Success: Data was created.'
    #success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
    
# pengumuman seleksi
class pengumumanLelangCreateView(BSModalCreateView):
    template_name = 'modal_pengumuman_seleksi.html'
    form_class = forms.pengumumanForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class pengumumanLelangUpdateView(BSModalUpdateView):
    template_name = 'modal_pengumuman_seleksi.html'
    form_class = forms.pengumumanForm
    model = models.pengumuman
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial

# persyaratan seleksi
class persyaratanSeleksiCreateView(BSModalCreateView):
    template_name = 'modal_persyaratan_seleksi.html'
    form_class = forms.persyaratanLelangForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class persyaratanSeleksiUpdateView(BSModalUpdateView):
    template_name = 'modal_persyaratan_seleksi.html'
    form_class = forms.persyaratanLelangForm
    model = models.persyaratan_lelang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
# 

# jadwal seleksi
class jadwalSeleksiCreateView(BSModalCreateView):
    template_name = 'modal_jadwal_seleksi.html'
    form_class = forms.jadwal_seleksiForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class jadwalSeleksiUpdateView(BSModalUpdateView):
    template_name = 'modal_jadwal_seleksi.html'
    form_class = forms.jadwal_seleksiForm
    model = models.jadwal_seleksi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
# 

# PenanggungJawab
class PenanggungJawabCreateView(BSModalCreateView):
    template_name = 'modal_panitia_seleksi.html'
    form_class = forms.penanggung_jawabForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class PenanggungJawabUpdateView(BSModalUpdateView):
    template_name = 'modal_panitia_seleksi.html'
    form_class = forms.penanggung_jawabForm
    model = models.penangung_jawab_seleksi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
#

def modal_itemlelang(request):
    return render(request, 'modal_itemlelang.html')


class itemlelangListView(SingleTableMixin, generic.ListView):
    model = models.item_lelang
    #form_class = forms.detail_itemlelangForm
    table_class = tables.item_lelangTable
    template_name = 'table_detail_itemlelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.item_lelang.objects.all().filter(id=self.kwargs['pk'])


class detail_itemlelang2ListView(SingleTableMixin, generic.ListView):
    model = models.detail_itemlelang
    #form_class = forms.detail_itemlelangForm
    table_class = tables.item_lelang_detail2Table
    template_name = 'table_detail_itemlelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.detail_itemlelang.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('urutan')

class detail_itemlelangListView(SingleTableMixin, generic.ListView):
    model = models.detail_itemlelang
    table_class = tables.item_lelang_detailTable
    template_name = 'table_detail_itemlelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.detail_itemlelang.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('urutan')

class nilai_detail_itemlelangListView(SingleTableMixin, generic.ListView):
    model = models.detail_itemlelang
    table_class = tables.nilai_item_lelang_detailTable
    template_name = 'table_detail_itemlelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.detail_itemlelang.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('urutan')
    
class pengumuman_lelangListView(SingleTableMixin, generic.ListView):
    model = models.pengumuman
    table_class = tables.pengumuman_Table
    template_name = 'table_pengumuman_lelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        itm_lelang = self.kwargs['item_lelang']
        tahapan = self.kwargs['current_step']
        auctioner = self.kwargs['auctioner']
        return models.pengumuman.objects.all().filter(item_lelang=itm_lelang, tahapan=tahapan).order_by('-last_updated')
    
class pengumuman_lelang2ListView(SingleTableMixin, generic.ListView):
    model = models.pengumuman
    table_class = tables.pengumuman2_Table
    template_name = 'table_pengumuman_lelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        itm_lelang = self.kwargs['item_lelang']
        tahapan = self.kwargs['current_step']
        dt = timezone.localtime()
        return models.pengumuman.objects.all().filter(item_lelang=itm_lelang, tahapan=tahapan, tgl_release__lt=dt).order_by('-last_updated')
    
class pengumuman_lelang3ListView(SingleTableMixin, generic.ListView):
    model = models.pengumuman
    table_class = tables.pengumuman3_Table
    template_name = 'table_pengumuman_lelang.html'
    current_date = datetime.now().date()

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        itm_lelang = self.kwargs['item_lelang']
        tahapan = self.kwargs['current_step']
        dt = timezone.localtime()
        return models.pengumuman.objects.all().filter(item_lelang=itm_lelang, tahapan=tahapan, tgl_release__lt=dt).order_by('-last_updated')

class dasar_hukumListView(SingleTableMixin, generic.ListView):
    model = models.dasar_hukum
    table_class = tables.dasar_hukum_Table
    template_name = 'table_dasarhukum.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.dasar_hukum.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-created')



    
class dasar_hukumListView2(SingleTableMixin, generic.ListView):
    model = models.dasar_hukum
    table_class = tables.dasar_hukum_Table2
    template_name = 'table_dasarhukum.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.dasar_hukum.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-created')
    
class alamat_panitiaListView(SingleTableMixin, generic.ListView):
    model = models.alamat_panitia
    table_class = tables.alamat_panitia_Table
    template_name = 'table_alamat_panitia.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.alamat_panitia.objects.all().filter(item_lelang=self.kwargs['pk'])

class persyaratan_lelangListView(SingleTableMixin, generic.ListView):
    model = models.persyaratan_lelang
    table_class = tables.persyaratan_lelang_Table
    template_name = 'table_persyaratan.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.persyaratan_lelang.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('no_urut')
    
class jadwal_seleksiListView(SingleTableMixin, generic.ListView):
    model = models.jadwal_seleksi
    table_class = tables.jadwal_seleksi_Table
    table_pagination = False
    template_name = 'table_jadwal_lelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.jadwal_seleksi.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('tahap__tree_id','tahap__lft')

class jadwal_seleksi2ListView(SingleTableMixin, generic.ListView):
    model = models.jadwal_seleksi
    table_class = tables.jadwal_seleksi2_Table
    template_name = 'table_jadwal_lelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.jadwal_seleksi.objects.all().filter(item_lelang=self.kwargs['pk'])

# TEMPLATE BERITA ACARA
class template_berita_acaraListView(SingleTableMixin, generic.ListView):
    model = models.template_berita_acara
    table_class = tables.template_berita_acara_Table
    template_name = 'table_jadwal_lelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.template_berita_acara.objects.all().order_by('-created')

class template_berita_acaraCreateView(BSModalCreateView):
    template_name = 'modal_template_ba.html'
    form_class = forms.template_berita_acaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
   

class template_berita_acaraUpdateView(BSModalUpdateView):
    template_name = 'modal_template_ba.html'
    form_class = forms.template_berita_acaraForm
    model = models.template_berita_acara
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial

class bidderLelangCreateView(BSModalCreateView):
    template_name = 'modal_bidderlelang.html'
    form_class = forms.bidderLelangForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class bidderLelangUpdateView(BSModalUpdateView):
    template_name = 'modal_bidderlelang.html'
    form_class = forms.bidderLelangForm
    model = models.bidder_lelang
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('index')
    
    def get_initial(self):
        return {
            "item_lelang": self.kwargs["lelang"],
            "id": self.kwargs["pk"]
        }

class auctionerLelangCreateView(BSModalCreateView):
    template_name = 'modal_auctionerlelang.html'
    form_class = forms.auctionerLelangForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class auctionerLelangUpdateView(BSModalUpdateView):
    template_name = 'modal_auctionerlelang.html'
    form_class = forms.auctionerLelangForm
    model = models.auctioner_lelang
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["lelang"], "id": self.kwargs["pk"]}

class viewerLelangCreateView(BSModalCreateView):
    template_name = 'modal_viewerlelang.html'
    form_class = forms.viewerLelangForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class viewerLelangUpdateView(BSModalUpdateView):
    template_name = 'modal_viewerlelang.html'
    form_class = forms.viewerLelangForm
    model = models.viewers_lelang
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["lelang"], "id": self.kwargs["pk"]}

#=========Auctioner
class auctioner_lelangListView(SingleTableMixin, generic.ListView):
    model = models.auctioner_lelang
    table_class = tables.auctioner_lelangTable
    template_name = 'table_auctioner_lelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.auctioner_lelang.objects.all().filter(item_lelang=self.kwargs['pk'])

#=========Viewer
class viewer_lelangListView(SingleTableMixin, generic.ListView):
    model = models.viewers_lelang
    table_class = tables.viewer_lelangTable
    template_name = 'table_viewer_lelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.viewers_lelang.objects.all().filter(item_lelang=self.kwargs['pk'])

#====
class bidder_lelangListView(SingleTableMixin, generic.ListView):
    model = models.bidder_lelang
    table_class = tables.bidder_lelangTable
    template_name = 'table_bidder_lelang.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.bidder_lelang.objects.all().filter(item_lelang=self.kwargs['pk'])
    
# penanggung jawab
class penanggung_jawabListView(SingleTableMixin, generic.ListView):
    model = models.penangung_jawab_seleksi 
    table_class = tables.penanggung_jawab_Table
    template_name = 'tabel_undangan_kelengkapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.penangung_jawab_seleksi.objects.all().filter(item_lelang=self.kwargs['pk']).order_by('-id')


class undangan_CreateView(BSModalCreateView):
    template_name = 'modal_undangan.html'
    form_class = forms.UndanganForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'item_lelang': self.kwargs['item_lelang'],
            'tahapan': self.kwargs['tahapan']
        })

        return initial   

class undangan_UpdateView(BSModalUpdateView):
    template_name = 'modal_undangan.html'
    form_class = forms.UndanganForm
    model = models.undangan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk']
        })

        return initial

class undanganBidderListView(SingleTableMixin, generic.ListView):
    model = models.undangan 
    table_class = tables.undangan_bidderTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.undangan.objects.all().filter(item_lelang=self.kwargs['item_lelang'], bidder__id=self.kwargs['bidder'], tahapan=self.kwargs['current_step']).order_by('-id')

class undanganBidder2ListView(SingleTableMixin, generic.ListView):
    model = models.undangan 
    table_class = tables.undangan_bidderTable
    template_name = 'tabel_persiapan.html'
    # def get_queryset(self, **kwargs):
    #     qs = super().get_queryset(**kwargs)
    #     return models.undangan.objects.all().filter(item_lelang=self.kwargs['item_lelang'], tahapan=self.kwargs['current_step']).order_by('-id')
    def get_queryset(self, **kwargs):
        if self.request.user.user_type =='B':
            bdr_user = bidder_user.objects.get(users = self.request.user)
            return models.undangan.objects.all().filter(item_lelang=self.kwargs['item_lelang'], bidder_user = bdr_user, tahapan=self.kwargs['current_step']).order_by('-id')
        elif self.request.user.user_type=='C':
            return models.undangan.objects.all().filter(item_lelang=self.kwargs['item_lelang'], auctioneer__users__id = self.request.user.id, tahapan=self.kwargs['current_step'])
            #if ba:
            #    auc = ba[0].auctioneer.all().filter(users= self.request.user)
            #    if auc:
            #        return models.undangan.objects.all().filter(item_lelang=self.kwargs['item_lelang'], auctioneer=auc[0],tahapan=self.kwargs['current_step'])
            #return models.undangan.objects.none()
        elif self.request.user.user_type=='V':
            return models.undangan.objects.all().filter(item_lelang=self.kwargs['item_lelang'], viewer__users__id = self.request.user.id, tahapan=self.kwargs['current_step'])
            #print(ba)
            #if ba:
            #    vwr = ba[0].viewer.all().filter(users= self.request.user)
            #    if vwr:
            #        return models.undangan.objects.all().filter(item_lelang=self.kwargs['item_lelang'], viewer=vwr[0],tahapan=self.kwargs['current_step'])
            #return models.undangan.objects.none()
        elif self.request.user.user_type=='A':            
            return models.undangan.objects.all().filter(item_lelang=self.kwargs['item_lelang'],tahapan=self.kwargs['current_step'])
        else:
            return models.undangan.objects.all().filter(item_lelang=self.kwargs['item_lelang'], tahapan=self.kwargs['current_step']).order_by('-id')
    
class undanganAuctionerListView(SingleTableMixin, generic.ListView):
    model = models.undangan 
    table_class = tables.undangan_auctionerTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        #auc = models.tim_lelang.objects.all().filter(users=self.kwargs['auctioner'])[0]
        # auctioneer=auc,
        return models.undangan.objects.all().filter(item_lelang=self.kwargs['item_lelang'],tahapan=self.kwargs['current_step']).order_by('-created')

class modalCreateBA(BSModalCreateView):

    template_name = 'modal_ba.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["item_lelang"], "tahapan": self.kwargs["tahapan"]}

class modalUpdateBA(BSModalUpdateView):
    template_name = 'modal_ba.html'
    form_class = forms.BeritaAcaraForm
    model = models.berita_acara
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })
        return initial

class BABidderListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_bidderTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type=='A':  
                   
            return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang'],tahapan=self.kwargs['current_step']).order_by('-last_updated')
        else:
            return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang'], bidder__id=self.kwargs['bidder'], tahapan=self.kwargs['current_step']).order_by('-last_updated')

class BABidder2ListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acara_bidderTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        # qs = super().get_queryset(**kwargs)
        # return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang'], tahapan=self.kwargs['current_step']).order_by('-id')
       
        if self.request.user.user_type =='B':
            bdr_user = bidder_user.objects.get(users = self.request.user)
            return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang'], bidder_user = bdr_user, tahapan=self.kwargs['current_step']).order_by('-last_updated')
        elif self.request.user.user_type=='C':
            return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang'], tahapan=self.kwargs['current_step']).order_by('-last_updated')
            #if ba:
            #    auc = ba[0].auctioneer.all().filter(users= self.request.user)
            #    if auc:
            #        return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang'], auctioneer=auc[0],tahapan=self.kwargs['current_step'])
            #return models.undangan.objects.none()
        elif self.request.user.user_type=='V':
            ba = models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang'], viewer__users__id = self.request.user.id,tahapan=self.kwargs['current_step']).order_by('-last_updated')
            if ba:
                vwr = ba[0].viewer.all().filter(users= self.request.user)
                if vwr:
                    return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang'], viewer=vwr[0],tahapan=self.kwargs['current_step']).order_by('-last_updated')
            return models.undangan.objects.none()
        elif self.request.user.user_type=='A':            
            return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang'],tahapan=self.kwargs['current_step']).order_by('-last_updated')
        else:
            return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang'], tahapan=self.kwargs['current_step']).order_by('-last_updated')

class BAAuctionerListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara
    form_class = forms.BeritaAcaraForm
    table_class = tables.berita_acaraTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type=='C':
#            auc = doc.auctioneer.all().filter(users= self.request.user)[0]
            return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang'],tahapan=self.kwargs['current_step']).order_by('-last_updated')
        elif self.request.user.user_type=='V':
            vwr = doc.viewer.all(users= self.request.user)[0]
            return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang'], viewer=vwr,tahapan=self.kwargs['current_step']).order_by('-last_updated')
        elif self.request.user.user_type=='A':            
            return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang'],tahapan=self.kwargs['current_step']).order_by('-last_updated')
        else:
            return models.berita_acara.objects.none()

"""class berita_acaraListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara
    table_class = tables.berita_acara_persiapanTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['pk'],tahapan=8).order_by('-id')

class berita_acara_bidderListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara
    table_class = tables.berita_acara_persiapan2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara_persiapan.objects.all().filter(item_lelang=self.kwargs['pk'], tahapan=8).order_by('-id')
"""

# dibawah ini adalah table pengambilan Undangan
class pengambilan_undanganListView(SingleTableMixin, generic.ListView):
    model = models.pengambilan_undangan
    table_class = tables.pengambilan_undangan_Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.pengambilan_undangan.objects.all().filter(undangan__item_lelang=self.kwargs['pk'])
    
# dibawah ini adalah table pengambilan BA
class pengambilan_baListView(SingleTableMixin, generic.ListView):
    model = models.pengambilan_ba
    table_class = tables.pengambilan_berita_acara_Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.pengambilan_ba.objects.all().filter(item_lelang=self.kwargs['pk'])
    
def docxview(request, pk):
    from docx import Document
    from htmldocx import HtmlToDocx
    import requests

    docs = models.berita_acara.objects.filter(pk=pk)
    context = {}
    if docs.exists():
        dokumen = docs[0]
        context['nomor']=dokumen.nomor
        context['judul']=dokumen.judul
        context['tanggal']=timezone.localtime(dokumen.tanggal)
        context['keterangan']=dokumen.keterangan
        tahapan = dokumen.tahapan
        url = ""

        itm_lelang = models.item_lelang.objects.get(pk=dokumen.item_lelang.id)
#        pansel = models.penangung_jawab_seleksi.objects.all().filter(item_lelang=dokumen.item_lelang.id)
        pansel = models.auctioner_lelang.objects.all().filter(item_lelang=dokumen.item_lelang.id)
        ketua_pansel = models.penangung_jawab_seleksi.objects.all().filter(item_lelang=dokumen.item_lelang.id).filter(tanggung_jawab="ketua")
        sekretaris_pansel = models.penangung_jawab_seleksi.objects.all().filter(item_lelang=dokumen.item_lelang.id).filter(tanggung_jawab="sekretaris")
        jadwal = models.jadwal_seleksi.objects.all().filter(item_lelang=dokumen.item_lelang.id, tahap=dokumen.tahapan)
        context['seleksi'] = itm_lelang.nama_lelang

        # perbaikan
        if not jadwal:
            # messages.error(request, "Jadwal Tidak Tersedia")
            return JsonResponse({"error_message": "Jadwal Tidak Tersedia"}, status=400, content_type="application/json")
            # return redirect(request.META.get('HTTP_REFERER', '/'))

        if not ketua_pansel:
            # messages.error(request, "Ketua Belum Di Input")
            return JsonResponse({"error_message": "Ketua Belum Di Input"}, status=400, content_type="application/json")
            # return redirect(request.META.get('HTTP_REFERER', '/'))

        if not sekretaris_pansel:
            # messages.error(request, "Sekretaris Belum Di Input")
            return JsonResponse({"error_message": "Sekretaris Belum Di Input"}, status=400, content_type="application/json")
            # return redirect(request.META.get('HTTP_REFERER', '/'))
        # end
        
        context["jadwal"] = jadwal[0]
        context['tahun'] = itm_lelang.tahun
        context['pansel'] = pansel
        context['ketua_pansel'] = ketua_pansel[0].nama
        context['sekretaris_pansel'] = sekretaris_pansel[0].nama

        # Dokumen Seleksi
        if tahapan.id == 10:
            template_name = 'berita_acara/ba_pengambilan_doksel.html'
            doksel = dokumen_seleksi.objects.filter(item_lelang = itm_lelang)
            if doksel:
                pengumuman_queryset = models.pengumuman.objects.filter(item_lelang = itm_lelang, tahapan = 2)
                if pengumuman_queryset:
                    pengumuman = pengumuman_queryset.first()
                    context['pengumuman'] = pengumuman
                table = pengambilan_dokumen_seleksi.objects.filter(dokumen_seleksi=doksel[0]).order_by("tgl_download","bidder_perwakilan__id",).distinct("tgl_download","bidder_perwakilan__id")
                context['table'] = table
            else:
                context['pengumuman'] = None
                context['table'] = None

        # Penyampaian Pertanyaan
        elif tahapan.id == 16:
            template_name = 'berita_acara/ba_pertanyaan.html'
            pengumuman = models.pengumuman.objects.filter(item_lelang = itm_lelang, tahapan = 2)
            if pengumuman:
                context['pengumuman'] = pengumuman.first()
            table = p_pertanyaan.objects.filter(item_lelang = itm_lelang).order_by("created","perwakilan__id").distinct("created","perwakilan__id")
            context['table'] = table

        # aanwizing
        elif tahapan.id == 23:
            template_name = 'berita_acara/ba_anwizing.html'
            table = daftar_hadir.objects.filter(item_lelang = itm_lelang,tahapan = 209).order_by("tgl_kehadiran",'bidder_perwakilan__nama_lengkap')
            context['table'] = table
        
        # simulasi
        elif tahapan.id == 28:
            template_name = 'berita_acara/ba_simulasi.html'
            table = daftar_hadir.objects.filter(item_lelang = itm_lelang,tahapan = 211).order_by("tgl_kehadiran",'bidder_perwakilan__nama_lengkap')
            context['table'] = table

        # addendum
        elif tahapan.id == 36:
            template_name = 'berita_acara/ba_pengambilan_addendum.html'
            table = pengambilan_dokumen_addendum.objects.filter(dokumen_addendum__item_lelang = itm_lelang).order_by("created","bidder_perwakilan__id").distinct("created","bidder_perwakilan")
            #print(table)
            context['table'] = table

        # permohonan keikutsertaan
        elif tahapan.id == 41:
            template_name = 'berita_acara/ba_keikutsertaan.html' 
            #   table = permohonan_keikutsertaan.objects.filter(item_lelang = itm_lelang).order_by('bidder_id','created').distinct('bidder_id')                  
            lebih_dari_waktu_yg_ditentukan_item = models.jadwal_seleksi.objects.get(pk=2917).tanggal_akhir + timedelta(hours=7)
            
            current_time = datetime.now(pytz.timezone('Asia/Jakarta'))
            current_time_greater_than = current_time > lebih_dari_waktu_yg_ditentukan_item
            
            
            berita_list = models.berita_acara.objects.filter(item_lelang=itm_lelang, tahapan=41).order_by('-last_updated').prefetch_related('bidder_user')
            bidder_users = []
            for berita in berita_list:
                bidder_users.extend(berita.bidder_user.all())
            list_bidder_semuanya = list(set(bidder_users))
            
            
            table = permohonan_keikutsertaan.objects.filter(item_lelang = itm_lelang).order_by("created","perwakilan__id").distinct("created","perwakilan")   
            table_mengikuti = table.filter(pernyataan = "MENGIKUTI")
            table_tidak_mengikuti = table.filter(pernyataan = "TIDAK_MENGIKUTI")
            
            table_mengikuti_bidder = []
            table_tidak_mengikuti_bidder = []
            
            for item in table_mengikuti:
                table_mengikuti_bidder.append(item.bidder)
            
            for item in table_tidak_mengikuti:
                table_tidak_mengikuti_bidder.append(item.bidder)
            
            if current_time_greater_than:
                # Filter bidder yang belum ada di table_tidak_mengikuti, tetapi sudah ada di list_bidder_semuanya setelah dikecualikan table_mengikuti_bidder
                bidder_yang_belum_tercatat = [
                    bidder for bidder in list_bidder_semuanya
                    if bidder not in table_mengikuti_bidder and bidder not in table_tidak_mengikuti_bidder
                ]

                # **TANPA INSERT KE DATABASE**: hanya menambah ke list table_tidak_mengikuti_bidder
                table_tidak_mengikuti_bidder.extend(bidder_yang_belum_tercatat)

                # Masukkan bidder yang belum tercatat ke dalam table_tidak_mengikuti
                for bidder in bidder_yang_belum_tercatat:
                    bidder_perwakilan_u = bidder_perwakilan.objects.filter(bidder=bidder).first()
                    permohonan_keikutsertaan.objects.create(
                        item_lelang=itm_lelang,
                        bidder=bidder,
                        pernyataan="TIDAK_MENGIKUTI",
                        perwakilan=bidder_perwakilan_u
                    )

                # Update ulang table_tidak_mengikuti setelah penambahan
                table_tidak_mengikuti = permohonan_keikutsertaan.objects.filter(
                    item_lelang=itm_lelang, pernyataan="TIDAK_MENGIKUTI"
                )
            
            context['table_mengikuti'] = table_mengikuti
            context['table_tidak_mengikuti'] = table_tidak_mengikuti
            context['table'] = table

        # pemeriksaan kelengkapan
        elif tahapan.id == 48:
            template_name = 'berita_acara/ba_pemeriksaan_kelengkapan.html'
            table = form_pemeriksaan.objects.filter(item_lelang = itm_lelang).order_by("created")
            context['table'] = table


        # verifikasi dokumen permohonan
        elif tahapan.id == 55:
            template_name = 'berita_acara/ba_verifikasi.html'
            context['table'] = form_verifikasi.objects.filter(item_lelang = itm_lelang)

        # evaluasi
        elif tahapan.id == 62:
            
            template_name = 'berita_acara/ba_evaluasi.html'
            doksel = dokumen_seleksi.objects.filter(item_lelang = itm_lelang)
            if doksel:
                table_pengambilan_doksel = pengambilan_dokumen_seleksi.objects.filter(dokumen_seleksi=doksel[0]).order_by("tgl_download","bidder_perwakilan__id",).distinct("tgl_download","bidder_perwakilan__id")
                context['table_pengambilan_doksel'] = table_pengambilan_doksel
                table_addendum_pengambilan_doksel = pengambilan_dokumen_addendum.objects.filter(dokumen_addendum__item_lelang = itm_lelang).order_by("created","bidder_perwakilan__id").distinct("created","bidder_perwakilan")  
                context['table_addendum_pengambilan_doksel'] = table_addendum_pengambilan_doksel
                table_permohonan_keikutsertaan = permohonan_keikutsertaan.objects.filter(item_lelang = itm_lelang).order_by("created","perwakilan__id").distinct("created","perwakilan")  
                context['table_permohonan_keikutsertaan'] = table_permohonan_keikutsertaan
                table_pemeriksaan_kelengkapan = form_pemeriksaan.objects.filter(item_lelang = itm_lelang).order_by("created")
                context['table_pemeriksaan_kelengkapan'] = table_pemeriksaan_kelengkapan
                table_form_verifikasi = form_verifikasi.objects.filter(item_lelang = itm_lelang)
                context['table_form_verifikasi'] = table_form_verifikasi
                table = form_evaluasi.objects.filter(item_lelang = itm_lelang).order_by('created')
                context['table'] = table
                table_hasil_kesimpulan = hasil_kesimpulan.objects.filter(item_lelang = itm_lelang).order_by('created')
                context['table_hasil_kesimpulan'] = table_hasil_kesimpulan

        # Sanggahan
        elif tahapan.id == 73:
            context['table'] = form_sanggahan.objects.filter(item_lelang = itm_lelang).order_by('created')
            context['jawaban'] = jawaban_sanggahan.objects.filter(item_lelang = itm_lelang).order_by('created')
            context['sanggahan'] = form_sanggahan.objects.filter(item_lelang = itm_lelang,status_sanggah = 'Ada').order_by('created')
            context['not_sanggahan'] = form_sanggahan.objects.filter(item_lelang = itm_lelang,status_sanggah = 'Tidak Ada').order_by('created')
            template_name = 'berita_acara/ba_sanggahan.html'
            # return render(request,template_name,context)

        # SMRA
        # Putaran Lelang Harian
        elif tahapan.id == 90:
            # context['table'] = smra2models.obyek_seleksi_smra.objects.filter(item = itm_lelang).order_by('created')
            context['table'] = smra2models.obyek_seleksi_smra.objects.filter(item__item_lelang__id = itm_lelang.id).order_by('created')
            context['undangan'] = adm_lelangmodels.undangan.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "88").order_by('-id')
            context['ba'] = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "90").order_by('-id')
            context['round'] = smra2models.sum_round_smra2.objects.filter(item_lelang=dokumen.item_lelang.id).order_by('-id')
            highest_round_value = smra2models.hasil_smra2.objects.filter(item_lelang=dokumen.item_lelang.id).aggregate(Max('round'))['round__max']
            hasil_max_round = smra2models.hasil_smra2.objects.filter(item_lelang=dokumen.item_lelang.id).values_list('item', flat=True).order_by('item')
#            hasil_max_round = smra2models.hasil_smra2.objects.filter(item_lelang=dokumen.item_lelang.id, round=highest_round_value).order_by('item')
            data_items_array = list(set(hasil_max_round))
            hari = context['tanggal'].weekday()
            putaran = smra2models.round_schedule_smra2.objects.filter(item=dokumen.item_lelang.id, hari=hari).aggregate(
                min_mulai=Min("mulai"),
                max_selesai=Max("selesai"))

            print(hari, context['tanggal'], putaran)
            
            # FORMAT PRICE RUPIAH -> Rp3.000.000.000,00
            # hasil = []
            # for h in hasil_max_round:
            #     h.price = f"Rp{h.price:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')
            #     hasil.append(h)
            # context['hasil'] = hasil 
            result_data = []
            for t in data_items_array:
                data = smra2models.hasil2_smra.objects.filter(item=t).order_by('item__id','round', 'ranking')
                isi = []
                judul = ""
                for u in data:
                    judul = u.item.band + '/' + u.item.cakupan 
                    isi.append({
                        'putaran': u.round,
                        'peserta': u.bidder,
                        'harga': u.price,
                        'waktu': u.submit
                    })

                var = {
                    'judul': judul,
                    'cakupan': u.item.cakupan, # 'Regional 1', 'Regional 2', 'Regional 3'
                    'isi': isi
                }

                result_data.append(var)
            
            result_data = sorted(result_data, key=lambda x: x['cakupan'])
            context['json'] = result_data

            # Hari Ke Lelang : Nomor -> Abjad
            hari_ke = len(context['ba'])
            if hari_ke == 1:
                context['hari_ke'] = "Satu"
            elif hari_ke == 2:
                context['hari_ke'] = "Dua"
            elif hari_ke == 3:
                context['hari_ke'] = "Tiga"
            elif hari_ke == 4:
                context['hari_ke'] = "Empat"
            elif hari_ke == 5:
                context['hari_ke'] = "Lima"
            else:
                context['hari_ke'] = hari_ke
                
            context['lastes_round'] = highest_round_value
            context['putaran'] = putaran

            # return render(request,template_name,context)
            template_name = 'berita_acara/ba_putaran_lelang_harian.html'

        # Penawaran Beauty Contest
        elif tahapan.id == 119:
            context['table'] = dokumen_bc.objects.filter(item__item_lelang__id = itm_lelang.id).order_by('item__urutan')
            template_name = 'berita_acara/ba_penawaran_beauty_contestl.html'

            # return render(request,template_name,context)

        # Tahapan Penilaian Beauty Contest BA
        elif tahapan.id == 188:
            context['table'] = hasil_beauty_contest.objects.filter(item__item_lelang__id=itm_lelang.id).order_by('item__urutan')
            # return JsonResponse({"models_to_return": list(context['table'])},safe=False)

            template_name = 'berita_acara/ba_penilaian_beauty_contest.html'
            # return render(request,template_name,context)

        # Tahapan Gabungan Penilaian Negosiasi
        elif tahapan.id == 151:
            context['table'] = gabunganmodels.hasil_gabungan.objects.filter(item__item_lelang__id=itm_lelang.id).order_by('item__urutan')
            # return JsonResponse({"models_to_return": list(context['table'])},safe=False)
            
            template_name = 'berita_acara/ba_gabungan_penilaian_negosiasi.html'
            # return render(request,template_name,context)

        # Negosiasi Penawaran Harga
        elif tahapan.id == 126:
            context['table'] = negosiasimodels.penawaran.objects.filter(item__item_lelang__id=itm_lelang.id).order_by('item__urutan')            
            template_name = 'berita_acara/ba_negosiasi_penawaran_harga.html'

        elif tahapan.id == 132:
            context['table'] = negosiasimodels.evaluasi_penawaran.objects.filter(penawaran__item__item_lelang__id=itm_lelang.id)
            # return JsonResponse({"models_to_return": list(context['table'])},safe=False)
            template_name = 'berita_acara/ba_negosiasi_hasil_penilaian.html'
           # return render(request,template_name,context)
        elif tahapan.id == 158:
            ps_pb = pascaseleksimodels.pemilihan_blok_pasca_seleksi.objects.filter(item__item_lelang__id=itm_lelang.id).order_by('ranking')

            query = '''
                select a.id ,a.id as pemilihan_blok, b.harga, f.nama_lengkap,e.nama_perusahaan, d.rentang_frekuensi,  a.ranking ,b.id as id_penawaran from pasca_seleksi_pemilihan_blok_pasca_seleksi as a
                JOIN negosiasi_penawaran as b on b.bidder_id = a.bidder_id and b.item_id = a.item_id
                JOIN userman_bidder_user as c on c.id = a.bidder_id
                JOIN adm_lelang_detail_itemlelang as d on d.id = a.item_id
                JOIN userman_bidder as e on e.id = c.bidder_id
                JOIN userman_users as f on f.id = c.users_id
                order by ranking
            '''

            queryset = pascaseleksimodels.pemilihan_blok_pasca_seleksi.objects.raw(query)

            context['table'] = ps_pb
            context['table2'] = pascaseleksimodels.pemilihan_blok_pasca_seleksi.objects.filter(persetujuan=True)
            template_name = 'berita_acara/ba_pemilihan_blok.html'

        elif tahapan.id == 145:
            context['table'] = negosiasimodels.evaluasi_revisi_penawaran.objects.filter(revisi_penawaran__item__item_lelang__id=itm_lelang.id)
            template_name = 'berita_acara/ba_negosiasi_evaluasi_penawaran_harga.html'

        elif tahapan.id == 168:
            context['table'] = pascaseleksimodels.form_ps_sanggahan.objects.filter(item_lelang = itm_lelang).order_by('created')
            context['jawaban'] = pascaseleksimodels.jawaban_ps_sanggahan.objects.filter(item_lelang = itm_lelang).order_by('created')
            context['sanggahan'] = pascaseleksimodels.form_ps_sanggahan.objects.filter(item_lelang = itm_lelang,status_sanggah = 'Ada').order_by('created')
            context['not_sanggahan'] = pascaseleksimodels.form_ps_sanggahan.objects.filter(item_lelang = itm_lelang,status_sanggah = 'Tidak Ada').order_by('created')
            template_name = 'berita_acara/ba_sanggahan_pasca_seleksi.html'
        
        elif tahapan.id == 230:
        # elif tahapan.id == 172:
            # context['table'] = negosiasimodels.penawaran.objects.filter(item__item_lelang__id=itm_lelang.id)
            ps_ketua = models.penangung_jawab_seleksi.objects.all().filter(item_lelang=dokumen.item_lelang.id).filter(tanggung_jawab="ketua")
            ps_sekretaris = models.penangung_jawab_seleksi.objects.all().filter(item_lelang=dokumen.item_lelang.id).filter(tanggung_jawab="sekretaris")
            #ps_dasar_hukum = rencanaseleksimodels.dasar_hukumnya.objects.all().filter(item_lelang=dokumen.item_lelang.id)
            # bidder di lelang ini
            ps_bidder = adm_lelangmodels.bidder_lelang.objects.filter(item_lelang=dokumen.item_lelang.id)
            id_bidder = [item.id for item in ps_bidder]
            ps_perwakilan = bidder_perwakilan.objects.filter(bidder__in=id_bidder)

            # pengumuman
            ps_pengumuman = adm_lelangmodels.pengumuman.objects.filter(item_lelang=dokumen.item_lelang.id).order_by('created')
            # doksel
            ps_undangan_doksel = adm_lelangmodels.undangan.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "4").order_by('-id')
            ps_pengambilan_dokumen_seleksi = pengambilan_dokumen_seleksi.objects.filter(dokumen_seleksi__item_lelang=dokumen.item_lelang.id)
            ps_ba_doksel = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "10").order_by('-id')
            # pertanyaan
            ps_pertanyaan = p_pertanyaan.objects.filter(item_lelang=dokumen.item_lelang.id)
            ps_ba_pertanyaan = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "16").order_by('-id')
            # aanwijing
            ps_undangan_aanwijing = adm_lelangmodels.undangan.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "21").order_by('-id')
            ps_ba_aanwijing = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "23").order_by('-id')
            # simulasi
            ps_undangan_simulasi = adm_lelangmodels.undangan.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "26").order_by('-id')
            ps_ba_simulasi = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "62").order_by('-id')
            # addendum 
            ps_addendum_doksel = p_addendum.objects.filter(item_lelang=dokumen.item_lelang.id)
            # permohonan
            ps_permohonan = permohonan_keikutsertaan.objects.filter(item_lelang=dokumen.item_lelang.id)
            ps_ba_permohonan = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "41").order_by('-id')
            # pemeriksaan dokumen
            ps_undangan_pemeriksaan = adm_lelangmodels.undangan.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "44").order_by('-id')
            ps_pemeriksaan = form_pemeriksaan.objects.filter(item_lelang=dokumen.item_lelang.id)
            ps_ba_pemeriksaan = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "48").order_by('-id')
            # verifikasi
            ps_undangan_verifikasi = adm_lelangmodels.undangan.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "51").order_by('-id')
            ps_verifikasi = form_verifikasi.objects.filter(item_lelang=dokumen.item_lelang.id)
            ps_ba_verifikasi = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "55").order_by('-id')
            # hasil evaluasi
            # ps_hasil_evaluasi = hasil_kesimpulan.objects.filter(item_lelang=dokumen.item_lelang.id, hasil_pemeriksaan = "t")
            query_ps_hasil_evaluasi = (
                "select c.nama_perusahaan, a.* from administrasi_hasil_kesimpulan as a "
                "join userman_bidder as c on c.id = a.bidder_id "
                "where hasil_pemeriksaan = 't' and item_lelang_id = " + str(itm_lelang.id)
            )
            queryset_hasil_evaluasi = hasil_kesimpulan.objects.raw(query_ps_hasil_evaluasi)
            ps_ba_hasil_evaluasi = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "62").order_by('-id')
            ps_pengumuman_hasil_evaluasi = adm_lelangmodels.pengumuman.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "64").order_by('-id')
            
            # adm sanggahan
            ps_sanggahan_sanggahan = form_sanggahan.objects.filter(item_lelang=dokumen.item_lelang.id).order_by('-id')
            ps_sanggahan_sanggahan_ada = form_sanggahan.objects.filter(item_lelang=dokumen.item_lelang.id, status_sanggah="Ada").order_by('-id')
            ps_sanggahan_sanggahan_tidak = form_sanggahan.objects.filter(item_lelang=dokumen.item_lelang.id, status_sanggah="Tidak Ada").order_by('-id')

            # SMRA
            ps_undangan_smra = adm_lelangmodels.undangan.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "88").order_by('-id')
            ps_ba_smra = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "90").order_by('-id')
            ps_putaran_smra = smra2models.sum_round_smra2.objects.filter(item_lelang=dokumen.item_lelang.id).order_by('-id')

            query_ps_hasil_smra = (
                "SELECT a.id, a.item_id, a.price, a.ranking, c.nama_perusahaan, a.round "
                "FROM smra2_hasil2_smra as a "
                "INNER JOIN userman_bidder_user as b ON b.id = a.bidder_id "
                "INNER JOIN userman_bidder as c ON c.id = b.bidder_id "
                "WHERE item_lelang = "+str(itm_lelang.id)+
                " AND round = (SELECT MAX(round) FROM smra2_hasil2_smra WHERE item_lelang = "+str(itm_lelang.id)+") "
                "ORDER BY ranking"
            )
            
            queryset_ps_hasil_smra = hasil_kesimpulan.objects.raw(query_ps_hasil_smra)

            # Pemilihan Blok
            ps_undangan_pemilihan_blok = adm_lelangmodels.undangan.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "153").order_by('-id')
            ps_ba_pemilihan_blok = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "158").order_by('-id')
            ps_hasil_pemilihan_blok = pascaseleksimodels.pemilihan_blok_pasca_seleksi.objects.filter(item__item_lelang=dokumen.item_lelang.id).order_by('ranking')
            ps_blok_pasca_seleksi = pascaseleksimodels.blok_pasca_seleksi.objects.filter(item__item_lelang=dokumen.item_lelang.id).order_by('id')

            # sanggahan pasca seleksi
            ps_ba_sanggahan_ps = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "168").order_by('-id')
            ps_sanggahan_sanggahan_ps = pascaseleksimodels.form_ps_sanggahan.objects.filter(item_lelang=dokumen.item_lelang.id).order_by('-id')
            ps_sanggahan_sanggahan_ada_ps = pascaseleksimodels.form_ps_sanggahan.objects.filter(item_lelang=dokumen.item_lelang.id, status_sanggah="Ada").order_by('-id')
            ps_sanggahan_sanggahan_tidak_ps = pascaseleksimodels.form_ps_sanggahan.objects.filter(item_lelang=dokumen.item_lelang.id, status_sanggah="Tidak Ada").order_by('-id')

            # jadwal selekti untuk waktu tahapan 
            # tahapan_pertanyaan
            ps_tahapan_pertanyaan = adm_lelangmodels.jadwal_seleksi.objects.filter(item_lelang=dokumen.item_lelang.id, tahap="13")
            ps_tahapan_permohonan_keikutsertaan = adm_lelangmodels.jadwal_seleksi.objects.filter(item_lelang=dokumen.item_lelang.id, tahap="38")
            ps_tahapan_sanggahan_adm = adm_lelangmodels.jadwal_seleksi.objects.filter(item_lelang=dokumen.item_lelang.id, tahap="66")
            ps_tahapan_sanggahan_ps = adm_lelangmodels.jadwal_seleksi.objects.filter(item_lelang=dokumen.item_lelang.id, tahap="86")

            # pengecekan jika ketua atau sekretaris tidak ada
            if ps_ketua:
                context['ps_ketua'] = ps_ketua[0]
            if ps_sekretaris:
                context['ps_sekretaris'] = ps_sekretaris[0]
            # bidder
            context['ps_bidder'] = ps_perwakilan
            # 
            #context['ps_dasar_hukum'] = ps_dasar_hukum
            context['ps_pengumuman'] = ps_pengumuman[0]
            # doksel
            context['ps_undangan_doksel'] = ps_undangan_doksel[0]
            if ps_pengambilan_dokumen_seleksi:
                context['ps_pengambilan_dokumen_seleksi'] = ps_pengambilan_dokumen_seleksi[0]
            else:
                context['ps_pengambilan_dokumen_seleksi'] = None
            context['ps_ba_doksel'] = ps_ba_doksel[0]
            # pertanyaan
            context['ps_tahapan_pertanyaan'] = ps_tahapan_pertanyaan[0]
            context['ps_pertanyaan'] = ps_pertanyaan[0]
            context['ps_ba_pertanyaan'] = ps_ba_pertanyaan[0]
            # aanwizjing
            if len(ps_undangan_aanwijing) >0:
                context['ps_undangan_aanwijing']= ps_undangan_aanwijing[0]
            context['ps_ba_aanwijing'] = ps_ba_aanwijing[0]
            # simulasi
            if len(ps_undangan_simulasi) >0:
                context['ps_undangan_simulasi'] = ps_undangan_simulasi[0]
            context['ps_ba_simulasi'] = ps_ba_simulasi[0]
            # addendum
            if ps_addendum_doksel:
                context['ps_addendum_doksel'] = ps_addendum_doksel[0]
            else:
                context['ps_addendum_doksel'] = "None"
            # permohonan keikutsertaan
            context['ps_tahapan_permohonan_keikutsertaan'] = ps_tahapan_permohonan_keikutsertaan[0]
            context['ps_permohonan'] = ps_permohonan[0]
            context['ps_ba_permohonan'] = ps_ba_permohonan[0]
            # pemeriksaan dokumen
            context['ps_undangan_pemeriksaan'] = ps_undangan_pemeriksaan[0]
            context['ps_ba_pemeriksaan'] = ps_ba_pemeriksaan[0]
            context['ps_pemeriksaan'] = ps_pemeriksaan

            # verifikasi
            if ps_undangan_verifikasi :
                context['ps_undangan_verifikasi'] = ps_undangan_verifikasi[0]
            else :
                context['ps_undangan_verifikasi'] = "None"

            context['ps_verifikasi'] = ps_verifikasi
            context['ps_ba_verifikasi'] = ps_ba_verifikasi[0]
            # hasil evaluasi
            context['ps_ba_hasil_evaluasi'] = ps_ba_hasil_evaluasi[0]
            context['ps_hasil_evaluasi'] = queryset_hasil_evaluasi
            context['ps_pengumuman_hasil_evaluasi'] = ps_pengumuman_hasil_evaluasi[0]
            # sanggahan
            context['ps_sanggahan_sanggahan'] = ps_sanggahan_sanggahan[0]
            context['ps_tahapan_sanggahan_adm'] = ps_tahapan_sanggahan_adm[0]
            context['ps_sanggahan_sanggahan_ada'] = ps_sanggahan_sanggahan_ada
            context['ps_sanggahan_sanggahan_tidak'] = ps_sanggahan_sanggahan_tidak
            # smra
            #context['ps_undangan_smra'] = ps_undangan_smra[0]
            #context['ps_ba_smra'] = ps_ba_smra
            #context['ps_putaran_smra'] = ps_putaran_smra[0]
            #context['queryset_ps_hasil_smra'] = queryset_ps_hasil_smra

            # pemilihan blok hasil
            context['ps_undangan_pemilihan_blok'] = ps_undangan_pemilihan_blok
            context['ps_ba_pemilihan_blok'] = ps_ba_pemilihan_blok
            context['ps_hasil_pemilihan_blok'] = ps_hasil_pemilihan_blok
            context['ps_blok_pasca_seleksi'] = ps_blok_pasca_seleksi
            # sanggahan
            context['ps_tahapan_sanggahan_ps'] = ps_tahapan_sanggahan_ps[0]
            context['ps_ba_sanggahan_ps'] = ps_ba_sanggahan_ps[0]


            template_name = 'berita_acara/ba_sanggahan_hasil_seleksi.html'

        elif tahapan.id == 197:
            context['table'] = negosiasimodels.revisi_penawaran.objects.filter(item__item_lelang__id=itm_lelang.id)
            template_name = 'berita_acara/ba_negosiasi_penawaran_harga.html'
        # Negosiasi Penawaran Harga
        elif tahapan.id == 92:
            context['table'] = smra2models.obyek_seleksi_smra.objects.filter(item__item_lelang__id = itm_lelang.id).order_by('item__urutan')
            context['undangan'] = adm_lelangmodels.undangan.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "88").order_by('-id')
            context['ba'] = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "90").order_by('-id')
            context['ba2'] = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "92").order_by('-id')
            context['round'] = smra2models.sum_round_smra2.objects.filter(item_lelang=dokumen.item_lelang.id).order_by('-id')
            highest_round_value = smra2models.hasil_smra2.objects.filter(item_lelang=dokumen.item_lelang.id).aggregate(Max('round'))['round__max']
            queryset_result = smra2models.hasil_smra2.objects.filter(item_lelang=dokumen.item_lelang.id, berlaku=True).values_list('item', flat=True).order_by('item')
            data_items_array = list(set(queryset_result))
            
            hari = context['tanggal'].weekday()
            context['lastes_round'] = highest_round_value
            putaran = smra2models.round_schedule_smra2.objects.filter(item=dokumen.item_lelang.id).aggregate(
                min_hari_mulai=Min("hari"),
                max_hari_selesai=Max("hari"),
                min_jam_mulai=Min("mulai"),
                max_jam_selesai=Max("selesai"),
            )
            putaran['min_hari_mulai'] = smra2models.DAY_OF_THE_WEEK[putaran['min_hari_mulai']]
            putaran['max_hari_selesai'] = smra2models.DAY_OF_THE_WEEK[putaran['max_hari_selesai']]
            context['putaran'] = putaran

            result_data = []
            
            for t in data_items_array:
                data = smra2models.hasil2_smra.objects.filter(item=t).order_by('item__urutan', 'round', 'ranking')
                
                isi_per_peserta = defaultdict(list)
                judul = "Obyek Seleksi -"

                for u in data:
                    judul = u.item.band + '/' + u.item.cakupan # Obyek Seleksi 1400 simu/Regional 2
                    isi_per_peserta[u.bidder].append({
                        'putaran': u.round,
                        'harga': u.price,
                        'waktu': u.submit
                    })

                isi_final = [{'peserta': peserta, 'data': isi} for peserta, isi in isi_per_peserta.items()]

                result_data.append({
                    'judul': judul,
                    'cakupan': u.item.cakupan,  # 'Regional 1', 'Regional 2', 'Regional 3'
                    'isi': isi_final 
                })

            result_data = sorted(result_data, key=lambda x: x['cakupan'])
            context['json'] = result_data
            
            template_name = 'berita_acara/ba_smra.html'
            # return render(request,template_name,context)
        elif tahapan.id == 96:
            # get hari menghitung panjang ba
            context['ba'] = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "96").order_by('-id')
            # dapetin data lampiran
            hasil = ccamodels.hasil_cca.objects.filter(item_lelang = itm_lelang.id, valid=True).distinct('round').order_by('round')
            tbls = []
            waktu = []

            for i in hasil:
                isi = []
                # tbls.append(ccamodels.hasil2_detail_cca.objects.all().filter(parent__item_lelang = itm_lelang.id, parent__round=i.round, parent__valid=True).order_by('-parent__round','ranking'))
                data1 = ccamodels.hasil2_detail_cca.objects.all().filter(parent__item_lelang = itm_lelang.id, parent__round=i.round, parent__valid=True).order_by('-parent__round','ranking')
                data2 = ccamodels.hasil_detail_cca.objects.all().filter(parent__item_lelang = itm_lelang.id, parent__round=i.round, parent__valid=True).order_by('-parent__round',)

                entry2 = {
                    'mulai': i.mulai,
                    'selesai': i.selesai,
                }

                for u in data1:
                    entry = {
                        'round': i.round,
                        'bidder': u.parent.bidder,
                        'item': u.item,
                        'price': u.price,
                        'eli': i.eli,
                        'valid': i.valid,
                        'submit': i.submit,
                        'blok': None
                    }
                    
                    for s in data2:
                        if s.parent.bidder == u.parent.bidder:
                            entry['blok'] = s.block
                            break

                    isi.append(entry)
                    waktu.append(entry2)

                tbls.append(isi)

            context['detail'] = tbls
            context['waktu'] = waktu
                
            template_name = 'berita_acara/ba_putaran_lelang_harian_cca_clock.html'
        elif tahapan.id == 102:
            # dapetin hari
            # get hari menghitung panjang ba
            context['ba'] = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "102").order_by('-id')
            # dapetin data lampiran
            hasil = ccamodels.hasil_cca.objects.filter(item_lelang = itm_lelang.id, valid=True).distinct('round').order_by('round')
            tbls = []
            waktu = []

            for i in hasil:
                isi = []
                # tbls.append(ccamodels.hasil2_detail_cca.objects.all().filter(parent__item_lelang = itm_lelang.id, parent__round=i.round, parent__valid=True).order_by('-parent__round','ranking'))
                data1 = ccamodels.hasil2_detail_cca.objects.all().filter(parent__item_lelang = itm_lelang.id, parent__round=i.round, parent__valid=True).order_by('-parent__round','ranking')
                data2 = ccamodels.hasil_detail_cca.objects.all().filter(parent__item_lelang = itm_lelang.id, parent__round=i.round, parent__valid=True).order_by('-parent__round',)

                entry2 = {
                    'mulai': i.mulai,
                    'selesai': i.selesai,
                }

                for u in data1:
                    entry = {
                        'round': i.round,
                        'bidder': u.parent.bidder,
                        'item': u.item,
                        'price': u.price,
                        'eli': i.eli,
                        'valid': i.valid,
                        'submit': i.submit,
                        'blok': None
                    }
                    
                    for s in data2:
                        if s.parent.bidder == u.parent.bidder:
                            entry['blok'] = s.block
                            break

                    isi.append(entry)
                    waktu.append(entry2)

                tbls.append(isi)

            context['detail'] = tbls
            context['waktu'] = waktu
                
            template_name = 'berita_acara/ba_putaran_lelang_harian_cca_supplement.html'
        elif tahapan.id == 108:
           # get hari menghitung panjang ba
            context['ba'] = adm_lelangmodels.berita_acara.objects.filter(item_lelang=dokumen.item_lelang.id, tahapan = "108").order_by('-id')
            # dapetin data lampiran
            hasil = ccamodels.hasil_cca.objects.filter(item_lelang = itm_lelang.id, valid=True).distinct('round').order_by('round')
            tbls = []
            waktu = []

            for i in hasil:
                data1 = ccamodels.hasil2_detail_cca.objects.all().filter(parent__item_lelang = itm_lelang.id, parent__round=i.round, parent__valid=True).order_by('-parent__round','ranking')
                data2 = ccamodels.hasil_detail_cca.objects.all().filter(parent__item_lelang = itm_lelang.id, parent__round=i.round, parent__valid=True).order_by('-parent__round',)

                isi = []

                entry2 = {
                    'mulai': i.mulai,
                    'selesai': i.selesai,
                }

                for u in data1:
                    entry = {
                        'round': i.round,
                        'bidder': u.parent.bidder,
                        'item': u.item,
                        'price': u.price,
                        'eli': i.eli,
                        'valid': i.valid,
                        'submit': i.submit,
                        'ranking': u.ranking_putaran,
                        'blok': None
                    }
                    
                    for s in data2:
                        if s.parent.bidder == u.parent.bidder:
                            entry['blok'] = s.block
                            break

                    isi.append(entry)
                    waktu.append(entry2)

                tbls.append(isi)
            context['detail'] = tbls
            context['waktu'] = waktu

            template_name = 'berita_acara/ba_putaran_lelang_harian_cca_assigment.html'

        kop_surat = settings.BASE_DIR / 'templates/berita_acara/YTdiySKF.docx'
        document = Document(kop_surat)
        new_parser = HtmlToDocx()
        strhtml = render_to_string(template_name, context)
        new_parser.table_style = 'TableGrid'
        new_parser.add_html_to_document(strhtml, document)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        document.save(response)
        return response
       

class PdfsView(PDFView):

    template_name = 'berita_acara/ba_pengambilan_doksel.html'
 
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        docs = models.berita_acara.objects.get(pk=kwargs['pk'])
        context = {}
        if docs.exist():
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
        return context

# Undangan Rekapitulasi
class undanganRekapitulasiListView(SingleTableMixin, generic.ListView):
    model = models.undangan 
    table_class = tables.undangan_rekapitulasiTable
    template_name = 'table_persyaratan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.undangan.objects.all().filter(item_lelang=self.kwargs['item_lelang']).order_by('-id')
    
# pengumuman rekapitulasi
class pengumumanRekapitulasiListView(SingleTableMixin, generic.ListView):
    model = models.pengumuman 
    table_class = tables.pengumuman_rekapitulasiTable
    template_name = 'table_persyaratan_p.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.pengumuman.objects.all().filter(item_lelang=self.kwargs['item_lelang']).order_by('-id')
    
    
# berita acara rekapitulasi
class beritaacaraRekapitulasiListView(SingleTableMixin, generic.ListView):
    model = models.berita_acara 
    table_class = tables.berita_acara_rekapitulasiTable
    template_name = 'table_persyaratan_BA.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang']).order_by('-id')
    
    
# doksel rekapitulasi
class dokselRekapitulasiListView(SingleTableMixin, generic.ListView):
    model = p_dokumen 
    table_class = tables.doksel_rekapitulasiTable
    template_name = 'table_persyaratan_doksel.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.berita_acara.objects.all().filter(item_lelang=self.kwargs['item_lelang']).order_by('-id')

# email rekapitulasi
class emailRekapitulasiListView(SingleTableMixin, generic.ListView):
    model = Notifikasi
    table_class = tables.email_rekapitulasiTable
    template_name = 'table_persyaratan_doksel.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return Notifikasi.objects.all().order_by('-id')
    

# check data bidder
def api_check_bidder(request, pk, objek_lelang):
    if request.user.is_authenticated:
        if request.method == 'GET':
            existing_bidders = obyek_seleksi_smra.objects.filter(item=objek_lelang).values_list('bidder_user', flat=True)
            bdr = models.bidder_lelang.objects.filter(item_lelang=pk).values_list('bidder', flat=True)
            available_bidders = bidder_user.objects.filter(id__in=bdr).exclude(id__in=existing_bidders).values("id")
            return JsonResponse(list(available_bidders), safe=False)
        
    return JsonResponse({"error": "Unauthorized"}, status=401)