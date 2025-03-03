from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms
from . import tables
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
#from smra.models import undangan_smra_cca
#from smra.forms import undangan_smra_ccaForm
from rencana_seleksi.models import jadwal_seleksinya, rencana_seleksinya
from rencana_seleksi.forms import RencanaSeleksiForm
from adm_lelang.models import item_lelang, auctioner_lelang, bidder_lelang, jadwal_seleksi, detail_itemlelang
from userman.models import tim_lelang, bidder_perwakilan, bidder, bidder_user, Users
from django_tables2 import SingleTableMixin,MultiTableMixin
from django_filters.views import FilterView
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django.utils import timezone
from adm_lelang import utils
from datetime import datetime, timedelta


@login_required
def home(request):
    url = "/beauty_contest/management/"
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_bc.html',context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_bc_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_bc_auctioneer.html', context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'index_bc_auctioneer.html', context)
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')            
    else:
        # return render(request, 'index_bc.html')
        return render(request, 'new_index/konten/portal_user/portal_user_viewer.html') 

@login_required
def penilaian(request):
    url = "/beauty_contest/penilaian/"
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'penilaian_bc_auctioner.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'penilaian_bc_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'penilaian_bc_auctioner.html', context)
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'penilaian_bc_auctioner.html', context)  
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')            
    else:
        return render(request, 'index_bc.html')


@login_required
def penawaran(request):
    url = "/beauty_contest/penawaran/"
    if request.user.is_authenticated:
        if request.user.user_type == 'A':
            context = utils.get_judul_context_admin(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'penawaran_bc_auctioner.html', context)
        elif request.user.user_type == 'B':
            context = utils.get_judul_context_bidder(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'penawaran_bc_bidder.html', context)
        elif request.user.user_type == 'C':
            context = utils.get_judul_context_auctioneer(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'penawaran_bc_auctioner.html', context) 
        elif request.user.user_type == 'V':
            context = utils.get_judul_context_viewers(request)
            tabs = utils.get_tab_context(request,url, context["item_lelang"])
            context.update(tabs)
            return render(request, 'penawaran_bc_auctioner.html', context) 
        else:
            return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')                
    else:
        return render(request, 'index_bc.html')


class kriteria_evaluasiListView(SingleTableMixin, generic.ListView):
    model = models.parameter_evaluasi
    table_class = tables.kriteria_evaluasi_Table
    template_name = 'table_kriteria_evaluasi.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.parameter_evaluasi.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])
    
class kriteria_evaluasibcGroupView(MultiTableMixin, generic.ListView):
    model = models.parameter_evaluasi
    template_name = 'kriteria_evaluasi_group.html'
    #table_class = tables.obyek_seleksi_groupTable
    def get_tables(self):
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk']).order_by('id')
        tbls = []
        for i in item_llg:
            tbls.append(tables.kriteria_evaluasi_Table(models.parameter_evaluasi.objects.all().filter(item=i)))

        return tbls

    def get_context_data(self, **kwargs):
        context = super(kriteria_evaluasibcGroupView, self).get_context_data(**kwargs)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk']).order_by('id')
        tabs = []
        for i in item_llg:
            tabs.append(i)
        context['tabs'] = tabs
        return context

class input_penilaianListView(SingleTableMixin, generic.ListView):
    model = models.penilaian_bc
    table_class = tables.input_penilaian_Table
    template_name = 'table_input_penilaian.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.penilaian_bc.objects.all().filter(item=self.kwargs['pk'])
    
class input_penilaianListView2(SingleTableMixin, generic.ListView):
    model = models.penilaian_bc
    table_class = tables.input_penilaian_Table2
    template_name = 'table_input_penilaian.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.penilaian_bc.objects.all().filter(item=self.kwargs['pk'])
    

class input_penilaianGroupView(MultiTableMixin, generic.ListView):
    model = models.penilaian_bc
    template_name = 'tabs_penilaian_bc.html'
    table_class = tables.obyek_seleksi_groupTable
    tables = []
    #def get_tables(self):
    #    bidder = models.penilaian_bc.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).distinct("bidder")
    #    tbls = []
    #    for b in bidder:
    #        item = models.penilaian_bc.objects.all().filter(bidder=b.bidder,item__item_lelang__id=b.item.item_lelang.id).distinct("item").order_by('item')
    #        for i in item:
    #            tbls.append(tables.input_penilaian_Table(models.penilaian_bc.objects.all().filter(item=i.item, bidder=b.bidder).order_by('item')))#

    #    return tbls

    def get_context_data(self, **kwargs):
        context = super(input_penilaianGroupView, self).get_context_data(**kwargs)
        bidder = models.penilaian_bc.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).distinct("bidder").order_by('bidder')
        tabs = []
        for b in bidder:
            bdr = []
            item = models.penilaian_bc.objects.all().filter(bidder=b.bidder,item__item_lelang__id=b.item.item_lelang.id).distinct("item").order_by('item')
            for i in item:
#                bdr.append(i.item)
                table = tables.input_penilaian_Table(models.penilaian_bc.objects.all().filter(item=i.item, bidder=b.bidder).order_by('item'))
                bdr.append({"i":i, "t": table})
            tabs.append({'b': b, 'i':bdr})
        context['tabs'] = tabs
        print(tabs)
        return context


class sum_penilaianListView(SingleTableMixin, generic.ListView):
    model = models.sum_penilaian
    table_class = tables.sum_penilaian_Table2
    template_name = 'table_input_penilaian.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.sum_penilaian.objects.all().filter(item=self.kwargs['pk']).order_by('-sum')
    
class sum_penilaianListView2(SingleTableMixin, generic.ListView):
    model = models.sum_penilaian
    table_class = tables.sum_penilaian_Table2
    template_name = 'table_input_penilaian.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return models.sum_penilaian.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).order_by('-sum')
    
class hasilListView(MultiTableMixin, generic.ListView):
    model = models.hasil_beauty_contest
    table_class = tables.hasil_Table2
    template_name = 'hasil_bc_tables.html'
    tables = []
    def get_tables(self):
        item_llg = models.hasil_beauty_contest.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).distinct("item")
        tbls = []
        for i in item_llg:
            if self.request.user.user_type =='B':
                bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)
                table = tables.hasil_Table2(models.hasil_beauty_contest.objects.all().filter(item=i.item, bidder=bdr[0]).order_by('ranking'))
                tbls.append(table)
            else:
                sum_penawaran = detail_itemlelang.objects.get(id=i.item.id)
                max_block = sum_penawaran.max_block
                table = tables.hasil_Table2(models.hasil_beauty_contest.objects.all().filter(item=i.item).order_by('ranking')[:max_block])
                tbls.append(table)
        return tbls

    def get_context_data(self, **kwargs):
        context = super(hasilListView, self).get_context_data(**kwargs)
        item_llg = models.hasil_beauty_contest.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).distinct("item")
        tabs = []
        for i in item_llg:
            tabs.append(i)
        context['tabs'] = tabs
        return context

    #def get_queryset(self, **kwargs):
    #    qs = super().get_queryset(**kwargs)
    #    sum_penawaran = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk'])
    #    max_block = sum_penawaran.max_block

    #    return models.hasil_beauty_contest.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).order_by('-penilaian')[:max_block]
# crud
class dokumen_bcListView(SingleTableMixin, generic.ListView):
    model = models.dokumen_bc
    form_class = forms.dokumen_bcForm
    table_class = tables.dokumen_beauty_content_Table
    template_name = 'table_dokumen_beauty.html'
    def get_table_class(self):
        if self.request.user.user_type =='B':
            return tables.dokumen_beauty_content_Table
        else:
            return tables.dokumen_beauty_content_Table2

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type=='B':
            bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)
            return models.dokumen_bc.objects.all().filter(bidder = bdr[0], item__item_lelang__id=self.kwargs['pk'])
        else:
            return models.dokumen_bc.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])
        #return models.dokumen_bc.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])

# viewOnly
class dokumen_bcListView2(SingleTableMixin, generic.ListView):
    model = models.dokumen_bc
    table_class = tables.dokumen_beauty_content_Table2
    template_name = 'table_dokumen_beauty.html'
    def get_table_class(self):
        if self.request.user.user_type =='B':
            return tables.dokumen_beauty_content_Table2
        else:
            return tables.dokumen_beauty_content_Table2

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.user_type=='B':
            bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)
            return models.dokumen_bc.objects.all().filter(bidder = bdr[0], item__item_lelang__id=self.kwargs['pk'])
        else:
            return models.dokumen_bc.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])
        #return models.dokumen_bc.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])

# crud
class dokumen_persyaratanListView(SingleTableMixin, generic.ListView):
    model = models.format_dokumen_bc
    form_class = forms.dokumen_bcForm
    table_class = tables.dokumen_persyaratan_Table
    template_name = 'table_dokumen_beauty.html'
    # def get_table_class(self):
    #     if self.request.user.user_type =='B':
    #         return tables.dokumen_persyaratan_Table2
    #     else:
    #         return tables.dokumen_persyaratan_Table

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        # if self.request.user.user_type == 'B':
        #          bdr = Users.objects.all().filter(id = self.request.user.id)
        #          print(bdr)
        #          return models.format_dokumen_bc.objects.all().filter(dibuat_oleh = bdr[0], item__item_lelang__id=self.kwargs['pk'])
        # else:
        #         return models.format_dokumen_bc.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])
        return models.format_dokumen_bc.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).order_by('-last_updated')

# viewOnly
class dokumen_persyaratanListView2(SingleTableMixin, generic.ListView):
    model = models.format_dokumen_bc
    table_class = tables.dokumen_persyaratan2_Table
    template_name = 'table_dokumen_beauty.html'
    # def get_table_class(self):
    #     if self.request.user.user_type =='B':
    #         return tables.dokumen_persyaratan_Table
    #     else:
    #         return tables.dokumen_persyaratan_Table2

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        # if self.request.user.user_type=='B':
        #     bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)
        #     return models.dokumen_bc.objects.all().filter(bidder = bdr[0], item__item_lelang__id=self.kwargs['pk'])
        # else:
        #     return models.dokumen_bc.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])
        return models.format_dokumen_bc.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).order_by('-last_updated')
# viewOnly
class dokumen_persyaratanListView3(SingleTableMixin, generic.ListView):
    model = models.dokumen_bc
    table_class = tables.dokumen_persyaratan3_Table
    template_name = 'table_dokumen_beauty.html'
    # def get_table_class(self):
    #     if self.request.user.user_type =='B':
    #         return tables.dokumen_persyaratan_Table
    #     else:
    #         return tables.dokumen_persyaratan_Table2

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
    #     if self.request.user.user_type=='B':
    #         bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)
    #         return models.dokumen_bc.objects.all().filter(bidder = bdr[0], item__item_lelang__id=self.kwargs['pk'])
    #     else:
    #         return models.dokumen_bc.objects.all().filter(item__item_lelang__id=self.kwargs['pk'])
        return models.dokumen_bc.objects.all().filter(item__item_lelang__id=self.kwargs['pk']).order_by('-last_updated')

# modal
class parameterevaluasiCreateView(BSModalCreateView):

    template_name = 'modal_kriteria_evaluasi.html'
    form_class = forms.parameterevaluasiForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item": self.kwargs["pk"]}
# modal
class dokumenbcCreateView(BSModalCreateView):

    template_name = 'modal_dokumen_beauty.html'
    form_class = forms.dokumenbcForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item": self.kwargs["pk"]}

# modal Dokumen Persyaratan
class dokumenpersyaratanCreateView(BSModalCreateView):

    template_name = 'modal_persyaratan_dok.html'
    form_class = forms.dokumenpersyaratan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item": self.kwargs["pk"]}
# modal
# modal Update
class dokumenpersyaratanUpdateView(BSModalUpdateView):
    template_name = 'modal_persyaratan_dok.html'
    form_class = forms.dokumenpersyaratan
    model = models.format_dokumen_bc
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            # 'item_lelang': self.kwargs['pk'],
        })

        return initial
 #modal   
class penilaianbcreateView(BSModalCreateView):

    template_name = 'modal_input_penilaian.html'
    form_class = forms.penilaianbcForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        return {"item": self.kwargs["pk"]}
# modal
class penilaianbUpdateView(BSModalUpdateView):
    template_name = 'modal_input_penilaian.html'
    form_class = forms.penilaianbcForm
    model = models.penilaian_bc
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
            # 'item_lelang': self.kwargs['pk'],
        })

        return initial
    
#update    
class parameterevaluasiUpdateView(BSModalUpdateView):
    template_name = 'modal_kriteria_evaluasi.html'
    form_class = forms.parameterevaluasiForm
    model = models.parameter_evaluasi
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial

#update    
class dokumenbcUpdateView(BSModalUpdateView):
    template_name = 'modal_dokumen_beauty_update.html'
    form_class = forms.dokumenbcForm
    model = models.dokumen_bc
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })
        return initial


class obyek_seleksibcGroupView(MultiTableMixin, generic.ListView):
    model = models.obyek_seleksi_bc
    template_name = 'obyek_seleksi_group.html'
    #table_class = tables.obyek_seleksi_groupTable
    def get_tables(self):
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk']).order_by('id')
        tbls = []
        for i in item_llg:
            tbls.append(tables.obyek_seleksiTable(models.obyek_seleksi_bc.objects.all().filter(item=i)))

        return tbls

    def get_context_data(self, **kwargs):
        context = super(obyek_seleksibcGroupView, self).get_context_data(**kwargs)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang__id=self.kwargs['pk']).order_by('id')
        tabs = []
        for i in item_llg:
            tabs.append(i)
        context['tabs'] = tabs
        return context

class obyek_seleksibcView(SingleTableMixin, generic.ListView):
    model = models.obyek_seleksi_bc
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
            obj =  models.obyek_seleksi_bc.objects.all().filter(bidder_user = bdr_user, item__item_lelang=self.kwargs['pk'])
        else:
            obj =  models.obyek_seleksi_bc.objects.all().filter(item__item_lelang=self.kwargs['pk'])
        return obj

class obyek_seleksibcCreateView(BSModalCreateView):
    template_name = 'modal_obyek_seleksi_bc.html'
    form_class = forms.obyek_seleksibcForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')

    def get_initial(self):
        return {"item_lelang": self.kwargs["pk"]}

class obyek_seleksibcUpdateView(BSModalUpdateView):
    template_name = 'modal_obyek_seleksi_bc.html'
    form_class = forms.obyek_seleksibcForm
    model = models.obyek_seleksi_bc
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')

    def get_initial(self):
        return {"id": self.kwargs["pk"]}