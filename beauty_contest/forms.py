from django import forms
from . import models
from bootstrap_modal_forms.forms import BSModalModelForm
from ckeditor.widgets import CKEditorWidget
#from smra.models import undangan_smra_cca
from adm_lelang.models import bidder_lelang, detail_itemlelang, item_lelang
from userman.models import bidder_user, bidder, bidder_perwakilan


class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'


class parameter_evaluasiForm(forms.ModelForm):
    class Meta:
        model = models.parameter_evaluasi
        fields = [
            "item",
            "parameter",
        ]


class dokumen_bcForm(forms.ModelForm):
    class Meta:
        model = models.dokumen_bc
        fields = [
            "item",
            "dokumen_bc",
            "bidder",
            "perwakilan"
        ]
    def __init__(self, *args, **kwargs):
        super(dokumen_bcForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            penilaian = models.dokumen_bc.objects.get(pk=kwargs['initial']['id'])
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id=penilaian.item.id, disabled=False), 
                required=False, 
                widget=forms.Select)
            self.fields['perwakilan'] = forms.ModelChoiceField(
                queryset=bidder_perwakilan.objects.all().filter(bidder__users__id = self.request.user.id), 
                required=False, 
                widget=forms.Select)
        else:
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(item_lelang__id=kwargs['initial']['item'], disabled=False), 
                required=False, 
                widget=forms.Select)
            self.fields['perwakilan'] = forms.ModelChoiceField(
                queryset=bidder_perwakilan.objects.all().filter(bidder__users__id = self.request.user.id), 
                required=False, 
                widget=forms.Select)

class parameterevaluasiForm(BSModalModelForm):
    class Meta:
        model = models.parameter_evaluasi
        fields = [
            "parameter",
            "bobot",
            "item",
        ]
        widgets = {
            "parameter": forms.Textarea(attrs={'rows':2}),
        }
    def __init__(self, *args, **kwargs):
        super(parameterevaluasiForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            penilaian = models.parameter_evaluasi.objects.get(pk=kwargs['initial']['id'])
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id=penilaian.item.id), 
                required=False, 
                widget=forms.Select)
        else:
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(item_lelang__id=kwargs['initial']['item']), 
                required=False, 
                widget=forms.Select)
        
class dokumenbcForm(BSModalModelForm):

    class Meta:
        model = models.dokumen_bc
        fields = [
            "dokumen_bc",
            "bidder",
            "item",
            "perwakilan",
            "nama_dok",
        ]
        widgets = {
            "dokumen_bc": forms.FileInput(),
        }
    def __init__(self, *args, **kwargs):
         super(dokumenbcForm, self).__init__(*args, **kwargs)
         if kwargs['initial'].get('id') is not None:
            penilaian = models.dokumen_bc.objects.get(pk=kwargs['initial']['id'])
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id=penilaian.item.id), 
                required=False, 
                widget=forms.Select)
            self.fields['perwakilan'] = forms.ModelChoiceField(
                queryset=bidder_perwakilan.objects.all().filter(bidder__users__id = self.request.user.id), 
                required=False, 
                widget=forms.Select)
         else:
            obsel = models.obyek_seleksi_bc.objects.all().filter(item__item_lelang__id=kwargs['initial']['item'], 
                bidder_user__users__id = self.request.user.id)
            item_id = []
            bidder_id = []
            for o in obsel:
                item_id.append(o.item.id)
                bidder_id.append(o.item.id)

            obsel = models.dokumen_bc.objects.all().filter(item__item_lelang__id=kwargs['initial']['item'], 
                bidder__users__id = self.request.user.id)
            exclude_item_id = []
            for o in obsel:
                exclude_item_id.append(o.item.id)

            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id__in = item_id).exclude(id__in = exclude_item_id), 
                required=False, 
                widget=forms.Select)
            bdr = bidder_user.objects.all().get(users__id = self.request.user.id)
            self.fields['bidder'] = forms.CharField(initial=bdr.id) #forms.TextInput(bdr)
            self.fields['perwakilan'] = forms.ModelChoiceField(
                queryset=bidder_perwakilan.objects.all().filter(bidder__users__id = self.request.user.id), 
                required=False, 
                widget=forms.Select)
        
class penilaianbcForm(BSModalModelForm):

    class Meta:
        model = models.penilaian_bc
        fields = [
            "penilaian",
            "bidder",
            "parameter",
            "hasil_evaluasi","keterangan",
            "item",
        ]
        widgets = {
            "penilaian": forms.NumberInput(),
            "item": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),

        }
    def __init__(self, *args, **kwargs):
        super(penilaianbcForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            penilaian = models.penilaian_bc.objects.get(pk=kwargs['initial']['id'])
            self.fields['bidder'] = forms.ModelChoiceField(
                queryset=bidder_user.objects.all().filter(id=penilaian.bidder.id), 
                required=False, 
                widget=forms.Select)
            self.fields['parameter'] = forms.ModelChoiceField(
                queryset=models.parameter_evaluasi.objects.all().filter(id=penilaian.parameter.id), 
                required=False, 
                widget=forms.Select)

class obyek_seleksibcForm(BSModalModelForm):
    class Meta:
        model = models.obyek_seleksi_bc
        fields = ["item", "bidder_user", 'block']
    def __init__(self, *args, **kwargs):
        super(obyek_seleksibcForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            undangan = models.obyek_seleksi_bc.objects.get(pk=kwargs['initial']['id'])
            self.fields['bidder_user'] = forms.ModelChoiceField(
                queryset=bidder_user.objects.all().filter(id=undangan.bidder_user.id), 
                required=False, 
                widget=forms.Select)
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id=undangan.item.id), 
                required=False, 
                widget=forms.Select)
        else:
            bdr = bidder_lelang.objects.all().values('bidder').filter(item_lelang=kwargs['initial']['item_lelang'])
            print(bdr)
            self.fields['bidder_user'] = forms.ModelChoiceField(
                queryset=bidder_user.objects.all().filter(id__in=bdr), 
                required=False, 
                widget=forms.Select)
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(item_lelang=kwargs['initial']['item_lelang']), 
                required=False, 
                widget=forms.Select)

class dokumenpersyaratan(BSModalModelForm):

    class Meta:
        model = models.format_dokumen_bc
        fields = [
            "judul",
            "nomor",
            "fotmat_doc",
            "tgl_penetapan",
            "format_xls",
            "keterangan",
            "item",
        ]
        widgets = {
            "item": forms.HiddenInput(),
            "tgl_penetapan": DateTimeInput(format=('%Y-%m-%d %H:%M:%S'))
        }
    def __init__(self, *args, **kwargs):
        super(dokumenpersyaratan, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            penilaian = models.format_dokumen_bc.objects.get(pk=kwargs['initial']['id'])
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id=penilaian.item.id), 
                required=False, 
                widget=forms.Select)
        else:
            obsel = models.obyek_seleksi_bc.objects.all().filter(item__item_lelang__id=kwargs['initial']['item'])
            item_id = []
            bidder_id = []
            for o in obsel:
                item_id.append(o.item.id)
                bidder_id.append(o.item.id)

            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id__in = item_id), 
                required=False, 
                widget=forms.Select)
            #bdr = bidder_user.objects.all().get(users__id = self.request.user.id)
            #self.fields['bidder'] = forms.CharField(initial=bdr.id) #forms.TextInput(bdr)