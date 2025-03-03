from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from . import models

class blokSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.blok
        fields = [
            "id",
            "item_lelang",
            "users",
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "link_teleconference",
            "keterangan",
            "link_file",
        ]

class pemilihan_blok_pasca_seleksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.pemilihan_blok_pasca_seleksi
        fields = [
            "id",
            "item_lelang",
            "item",
            "bidder",
            "ranking",
            "blok",
            # "nama_perusahaan",
            # "sampul1",
            # "bidbond",
            # "sampul2",
            # "hasil_blok",
        ]



class seleksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.seleksi
        fields = [
            "id",
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "file_link",
        ]

class sanggahanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.sanggahan
        fields = [
            "id",
            "item_lelang",
            "status_sanggahan",
            "file_link",
            'bidder',
            'keterangan',
            'waktu_sanggahan'
        ]

class sanggahan_jawabanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.sanggahan_jawaban
        fields = [
            "id",
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

class jawaban_atas_sanggahanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.jawaban_atas_sanggahan
        fields = [
            "id",
            "item_lelang",
            "nama_perusahaan",
            "sampul1",
            "bidbond",
            "hasil_sanggahan",
        ]

class pemenangSerializer(serializers.ModelSerializer):
    file_link = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.pemenang
        fields = [
            "id",
            "item_lelang",
            "auctioneer",
            "bidder",
            "viewer",
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "file_link",
        ]

class pengumuman_pemenangSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.pengumuman_pemenang
        fields = [
            "id",
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "keterangan",
            "file_link",
        ]

class berita_acara_pasca_seleksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.berita_acara_pasca_seleksi
        fields = [
            "id",
            "item_lelang",
            "nomor",
            "judul",
            "tanggal",
            "link_file",
            "keterangan",
            "owner",
        ]

class form_ps_sanggahanSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.form_ps_sanggahan
        fields = [
            "id",
            "item_lelang",
            "bidder",
            "status_sanggah",
            "waktu_sanggahan",
            "keterangan",
            "file",
        ]

class undangan_ps_sanggahanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.undangan_ps_sanggahan
        fields = [
            "id",
            "item_lelang",
            "bidder",
            "nomor",
            "judul",
            "tanggal",
            "tempat",
            "agenda",
            "keterangan",
            "link_teleconference",
            "file",
        ]

class jawaban_ps_sanggahanSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.jawaban_ps_sanggahan
        fields = [
            "id",
            "item_lelang",
            "bidder",
            "jawaban_sanggah",
            "keterangan",
            "tindak_lanjut_seleksi",
            "file",
        ]

class blok_paska_seleksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.blok_pasca_seleksi
        fields = [
            "id",
            "item",
            "nama_block",
        ]

class pemenang_blok_pasca_seleksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.pemilihan_blok_pasca_seleksi
        fields = [
            "id",
            "item_lelang",
            "item",
            "bidder",
            "ranking",
            "penawaran",
            "keterangan"
            #"blok",
            # "nama_perusahaan",
            # "sampul1",
            # "bidbond",
            # "sampul2",
            # "hasil_blok",
        ]