from django import forms
from adm_lelang.models import item_lelang, detail_itemlelang, bidder_lelang, auctioner_lelang, viewers_lelang
from . import models
from bootstrap_modal_forms.forms import BSModalModelForm
from ckeditor.widgets import CKEditorWidget
from userman.models import bidder, tim_lelang, Users, bidder_user, bidder_perwakilan, viewers


class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'

#form undangan pemilihan blok
#u for undangan
class u_pemilihan_blokForm(BSModalModelForm):
    class Meta:
        model = models.blok
        fields = [
            "users",
            "item_lelang",
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
            "item_lelang": forms.HiddenInput(),
            "tanggal": DateTimeInput(),
        }
        
#form pemilihan blok
#ps untuk pasca seleksi

class pemilihan_blok_psForm(BSModalModelForm):
    class Meta:
        model = models.pemilihan_blok_pasca_seleksi
        fields = [
            "blok",
        ]
    def __init__(self, *args, **kwargs):
        super(pemilihan_blok_psForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            undangan = models.pemilihan_blok_pasca_seleksi.objects.get(pk=kwargs['initial']['id'])
            bdr = models.pemilihan_blok_pasca_seleksi.objects.filter(item=undangan.item)
            id = []
            for i in bdr:
                if i.blok:
                    id.append(i.blok.id)
            self.fields['blok'] = forms.ModelMultipleChoiceField(
                queryset=models.blok_pasca_seleksi.objects.all().filter(item=undangan.item).exclude(id__in=id), 
                required=True, 
                widget=forms.RadioSelect)

#form hasil seleksi

class seleksinyaForm(BSModalModelForm):
    class Meta:
        model = models.seleksi
        fields =[
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "file_link",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
        }
#form sanggahan

class sanggahannyaForm(BSModalModelForm):
    class Meta : 
        model = models.sanggahan
        fields = [
            "item_lelang",
            "status_sanggahan",
            "file_link",
            "bidder",
            "keterangan"
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
        }

        
#form sanggahan dan jawaban

class sanggahan_jawabForm(BSModalModelForm):
    class Meta :
        model = models.sanggahan_jawaban
        fields = [
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "waktu",
            "agenda",
            "link_teleconference",
            "keterangan",
            "link_file",
        ]
        widgets = {
            "link_teleconference": forms.Textarea(attrs={'rows':2}),
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "agenda": forms.Textarea(attrs={'rows':2}),
            "item_lelang": forms.HiddenInput(),
        }
        
#form jawaban atas sanggahan

class jawab_atas_sanggahForm(BSModalModelForm):
    class Meta :
        model = models.jawaban_atas_sanggahan
        fields = [
            "item_lelang",
            "nama_perusahaan",
            "sampul1",
            "bidbond",
            "hasil_sanggahan",
        ]
        widgets = {
            "item_lelang": forms.HiddenInput(),
        }
        
#form penetapan pemenang

class pemenangnyaForm(BSModalModelForm):
    class Meta :
        model = models.pemenang
        fields = [
            "item_lelang",
            "bidder",
            "auctioneer",
            "viewer",
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "file_link",
        ]
        widgets = {
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "item_lelang": forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
#        print(kwargs)
        super(pemenangnyaForm, self).__init__(*args, **kwargs)
        if kwargs['initial'].get('id') is not None:
            undangan = models.pemenang.objects.get(pk=kwargs['initial']['id'])
            bdr = bidder_lelang.objects.all().values('bidder').filter(item_lelang=undangan.item_lelang)
            self.fields['bidder'] = forms.ModelMultipleChoiceField(
                queryset=models.bidder_user.objects.all().filter(id__in=bdr), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
            auc = auctioner_lelang.objects.all().values('auctioner').filter(item_lelang=undangan.item_lelang)
            self.fields['auctioneer'] = forms.ModelMultipleChoiceField(
                queryset=models.tim_lelang.objects.all().filter(id__in=auc), 
                required=False,
                widget=forms.CheckboxSelectMultiple)
            vwr = viewers_lelang.objects.all().values('viewer').filter(item_lelang=undangan.item_lelang)
            self.fields['viewer'] = forms.ModelMultipleChoiceField(
                queryset=viewers.objects.all().filter(id__in=vwr), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
        else:
            bdr = bidder_lelang.objects.all().values('bidder').filter(item_lelang=kwargs['initial']['item_lelang'])
            self.fields['bidder'] = forms.ModelMultipleChoiceField(
                queryset=models.bidder_user.objects.all().filter(id__in=bdr), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
            auc = auctioner_lelang.objects.all().values('auctioner').filter(item_lelang=kwargs['initial']['item_lelang'])
            self.fields['auctioneer'] = forms.ModelMultipleChoiceField(
                queryset=models.tim_lelang.objects.all().filter(id__in=auc), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
            viu = viewers_lelang.objects.all().values('viewer').filter(item_lelang=kwargs['initial']['item_lelang'])
            self.fields['viewer'] = forms.ModelMultipleChoiceField(
                queryset=viewers.objects.all().filter(id__in=viu), 
                required=False, 
                widget=forms.CheckboxSelectMultiple)
            
#form pengumuman penetapan pemenang
#p untuk pemenang

class pengumuman_pForms(BSModalModelForm):
    class Meta :
        model = models.pengumuman_pemenang
        fields = [
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "file_link",
        ]
        widgets = {
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "item_lelang": forms.HiddenInput(),
        }
        
        
#form Berita acara

class ba_pasca_seleksiForm(BSModalModelForm):
    class Meta :
        model = models.berita_acara_pasca_seleksi
        fields = [
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "link_file",
            "owner",
        ]
        widgets = {
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "item_lelang": forms.HiddenInput(),
        }
        
        
        
        
#form 'form sanggahan pasca seleksi'

class ps_sanggahannya_jawabForm(BSModalModelForm):
    class Meta :
        model = models.form_ps_sanggahan
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
            "bidder": forms.HiddenInput(),
            
        }
    def __init__(self, *args, **kwargs):
        super(ps_sanggahannya_jawabForm, self).__init__(*args, **kwargs)
        #userid  = self.request.user.id
        #bdr = bidder_user.objects.get(users__id = userid)
        #queryset= bidder_perwakilan.objects.all().filter(bidder=bdr.id)
        #self.fields['bidder'] = forms.ModelMultipleChoiceField(queryset, required=False, widget=forms.Select)   
        
class kirim_undg_sanggahan_jawabForm(BSModalModelForm):
    class Meta :
        model = models.undangan_ps_sanggahan
        fields = [
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "link_teleconference",
            "keterangan",
            "file",
            "bidder",
        ]
        widgets = {
            "link_teleconference": forms.Textarea(attrs={'rows':2}),
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "agenda": forms.Textarea(attrs={'rows':2}),
            "tempat": forms.Textarea(attrs={'rows':2}),
            "item_lelang": forms.HiddenInput(),
        }
        
        
class jawab_sanggahan_psForm(BSModalModelForm):
    class Meta :
        model = models.jawaban_ps_sanggahan
        fields = [
            "item_lelang",
            "bidder",
            "jawaban_sanggah",
            "keterangan",
            "tindak_lanjut_seleksi",
            "file",
        ]
        widgets = {
            "keterangan": forms.Textarea(attrs={'rows':2}),
            "item_lelang": forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super(jawab_sanggahan_psForm, self).__init__(*args, **kwargs)
        if  kwargs['initial'].get("id"):
            id = kwargs['initial']["id"]
            data = models.jawaban_ps_sanggahan.objects.get(pk=id)
            bdr_llg = bidder_lelang.objects.all().filter(item_lelang = data.item_lelang)
            id = []
            for b in bdr_llg:
                id.append(b.bidder.bidder.id)
            #bdr = bidder.objects.all().filter(id__in = id)
            bdr = bidder_user.objects.all().filter(id=data.bidder.id)
            self.fields['bidder'] = forms.ModelChoiceField(
                queryset= bdr, 
                required=False, 
                widget=forms.RadioSelect)
        else:
            itm_lelang = kwargs['initial']["item_lelang"]

            frm_sanggahan = models.form_ps_sanggahan.objects.all().filter(item_lelang = itm_lelang, status_sanggah = "Ada")
            id2 = []
            print("sanggah")
            for d in frm_sanggahan:
                id2.append(d.bidder.id)
               # print(d.bidder.id)

            frm_janggahan = models.jawaban_ps_sanggahan.objects.all().filter(item_lelang = itm_lelang)
            id1 = []
            print("jawab")
            for c in frm_janggahan:
                id1.append(c.bidder.id)
                #print(c.bidder.id)

            bdr_llg = bidder_lelang.objects.all().filter(item_lelang = itm_lelang)
            id = []
            for b in bdr_llg:
                id.append(b.bidder.bidder.id)

            bdr = bidder_user.objects.all().filter(id__in = id2).exclude(id__in = id1)
            self.fields['bidder'] = forms.ModelChoiceField(
                queryset= bdr, 
                required=False, 
                widget=forms.RadioSelect)

class blok_paska_seleksiForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(blok_paska_seleksiForm,self).__init__(*args, **kwargs)
        if kwargs['initial']['id']:
            d = models.blok_pasca_seleksi.objects.get(pk = kwargs['initial']['id'])
            self.fields['item'].queryset = detail_itemlelang.objects.filter(item_lelang=d.item.item_lelang, disabled=False)
        else:
            id = kwargs['initial']['item_lelang']
            self.fields['item'].queryset = detail_itemlelang.objects.filter(item_lelang=id, disabled=False)

    class Meta :
        model = models.blok_pasca_seleksi
        fields = [
            "item",
            "nama_block",
        ]

class pemenang_blok_paska_seleksiForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(pemenang_blok_paska_seleksiForm,self).__init__(*args, **kwargs)
        if kwargs['initial']['id']:
            d = models.pemilihan_blok_pasca_seleksi.objects.get(pk = kwargs['initial']['id'])
            self.fields['item'].queryset = detail_itemlelang.objects.filter(item_lelang=d.item.item_lelang)
            bdr = bidder_lelang.objects.all().values('bidder').filter(item_lelang=d.item.item_lelang)
            self.fields['bidder'] = forms.ModelChoiceField(
                queryset=models.bidder_user.objects.all().filter(id__in=bdr), 
                required=False, 
                widget=forms.RadioSelect)
        else:
            id = kwargs['initial']['item_lelang']
            self.fields['item'].queryset = detail_itemlelang.objects.filter(item_lelang=id)
            bdr = bidder_lelang.objects.all().values('bidder').filter(item_lelang=id)
            self.fields['bidder'] = forms.ModelChoiceField(
                queryset=models.bidder_user.objects.all().filter(id__in=bdr), 
                required=False, 
                widget=forms.RadioSelect)

    class Meta:
        model = models.pemilihan_blok_pasca_seleksi
        fields = [
            "item",
            "bidder",
            "ranking",
            "penawaran",
            "keterangan"
        ]
    