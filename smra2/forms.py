from django import forms
from . import models
from adm_lelang.models import bidder_lelang, auctioner_lelang,viewers_lelang, detail_itemlelang
from userman.models import bidder_user
from bootstrap_modal_forms.forms import BSModalModelForm


class DateInput(forms.DateInput):
    input_type = 'date'
class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'

class price_increaseForm(BSModalModelForm):
    class Meta:
        model = models.price_increase
        fields = ["item", "detail_item", "rentang_min", "rentang_max", "kenaikan"]
        widgets = {
            "item": forms.HiddenInput(),
            "rentang_min": forms.TextInput(),
            "rentang_max": forms.TextInput(),
        }
    def __init__(self, *args, **kwargs):
        super(price_increaseForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            id = kwargs['initial'].get('id')
            obj = models.price_increase.objects.get(pk=kwargs['initial']['id'])
            self.fields['detail_item'] = forms.ModelChoiceField(
                queryset=models.detail_itemlelang.objects.all().filter(item_lelang__id=obj.item.id), 
                required=False, 
                widget=forms.Select)
        else:
            id = kwargs['initial']['item']
            self.fields['detail_item'] = forms.ModelChoiceField(
                queryset=models.detail_itemlelang.objects.all().filter(item_lelang__id=id), 
                required=False, 
                widget=forms.Select)

class obyekSeleksi2Form(BSModalModelForm):
    class Meta:
        model = detail_itemlelang
        fields = ["item_lelang","band","bandwidth", "spectrum_cap","max_block","harga_minimal", "urutan","disabled"]
        widgets = {
            "item_lelang": forms.HiddenInput(),
        }

class obyek_seleksiForm(BSModalModelForm):
    class Meta:
        model = models.obyek_seleksi_smra
        fields = ["item", "bidder_user","ipaddress", "is_block_ip","blok_awal"]

    def __init__(self, *args, **kwargs):
        super(obyek_seleksiForm, self).__init__(*args, **kwargs)
                
        if kwargs['initial'].get('id') is not None:
            undangan = models.obyek_seleksi_smra.objects.get(pk=kwargs['initial']['id'])
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
            #print(bdr)

            # ori
            self.fields['bidder_user'] = forms.ModelChoiceField(
                queryset=bidder_user.objects.all().filter(id__in=bdr), 
                required=False, 
                disabled=True,
                widget=forms.Select)
            self.fields['item'] = forms.ModelChoiceField(
                queryset=detail_itemlelang.objects.all().filter(item_lelang=kwargs['initial']['item_lelang'], disabled=False), 
                required=False, 
                widget=forms.Select)

class bidSMRA2(BSModalModelForm):

    class Meta:
        model = models.round_smra2
        fields = [
            "id",
            "price",
            "block",
            "round",
            "item",
            "bidder",
            "round",
        ]
        widgets = {
            "round": forms.HiddenInput(),
            "item": forms.HiddenInput(),
            "bidder": forms.HiddenInput(),
        }

class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'
class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'
    
class jadwalSMRAForm(BSModalModelForm):
    class Meta:
        model = models.round_schedule_smra2
        fields = [
            "hari",
            "mulai",
            "selesai",
            "item",
        ]
        widgets = {
            "item": forms.HiddenInput(),
            "mulai": forms.TimeInput(attrs={'type': 'time'},format='%H:%M'),
            "selesai": forms.TimeInput(attrs={'type': 'time'},format='%H:%M')
        }