from django import forms
from . import models
from adm_lelang.models import bidder_lelang, auctioner_lelang,viewers_lelang
from userman.models import bidder, tim_lelang, bidder_user, viewers
from bootstrap_modal_forms.forms import BSModalModelForm
from django.db.models import F

class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'
class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'
    
class jadwalSMRAForm(BSModalModelForm):
    class Meta:
        model = models.round_schedule_smra
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


class bidderLelangForm(BSModalModelForm):
    ip_address = forms.GenericIPAddressField(error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'})
    class Meta:
        model = bidder_lelang
        fields = [
            "eligibility",
            "bidder",
            "item_lelang",
            "ip_address"
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super(bidderLelangForm, self).__init__(*args, **kwargs)
        item_lelang = kwargs['initial']['item_lelang']
        excluded_bidder_ids = bidder_lelang.objects.filter(item_lelang=item_lelang)
        self.fields["bidder"].queryset = bidder_user.objects.all().exclude(id__in=bidder_lelang.objects.values('bidder').filter(id__in=excluded_bidder_ids))


class auctionerLelangForm(BSModalModelForm):
    class Meta:
        model = auctioner_lelang
        fields = [
            "auctioner",
            "item_lelang",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super(auctionerLelangForm, self).__init__(*args, **kwargs)
        item_lelang = kwargs['initial']['item_lelang']
        excluded_tim_lelang_ids = auctioner_lelang.objects.filter(item_lelang=item_lelang)
        self.fields["auctioner"].queryset = tim_lelang.objects.all().exclude(id__in=auctioner_lelang.objects.values('auctioner').filter(id__in=excluded_tim_lelang_ids))

class viewerLelangForm(BSModalModelForm):
    class Meta:
        model = viewers_lelang
        fields = [
            "viewer",
            "item_lelang",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super(viewerLelangForm, self).__init__(*args, **kwargs)
        item_lelang = kwargs['initial']['item_lelang']
        excluded_viewers_ids = viewers_lelang.objects.filter(item_lelang=item_lelang)
        self.fields["viewer"].queryset = viewers.objects.all().exclude(id__in=viewers_lelang.objects.values('viewer').filter(id__in=excluded_viewers_ids))
# undangan
class undangan_smra_ccaForm(BSModalModelForm):
    
    class Meta:
        model = models.undangan_smra_cca
        fields = [
            "item_lelang",
            "bidder",
            "auctioneer",
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "link_teleconference",
            "keterangan",
            "link_file",
        ]
        widgets = {
            "link_teleconference": forms.Textarea(attrs={'rows':2}),
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "agenda": forms.Textarea(attrs={'rows':2}),
            "tanggal": DateTimeInput(),
            "item_lelang": forms.HiddenInput(),
        }
    

    def __init__(self, *args, **kwargs):
#        print(kwargs)
        super(undangan_smra_ccaForm, self).__init__(*args, **kwargs)
        bdr = bidder_lelang.objects.all().values('bidder').filter(item_lelang=kwargs['initial']['item_lelang'])
        print(bdr)
        self.fields['bidder'] = forms.ModelMultipleChoiceField(
            queryset=bidder.objects.all().filter(id__in=bdr), 
            required=False, 
            widget=forms.CheckboxSelectMultiple)
        auc = auctioner_lelang.objects.all().values('auctioner').filter(item_lelang=kwargs['initial']['item_lelang'])
        self.fields['auctioneer'] = forms.ModelMultipleChoiceField(
            queryset=tim_lelang.objects.all().filter(id__in=auc), 
            required=False, 
            widget=forms.CheckboxSelectMultiple)
         



# form berita acara
class BeritaAcaraForm(BSModalModelForm):
    class Meta:
        model = models.berita_acara_lelang
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