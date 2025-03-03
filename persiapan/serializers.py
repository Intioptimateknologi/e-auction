from rest_framework import serializers
from userman.models import bidder, tim_lelang
from . import models

class p_dokumenSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    auctioneers = serializers.PrimaryKeyRelatedField(
        queryset=tim_lelang.objects.all(),
        required=False,
        allow_empty=True,
        many=True,
    )

    bidders = serializers.PrimaryKeyRelatedField(
        queryset=bidder.objects.all(),
        required=False,
        allow_empty=True,
        many=True,
    )
    class Meta:
        model = models.p_dokumen
        fields = [
            "id",
            "item_lelang",
            "bidder",
            "auctioneer",
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "keterangan",
            "link_teleconference",
            "file",
            "diubah_oleh",
            "tahapan",
        ]

class penyusunan_jawabanSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.penyusunan_jawaban
        fields = [
            "id",
            "item_lelang",
            "bidder",
            "auctioneer",
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "keterangan",
            "link_teleconference",
            "file",
        ]

class aanwizingSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.aanwizing
        fields = [
            "id",
            "item_lelang",
            "bidder",
            "auctioneer",
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "keterangan",
            "link_teleconference",
            "file",
        ]

class simulasiSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.simulasi
        fields = [
            "id",
            "item_lelang",
            "bidder",
            "auctioneer",
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "keterangan",
            "link_teleconference",
            "file",
        ]

class p_addendumSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.p_addendum
        fields = [
            "id",
            "item_lelang",
            "bidder",
            "auctioneer",
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "keterangan",
            "link_teleconference",
            "file",
        ]

class dokumen_seleksiSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = models.dokumen_seleksi
        fields = [
            "id",
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "file",
        ]

        def validate_file(self, value):
            if not value:
                return None  # Allow empty file submission
            # Additional validation logic if required
            return value

class pengambilan_dokumen_seleksiSerializer(serializers.ModelSerializer):
    file = serializers.ReadOnlyField(source='dokumen_seleksi.file.url')
    print(file)
    #file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.pengambilan_dokumen_seleksi
        fields = [
            "id",
            "dokumen_seleksi",
            "bidder_perwakilan",
            "tgl_download",
            "file"
        ]

       

class pengambilan_dokumen_addendumSerializer(serializers.ModelSerializer):
    file = serializers.ReadOnlyField(source='dokumen_addendum.file.url')
    class Meta:
        model = models.pengambilan_dokumen_addendum
        fields = [
            "id",
            "dokumen_addendum",
            "bidder_perwakilan",
            "tgl_download",
            "file"
        ]

        def validate_file(self, value):
            if not value:
                return None  # Allow empty file submission
            # Additional validation logic if required
            return value

class p_pertanyaanSerializer(serializers.ModelSerializer):
    file_pdf = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    file_excel = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    file_word = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = models.p_pertanyaan
        fields = [
            "id",
            "item_lelang",
            "bidder",
            "pertanyaan",
            "file_word",
            "file_pdf",
            "file_excel",
            "perwakilan",
        ]

class berita_acara_persiapanSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    # bidder = serializers.Field(required=False, max_length=None, allow_empty_file=True, use_url=True)
    
    class Meta:
        model = models.berita_acara_persiapan
        fields = [
            "id",
            "bidder",
            "auctioneer",
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",            
            "keterangan",
            "file",
            "owner",
            "diubah_oleh",
            "tahapan",
            "last_updated",
        ]

class daftar_hadirSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.daftar_hadir
        fields = [
            "id",
            "item_lelang",
            "bidder_perwakilan",
            "nama_perwakilan",
            "nama_perusahaan",
            "tgl_kehadiran",
            "diubah_oleh",
            "last_updated",
            "tahapan",
        ]