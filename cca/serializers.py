from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField, JSONField
from drf_extra_fields.fields import DecimalRangeField
from adm_lelang.serializers import detail_itemlelangSerializer
from adm_lelang.models import detail_itemlelang

from . import models

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)

class round_ccaSerializer(serializers.ModelSerializer):
    status_round = ChoiceField(models.round_cca.STATUS.choices)
    band = serializers.SerializerMethodField()

    class Meta:
        model = models.round_cca
        fields = [
            "id",
            "bidder",
            "item_lelang",
            "status_round",
            "mulai",
            "selesai",
            "round",
            "lock",
            "jenis",
            "status_sah",
            "eli_point",
            "activity",
            "band",
        ]
    def get_band(self, obj):
        return detail_itemlelangSerializer(detail_itemlelang.objects.all().filter(item_lelang = obj.item_lelang), many=True).data

class sum_round_ccaSerializer(serializers.ModelSerializer):
    status_round = ChoiceField(models.round_cca.STATUS.choices)
    band = serializers.SerializerMethodField()

    class Meta:
        model = models.sum_round_cca
        fields = [
            "id",
            "item_lelang",
            "status_round",
            "mulai",
            "selesai",
            "round",
            "band",
            "count",
        ]
    def get_band(self, obj):
        return detail_itemlelangSerializer(detail_itemlelang.objects.all().filter(item_lelang = obj.item_lelang), many=True).data


class round_cca2Serializer(serializers.ModelSerializer):
    status_round = ChoiceField(models.round_cca.STATUS.choices)
    class Meta:
        model = models.round_cca2
        fields = [
            "id",
            "price",
            "prev_price"
            "bidder",
            "item",
            "activity",
            "corrected",
        ]

class round_detail_ccaSerializer(serializers.ModelSerializer):
    band = ReadOnlyField(source='item.band')
    max_block = ReadOnlyField(source='item.max_block')
    spectrum_cap = ReadOnlyField(source='item.spectrum_cap')
    #item_lelang = ReadOnlyField(source='parent.item_lelang')
    class Meta:
        model = models.round_detail_cca
        fields = [
            "id",
            "price",
            "block",
            "prev_price",
            "prev_block",
            "max_block",
            "spectrum_cap",
            "eli_per_block",
            "parent",
            "item",
            "band",
            "valid",
            "harga_minimal"
            #"item_lelang",
        ]

class auctioner_hasilSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.auctioner_hasil_cca
        fields = [
            "id",
            "round",
            "item",
            "item_lelang",
            "block",
            "harga"
        ]

class obyek_seleksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.obyek_seleksi_cca
        fields = [
            "item", "bidder_user", "ipaddress","is_block_ip", "eli_awal","created", "dibuat_oleh", "diubah_oleh"
        ]

class matrix_hasil_crSerializer(serializers.ModelSerializer):
    kombinasi = serializers.JSONField()
    json_agg = serializers.JSONField()

    class Meta:
        model = models.matrix_hasil_cr
        fields = [
            "parent",
            "json_agg",
            "kombinasi",
            "total",
        ]

class matrix2_crSerializer(serializers.ModelSerializer):
    kombinasi = serializers.JSONField()
    json_agg = serializers.JSONField()
    round = ReadOnlyField(source='parent.round')


    class Meta:
        model = models.matrix2_cr
        fields = [
            "parent",
            "json_agg",
            "kombinasi",
            "total",
            "round"
        ]

class hasil_ccaSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField()
    class Meta:
        model = models.hasil_cca
        fields = [
            "round",
            "bidder",
            "item_lelang",
            "valid",
            "detail"
        ]
    def get_detail(elf, obj):
        return matrix_hasil_crSerializer(models.matrix_hasil_cr.objects.all().filter(parent=obj), many=True).data

class price_increaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.cca_price_increase
        fields = ["item","detail_item","rentang_min","rentang_max", "kenaikan"]
