from django.views import generic
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from datetime import datetime,timedelta
from . import models
from . import forms
from . import tables
from django.db.models import Q
from django.shortcuts import render
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from adm_lelang.models import pengumuman
from administrasi.models import hasil_evaluasi
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django.shortcuts import render, redirect
from django.utils import timezone

def home(request):
    return render(request, 'index_portal.html')

def manage(request):
    return render(request, 'manage.html')

def manage_banner(request):
    return render(request, 'manage_banner.html')


# profil
class ProfilTableView(SingleTableMixin, generic.ListView):
    table_class = tables.profilTable
    model = models.profil
    template_name = "tabel_profil.html"

class BannerTableView(SingleTableMixin, generic.ListView):
    table_class = tables.BannerTable
    model = models.banner
    #queryset = models.banner.objects.all()
    paginate_by = 10
    template_name = "banner_tables.html"

class portal_blockTableView(SingleTableMixin, generic.ListView):
    table_class = tables.portal_blockTable
    model = models.portal_block
    #queryset = models.banner.objects.all()
    paginate_by = 10
    template_name = "banner_tables.html"
    
class istilah_lelangTableView(SingleTableMixin, generic.ListView):
    table_class = tables.istilah_lelangTable
    model = models.istilah_lelang
    #queryset = models.banner.objects.all()
    paginate_by = 10
    template_name = "banner_tables.html"
    
class histori_lelangTableView(SingleTableMixin, generic.ListView):
    table_class = tables.history_lelangTable
    model = models.history_lelang
    #queryset = models.banner.objects.all()
    paginate_by = 20
    template_name = "banner_tables.html"

class lelang_mancaTableView(SingleTableMixin, generic.ListView):
    table_class = tables.lelang_mancaTable
    model = models.lelang_mancanegara
    #queryset = models.banner.objects.all()
    paginate_by = 10
    template_name = "banner_tables.html"
    
class aturan_lelangTableView(SingleTableMixin, generic.ListView):
    table_class = tables.aturan_lelangTable
    model = models.aturan_lelang
    #queryset = models.banner.objects.all()
    paginate_by = 10
    template_name = "banner_tables.html"

def get_front_banner(request):
    banner = models.banner.objects.all().filter(tag='front')
    return render(request, 'banner_front.html',{'banner': banner})

def get_lelang_by_country(request):
    country = models.lelang_mancanegara.objects.all().order_by('-last_updated')
    
    tgl_skrng = datetime.now().date()
    hari_sblm = tgl_skrng - timedelta(days=31)
    hari_sesudah = tgl_skrng + timedelta(days=1)
    
    return render(request, 'lelang_country.html',{'country': country, 'tgl_skrng': tgl_skrng, 'hari_sblm': hari_sblm, 'hari_sesudah': hari_sesudah})

def get_istilah_lelang(request):
    istilah = models.istilah_lelang.objects.all()
    paginator = Paginator(istilah, 6)
    page_number = request.GET.get('page')
    istilah2 = paginator.get_page(page_number)
    return render(request, 'istilah_lelang.html',{'istilah2': istilah2})

def get_profile(request):
    # if request.user.is_authenticated:
    profile = models.portal_block.objects.all().order_by('order')
    
    return render(request, 'profil.html',{'profil': profile})
    # return render(request, 'index_portal.html') 


def get_history_lelang(request):
    history = models.history_lelang.objects.all().order_by('-last_updated')
    
    tgl_skrng = datetime.now().date()
    hari_sblm = tgl_skrng - timedelta(days=31)
    
    hari_sesudah = tgl_skrng + timedelta(days=1)
    #print(hari_sblm)
    return render(request, 'history_lelang.html',{'history': history, 'tgl_skrng': tgl_skrng, 'hari_sblm': hari_sblm,  'hari_sesudah': hari_sesudah})

def get_aturan_lelang(request):
    aturan_llng = models.aturan_lelang.objects.all().order_by('-last_updated')
    paginator = Paginator(aturan_llng, 6)
    page_number = request.GET.get('page')
    aturan_lelang_page = paginator.get_page(page_number)
    
    tgl_skrng = datetime.now().date()
    hari_sblm = tgl_skrng - timedelta(days=1)
    hari_sesudah = tgl_skrng + timedelta(days=1)
    #print(vars(aturan_lelang_page))
    return render(request, 'aturan_lelang.html',{'aturan': aturan_lelang_page, 'tgl_skrng': tgl_skrng, 'hari_sblm': hari_sblm,  'hari_sesudah': hari_sesudah})

def get_notice_lelang(request):
    notice_llng = models.notice_lelang.objects.all().order_by('-last_updated')
    paginator = Paginator(notice_llng, 3)
    page_number = request.GET.get('page')
    notice_lelang_page = paginator.get_page(page_number)
    
    #print(vars(aturan_lelang_page))
    return render(request, 'notice_lelang.html',{'notice': notice_lelang_page})


def index_istilah_lelang (request):
    istilah = models.istilah_lelang.objects.all().order_by('nama_istilah')
    search_query = request.GET.get('cari')
    if search_query:
        istilah = istilah.filter(Q(nama_istilah__icontains=search_query)| Q(penjelasan__icontains=search_query) )
        
    return render(request, 'index_istilah_lelang.html',{'istilah': istilah})

def get_pengumuman (request):
    p_umum = pengumuman.objects.all().order_by('-tgl_release')
    return render(request, 'pengumuman.html',{'p_umum': p_umum})

def get_pengumuman3 (request):
    dt = timezone.localtime()
    p_umum1 = pengumuman.objects.all().order_by('-tgl_release')
    print(p_umum1)
    tgl_skrng = datetime.now().date()
    time_release = datetime.now() - timedelta(days=0)
    hari_sblm = tgl_skrng - timedelta(days=1)
    hari_sesudah = tgl_skrng + timedelta(days=1)
    
    return render(request, 'pengumuman3.html',{'p_umum2': p_umum1, 'tgl_skrng': tgl_skrng, 'hari_sblm': hari_sblm,  'hari_sesudah': hari_sesudah, 'time_release': time_release})

def get_pengumuman2 (request):
    p_hasil_evaluasi = hasil_evaluasi.objects.all().order_by('tanggal')
    return render(request, 'pengumuman2.html',{'p_hasil_evaluasi': p_hasil_evaluasi})



class bannerListView(generic.ListView): 
    model = models.banner
    form_class = forms.bannerForm


class bannerCreateView(generic.CreateView):
    template_name = 'modal_banner.html'
    form_class = forms.bannerForm
    model = models.banner
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class bannerDetailView(generic.DetailView):
    model = models.banner
    form_class = forms.bannerForm


class bannerUpdateView(generic.UpdateView):
    model = models.banner
    form_class = forms.bannerForm
    pk_url_kwarg = "pk"


class bannerDeleteView(generic.DeleteView):
    model = models.banner
    success_url = reverse_lazy("portal_banner_list")


class aturan_lelangListView(generic.ListView):
    model = models.aturan_lelang
    form_class = forms.aturan_lelangForm


class aturan_lelangCreateView(generic.CreateView):

    template_name = 'modal_hukum.html'
    form_class = forms.aturan_lelangForm
    model = models.aturan_lelang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class aturan_lelangDetailView(generic.DetailView):
    model = models.aturan_lelang
    form_class = forms.aturan_lelangForm


class aturan_lelangUpdateView(generic.UpdateView):
    template_name = 'modal_hukum_update.html'
    model = models.aturan_lelang
    form_class = forms.aturan_lelangForm
    pk_url_kwarg = "pk"


class aturan_lelangDeleteView(generic.DeleteView):
    model = models.aturan_lelang
    success_url = reverse_lazy("portal_aturan_lelang_list")


class notice_lelangListView(generic.ListView):
    model = models.notice_lelang
    form_class = forms.notice_lelangForm


class notice_lelangCreateView(generic.CreateView):
    template_name = 'modal_notice.html'
    form_class = forms.notice_lelangForm
    model = models.notice_lelang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class notice_lelangDetailView(generic.DetailView):
    model = models.notice_lelang
    form_class = forms.notice_lelangForm


class notice_lelangUpdateView(generic.UpdateView):
    template_name = 'modal_notice_update.html'
    model = models.notice_lelang
    form_class = forms.notice_lelangForm
    pk_url_kwarg = "pk"

class notice_lelangDeleteView(generic.DeleteView):
    model = models.notice_lelang
    success_url = reverse_lazy("portal_notice_lelang_list")


class history_lelangListView(generic.ListView):
    model = models.history_lelang
    form_class = forms.history_lelangForm


class history_lelangCreateView(BSModalCreateView):
    template_name = 'modal_histori.html'
    form_class = forms.history_lelangForm
    model = models.history_lelang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class history_lelangDetailView(generic.DetailView):
    model = models.history_lelang
    form_class = forms.history_lelangForm


class history_lelangUpdateView(generic.UpdateView):
    template_name = 'modal_histori_update.html'
    model = models.history_lelang
    form_class = forms.history_lelangForm
    pk_url_kwarg = "pk"


class history_lelangDeleteView(generic.DeleteView):
    model = models.history_lelang
    success_url = reverse_lazy("portal_history_lelang_list")


class portal_blockListView(generic.ListView):
    model = models.portal_block
    form_class = forms.portal_blockForm


class portal_blockCreateView(generic.CreateView):
    template_name = 'modal_profil.html'
    model = models.portal_block
    form_class = forms.portal_blockForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')


class portal_blockDetailView(generic.DetailView):
    model = models.portal_block
    form_class = forms.portal_blockForm


class portal_blockUpdateView(generic.UpdateView):
    model = models.portal_block
    form_class = forms.portal_blockForm
    pk_url_kwarg = "pk"


class portal_blockDeleteView(generic.DeleteView):
    model = models.portal_block
    success_url = reverse_lazy("portal_portal_block_list")


class lelang_mancanegaraListView(generic.ListView):
    model = models.lelang_mancanegara
    form_class = forms.lelang_mancanegaraForm


class lelang_mancanegaraCreateView(generic.CreateView):
    template_name = 'modal_manca.html'
    form_class = forms.lelang_mancanegaraForm
    model = models.lelang_mancanegara
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class lelang_mancanegaraDetailView(generic.DetailView):
    model = models.lelang_mancanegara
    form_class = forms.lelang_mancanegaraForm


class lelang_mancanegaraUpdateView(generic.UpdateView):
    template_name = 'modal_manca_update.html'
    model = models.lelang_mancanegara
    form_class = forms.lelang_mancanegaraForm
    pk_url_kwarg = "pk"


class lelang_mancanegaraDeleteView(generic.DeleteView):
    model = models.lelang_mancanegara
    success_url = reverse_lazy("portal_lelang_mancanegara_list")


class istilah_lelangListView(generic.ListView):
    model = models.istilah_lelang
    form_class = forms.istilah_lelangForm


class istilah_lelangCreateView(generic.CreateView):
    model = models.istilah_lelang
    form_class = forms.istilah_lelangForm


class istilah_lelangDetailView(generic.DetailView):
    model = models.istilah_lelang
    form_class = forms.istilah_lelangForm


class istilah_lelangUpdateView(generic.UpdateView):
    model = models.istilah_lelang
    form_class = forms.istilah_lelangForm
    pk_url_kwarg = "pk"


class istilah_lelangDeleteView(generic.DeleteView):
    model = models.istilah_lelang
    success_url = reverse_lazy("portal_istilah_lelang_list")

class profilUpdateView(BSModalUpdateView):
    template_name = 'modal_profil_update.html'
    form_class = forms.portal_blockForm
    model = models.portal_block
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    
class istilahUpdateView(BSModalUpdateView):
    template_name = 'modal_istilah_update.html'
    form_class = forms.istilah_lelangForm
    model = models.istilah_lelang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    
class historiUpdateView(BSModalUpdateView):
    template_name = 'modal_histori_update.html'
    form_class = forms.history_lelangForm
    model = models.history_lelang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    
class lelangmancaUpdateView(BSModalUpdateView):
    template_name = 'modal_manca_update.html'
    form_class = forms.lelang_mancanegaraForm
    model = models.lelang_mancanegara
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    
class dasarhukumUpdateView(BSModalUpdateView):
    template_name = 'modal_hukum_update.html'
    form_class = forms.aturan_lelangForm
    model = models.aturan_lelang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    
class bannerslideUpdateView(BSModalUpdateView):
    template_name = 'modal_banner_update.html'
    form_class = forms.bannerForm
    model = models.banner
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial
    
class IstilahTambahView(BSModalCreateView):
    template_name = 'modal_istilah.html'
    form_class = forms.istilah_lelangForm
    model = models.istilah_lelang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')