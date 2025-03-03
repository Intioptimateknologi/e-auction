from django.contrib import admin
from django import forms

from . import models

#class UsersAdminForm(forms.ModelForm):

#    class Meta:
#        model = models.Users
#        fields = "__all__"


#class UsersAdmin(admin.ModelAdmin):
#    form = UsersAdminForm
#    list_display = [
#        "isactive",
##        "email",
 #       "created",
#        "username",
#        "last_updated",
#        "password",
##        "mobile_number",
#    ]
#    readonly_fields = [
#        "isactive",
#        "email",
#        "created",
#        "username",
#        "last_updated",
#        "password",
#        "mobile_number",
#    ]


"""class tim_lelangAdminForm(forms.ModelForm):

    class Meta:
        model = models.tim_lelang
        fields = "__all__"


class tim_lelangAdmin(admin.ModelAdmin):
    form = tim_lelangAdminForm
    list_display = [
        "last_updated",
        "sk_pengangkatan",
        "created",
        "nip",
        "jabatan_dalam_tim",
        "jabatan",
    ]
    readonly_fields = [
        "last_updated",
        "sk_pengangkatan",
        "created",
        "nip",
        "jabatan_dalam_tim",
        "jabatan",
    ]

class dokumen_perusahaanAdminForm(forms.ModelForm):

    class Meta:
        model = models.dokumen_perusahaan
        fields = "__all__"

class dokumen_perusahaanAdmin(admin.ModelAdmin):
    form = dokumen_perusahaanAdminForm
    list_display = [
        "dokumen",
        "nama_dokumen",
        "verification_note",
        "last_updated",
        "verified_at",
        "created",
        "verified",
    ]
    readonly_fields = [
        "dokumen",
        "nama_dokumen",
        "verification_note",
        "last_updated",
        "verified_at",
        "created",
        "verified",
    ]

class bidderAdminForm(forms.ModelForm):

    class Meta:
        model = models.bidder
        fields = "__all__"


class bidderAdmin(admin.ModelAdmin):
    form = bidderAdminForm
    list_display = [
        "nik",
        "alamat_perusahaan",
        "jenis_penyelenggara",
        "verified",
        "verified_at",
        "jabatan_di_perusahaan",
        "telp_perusahaan",
        "nama_perusahaan",
        "tgl_lahir",
        "last_updated",
        "created",
        "verification_note",
        "npwp_perusahaan",
        "email_perusahaan",
        "nib_perusahaan",
    ]
    readonly_fields = [
        "nik",
        "alamat_perusahaan",
        "jenis_penyelenggara",
        "verified",
        "verified_at",
        "jabatan_di_perusahaan",
        "telp_perusahaan",
        "nama_perusahaan",
        "tgl_lahir",
        "last_updated",
        "created",
        "verification_note",
        "npwp_perusahaan",
        "email_perusahaan",
        "nib_perusahaan",
    ]




admin.site.register(models.dokumen_perusahaan, dokumen_perusahaanAdmin)
admin.site.register(models.Users, UsersAdmin)
admin.site.register(models.tim_lelang, tim_lelangAdmin)
admin.site.register(models.bidder, bidderAdmin)
"""
