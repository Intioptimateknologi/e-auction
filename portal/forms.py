from django import forms
from . import models
from django_countries.widgets import CountrySelectWidget
from bootstrap_modal_forms.forms import BSModalModelForm


class bannerForm(BSModalModelForm):
    class Meta:
        model = models.banner
        fields = [
            "nama_banner",
            "image",
            "tag",
            "caption",
            "updated_by",
        ]
       

class aturan_lelangForm(BSModalModelForm):
    class Meta:
        model = models.aturan_lelang
        fields = [
            "jenis_kebjakan",
            "nomor",
            "file",
            "tanggal",
            "nama_kebijakan",
            "keterangan",
            "updated_by",
        ]
        widgets = {
            "tanggal": forms.DateInput(format=('%Y-%m-%d'), attrs={"class": "form-control "}),
        }

class notice_lelangForm(BSModalModelForm):
    class Meta:
        model = models.notice_lelang
        fields = [
            "tanggal",
            "nama_notice",
            "updated_by",
        ]
        widgets = {
            "tanggal": forms.DateInput(format=('%Y-%m-%d'), attrs={"class": "form-control "}),
        }


class history_lelangForm(BSModalModelForm):
    class Meta:
        model = models.history_lelang
        fields = [
            "tahun",
            "pita",
            "bandwidth",
            "penyelenggaraan",
            "keterangan",
            "updated_by",
            "pemenang",
            "image"
            
        ]
        widgets = {
            "tahun": forms.DateInput(format=('%Y-%m-%d'), attrs={"class": "form-control form-control-sm"}),
            "pita": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "bandwidth": forms.TextInput(attrs={"class": "form-control form-control-sm", "rows": 3}),
            # "penyelenggaraan": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "penyelenggaraan": forms.Select(choices=(("Jaringan Bergerak Seluler", "Jaringan Bergerak Seluler"), ("Jartaplok PS BWA","Jartaplok PS BWA")), attrs={"class": "form-control form-control-sm"}),
            "keterangan": forms.Textarea(attrs={"class": "form-control form-control-sm"}),
        }
       


class portal_blockForm(BSModalModelForm):
    class Meta:
        model = models.portal_block
        fields = [
            "tag",
            "judul",
            "content",
            "order",
            "updated_by"
        ]
        widgets = {
            "tag": forms.TextInput(attrs={"class": "form-control form-control-sm", "style": "width: 400px;"}),
            "judul": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "content": forms.Textarea(attrs={"class": "form-control form-control-sm", "rows": 3}),
            "order": forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
        }
       


class lelang_mancanegaraForm(BSModalModelForm):
    class Meta:
        model = models.lelang_mancanegara
        fields = [
            "keterangan",
            "tahun",
            "pita",
            "negara",
            "bandwidth",
            "nama_negara",
            "image"
        ]
        widgets = {
            "negara": CountrySelectWidget(),
            "tahun": forms.DateInput(format='%Y', attrs={"class": "form-control form-control-sm"}),
            "pita": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "keterangan": forms.Textarea(attrs={"class": "form-control form-control-sm"}),
            "bandwidth": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "nama_negara": forms.TextInput(attrs={"class": "form-control form-control-sm", "rows":"5"}),
            
            }


class istilah_lelangForm(BSModalModelForm):
    class Meta:
        model = models.istilah_lelang
        fields = [
            "nama_istilah",
            "penjelasan",
        ]
            
        widgets = {
            "nama_istilah": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "penjelasan": forms.TextInput(attrs={"class": "form-control form-control-sm", "row":"5"}),
        }