from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms
from . import tables
#from smra.models import undangan_smra_cca, berita_acara_lelang
#from smra.forms import undangan_smra_ccaForm
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required
from adm_lelang import utils
from django.shortcuts import render, redirect
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from userman.models import tim_lelang, bidder_perwakilan, bidder
from adm_lelang.models import auctioner_lelang, bidder_lelang, item_lelang, detail_itemlelang, jadwal_seleksi
from persiapan.models import p_dokumen, berita_acara_persiapan
#from persiapan.forms import DokumenForm,BeritaAcaraForm
from persiapan.tables import p_dokumensTable,berita_acara_persiapanTable
from django.utils import timezone
from datetime import datetime, timedelta

@login_required
def home(request):
    url = "/gabungan/management/"
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'index_gabungan.html')
        elif request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_gabungan_auctioneer.html', context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_gabungan_auctioneer.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_gabungan_bidder.html')
        elif request.user.user_type == 'C':
            # context = {}
            # user = request.user
            # auc = tim_lelang.objects.all().filter(users_id = request.user.id)
            # if (auc):
            #     context['auctioner'] = auc[0]
            #     if request.GET.get("id"):
            #         context["item_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) #bidder_lelang.objects.all().filter(bidder = bidder_id)
            #     else:
            #         context["item_lelang"] = item_lelang.objects.all()[0] #bidder_lelang.objects.all().filter(bidder = bidder_id)
            #     context['user_type'] = request.user.user_type
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_gabungan_auctioneer.html', context)    
        else:            
            return render(request, 'index_gabungan.html')
    else:
        return render(request, 'index_gabungan.html')
    
def penilaian(request):
    url = "/gabungan/penilaian/"
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'index_gabungan.html')
        elif request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_gabungan_auctioneer_penilaian.html', context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_gabungan_auctioneer_penilaian.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_gabungan_penilaian_bidder.html', context)
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
             return render(request, 'index_gabungan_auctioneer_penilaian.html', context)    
        else:            
            return render(request, 'index_gabungan.html')
    else:
        return render(request, 'index_gabungan.html')

class penentuan_parameterListView(SingleTableMixin, generic.ListView):
    model = models.penentuan_parameter
    form_class = forms.penentuan_parameterForm
    table_class = tables.penentuan_parameterTable
    template_name = 'table_p_parameter.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.penentuan_parameter.objects.all().filter(item=self.kwargs['pk'])


class penentuan_parameterCreateView(generic.CreateView):
    model = models.penentuan_parameter
    form_class = forms.penentuan_parameterForm


class penentuan_parameterDetailView(generic.DetailView):
    model = models.penentuan_parameter
    form_class = forms.penentuan_parameterForm


class penentuan_parameterUpdateView(generic.UpdateView):
    model = models.penentuan_parameter
    form_class = forms.penentuan_parameterForm
    pk_url_kwarg = "pk"


class penentuan_parameterDeleteView(generic.DeleteView):
    model = models.penentuan_parameter
    success_url = reverse_lazy("gabungan_penentuan_parameter_list")


"""class ba_gabunganListView(SingleTableMixin, generic.ListView):
    model = berita_acara_lelang 
    table_class = tables.berita_acara1
    template_name = 'table_ba_gabungan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return berita_acara_lelang.objects.all().filter(item_lelang=self.kwargs['pk'])
    
class ba_gabunganList2View(SingleTableMixin, generic.ListView):
    model = berita_acara_lelang 
    table_class = tables.berita_acara2
    template_name = 'table_ba_gabungan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return berita_acara_lelang.objects.all().filter(item_lelang=self.kwargs['pk'])


class ba_gabunganCreateView(generic.CreateView):
    model = models.ba_gabungan
    form_class = forms.ba_gabunganForm


class ba_gabunganDetailView(generic.DetailView):
    model = models.ba_gabungan
    form_class = forms.ba_gabunganForm


class ba_gabunganUpdateView(generic.UpdateView):
    model = models.ba_gabungan
    form_class = forms.ba_gabunganForm
    pk_url_kwarg = "pk"


class ba_gabunganDeleteView(generic.DeleteView):
    model = models.ba_gabungan
    success_url = reverse_lazy("gabungan_ba_gabungan_list")
"""
    

class penilaian_gabunganListView(SingleTableMixin, generic.ListView):
    model = models.penilaian_gabungan 
    form_class = forms.penilaian_gabunganForm
    table_class = tables.nilai_gabungan
    template_name = 'table_p_gabungan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.penilaian_gabungan.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])

class hasil_gabunganListView(SingleTableMixin, generic.ListView):
    model = models.hasil_gabungan 
    form_class = forms.penilaian_gabunganForm
    table_class = tables.hasil_gabungan
    template_name = 'table_p_gabungan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.hasil_gabungan.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).order_by('ranking')

#class sum_gabunganListView(SingleTableMixin, generic.ListView):
#    model = models.sum_gabungan 
#    table_class = tables.sum_gabungan_Table2
#    template_name = 'table_p_gabungan.html'
#    def get_queryset(self, **kwargs):
#        qs = super().get_queryset(**kwargs)
#        return models.sum_gabungan.objects.all().filter(item_lelang=self.kwargs['pk'])
    
#class sum_gabungan2ListView(SingleTableMixin, generic.ListView):
#    model = models.sum_gabungan 
#    table_class = tables.sum_gabungan_Table2
#    template_name = 'table_p_gabungan.html'
#    def get_queryset(self, **kwargs):
#        qs = super().get_queryset(**kwargs)
#        return models.sum_gabungan.objects.all().filter(item_lelang=self.kwargs['pk'], bidder=self.kwargs['code'])


class penilaian_gabunganCreateView(generic.CreateView):
    model = models.penilaian_gabungan
    form_class = forms.penilaian_gabunganForm


class penilaian_gabunganDetailView(generic.DetailView):
    model = models.penilaian_gabungan
    form_class = forms.penilaian_gabunganForm


class penilaian_gabunganUpdateView(generic.UpdateView):
    model = models.penilaian_gabungan
    form_class = forms.penilaian_gabunganForm
    pk_url_kwarg = "pk"


class penilaian_gabunganDeleteView(generic.DeleteView):
    model = models.penilaian_gabungan
    success_url = reverse_lazy("gabungan_penilaian_gabungan_list")

# modal
"""class undangan_gabunganCreateView(BSModalCreateView):

    template_name = 'modal_undangan.html'
    form_class = undangan_smra_ccaForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
# modal
class bagabunganCreateView(BSModalCreateView):

    template_name = 'modal_ba_gabungan.html'
    form_class = forms.BeritaAcaraForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
    
 """   
# modal
class pgabunganCreateView(BSModalCreateView):

    template_name = 'modal_p_gabungan.html'
    form_class = forms.penilaiangabunganForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}
# modal
class pparameterCreateView(BSModalCreateView):

    template_name = 'modal_p_parameter.html'
    form_class = forms.penentuanparameterForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item": self.kwargs["pk"]}

#update
"""
class undangan_gabunganUpdateView(BSModalUpdateView):
    template_name = 'modal_undangan_update.html'
    form_class = undangan_smra_ccaForm
    model = undangan_smra_cca
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
       
#update    
class bagabunganUpdateView(BSModalUpdateView):
    template_name = 'modal_ba_gabungan.html'
    form_class = forms.BeritaAcaraForm
    model = berita_acara_lelang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            'item_lelang': self.kwargs['id'],
        })

        return initial
"""
#update    
class pgabunganUpdateView(BSModalUpdateView):
    template_name = 'modal_p_gabungan.html'
    form_class = forms.penilaiangabunganForm
    model = models.penilaian_gabungan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            #'item_lelang': self.kwargs['id'],
        })

        return initial
    
#update    
class pparameterUpdateView(BSModalUpdateView):
    template_name = 'modal_p_parameter.html'
    form_class = forms.penentuanparameterForm
    model = models.penentuan_parameter
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial