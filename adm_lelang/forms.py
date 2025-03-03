from django import forms
from adm_lelang.models import item_lelang
from . import models
from bootstrap_modal_forms.forms import BSModalModelForm
from ckeditor.widgets import CKEditorWidget
from mptt.forms import TreeNodeChoiceField
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'

class itemLelangForm(BSModalModelForm):
    class Meta:
        model = models.item_lelang
        fields = [
            "id",
            "tayang",
            "nama_lelang",
            "keterangan",
            "tahun"
        ]
        widgets = {
            "nama_lelang": forms.Textarea(attrs={'rows':2}),
            "keterangan": forms.Textarea(attrs={'rows':4})
        }


class pengumumanForm(BSModalModelForm):
    class Meta:
        model = models.pengumuman
        fields = [
            "nomor", "judul", "pengumuman","item_lelang","dokumen","tgl_release","tahapan","image"]
        widgets = {
            "pengumuman": forms.Textarea(attrs={'rows':4}),
            "item_lelang": forms.HiddenInput(),
            "tahapan": forms.HiddenInput(),
            #"dokumen": forms.FileInput(),
            "tgl_release": DateInput(format=('%Y-%m-%d')),

        }

class dasarHukumForm(BSModalModelForm):

    class Meta:
        model = models.dasar_hukum
        fields = ["item_lelang","nomor", "judul", "tanggal", "keterangan", "attachment",]
        widgets = {
            "judul": forms.Textarea(attrs={'rows':2}),
            "keterangan": forms.Textarea(attrs={'rows':4}),
            "attachment": forms.FileInput(),
            "tanggal": DateInput(format=('%Y-%m-%d')),
            "item_lelang": forms.HiddenInput()
        }

class persyaratanLelangForm(BSModalModelForm):
    dokumen = forms.Field(widget=forms.FileInput, required=False)
    class Meta:
        model = models.persyaratan_lelang
        fields = ["item_lelang","no_urut", "keterangan","persyaratan","dokumen"]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "persyaratan": forms.Textarea(attrs={'rows':2}),
            "dokumen": forms.FileInput(),
        }

class detail_itemlelangForm(BSModalModelForm):
    class Meta:
        model = models.detail_itemlelang
        fields = [
            "id",
            'urutan',
            "teknologi",
            "band",
            "rentang_frekuensi",
            "item_lelang",
            "penyelenggaraan",
            "bandwidth",
            "cakupan",
            "keterangan",
            # 
        ]
        widgets = {
            "harga_minimal": forms.NumberInput(),
            "item_lelang": forms.HiddenInput()
        }

    # def __init__(self, *args, **kwargs):
    #     super(detail_itemlelangForm, self).__init__(*args, **kwargs)
    #     self.fields["item_lelang"].queryset = item_lelang.objects.all()

class item_lelangForm(BSModalModelForm):
    class Meta:
        model = models.item_lelang
        fields = [
            "tayang",
            "nama_lelang",
            "keterangan",
        ]
        widgets = {
            "nama_lelang": forms.Textarea(attrs={'rows':2}),
            "keterangan": forms.Textarea(attrs={'rows':4})
        }

class bidder_lelangForm(forms.ModelForm):
    #ip_address = forms.GenericIPAddressField( )
    class Meta:
        model = models.bidder_lelang
        fields = [
            "bidder",
            "item_lelang",
            "eligibility",
            "ip_address"
        ]

class jadwal_seleksiForm(BSModalModelForm):
    tahap=TreeNodeChoiceField(queryset=models.tahapan_lelang2.objects.all(),
                level_indicator='+--'),
    class Meta:
        model = models.jadwal_seleksi
        fields = [
            "tahap",
            "tanggal_awal",
            "tanggal_akhir",
            "item_lelang",
            "perubahan"
        ]
        widgets = {
            "tanggal_awal": DateTimeInput(format=('%Y-%m-%d %H:%M')),
            "tanggal_akhir": DateTimeInput(format=('%Y-%m-%d %H:%M')),
            "item_lelang": forms.HiddenInput(),
        }
    # def __init__(self, *args, **kwargs):
    #     super(jadwal_seleksiForm, self).__init__(*args, **kwargs)
    #     self.fields["jadwal_seleksi"].queryset = item_lelang.objects.all()

class alamatPanitiaForm(BSModalModelForm):
   
    class Meta:
        model = models.alamat_panitia
        fields = [
            # "cq",
            "alamat",
            "kota",
            "kodepos",
            "provinsi",
            "status",
            "keterangan",
            "telp",
            "email",
            "item_lelang"
        ]
        widgets = {
            "alamat": forms.Textarea(attrs={'rows':2}),
            "item_lelang": forms.HiddenInput()
        }

class dasar_hukumForm(forms.ModelForm):
    class Meta:
        model = models.dasar_hukum
        fields = [
            "judul",
            "attachment",
        ]

class penanggung_jawabForm(BSModalModelForm):
    class Meta:
        model = models.penangung_jawab_seleksi
        fields = [
            "item_lelang",
            "nama",
            "nip",
            "tanggung_jawab",
            "tgl_mulai",
            "tgl_akhir",
            "status",
            "keterangan",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "tgl_mulai": DateInput(format=('%Y-%m-%d')),
            "tgl_akhir": DateInput(format=('%Y-%m-%d')),
        }

class template_berita_acaraForm(BSModalModelForm):
    class Meta:
        model = models.template_berita_acara
        fields = [
            "nama_template", "keterangan_template","template_code_menu","template_code_sub","dokumen",]
        widgets = {
            "item_lelang": forms.HiddenInput(),
        }

class UndanganForm(BSModalModelForm):
    class Meta:
        model = models.undangan
        fields = [
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "keterangan",
            "link_teleconference",
            "file",
            "bidder_user",
            "auctioneer",
            "item_lelang",
            "viewer",
            "tahapan",
            "waktu_awal",
            "waktu_akhir",
            
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "tempat": forms.TextInput(attrs={'rows':2}),
            "agenda": forms.Textarea(attrs={'rows':2}),
            "tanggal": DateInput(format=('%Y-%m-%d')),
            "waktu_akhir": DateTimeInput(format=('%Y-%m-%d %H:%M')),
            "waktu_awal": DateTimeInput(format=('%Y-%m-%d %H:%M')),
            "tahapan": forms.HiddenInput(),
            "link_teleconference": forms.TextInput(attrs={'rows':2}),
        }
    def __init__(self, *args, **kwargs):
#        print(kwargs)
        super(UndanganForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            undangan = models.undangan.objects.get(pk=kwargs['initial']['id'])
            bdr = models.bidder_lelang.objects.all().values('bidder').filter(item_lelang=undangan.item_lelang)
            self.fields['bidder_user'] = forms.ModelMultipleChoiceField(
                queryset=models.bidder_user.objects.all().filter(id__in=bdr), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
            auc = models.auctioner_lelang.objects.all().values('auctioner').filter(item_lelang=undangan.item_lelang)
            self.fields['auctioneer'] = forms.ModelMultipleChoiceField(
                queryset=models.tim_lelang.objects.all().filter(id__in=auc), 
                required=False,
                widget=forms.CheckboxSelectMultiple)
            vwr = models.viewers_lelang.objects.all().values('viewer').filter(item_lelang=undangan.item_lelang)
            self.fields['viewer'] = forms.ModelMultipleChoiceField(
                queryset=models.viewers.objects.all().filter(id__in=vwr), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
        else:
            bdr = models.bidder_lelang.objects.all().values('bidder').filter(item_lelang=kwargs['initial']['item_lelang'])
            #print(bdr)
            self.fields['bidder_user'] = forms.ModelMultipleChoiceField(
                queryset=models.bidder_user.objects.all().filter(id__in=bdr), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
            auc = models.auctioner_lelang.objects.all().values('auctioner').filter(item_lelang=kwargs['initial']['item_lelang'])
            self.fields['auctioneer'] = forms.ModelMultipleChoiceField(
                queryset=models.tim_lelang.objects.all().filter(id__in=auc), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
            viu = models.viewers_lelang.objects.all().values('viewer').filter(item_lelang=kwargs['initial']['item_lelang'])
            self.fields['viewer'] = forms.ModelMultipleChoiceField(
                queryset=models.viewers.objects.all().filter(id__in=viu), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
            

class BeritaAcaraForm(BSModalModelForm):
    class Meta:
        model = models.berita_acara
        fields = [
            "auctioneer",
            "bidder_user",
            "viewer",
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "file",
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
        if kwargs['initial'].get('id') is not None:
            undangan = models.berita_acara.objects.get(pk=kwargs['initial']['id'])
            bdr = models.bidder_lelang.objects.all().values('bidder').filter(item_lelang=undangan.item_lelang)
            self.fields['bidder_user'] = forms.ModelMultipleChoiceField(
                queryset=models.bidder_user.objects.all().filter(id__in=bdr), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
            auc = models.auctioner_lelang.objects.all().values('auctioner').filter(item_lelang=undangan.item_lelang)
            self.fields['auctioneer'] = forms.ModelMultipleChoiceField(
                queryset=models.tim_lelang.objects.all().filter(id__in=auc), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
            viu = models.viewers_lelang.objects.all().values('viewer').filter(item_lelang=undangan.item_lelang)
            self.fields['viewer'] = forms.ModelMultipleChoiceField(
                queryset=models.viewers.objects.all().filter(id__in=viu), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
        else:
            bdr = models.bidder_lelang.objects.all().values('bidder').filter(item_lelang=kwargs['initial']['item_lelang'])
            #print(bdr)
            self.fields['bidder_user'] = forms.ModelMultipleChoiceField(
                queryset=models.bidder_user.objects.all().filter(id__in=bdr), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
            viu = models.viewers_lelang.objects.all().values('viewer').filter(item_lelang=kwargs['initial']['item_lelang'])
            self.fields['viewer'] = forms.ModelMultipleChoiceField(
                queryset=models.viewers.objects.all().filter(id__in=viu), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
            auc = models.auctioner_lelang.objects.all().values('auctioner').filter(item_lelang=kwargs['initial']['item_lelang'])
            self.fields['auctioneer'] = forms.ModelMultipleChoiceField(
                queryset=models.tim_lelang.objects.all().filter(id__in=auc), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)

class bidderLelangForm(BSModalModelForm):
    # ip_address = forms.GenericIPAddressField(error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'})
    
    class Meta:
        model = models.bidder_lelang
        fields = [
            "eligibility",
            "bidder",
            "item_lelang",
            # "ip_address"
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(bidderLelangForm, self).__init__(*args, **kwargs)
        id = kwargs['initial'].get('id')
        item_lelang = kwargs['initial'].get('item_lelang')
        
        excluded_bidder_ids = models.bidder_lelang.objects.filter(item_lelang=item_lelang)
        
        if id is not None:
            excluded_bidder_ids = excluded_bidder_ids.exclude(id=id)
        
        filtered_data = models.bidder_user.objects.all().exclude(id__in=models.bidder_lelang.objects.values('bidder').filter(id__in=excluded_bidder_ids))
        self.fields["bidder"].queryset = filtered_data

class auctionerLelangForm(BSModalModelForm):
    class Meta:
        model = models.auctioner_lelang
        fields = [
            "id",
            "auctioner",
            "item_lelang",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super(auctionerLelangForm, self).__init__(*args, **kwargs)
        item_lelang = kwargs['initial']['item_lelang']
        id = kwargs['initial'].get('id')
        excluded_tim_lelang_ids = models.auctioner_lelang.objects.filter(item_lelang=item_lelang)
        
        if id is not None:
            excluded_tim_lelang_ids = excluded_tim_lelang_ids.exclude(id=id)
            
        filtered_data = models.tim_lelang.objects.all().exclude(id__in=models.auctioner_lelang.objects.values('auctioner').filter(id__in=excluded_tim_lelang_ids))
        print('-> DEBUG: filtered_data', filtered_data)
        self.fields["auctioner"].queryset = filtered_data

class viewerLelangForm(BSModalModelForm):
    class Meta:
        model = models.viewers_lelang
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
        id = kwargs['initial'].get('id')
        excluded_viewers_ids = models.viewers_lelang.objects.filter(item_lelang=item_lelang)
        
        if id is not None:
            excluded_viewers_ids = excluded_viewers_ids.exclude(id=id)
        
        filtered_data = models.viewers.objects.all().exclude(id__in=models.viewers_lelang.objects.values('viewer').filter(id__in=excluded_viewers_ids))
        self.fields["viewer"].queryset = filtered_data
