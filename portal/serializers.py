from . import models
from drf_extra_fields.fields import Base64FileField
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
import PyPDF2
import io
import base64
from rest_framework import serializers

# class PDFBase64File(Base64FileField):
#     ALLOWED_TYPES = ['pdf']

#     def get_file_extension(self, filename, decoded_file):
#         try:
#             if base64.b64encode(decoded_file).decode('ascii')[0:4] != 'http':
#                 PyPDF2.PdfFileReader(io.BytesIO(decoded_file))
#         except PyPDF2.utils.PdfReadError as e:
#             print(e)
#         else:
#             return 'pdf'
class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        return 'pdf'
    
class JPGBase64File(Base64FileField):
    ALLOWED_TYPES = ['jpg']

    def get_file_extension(self, filename, decoded_file):
        return 'jpg'

class bannerSerializer(serializers.ModelSerializer):
    image = JPGBase64File(required=False)
    image = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    updated_by = serializers.ReadOnlyField(source="updated_by.nama_lengkap")
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    class Meta:
        model = models.banner
        fields = [
            "id",
            "created",
            "last_updated",
            "image",
            "tag",
            "caption",
            "nama_banner",
            "updated_by",
            "dibuat_oleh",
        ]

class aturan_lelangSerializer(serializers.ModelSerializer):
    file = PDFBase64File(required=False)
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    updated_by = serializers.ReadOnlyField(source="updated_by.nama_lengkap")
    # last_updated = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    class Meta:
        model = models.aturan_lelang
        fields = [
            "id",
            "last_updated",
            "jenis_kebjakan",
            "created",
            "nomor",
            "file",
            "nama_kebijakan",
            "tanggal",
            "keterangan",
            "updated_by",
            "dibuat_oleh",
        ]

class notice_lelangSerializer(serializers.ModelSerializer):
    updated_by = serializers.ReadOnlyField(source="updated_by.nama_lengkap")
    # last_updated = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    class Meta:
        model = models.notice_lelang
        fields = [
            "id",
            "last_updated",
            "nama_notice",
            "tanggal",
            "updated_by",
            "dibuat_oleh",
        ]


class history_lelangSerializer(serializers.ModelSerializer):
    image = JPGBase64File(required=False)
    image = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    updated_by = serializers.ReadOnlyField(source="updated_by.nama_lengkap")
    # tahun = serializers.DateField(format="%Y")
    # last_updated = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    class Meta:
        model = models.history_lelang
        fields = [
            "id",
            "last_updated",
            "image",
            "hasil",
            "nama_lelang",
            "pemenang",
            "tahun",
            "created",
            "keterangan",
            "penyelenggaraan",
            "pita",
            "bandwidth",
            "updated_by",
            "dibuat_oleh",
        ]

class portal_blockSerializer(serializers.ModelSerializer):
    updated_by = serializers.ReadOnlyField(source="updated_by.nama_lengkap")
    # last_updated = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    class Meta:
        model = models.portal_block
        fields = [
            "id",
            # "image_header",
            "last_updated",
            "created",
            "tag",
            "content",
            "judul",
            "order",
            "updated_by"
        ]

class lelang_mancanegaraSerializer(serializers.ModelSerializer):
    image = JPGBase64File(required=False)
    image = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    updated_by = serializers.ReadOnlyField(source="updated_by.nama_lengkap")
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    # last_updated = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    class Meta:
        model = models.lelang_mancanegara
        fields = [
            "id",
            "last_updated",
            "image",
            "keterangan",
            "created",
            "tahun",
            "pita",
            "negara",
            "nama_negara",
            "bandwidth",
            "updated_by",
            "dibuat_oleh",
        ]

class istilah_lelangSerializer(serializers.ModelSerializer):
    updated_by = serializers.ReadOnlyField(source="updated_by.nama_lengkap")
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    # last_updated = serializers.DateTimeField(format="%d/%m/%Y %H:%M" )

    class Meta:
        model = models.istilah_lelang
        fields = [
            "id",
            "nama_istilah",
            "penjelasan",
            "last_updated",
            "updated_by",
            "dibuat_oleh",
            "created",
            
        ]

class profilSerializer(serializers.ModelSerializer):
    updated_by = serializers.ReadOnlyField(source="updated_by.nama_lengkap")
    # last_updated = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    class Meta:
        model = models.profil
        fields = [
            "id",
            "latar_belakang",
            "visi",
            "misi",
            "status",
            "sejarah_seleksi",
            "tugas_dir",
            "last_updated",
            "updated_by"
            
        ]