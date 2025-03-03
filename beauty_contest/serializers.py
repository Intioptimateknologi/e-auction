from rest_framework import serializers

from . import models
from userman.serializers import bidderlistSerializer

class parameter_evaluasiSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.parameter_evaluasi
        fields = [
            "id",
            "item",
            "parameter",
            "bobot",
            "last_updated",
            "created",
        ]

class dokumen_bcSerializer(serializers.ModelSerializer):
    dokumen_bc = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.dokumen_bc
        fields = [
            "id",
            "item",
            "last_updated",
            "dokumen_bc",
            "bidder",
            "perwakilan",
            "created",
            "nama_dok"
        ]

class format_dokumen_bcSerializer(serializers.ModelSerializer):
    fotmat_doc = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    format_xls = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.format_dokumen_bc
        fields = [
            "item",
            "nomor",
            "tgl_penetapan",
            "fotmat_doc",
            "format_xls",
            "judul",
            "keterangan",
        ]


class input_penialianSerializer(serializers.ModelSerializer):
    perusahaan = serializers.ReadOnlyField(source='bidder.nama_perusahaan')
    params = serializers.ReadOnlyField(source='parameter.parameter')

    class Meta:
        model = models.penilaian_bc
        fields = [
            "id",
            "created",
            "last_updated",
            "penilaian",
            "bobot",
            "item",
            "bidder",
            "hasil_evaluasi",
            "keterangan",
            "parameter",
            "perusahaan",
            "params"
        ]

class sum_penilaianSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.sum_penilaian
        fields = [
            "id",
            "score",
            "bidder",
            "item_lelang",
        ]

class hasil_beautycontestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.hasil_beauty_contest
        fields = [
            "id",
            "item",
            "bidder",
            "penilaian",
            "ranking"
        ]

class obyek_seleksibcSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.obyek_seleksi_bc
        fields = [
            "item", "bidder_user", "block", "created", "dibuat_oleh", "diubah_oleh"
        ]
