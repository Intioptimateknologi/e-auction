from rest_framework import serializers

from . import models



class form_pemeriksaanSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.form_pemeriksaan
        fields = [
            "item_lelang",
            "bidder",
            "sampul1",
            "bidbond",
            "sampul2",
            "kesimpulan",
            "keterangan",
            "file",
        ]

class berita_acara_allSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.berita_acara_administrasi
        fields = [
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "bidder",
            "auctioneer",
            "file",
            "owner",
        ]

class permohonan_keikutsertaanSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    file2 = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.permohonan_keikutsertaan
        fields = [
            "id",
            "item_lelang",
            "pernyataan",
            "file",
            "file2",
            "status",
            "bidder",
            "perwakilan"
        ]
        
        


class form_verifikasiSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
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

class form_evaluasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.form_evaluasi
        fields = [
            "id",
            "item_lelang",
            "bidder",
            "hasil_pemeriksaan",
            "keterangan",
            "file"
        ]


class hasilKesimpulanSerialiser(serializers.ModelSerializer):
    class Meta:
        model = models.hasil_kesimpulan
        fields = [
            "item_lelang",
            "bidder",
            # "kelengkapan_sampul1",
            # "kelengkapan_sampul2",
            # "kelengkapan_bidbond",
            # "verifikasi_bidbond",
            # "verifikasi_sampul1",
            "kesimpulan1",
            "kesimpulan2",
            "kesimpulan3"
        ]
class form_sanggahanSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
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

class hasil_evaluasiSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.hasil_evaluasi
        fields = [
            "id",
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "pengumuman",
            "file",
        ]
        
class jawaban_sanggahanSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
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