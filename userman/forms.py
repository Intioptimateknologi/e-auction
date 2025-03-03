from django import forms
from django.contrib.auth.models import User, Group
from django.core.validators import MaxLengthValidator, MinLengthValidator
from .models import (Users, CustomGroup,tim_lelang, bidder, dokumen_perusahaan, UserMenu, bidder_user, Users, bidder_perwakilan, admin, viewers)
from adm_lelang.models import tahapan_lelang2
from django.forms.models import inlineformset_factory
from django.utils.html import format_html
from mptt.forms import TreeNodeChoiceField
from django.conf import settings
from django.urls import get_resolver
from bootstrap_modal_forms.forms import BSModalModelForm

class CustomFileInput(forms.FileInput): 
    def render(self, name, value, attrs=None, renderer=None):
        result = []
        result.append(super().render(name, value, attrs, renderer))
        if hasattr(value, "url"):
            #attrclass = attrs['class']
            result.append(
                f'''<p class="col-sm-7">
                Presently: <a href="{value.url}">"{value}"</a>'''
            )
        return format_html("".join(result))

class AdminForm(BSModalModelForm):
    class Meta:
        model = admin
        fields = [
            "sk_pengangkatan",
            "jabatan_dalam_tim",
            "jabatan",
            "nip",
            "users",
        ]
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.fields["users"].queryset = Users.objects.all().filter(is_active=True).filter(user_type='A').exclude(id__in=admin.objects.values('users'))
        
class UsersForm(BSModalModelForm):
    masaberlaku2 = forms.DateField(
        required=False, 
        widget=forms.TextInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = Users
        fields = [
            "email",
            "username",
            "password",
            "mobile_number",
            "nama_lengkap",
            "user_type",
            "masaberlaku1",
            "masaberlaku2",
            "is_active",
            "first_login",
            "pending",
            "customGroup",
        ]
       
        widgets = {
            "masaberlaku1":forms.TextInput(attrs={'type':'date'}),
            "masaberlaku2":forms.TextInput(attrs={'type':'date'}),
       #    "customGroup":forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
       #     "email":forms.EmailInput(attrs={'required': True, }),
       #     "username":forms.TextInput(attrs={'required': True, }),
       #     "nama_lengkap":forms.TextInput(attrs={'required': True, }),
       #     "password":forms.PasswordInput(attrs={'required': True, }),
       #     "mobile_number":forms.TextInput(attrs={'required': True, }),
       #     #"user_type":forms.Select(choices=Users.UserType)
       #userman.CustomGroup
        }

    #is_active = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super(UsersForm, self).__init__(*args, **kwargs)
    #self.fields['customGroup'] = forms.ModelMultipleChoiceField(queryset=CustomGroup.objects.all(),required=False, widget=forms.CheckboxSelectMultiple)
    #my_field = forms.ModelMultipleChoiceField(queryset=MyModel.objects.all(), widget=FilteredSelectMultiple("verbose name", is_stacked=False))
    

class GroupForm(BSModalModelForm):
    class Meta:
        model = CustomGroup
        fields = [
            "name",
            "keterangan",
            "active",
        ]

class tim_lelangForm(BSModalModelForm):
    class Meta:
        model = tim_lelang
        fields = [
            "nip",
            "users",
            "jabatan",  
            "jabatan_dalam_tim",
            "sk_pengangkatan",
        ]
    def __init__(self, *args, **kwargs):
        super(tim_lelangForm, self).__init__(*args, **kwargs)
        self.fields["users"].queryset = Users.objects.all().filter(is_active=True).filter(user_type='C').exclude(id__in=tim_lelang.objects.values('users'))

class viewForm(BSModalModelForm):
    class Meta:
        model = viewers
        fields = [
            "nip",
            "users",
            "jabatan",  
            "jabatan_dalam_tim",
            "sk_pengangkatan",
        ]
    def __init__(self, *args, **kwargs):
        super(viewForm, self).__init__(*args, **kwargs)
        self.fields["users"].queryset = Users.objects.all().filter(is_active=True).filter(user_type='V').exclude(id__in=viewers.objects.values('users'))
    
class bidderForm(BSModalModelForm):
    npwp_perusahaan = forms.CharField(
        min_length=16,
        max_length=16,
        validators=[MinLengthValidator(16), MaxLengthValidator(16)],
        widget=forms.TextInput(attrs={'placeholder': '________________'}),
    )
    
    nib_perusahaan = forms.CharField(
        min_length=13,
        max_length=13,
        validators=[MinLengthValidator(13), MaxLengthValidator(13)],
        widget=forms.TextInput(attrs={'placeholder': '_____________'}),
    )
    
    class Meta:
        model = bidder
        fields = [
            "nama_perusahaan",
            "alamat_perusahaan",
            "jenis_penyelenggara",
            "telp_perusahaan",
            "npwp_perusahaan",
            "email_perusahaan",
            "nib_perusahaan",
            "active"
        ]
        widgets = {
            "alamat_perusahaan": forms.Textarea(attrs={'rows':2}),
        }

class bidder_usersForm(BSModalModelForm):
    
    class Meta:
        model = bidder_user
        fields = ["users","bidder",'active']
    def __init__(self, *args, **kwargs):
        super(bidder_usersForm, self).__init__(*args, **kwargs)
        self.fields["users"].queryset = Users.objects.all().filter(is_active=True, user_type='B')
        self.fields["bidder"].queryset = bidder.objects.all().filter(active=True)

class bidder_perwakilanForm(BSModalModelForm):

    nik_perwakilan = forms.CharField(
        min_length=16,
        max_length=16,
        validators=[MinLengthValidator(16), MaxLengthValidator(16)],
        widget=forms.TextInput(attrs={'placeholder': '________________'}),
    )

    class Meta:
        model = bidder_perwakilan
        fields = ["bidder",'nama_lengkap','nik_perwakilan','email','mobile_number','jabatan', 'ip_address', 'active','sk_pengangkatan']
    def __init__(self, *args, **kwargs):
        super(bidder_perwakilanForm, self).__init__(*args, **kwargs)
        self.fields["bidder"].queryset = bidder_user.objects.all().filter(active=True)

class bidder_perwakilanForm2(BSModalModelForm):
    class Meta:
        model = bidder_perwakilan
        fields = ["bidder",'nama_lengkap','nik_perwakilan','email','ttd','profil_peruri']
        widgets = {
            "bidder":forms.HiddenInput(),
        }

class costum_group(BSModalModelForm):
    

    class Meta:
        model = CustomGroup
        fields = ['keterangan',"name","active"]

class dokumen_perusahaanForm(forms.ModelForm):
    class Meta:
        model = dokumen_perusahaan
        fields = [
            "dokumen",
            "nama_dokumen",
            "verification_note",
            "verified_at",
            "verified",
            "verified_by",
            "id_perusahaan",
        ]

    def __init__(self, *args, **kwargs):
        super(dokumen_perusahaanForm, self).__init__(*args, **kwargs)
        self.fields["verified_by"].queryset = User.objects.all()
        self.fields["id_perusahaan"].queryset = bidder.objects.all()


urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])

def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    l = lis[0]
    if isinstance(l, URLPattern):
        yield acc + [str(l.pattern)]
    elif isinstance(l, URLResolver):
        yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
    yield from list_urls(lis[1:], acc)


class MenuForm(BSModalModelForm):  
    class Meta:  
        model = UserMenu  
        fields = [
            "name",
            "slug",
            "additional_text",
            "additional_text2",
            "additional_text3",
            "additional_text4",
            "icon_class",
            "style_class",
            "parent",
            "link",
            "enabled",
            "order",
            "tahapan",
            "menu_type"
        ]
    widgets = {
        "parent":TreeNodeChoiceField(queryset=UserMenu.objects.all(),
        level_indicator='+--'),
        "tahapan":TreeNodeChoiceField(queryset=tahapan_lelang2.objects.all(),
        level_indicator='+--'),
    }

class TahapanForm(BSModalModelForm):  
    class Meta:  
        model = tahapan_lelang2  
        fields = [
            "name",
            "judul",
            "attribute",
            "orderby",
            "parent",
        ]
    widgets = {
        "parent":TreeNodeChoiceField(queryset=tahapan_lelang2.objects.all(),
        level_indicator='+--'),
    }


