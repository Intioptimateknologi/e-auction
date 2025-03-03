from django import forms
from . import models
from adm_lelang.models import item_lelang
from ckeditor.widgets import CKEditorWidget
from adm_lelang.models import bidder_lelang, auctioner_lelang,viewers_lelang, detail_itemlelang
from userman.models import bidder, tim_lelang, bidder_user,bidder_perwakilan
from bootstrap_modal_forms.forms import BSModalModelForm


class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'

class verifikasi_penawaranForm(BSModalModelForm):
    class Meta:
        model = models.penawaran
        fields = [
            "bidder",
            "item",
            "verified",
            "verified_by"
        ]
        widgets = {
            "verified_by": forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super(verifikasi_penawaranForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            undangan = models.penawaran.objects.get(pk=kwargs['initial']['id'])
            self.fields['bidder'] = forms.ModelChoiceField(
                queryset=bidder_user.objects.all().filter(id=undangan.bidder.id), 
                required=False, 
                widget=forms.Select)
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id=undangan.item.id), 
                required=False, 
                widget=forms.Select)
            self.fields['verified_by'] = forms.IntegerField(initial = self.request.user.id, 
                widget=forms.HiddenInput)

class PenawaranForm(BSModalModelForm):
    class Meta:
        model = models.penawaran
        fields = [
            "dokumen_penawaran",
            "harga",
            "blok",
            "bidder",
            "item",
            'perwakilan'
        ]
        widgets = {
            "harga": forms.NumberInput(),
            "blok": forms.NumberInput(),
            "bidder": forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super(PenawaranForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            undangan = models.penawaran.objects.get(pk=kwargs['initial']['id'])
            self.fields['bidder'] = forms.IntegerField(widget=forms.HiddenInput, initial=bidder_user.objects.all().get(users__id=self.request.user.id).id)
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id=undangan.item.id), 
                required=False, 
                widget=forms.Select)
            self.fields['perwakilan'] = forms.ModelChoiceField(
                queryset=bidder_perwakilan.objects.all().filter(bidder__users__id = self.request.user.id), 
                required=False, 
                widget=forms.Select)
        else:
            self.fields['bidder'] = forms.IntegerField(widget=forms.HiddenInput, initial=bidder_user.objects.all().get(users__id=self.request.user.id).id)
            obyek = models.obyek_seleksi_sampul2.objects.all().filter(bidder_user__users__id = self.request.user.id, item__item_lelang__id=kwargs['initial']['item'])
            o = []
            for j in obyek:
                o.append(j.item.id)
            exl = models.penawaran.objects.all().filter(bidder__users__id = self.request.user.id, item__item_lelang__id=kwargs['initial']['item'])
            e = []
            for ex in exl:
                e.append(ex.item.id)
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id__in = o).exclude(id__in=e), 
                required=False, 
                widget=forms.Select)
            self.fields['perwakilan'] = forms.ModelChoiceField(
                queryset=bidder_perwakilan.objects.all().filter(bidder__users__id = self.request.user.id), 
                required=False, 
                widget=forms.Select)

class EvaluasiPenawaranForm(BSModalModelForm):
    class Meta:
        model = models.evaluasi_penawaran
        fields = [
            "penawaran",
            "hasil",
            "catatan",
            "dokumen", 
        ]
    def __init__(self, *args, **kwargs):
        super(EvaluasiPenawaranForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            undangan = models.evaluasi_penawaran.objects.get(pk=kwargs['initial']['id'])
            self.fields['penawaran'] = forms.ModelChoiceField(
                queryset=models.penawaran.objects.all().filter(id=undangan.penawaran.id), 
                required=False, 
                widget=forms.Select)
        else:
            obyek = models.penawaran.objects.all().filter(item__item_lelang__id=kwargs['initial']['item'])
            o = []
            for j in obyek:
                o.append(j.id)
            exl = models.evaluasi_penawaran.objects.all().filter(penawaran__item__item_lelang__id=kwargs['initial']['item'])
            e = []
            for ex in exl:
                e.append(ex.penawaran.id)
            self.fields['penawaran'] = forms.ModelChoiceField(
                queryset=models.penawaran.objects.all().filter(id__in = o).exclude(id__in=e), 
                required=False, 
                widget=forms.Select)


class obyek_seleksiForm(BSModalModelForm):
    class Meta:
        model = models.obyek_seleksi_sampul2
        fields = ["item", "bidder_user", 'block']
    def __init__(self, *args, **kwargs):
        super(obyek_seleksiForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            undangan = models.obyek_seleksi_sampul2.objects.get(pk=kwargs['initial']['id'])
            self.fields['bidder_user'] = forms.ModelChoiceField(
                queryset=bidder_user.objects.all().filter(id=undangan.bidder_user.id), 
                required=False, 
                widget=forms.Select)
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(id=undangan.item.id), 
                required=False, 
                widget=forms.Select)
        else:
            bdr = bidder_lelang.objects.all().values('bidder').filter(item_lelang=kwargs['initial']['item'])
            #print(bdr)
            self.fields['bidder_user'] = forms.ModelChoiceField(
                queryset=bidder_user.objects.all().filter(id__in=bdr), 
                required=False, 
                widget=forms.Select)
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(item_lelang=kwargs['initial']['item']), 
                required=False, 
                widget=forms.Select)
