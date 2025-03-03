from . import models
from . import tables
from django import forms
from adm_lelang.models import item_lelang, bidder_lelang
from administrasi.models import form_sanggahan
from userman.models import bidder_perwakilan
from bootstrap_modal_forms.forms import BSModalModelForm
from ckeditor.widgets import CKEditorWidget
from userman.models import bidder, tim_lelang, Users, bidder_user, bidder_perwakilan

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'

# form pemeriksaan kelengkapan
class FormPemeriksaanForm(BSModalModelForm):
    class Meta:
        model = models.form_pemeriksaan
        fields = [
            "item_lelang",
            "bidder",
            "sampul1",
            "bidbond",
            "sampul2",
            "keterangan",
            "file",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "bidbond":forms.RadioSelect(attrs={'class': 'form-check form-check-inline'}),
        }

    def __init__(self, *args, **kwargs):
        super(FormPemeriksaanForm, self).__init__(*args, **kwargs)
        if  kwargs['initial'].get("id"):
            id = kwargs['initial']["id"]
            try:
                data = models.form_pemeriksaan.objects.get(pk=id)
                #bdr_llg = bidder_lelang.objects.all().filter(item_lelang = data.item_lelang)
                #id = []
                #for b in bdr_llg:
                #    id.append(b.bidder.id)
                bdr = bidder_user.objects.all().filter(id = data.bidder.id)
                self.fields['bidder'] = forms.ModelChoiceField(
                    queryset= bdr, 
                    required=False, 
                    widget=forms.RadioSelect)
            except:
                None
        else:
            # dptin item lelang
            itm_lelang = kwargs['initial']["item_lelang"]
            # dptin pemeriksaan untuk nge exclude <QuerySet [<form_pemeriksaan: PT XL>, <form_pemeriksaan: PT Telkom>]>
            pemeriksaan = models.form_pemeriksaan.objects.filter(item_lelang__id=itm_lelang)
            # dptin keikutsertaan untuk ngegate yang mengikuti <QuerySet [<permohonan_keikutsertaan: 101>, <permohonan_keikutsertaan: 45>, <permohonan_keikutsertaan: 46>]>
            keikutsertaan = models.permohonan_keikutsertaan.objects.filter(item_lelang__id=itm_lelang, pernyataan="MENGIKUTI")
            
            id2 = []
            for f in keikutsertaan:
                id2.append(f.bidder.bidder.id)
            # mendapatkan bidder id dari keikutsertaan
            #print(id2) #[40, 45, 45]

            id1 = []
            for d in pemeriksaan:
                id1.append(d.bidder.bidder.id)
            # mendapatkan bidder id dari pemeriksaan 
            #print(id1) #[45, 40]

            #filter bidder lelang untuk mendapatkan bidder user dengan nama bidder yang sudah ada di tabel
            bdr_llg = bidder_lelang.objects.all().filter(item_lelang = itm_lelang, bidder__bidder__id__in = id2).exclude(bidder__bidder__id__in = id1)
            id3 = []
            for b in bdr_llg:
                id3.append(b.bidder.bidder.id)

            #print(id3)
            # di filter dari bidder_user dengan nama bidder
            #bdr = bidder_perwakilan.objects.all().filter(bidder__bidder__id__in= id3)
            #self.fields['perwakilan'] = forms.ModelChoiceField(
            #    queryset= bdr, 
            #    required=False, 
            #    widget=forms.RadioSelect)
            
            bdr_llg = bidder_lelang.objects.all().filter(item_lelang = itm_lelang)
            id = []
            for b in bdr_llg:
                id.append(b.bidder.bidder.id)
                
            bdr = bidder_user.objects.all().filter(bidder_id__in = id3)
            self.fields['bidder'] = forms.ModelChoiceField(
                queryset= bdr, 
                required=False, 
                widget=forms.RadioSelect)

# form verifikasi
class FormVerifikasiForm(BSModalModelForm):
    class Meta:
        model = models.form_verifikasi
        fields = [
            "item_lelang",
            "bidder",
            "sampul1",
            "bidbond",
            "keterangan",
            "file",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
        }
    def __init__(self, *args, **kwargs):
        super(FormVerifikasiForm, self).__init__(*args, **kwargs)
        if  kwargs['initial'].get("id"):
            id = kwargs['initial']["id"]
            try:
                data = models.form_verifikasi.objects.get(pk=id)
                bdr_llg = bidder_lelang.objects.all().filter(item_lelang = data.item_lelang)
                id = []
                print("DEBUG_bdr_llg_ilhaz", bdr_llg);
                for b in bdr_llg:
                    id.append(b.bidder.bidder.id)
                    # id.append(b.bidder.id)
                # bdr = bidder.objects.all().filter(id__in = id)
                #bdr = bidder.objects.all().filter(id=data.bidder.id)
                bdr = bidder_user.objects.all().filter(id=data.bidder.id)
                # bdr = bidder_user.objects.all().filter(id__in = id3)
                self.fields['bidder'] = forms.ModelChoiceField(
                    queryset= bdr, 
                    required=False, 
                    widget=forms.RadioSelect)
            except:
                None
        else:
            itm_lelang = kwargs['initial']["item_lelang"]
            bdr_llg = bidder_lelang.objects.all().filter(item_lelang = itm_lelang)
            # pemeriksaan = models.form_pemeriksaan.objects.filter(item_lelang__id=itm_lelang, sampul1='Ada', sampul2='Ada', bidbond='Ada')
            pemeriksaan = models.form_pemeriksaan.objects.filter(item_lelang__id=itm_lelang)
            # print(pemeriksaan) [<form_pemeriksaan: PT XL>, <form_pemeriksaan: PT Telkom>]
            id1 = []
            for d in pemeriksaan:
                id1.append(d.bidder.id)
                # id1.append(d.bidder.bidder.id)
            # print(id1)
            # 85

            data_verifikasi = models.form_verifikasi.objects.filter(item_lelang__id=itm_lelang)
            # print(data)  [<form_verifikasi: 37>, <form_verifikasi: 38>, <form_verifikasi: 49>]>
            id2 = []
            for e in data_verifikasi:
                id2.append(e.bidder.id)
            # print(id2)#[37, 38, 49]

            # bdr_llg = bidder_lelang.objects.all().filter(item_lelang = itm_lelang).exclude(bidder__bidder__id__in = id2).filter(bidder__bidder__id__in = id1)
            bdr_llg = bidder_lelang.objects.all().filter(item_lelang = itm_lelang).exclude(bidder__id__in = id2).filter(bidder__id__in = id1)
            id3 = []
            for f in bdr_llg:
                id3.append(f.bidder.id)
                # id3.append(f.bidder.bidder.id)
            # print(id3)
            bdr = bidder_user.objects.all().filter(bidder_id__in = id3)
            bdr = bidder_user.objects.all().filter(pk__in = id3)
            self.fields['bidder'] = forms.ModelChoiceField(
                queryset= bdr, 
                required=False, 
                widget=forms.RadioSelect)

# form evaluasi
class FormEvaluasiForm(BSModalModelForm):
    class Meta:
        model = models.form_evaluasi
        fields = [
            "item_lelang",
            "bidder",
            "hasil_pemeriksaan",
            "keterangan",
            "file",
#            "table"
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
        }
    def __init__(self, *args, **kwargs):
        super(FormEvaluasiForm, self).__init__(*args, **kwargs)
        if  kwargs['initial'].get("id"):
            id = kwargs['initial']["id"]
            #try:
            data = models.form_evaluasi.objects.get(pk=id)
            bdr = bidder_user.objects.all().filter(id = data.bidder.id)
            self.fields['bidder'] =forms.ModelChoiceField(queryset=bdr,widget=forms.RadioSelect)
            self.fields['html'] = "<b>Test</b>"
        else:
            itm_lelang = kwargs['initial']["item_lelang"]
            bdr_llg = bidder_lelang.objects.all().filter(item_lelang = itm_lelang)
            id = []
            for b in bdr_llg:
                id.append(b.bidder.bidder.id)
            bdr = bidder_user.objects.all().filter(id__in = id)
            self.fields['bidder'] = forms.ModelChoiceField(
                queryset= bdr, 
                required=False, 
                widget=forms.RadioSelect)
            #self.fields["table"]=tables.hasil_kesimpulanTable2(models.hasil_kesimpulan.objects.all().filter(item_lelang=kwargs['initial']["item_lelang"]).order_by('-id'))
            #print(self.fields['table'])

# form sanggahan
class FormSanggahanForm(BSModalModelForm):
    class Meta:
        model = models.form_sanggahan
        fields = [
            "item_lelang",
            "bidder",
            "status_sanggah",
            "waktu_sanggahan",
            "file",
            "keterangan",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "waktu_sanggahan": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "bidder": forms.HiddenInput()
        }
    def __init__(self, *args, **kwargs):
        super(FormSanggahanForm, self).__init__(*args, **kwargs)
        #userid  = self.request.user.id
        #bdr = bidder_user.objects.get(users__id = userid)
        #queryset= bidder_perwakilan.objects.all().filter(bidder=bdr.id)
        #self.fields['bidder'] = forms.ModelMultipleChoiceField(bdr, required=False, widget=forms.Select)

# form permohonan keikutsertaan
class PermohonanKeikutsertaanForm(BSModalModelForm):
    class Meta:
        model = models.permohonan_keikutsertaan
        fields = [
            "item_lelang",
            "pernyataan",
            "bidder",
            "perwakilan",
            "status",
            "file",
            "file2",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "bidder": forms.HiddenInput()
        }
    def __init__(self, *args, **kwargs):
#        print(kwargs)
        super(PermohonanKeikutsertaanForm, self).__init__(*args, **kwargs)
        userid  = self.request.user.id
        self.fields['bidder']=userid
        if kwargs['initial'].get('id') is not None:
            try:
                bdr = models.permohonan_keikutsertaan.objects.get(pk=kwargs['initial'].get('id'))
                #print(bdr.bidder.bidder)
                perwakilan = bidder_perwakilan.objects.all().filter(bidder = bdr.bidder.bidder)
                self.fields['perwakilan'] = forms.ModelChoiceField(queryset=perwakilan,widget=forms.RadioSelect)
            except:
                None
        else:
            bdr = bidder_user.objects.get(users__id = userid)
            perwakilan = bidder_perwakilan.objects.all().filter(bidder = bdr)
            self.fields['perwakilan'] = forms.ModelChoiceField(queryset=perwakilan, widget=forms.RadioSelect)

# form hasil evaluasi
class HasilEvaluasiForm(BSModalModelForm):
    class Meta:
        model = models.hasil_evaluasi
        fields = [
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "pengumuman",
            "file",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "pengumuman": forms.Textarea(attrs={'rows':2}),
        }

# form berita acara
class BeritaAcaraForm(BSModalModelForm):
    class Meta:
        model = models.berita_acara_administrasi
        fields = [
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

# Jawaban Sanggahan
class JawabanSanggahanForm(BSModalModelForm):
    class Meta:
        model = models.jawaban_sanggahan
        fields = [
            "item_lelang",
            "bidder",
            "jawaban_sanggah",
            "keterangan",
            "tindak_lanjut_seleksi",
            "file",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
            "keterangan": forms.Textarea(attrs={'rows':2}),
        }
    def __init__(self, *args, **kwargs):
        super(JawabanSanggahanForm, self).__init__(*args, **kwargs)
        if  kwargs['initial'].get("id"):
            id = kwargs['initial']["id"]
            try:
                data = models.jawaban_sanggahan.objects.get(pk=id)

                bdr_llg = bidder_lelang.objects.all().filter(item_lelang = data.item_lelang)
                id = []
                
                for b in bdr_llg:
                    id.append(b.bidder.bidder.id)
                    
                bdr = bidder_user.objects.all().filter(id__in = id)
                self.fields['bidder'] = forms.ModelChoiceField(
                    queryset= bdr, 
                    required=False, 
                    widget=forms.RadioSelect)
            except:
                None
        else:
            itm_lelang = kwargs['initial']["item_lelang"]

            frm_sanggahan = form_sanggahan.objects.all().filter(item_lelang = itm_lelang, status_sanggah = "Ada")
            id2 = []
            
            for d in frm_sanggahan:
                id2.append(d.bidder.bidder.id)

            frm_janggahan = models.jawaban_sanggahan.objects.all().filter(item_lelang = itm_lelang)
            id1 = []
            
            for c in frm_janggahan:
                id1.append(c.bidder.id)

            bdr_llg = bidder_lelang.objects.all().filter(item_lelang = itm_lelang)
            id = []
            
            for b in bdr_llg:
                id.append(b.bidder.bidder.id)

            bdr = bidder_user.objects.all().filter(bidder_id__in = id2).exclude(bidder_id__in = id1)
            
            # print('-> DEBUG: id2', id2)
            # print('-> DEBUG: id1', id1)
            # print('-> DEBUG: id', id)
            
            self.fields['bidder'] = forms.ModelChoiceField(
                queryset= bdr, 
                required=False, 
                widget=forms.RadioSelect)
            
            
