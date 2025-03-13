from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from drf_extra_fields.fields import DecimalRangeField
from adm_lelang.models import detail_itemlelang
from userman.models import bidder_user
from datetime import datetime, timezone

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

class price_increaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.price_increase
        fields = ["item","detail_item","rentang_min","rentang_max", "kenaikan"]

class detail_itemlelangSerializer(serializers.ModelSerializer):

    class Meta:
        model = detail_itemlelang
        fields = [
            "id",
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
            # 
        ]

class sum_round_smra2Serializer(serializers.ModelSerializer):
    #detail_itemlelang = detail_itemlelangSerializer(read_only = True)
    band = serializers.SerializerMethodField()
    #band = ReadOnlyField(source='item.band')
    spectrum_cap = ReadOnlyField(source='item.spectrum_cap')
    max_block = ReadOnlyField(source='item.max_block')
    status_round = ChoiceField(models.round_smra2.STATUS.choices)
    sisa = serializers.SerializerMethodField()
    class Meta:
        model = models.sum_round_smra2
        fields = [
            "id","round","mulai1","selesai1","count","item","item_lelang","status_round","max_block","spectrum_cap",
            "band", "min_price","prev_price","khusus","sisa"
        ]
    def get_band(self, obj):
        itm = obj.item
        return detail_itemlelangSerializer(detail_itemlelang.objects.all().filter(id=itm.id), many=True).data
    def get_sisa(self, obj):
        return 0
        
class round_smraSerializer(serializers.ModelSerializer):
    band = serializers.SerializerMethodField()
    spectrum_cap = ReadOnlyField(source='item.spectrum_cap')
    max_block = ReadOnlyField(source='item.max_block')
    status_round = ChoiceField(models.round_smra2.STATUS.choices)
    sisa = serializers.SerializerMethodField()
    class Meta:
        model = models.round_smra2
        fields = [
            "id",
            "price",
            "block",
            "bidder",
            "item",
            "prev_price",
            "prev_block",
            "min_price",
            "status_round",
            "mulai",
            "selesai",
            "round",
            "item_lelang",
            "band",
            "max_block",
            "spectrum_cap",
            "lock",
            "penawaran",
            "khusus",
            "ext_data",
            "sisa",
            "otp"
        ]
    def get_sisa(self, obj):
        return 0
    def get_band(self, obj):
        return obj.item.band + "-" + obj.item.cakupan


class hasil_smra2Serializer(serializers.ModelSerializer):
    band = ReadOnlyField(source='item.band')
    nama_bidder = ReadOnlyField(source='bidder.nama_perusahaan')

    class Meta:
        model = models.hasil_smra2
        fields = [
            "id",
            "price",
            "block",
            "bidder",
            "item",
            "round",
            "item_lelang",
            "nama_bidder",
            "band",
            "submit",
            "penawaran",
            "valid",
            "berita_acara"
        ]

class auctioner_hasilSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.auctioner_hasil
        fields = [
            "id",
            "round",
            "item",
            "item_lelang",
            "block",
            "harga"
        ]

class hasil_highestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.hasil_highest
        fields = [
            "id",
            "bidder",
            "item_lelang",
            "harga",
            "round"
        ]

class bidder_usersSerializer(serializers.ModelSerializer):
    nama_perusahaan = serializers.ReadOnlyField(source='bidder.nama_perusahaan')
    nama_user = serializers.ReadOnlyField(source='users.nama_lengkap')
    username = serializers.ReadOnlyField(source='users.username')
    
    class Meta:
        model = bidder_user
        fields = [
            "id",
            "nama_perusahaan",
            "nama_user",
            "username"
        ]

class jadwalSMRASerializer(serializers.ModelSerializer):
    class Meta:
        model = models.round_schedule_smra2
        fields = [
            "id",
            "mulai",
            "selesai",
            "hari",
            "item",
        ]

class obyek_seleksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.obyek_seleksi_smra
        fields = [
            "item", "bidder_user", "ipaddress","is_block_ip", "blok_awal","created", "dibuat_oleh", "diubah_oleh"
        ]