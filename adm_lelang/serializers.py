from rest_framework import serializers

from . import models
from drf_extra_fields.fields import Base64FileField
import PyPDF2
import io

class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfFileReader(io.BytesIO(decoded_file))
        except PyPDF2.utils.PdfReadError as e:
            logger.warning(e)
        else:
            return 'pdf'

class JPGBase64File(Base64FileField):
    ALLOWED_TYPES = ['jpg']

    def get_file_extension(self, filename, decoded_file):
        return 'jpg'

class bidder_lelangSerializer(serializers.ModelSerializer):
    perusahaan = serializers.ReadOnlyField(source='bidder.nama_perusahaan')
    class Meta:
        model = models.bidder_lelang
        fields = [
            "id",
            "eligibility",
            "bidder",
            "item_lelang",
            "ip_address",
            "perusahaan"
        ]

class auctioner_lelangSerializer(serializers.ModelSerializer):
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    diubah_oleh = serializers.ReadOnlyField(source="diubah_oleh.nama_lengkap")
    class Meta:
        model = models.auctioner_lelang
        fields = [
            "id",
            "auctioner",
            "item_lelang",
            "last_updated",
            "created",
            "dibuat_oleh",
            "diubah_oleh"
        ]

class viewers_lelangSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.viewers_lelang
        fields = [
            "id",
            "viewer",
            "item_lelang"
        ]

class detail_itemlelangSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.detail_itemlelang
        fields = [
            "id",
            "urutan",
            "created",
            "teknologi",
            "harga_minimal",
            "band",
            "rentang_frekuensi",
            "last_updated",
            "item_lelang",
            "eligibility_point_per_block",
            "max_block",
            "spectrum_cap",
            # tambahan uat
            "penyelenggaraan",
            "bandwidth",
            "cakupan",
            "keterangan",
            "disabled"
            # 
        ]

class item_lelangSerializer(serializers.ModelSerializer):
    dibuat_oleh = serializers.ReadOnlyField(source="dibuat_oleh.nama_lengkap")
    diubah_oleh = serializers.ReadOnlyField(source="diubah_oleh.nama_lengkap")
    class Meta:
        model = models.item_lelang
        fields = [
            "id",
            "tayang",
            "created",
            "last_updated",
            "diubah_oleh",
            "dibuat_oleh",
            "nama_lelang",
            "keterangan",
            "tahun"
        ]

class jadwal_seleksiSerializer(serializers.ModelSerializer):
    tahapan = serializers.ReadOnlyField(source='tahap.name')

    class Meta:
        model = models.jadwal_seleksi
        fields = [
            "id",
            "tahap",
            "tanggal_awal",
            "tanggal_akhir",
            "perubahan",
            "item_lelang",
            "tahapan",
            "created",
            "last_updated",
            "diubah_oleh",
            "dibuat_oleh",
        ]

class dasar_hukumSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.dasar_hukum
        fields = [
            "id",
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "attachment",
        ]

class pengumuman_lelangSerializer(serializers.ModelSerializer):
    image = JPGBase64File(required=False)
    image = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    dokumen = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.pengumuman
        fields = [
            "id",
            "nomor",
            "judul",
            "item_lelang",
            "tahapan",
            "pengumuman",
            "dokumen",
            "tgl_release",
            "diubah_oleh",
            "created",
            "owner",
            "image"
        ]

class persyaratan_lelangSerializer(serializers.ModelSerializer):
    dokumen = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = models.persyaratan_lelang
        fields = [
            "id",
            "item_lelang",
            "no_urut",
            "persyaratan",
            "keterangan",
            "dokumen"
        ]

class alamat_panitiaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.alamat_panitia
        fields = [
            "id",
            "alamat",
            "kota",
            "telp",
            "kodepos",
            "email",
            "telp",
            "cq",
            "item_lelang",
            "status",
            "keterangan",
            "provinsi"
        ]

class template_berita_acaraSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.template_berita_acara
        fields = [
            "id",
            "nama_template",
            "keterangan_template",
            "template_code_menu",
            "template_code_sub",
            "item_lelang",
            "dokumen",
        ]

class tahapan_Serializer(serializers.ModelSerializer):
    leaf_nodes = serializers.SerializerMethodField()

    class Meta:
        model = models.tahapan_lelang2
        fields = [
            "id",
            "name",
            "judul",
            "attribute",
            "parent",
            "leaf_nodes"
        ]
    def get_leaf_nodes(self, obj):
        return tahapan_Serializer(obj.get_children(), many=True).data

class tahapan2_Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.tahapan_lelang2
        fields = [
            "id",
            "name",
            "judul",
            "attribute",
            "orderby",
            "parent",
            "level"
        ]

class undanganSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.undangan
        fields = [
            "id",
            "item_lelang",
            "bidder_user",
            "auctioneer",
            "viewer",
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "keterangan",
            "link_teleconference",
            "file",
            "diubah_oleh",
            "waktu_awal",
            "waktu_akhir",
            "tahapan",
        ]

class berita_acaraSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    
    class Meta:
        model = models.berita_acara
        fields = [
            "id",
            "bidder_user",
            "auctioneer",
            "viewer",
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",            
            "keterangan",
            "file",
            "diubah_oleh",
            "tahapan",
            "last_updated",
        ]

class pengambilan_undanganSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.pengambilan_undangan
        fields= [
            "id",
            "undangan",
            "bidder_user",
            "item_lelang",
            "tgl_download"
        ]


class pengambilan_baSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.pengambilan_ba
        fields= [
            "id",
            "ba",
            "user",
            "item_lelang",
            "tgl_download"
        ]

class penangung_jawabSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.penangung_jawab_seleksi
        fields= [
            "item_lelang",
            "nama",
            "nip",
            "tanggung_jawab",
            "tgl_mulai",
            "tgl_akhir",
            "status",
            "keterangan",
            "dibuat_oleh",
            "diubah_oleh",
            "created",
            "last_updated",
        ]