from django.views import generic
from django.urls import reverse_lazy
from .models import (Users, CustomGroup,tim_lelang, bidder_user, bidder, dokumen_perusahaan, admin, viewers, bidder_list, bidder_perwakilan, UserMenu, UserMenuGroup)
from .forms import (TahapanForm, bidder_perwakilanForm2,  UsersForm,GroupForm,tim_lelangForm,bidderForm, dokumen_perusahaanForm, MenuForm, bidder_usersForm,bidder_perwakilanForm, AdminForm, viewForm, costum_group)
from .tables import bidder_usersTable, bidder_perwakilanTable,bidder_perwakilan2Table
from adm_lelang.models import tahapan_lelang2
from django.shortcuts import render
from django.db import connection, transaction
from django_tables2 import SingleTableMixin

import requests
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
import json
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.shortcuts import render,redirect, get_object_or_404
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django_renderpdf.views import PDFView
from django.utils import timezone
import datetime

@login_required
def menu_manager(request):
    #model = UserMenu
    if request.user.is_authenticated:
        p = UserMenu.objects.all()
        return render(request, "usermenu_list.html", {"object_list": p})


@login_required
def tahapan_manager(request):
    #model = UserMenu
    if request.user.is_authenticated:
        p = tahapan_lelang2.objects.all()
        return render(request, "tahapan_list.html", {"object_list": p})

def bidder_home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/bidder/index_super.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def users(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/users/index_super.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def users_add(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/users/useradd_super.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')
    
def users_add_bidder(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/users/useradd_super_bidder.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def users_edit(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/users/useredit_super.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')
    
def users_add_bidder_add(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/users/useradd_super_bidderadd.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def users_add_bidder_edit(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/users/useradd_super_bidderedit.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')
    

# def tim_lelang(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser:
#             return render(request, 'userman/tim_lelang/index_super.html')
#         else:
#             return render(request, 'index_auth.html')
#     else:
#         return render(request, 'index.html')
    
def tim_lelang_add(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/tim_lelang/tim_lelangadd_super.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')
    
def tim_lelang_edit(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/tim_lelang/tim_lelangedit_super.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def edit_bidder(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/register/edit_biodata_bidder.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def admin_biodata(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/register/admin_edit_biodata.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def lihat_biodata(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/register/admin_lihat_biodata.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def biodata_bidder(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/register/biodata_bidder.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def list_akun(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/register/list_akun.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def tambah_akun(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/register/tambah_edit_akun.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

        
def user_biodata(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/users/user_super_biodata_admin.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def user_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/users/user_super_biodata_admin_view.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')
    
def user_edit(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/users/user_super_biodata_admin_edit.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')
    
def lelang_biodata(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/users/user_tim_lelang.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

def lelang_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/users/user_tim_lelang_view.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')
    
def lelang_edit(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'userman/users/user_tim_lelang_edit.html')
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')

class dokumen_perusahaanListView(generic.ListView):
    model = dokumen_perusahaan
    form_class = dokumen_perusahaanForm


class dokumen_perusahaanCreateView(generic.CreateView):
    model = dokumen_perusahaan
    form_class = dokumen_perusahaanForm


class dokumen_perusahaanDetailView(generic.DetailView):
    model = dokumen_perusahaan
    form_class = dokumen_perusahaanForm


class dokumen_perusahaanUpdateView(generic.UpdateView):
    model = dokumen_perusahaan
    form_class = dokumen_perusahaanForm
    pk_url_kwarg = "pk"


class dokumen_perusahaanDeleteView(generic.DeleteView):
    model = dokumen_perusahaan
    success_url = reverse_lazy("userman_dokumen_perusahaan_list")


class UsersListView(generic.ListView):
    model = Users
    form_class = UsersForm


class UsersCreateView(generic.CreateView):
    model = Users
    form_class = UsersForm


class UsersDetailView(generic.DetailView):
    model = Users
    form_class = UsersForm


class UsersUpdateView(generic.UpdateView):
    model = Users
    form_class = UsersForm
    pk_url_kwarg = "pk"


class UsersDeleteView(generic.DeleteView):
    model = Users
    success_url = reverse_lazy("userman_Users_list")


class tim_lelangListView(generic.ListView):
    model = tim_lelang
    form_class = tim_lelangForm


class timLelangInline():
    form_class = tim_lelangForm
    model = tim_lelang
    template_name = "userman/tim_lelang_form.html"
    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        self.object = form.save()
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('users:list_tim_lelang')

    def formset_tim_lelang_valid(self, formset):
        tim_lelang = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for tl in tim_lelang:
            tl.users = self.object
            tl.save()

class tim_lelangCreateView(timLelangInline, generic.CreateView):
    #model = models.tim_lelang
    #form_class = forms.tim_lelangForm
    model = Users
    form_class = UsersForm
    template_name = "userman/tim_lelang_form.html"
    
    def get_context_data(self, **kwargs):
        context = super(tim_lelangCreateView, self).get_context_data(**kwargs)
        context['named_formset'] = self.get_named_formsets()
        return context
    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'tim_lelang': TimLelangFormSet(),
            }
        else:
            return {
                'tim_lelang': TimLelangFormSet(self.request.POST or None, self.request.FILES or None),
            }
    
class tim_lelangDetailView(generic.DetailView):
    model = tim_lelang
    form_class = tim_lelangForm


class tim_lelangUpdateView(generic.UpdateView):
    #model = models.tim_lelang
    #form_class = forms.tim_lelangForm
    pk_url_kwarg = "pk"
    model = Users
    form_class = UsersForm
    template_name = "userman/tim_lelang_form.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address_form'] = tim_lelangForm()
        return context
    
    def form_valid(self, form):
        # Save the person object
        users = form.save()

        # Save the address object
        lelang_form = tim_lelangForm(self.request.POST)
        if lelang_form.is_valid():
            lelang = lelang_form.save(commit=False)
            lelang.users = users
            lelang.save()

        return super().form_valid(form)


class tim_lelangDeleteView(generic.DeleteView):
    model = tim_lelang
    success_url = reverse_lazy("userman_tim_lelang_list")


def sidebar(request):
    grp = []
    #for g in request.user.groups.all():
    #    grp.append(g.id)
    user = Users.objects.get(pk=request.user.id)
    for g in user.customGroup.all():
        grp.append(g.id)

    menugroup = UserMenuGroup.objects.values_list('menu', flat=True).all().filter(group__in=grp).distinct('menu')
    menu = UserMenu.objects.all() #.filter(menu_type='A').filter(id__in=menugroup).order_by('id')
    current_url = request.headers.get("Current-URL", "/")
    rendered_content = render_to_string('sidebar_htmx.html', {'menu': menu, 'menugroup': list(menugroup), "current_url": current_url})
    return HttpResponse(rendered_content)


def listmodule(request, pk):
    menugroup = UserMenuGroup.objects.values_list('menu', flat=True).all().filter(group=pk).distinct('menu')
    menu = UserMenu.objects.all()
    rendered_content = render_to_string('module_list.html', {'menu': menu, 'menugroup': list(menugroup)})
    # return HttpResponse(rendered_content)
    return JsonResponse(rendered_content, safe=False)

def listmoduletree(request):
    form =  MenuForm()
    return render(request, "module_list_tree.html", {"form": form})


class custom_groupCreateView(BSModalCreateView):
    template_name = 'modal_custom_group.html'
    form_class = GroupForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class custom_groupUpdateView(BSModalUpdateView):
    template_name = 'modal_custom_group.html'
    form_class = GroupForm
    model = CustomGroup
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })
        return initial

class menuCreateView(BSModalCreateView):
    template_name = 'modal_menu.html'
    form_class = MenuForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class menuUpdateView(BSModalUpdateView):
    template_name = 'modal_menu.html'
    form_class = MenuForm
    model = UserMenu
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })
        return initial

class tahapanCreateView(BSModalCreateView):
    template_name = 'modal_tahapan.html'
    form_class = TahapanForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class tahapanUpdateView(BSModalUpdateView):
    template_name = 'modal_tahapan.html'
    form_class = TahapanForm
    model = tahapan_lelang2
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })
        return initial


class bidderCreateView(BSModalCreateView):
    template_name = 'modal_bidder.html'
    form_class = bidderForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class bidderUpdateView(BSModalUpdateView):
    template_name = 'modal_bidder.html'
    form_class = bidderForm
    model = bidder
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })
        return initial

class users2CreateView(BSModalCreateView):
    template_name = 'modal_users.html'
    form_class = UsersForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class users2UpdateView(BSModalUpdateView):
    template_name = 'modal_users_updated.html'
    form_class = UsersForm
    model = Users
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })
        return initial
    
class usersgroup2UpdateView(BSModalUpdateView):
    template_name = 'modal_users_group.html'
    form_class = UsersForm
    model = Users
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })
        return initial
    
class bidder_userCreateView(BSModalCreateView):
    template_name = 'modal_bidder_user.html'
    form_class = bidder_usersForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class bidder_userUpdateView(BSModalUpdateView):
    template_name = 'modal_bidder_user.html'
    form_class = bidder_usersForm
    model = bidder_user
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial

class bidder_userListView(SingleTableMixin, generic.ListView):
    model = bidder_user
    table_class = bidder_usersTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return bidder_user.objects.all().filter(users__active=True)

class bidder_perwakilanCreateView(BSModalCreateView):
    template_name = 'modal_bidder_perwakilan_create.html'
    form_class = bidder_perwakilanForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class bidder_perwakilanUpdateView(BSModalUpdateView):
    template_name = 'modal_bidder_perwakilan.html'
    form_class = bidder_perwakilanForm
    model = bidder_perwakilan
    success_message = 'Success: Data was updated.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial

class bidder_perwakilan2CreateView(BSModalCreateView):
    template_name = 'modal_bidder_perwakilan2.html'
    form_class = bidder_perwakilanForm2
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        bdr = bidder_user.objects.all().filter(users__id = self.request.user.id)
        initial = ({
            'bidder': bdr[0].id,
        })
        return initial

class bidder_perwakilan2UpdateView(BSModalUpdateView):
    template_name = 'modal_bidder_perwakilan2.html'
    form_class = bidder_perwakilanForm2
    model = bidder_perwakilan
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })

        return initial

class bidder_perwakilanListView(SingleTableMixin, generic.ListView):
    model = bidder_perwakilan
    table_class = bidder_perwakilanTable
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return bidder_perwakilan.objects.all()


class bidder_perwakilan2ListView(SingleTableMixin, generic.ListView):
    model = bidder_perwakilan
    table_class = bidder_perwakilan2Table
    template_name = 'tabel_persiapan.html'
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        try:
            bdr_user = bidder_user.objects.get(users__id = self.request.user.id)
            return bidder_perwakilan.objects.all().filter(bidder = bdr_user)
        except:
            return []


# untuk admin
class adminCreateView(BSModalCreateView):
    template_name = 'modal_admin.html'
    form_class = AdminForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class adminUpdateView(BSModalUpdateView):
    template_name = 'modal_admin_update.html'
    form_class = AdminForm
    model = admin
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })
        return initial

# untuk auctioneer
class auctioneerCreateView(BSModalCreateView):
    template_name = 'modal_auctioneer.html'
    form_class = tim_lelangForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class auctioneerUpdateView(BSModalUpdateView):
    template_name = 'modal_auctioneer_update.html'
    form_class = tim_lelangForm
    model = tim_lelang
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })
        return initial
    
# untuk viewer
class viewerCreateView(BSModalCreateView):
    template_name = 'modal_viewer.html'
    form_class = viewForm
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class viewerUpdateView(BSModalUpdateView):
    template_name = 'modal_viewer_update.html'
    form_class = viewForm
    model = viewers
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })
        return initial

# untuk costumgroup
class costumgroupCreateView(BSModalCreateView):
    template_name = 'modal_custom_group.html'
    form_class = costum_group
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')

class costumgroupUpdateView(BSModalUpdateView):
    template_name = 'modal_custom_group.html'
    form_class = costum_group
    model = CustomGroup
    success_message = 'Success: Data was created.'
    success_url = reverse_lazy('index')
    def get_initial(self):
        initial = ({
            'id': self.kwargs['pk'],
        })
        return initial

class cetakPassword(PDFView):

    template_name = 'formulir_pass_user.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = Users.objects.get(pk=kwargs['pk'])
        context = {}
        if user:
            context['tanggal']=timezone.now()
            context['user'] = user.username
            context['password'] = user.password_terlihat
            context['masa_berlaku_awal'] = user.masaberlaku1
            context['sampai']=user.masaberlaku1 + datetime.timedelta(days=1) 
            context['masa_berlaku_akhir'] = user.masaberlaku2
            context['usertype'] = user.get_user_type_display()
            context['namalengkap'] = user.nama_lengkap
            context['dibuat'] = user.created
        return context

# api delete
# delete
def api_delete_users(request, id):
    if request.user.is_authenticated:
        if request.method == 'DELETE':

            query = 'DELETE FROM userman_users WHERE id = %s;'
            params = [id]

            with connection.cursor() as cursor:
                cursor.execute(query, params)
                transaction.commit()

            return JsonResponse('Users menu group deleted successfully', safe=False)