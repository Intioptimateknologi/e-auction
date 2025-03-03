from . import models
from django import forms
from adm_lelang.models import bidder_lelang, auctioner_lelang
from persiapan.models import daftar_hadir
from userman.models import bidder, tim_lelang, Users, bidder_user, bidder_perwakilan
from bootstrap_modal_forms.forms import BSModalModelForm
from ckeditor.widgets import CKEditorWidget
import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'

# form dokumen  
class DokumenForm(BSModalModelForm):
    class Meta:
        model = models.p_dokumen
        fields = [
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "keterangan",
            "link_teleconference",
            "file",
            "bidder",
            "auctioneer",
            "item_lelang",
            "diubah_oleh",
            "tahapan",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "tempat": forms.Textarea(attrs={'rows':2}),
            "agenda": forms.Textarea(attrs={'rows':2}),
            "tanggal": DateInput(format=('%Y-%m-%d')),
            "tahapan": forms.HiddenInput(),
            "link_teleconference": forms.Textarea(attrs={'rows':2}),
        }
    def __init__(self, *args, **kwargs):
#        print(kwargs)
        super(DokumenForm, self).__init__(*args, **kwargs)
        bdr = bidder_lelang.objects.all().values('bidder').filter(item_lelang=kwargs['initial']['item_lelang'])
        #print(bdr)
        self.fields['bidder'] = forms.ModelMultipleChoiceField(
            queryset=bidder.objects.all().filter(id__in=bdr), 
            required=False, 
            widget=forms.CheckboxSelectMultiple)
        auc = auctioner_lelang.objects.all().values('auctioner').filter(item_lelang=kwargs['initial']['item_lelang'])
        self.fields['auctioneer'] = forms.ModelMultipleChoiceField(
            queryset=tim_lelang.objects.all().filter(id__in=auc), 
            required=False, 
            widget=forms.CheckboxSelectMultiple)

# form penyusunan jawaban
class PenyusunanJawabanForm(BSModalModelForm):
    class Meta:
        model = models.penyusunan_jawaban
        fields = [
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "keterangan",
            "link_teleconference",
            "file",
            "bidder",
            "auctioneer",
            "item_lelang",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "tempat": forms.Textarea(attrs={'rows':2}),
            "agenda": forms.Textarea(attrs={'rows':2}),
            "link_teleconference": forms.Textarea(attrs={'rows':2}),
        }

# form aanwizing
class AanwizinForm(BSModalModelForm):
    class Meta:
        model = models.aanwizing
        fields = [
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "keterangan",
            "link_teleconference",
            "file",
            "bidder",
            "auctioneer",
            "item_lelang"
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "tempat": forms.Textarea(attrs={'rows':2}),
            "agenda": forms.Textarea(attrs={'rows':2}),
            "link_teleconference": forms.Textarea(attrs={'rows':2}),
        }

# form simulasi
class SimulasiForm(BSModalModelForm):
    class Meta:
        model = models.simulasi
        fields = [
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "keterangan",
            "link_teleconference",
            "file",
            "bidder",
            "auctioneer",
            "item_lelang"
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "tempat": forms.Textarea(attrs={'rows':2}),
            "agenda": forms.Textarea(attrs={'rows':2}),
            "link_teleconference": forms.Textarea(attrs={'rows':2}),
        }

# form persiapan addendum
class PersiapanAddendumForm(BSModalModelForm):
    class Meta:
        model = models.p_addendum
        fields = [
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "file",
            "item_lelang"
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "tempat": forms.Textarea(attrs={'rows':2}),
            "agenda": forms.Textarea(attrs={'rows':2}),
            "link_teleconference": forms.Textarea(attrs={'rows':2}),
            "tanggal": DateInput(format=('%Y-%m-%d')),
        }

# form dokumen_seleksi
class DokumenSeleksiForm(BSModalModelForm):
    class Meta:
        model = models.dokumen_seleksi
        fields = [
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "file",
            "item_lelang",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
        }

# form daftar_hadir
# form dokumen_seleksi
class DaftarHadirForm(BSModalModelForm):
    class Meta:
        model = models.daftar_hadir
        fields = [
            "item_lelang",
            "bidder_perwakilan",
            "tgl_kehadiran",
            "tahapan",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            # "tahapan": forms.HiddenInput(),
            "tgl_kehadiran": forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'min': datetime.date.today().isoformat(),
                }
            ),
        }
    def __init__(self, *args, **kwargs):
        super(DaftarHadirForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            bdr = models.daftar_hadir.objects.get(pk=kwargs['initial'].get('id'))
            perwakilan = bidder_perwakilan.objects.all().filter(id = bdr.bidder_perwakilan.id)
            self.fields['bidder_perwakilan'].queryset = perwakilan
        else:
            item_lelang = kwargs['initial']['item_lelang']
            tahapan = kwargs['initial']['tahapan']
            bidders_lelang = models.bidder_lelang.objects.filter(item_lelang=item_lelang)
            current_date = datetime.date.today().strftime('%Y-%m-%d')
            bidder_ids = [bidder.bidder.id for bidder in bidders_lelang]
            perwakilan = models.bidder_perwakilan.objects.filter(bidder__in=bidder_ids)
            # perwakilan = models.bidder_perwakilan.objects.filter(bidder__in=bidder_ids).exclude(id__in=daftar_hadir.objects.values('bidder_perwakilan').filter(tgl_kehadiran=current_date).filter(tahapan=tahapan))
            # perwakilan = models.bidder_perwakilan.objects.filter(bidder__in=bidder_ids).exclude(id__in=daftar_hadir.objects.values('bidder_perwakilan').filter(tahapan=tahapan))
            self.fields['bidder_perwakilan'].queryset = perwakilan
        

# form persiapan pertanyaan
class PertanyaanForm(BSModalModelForm):
    class Meta:
        model = models.p_pertanyaan
        fields = [
            "item_lelang",
            "bidder",
            "file_word",
            "file_pdf",
            "file_excel",
            "perwakilan",
            
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "bidder": forms.HiddenInput(),
            "pertanyaan": forms.Textarea(attrs={'rows':2}),
        }
    def __init__(self, *args, **kwargs):
#        print(kwargs)
        super(PertanyaanForm, self).__init__(*args, **kwargs)
        userid  = self.request.user.id
        if kwargs['initial'].get('id') is not None:
            bdr = models.p_pertanyaan.objects.get(pk=kwargs['initial'].get('id'))
            perwakilan = bidder_perwakilan.objects.all().filter(bidder = bdr.bidder)
            self.fields['perwakilan'] = forms.ModelChoiceField(queryset=perwakilan)
        else:
            bdr = bidder_user.objects.get(users__id = userid)
            perwakilan = bidder_perwakilan.objects.all().filter(bidder = bdr)
            self.fields['perwakilan'] = forms.ModelChoiceField(queryset=perwakilan)
            self.fields['bidder'] = forms.IntegerField(widget=forms.HiddenInput, initial=bdr.id)

# form berita acara
class BeritaAcaraForm(BSModalModelForm):
    class Meta:
        model = models.berita_acara_persiapan
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
            "diubah_oleh",
            "tahapan",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "tanggal": DateInput(format=('%Y-%m-%d')),
            "tahapan": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
        }
    def __init__(self, *args, **kwargs):
#        print(kwargs)
        super(BeritaAcaraForm, self).__init__(*args, **kwargs)
        bdr = bidder_lelang.objects.all().values('bidder').filter(item_lelang=kwargs['initial']['item_lelang'])
        self.fields['bidder'] = forms.ModelMultipleChoiceField(
            queryset=bidder.objects.all().filter(id__in=bdr), 
            required=False, 
            widget=forms.CheckboxSelectMultiple)
        auc = auctioner_lelang.objects.all().values('auctioner').filter(item_lelang=kwargs['initial']['item_lelang'])
        self.fields['auctioneer'] = forms.ModelMultipleChoiceField(
            queryset=tim_lelang.objects.all().filter(id__in=auc), 
            required=False, 
            widget=forms.CheckboxSelectMultiple)

class PengambilanDokumenSeleksiForm(BSModalModelForm):
    class Meta:
        model = models.pengambilan_dokumen_seleksi
        fields = [
            "bidder_perwakilan",
            "dokumen_seleksi"
        ]
    def __init__(self, *args, **kwargs):
#        print(kwargs)
        super(PengambilanDokumenSeleksiForm, self).__init__(*args, **kwargs)
        self.fields['bidder_perwakilan'] = forms.ModelMultipleChoiceField(
            queryset= bidder_perwakilan.objects.all().filter(bidder=kwargs['initial']['bdr']), 
            required=False, 
            widget=forms.Select)

class PengambilanAddendumDokumenSeleksiForm(BSModalModelForm):
    class Meta:
        model = models.pengambilan_dokumen_addendum
        fields = [
            "bidder_perwakilan",
            "dokumen_addendum"
        ]
    def __init__(self, *args, **kwargs):
#        print(kwargs)
        super(PengambilanAddendumDokumenSeleksiForm, self).__init__(*args, **kwargs)
        self.fields['bidder_perwakilan'] = forms.ModelMultipleChoiceField(
            queryset= bidder_perwakilan.objects.all().filter(bidder=kwargs['initial']['bdr']), 
            required=False, 
            widget=forms.Select)
#        self.fields["dokumen_seleksi"] = kwargs['initial']['id']
