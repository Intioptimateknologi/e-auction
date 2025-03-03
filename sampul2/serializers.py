from rest_framework import serializers

from . import models


class penyampaian_penawaranSerializer(serializers.ModelSerializer):
    dokumen_penawaran = serializers.FileField(required=False,max_length=None, allow_empty_file=True, use_url=True)
    harga = serializers.FloatField(required=False)
    blok = serializers.IntegerField(required=False)

    class Meta:
        model = models.penawaran
        fields = [
            "id",
            "dokumen_penawaran",
            "harga",
            "blok",
            "bidder",
            "item",
            "perwakilan",
            "verified"
        ]

class evaluasi_penawaranSerializer(serializers.ModelSerializer):
    dokumen = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = models.evaluasi_penawaran
        fields = [
            "id",
            "penawaran",
            "hasil",
            "catatan",
            "dokumen"

        ]

class obyek_seleksi_sampul2Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.obyek_seleksi_sampul2
        fields = [
            "item", "bidder_user", "block", "created", "dibuat_oleh", "diubah_oleh"
        ]

class hasil_sampul2Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.hasil_sampul2
        fields = [
            "item", "bidder", "harga","ranking"
        ]
