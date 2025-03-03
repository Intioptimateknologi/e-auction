from django import forms
from .models import rencana_seleksinya

class RencanaSeleksiForm(forms.ModelForm):
    class Meta:
        model = rencana_seleksinya
        fields = ('judul', 'tahun')


# class PenanggungJawabForm(forms.ModelForm):
#     class Meta:
#         model = rencana_penanggung_jawab
#         fields = ('judul', 'tahun', 'nama_lengkap', 'nip', 'jabatan_kominfo', 'jabatan_tim', 'status')