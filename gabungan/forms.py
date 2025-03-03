from django import forms
from . import models
#from smra.models import berita_acara_lelang
from bootstrap_modal_forms.forms import BSModalModelForm
from beauty_contest.models import obyek_seleksi_bc
from smra2.models import obyek_seleksi_smra
from adm_lelang.models import detail_itemlelang, item_lelang

# form berita acara
"""class BeritaAcaraForm(BSModalModelForm):
    class Meta:
        model = berita_acara_lelang
        fields = [
            "auctioneer",
            "bidder",
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "file",
            "owner",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
        }
"""

class penentuan_parameterForm(forms.ModelForm):
    class Meta:
        model = models.penentuan_parameter
        fields = [
            "obyek_bc",
            "obyek_smra",
            "bobot",
            "item",
        ]


class ba_gabunganForm(forms.ModelForm):
    class Meta:
        model = models.ba_gabungan
        fields = [
            "dokumen_ba",
            "item_lelang",
        ]
        
class penilaian_gabunganForm(forms.ModelForm):
    class Meta:
        model = models.penilaian_gabungan
        fields = [
            "penilaian",
            "bidder",
            "parameter",
            "item",
        ]

# BootstrapModal 
class penentuanparameterForm(BSModalModelForm):
    class Meta:
        model = models.penentuan_parameter
        fields = [
            "obyek_bc",
            "obyek_smra",
            "item",
            "bobot",
            "bobot2"
        ]
        widgets = {
            "item": forms.HiddenInput()
        }
    def __init__(self, *args, **kwargs):
        super(penentuanparameterForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            penilaian = models.penentuan_parameter.objects.get(pk=kwargs['initial']['id'])
            self.fields['item'] = forms.ModelChoiceField(
                queryset=item_lelang.objects.all().filter(id=penilaian.item.id), 
                required=False, 
                widget=forms.Select)
            obsel = models.obyek_seleksi_bc.objects.all().filter(item__id=penilaian.obyek_bc.id)
            item_id = []
            bidder_id = []
            for o in obsel:
                item_id.append(o.item.id)
                bidder_id.append(o.id)
            self.fields['obyek_bc'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id__in=item_id), 
                required=False, 
                widget=forms.Select)
            print(penilaian.obyek_bc)
            obsel2 = models.obyek_seleksi_smra.objects.all().filter(item__id=penilaian.obyek_smra.id)
            item_id = []
            bidder_id = []
            for o in obsel2:
                item_id.append(o.item.id)
                bidder_id.append(o.id)
            self.fields['obyek_smra'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id__in=item_id), 
                required=False, 
                widget=forms.Select)
        else:
            obsel = models.obyek_seleksi_bc.objects.all().filter(item__item_lelang__id=kwargs['initial']['item'])
            item_id = []
            bidder_id = []
            for o in obsel:
                item_id.append(o.item.id)
                bidder_id.append(o.id)
            self.fields['obyek_bc'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id__in=item_id), 
                required=False, 
                widget=forms.Select)

            obsel2 = models.obyek_seleksi_smra.objects.all().filter(item__item_lelang__id=kwargs['initial']['item'])
            item_id = []
            bidder_id = []
            for o in obsel2:
                item_id.append(o.item.id)
                bidder_id.append(o.item.id)

            self.fields['obyek_smra'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id__in=item_id), 
                required=False, 
                widget=forms.Select)
            self.fields['item'] = forms.IntegerField(initial=kwargs['initial']['item'], widget=forms.HiddenInput)

class bagabunganForm(BSModalModelForm):
    class Meta:
        model = models.ba_gabungan
        fields = [
            "dokumen_ba",
            "item_lelang",
        ]
        widgets = {
            "dokumen_bc": forms.FileInput(),
            "item_lelang": forms.HiddenInput()
        }
        
class penilaiangabunganForm(BSModalModelForm):
    class Meta:
        model = models.penilaian_gabungan
        fields = [
            "penilaian",
            "bidder",
            "parameter",
            "item",
        ]
        widgets = {
            "dokumen_bc": forms.FileInput(),
            "item": forms.HiddenInput()
        }