from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField

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

class round_cca2Serializer(serializers.ModelSerializer):
    band = ReadOnlyField(source='item.band')
    spectrum_cap = ReadOnlyField(source='item.spectrum_cap')
    max_block = ReadOnlyField(source='item.max_block')
    status_round = ChoiceField(models.round_cca2.STATUS.choices)
    class Meta:
        model = models.round_cca2
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
            "penawaran"
        ]


class hasil_cca2Serializer(serializers.ModelSerializer):
    band = ReadOnlyField(source='item.band')
    nama_bidder = ReadOnlyField(source='bidder.nama_perusahaan')

    class Meta:
        model = models.hasil_cca2
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
            "valid"
        ]



class jadwalSMRASerializer(serializers.ModelSerializer):

    class Meta:
        model = models.round_schedule_smra
        fields = [
            "id",
            "mulai",
            "selesai",
            "hari",
            "item",
        ]

STATUS =(
        ("STA", "START"),
        ("STO", "STOP"),
        ("SUS", "SUSPEND"),
        ("CLO", "CLOSED"),
        ("INI","INIT"),
        ("NON","NONE"))
class bidding_round_smraSerializer(serializers.ModelSerializer):
    
    #status_round = ChoiceField(choices=models.bidding_round_smra.STATUS)
    status_round = serializers.SerializerMethodField()

    class Meta:
        model = models.bidding_round_smra
        fields = [
            "round_state",
            "item",
            "status_round",
            "start_time",
            "stop_time"
        ]
    def get_status_round(self, obj):
        return obj.get_status_round_display()

class round_smraSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.round_smra
        fields = [
            "price",
            "block",
            "bidder",
            "item",
            "prev_price",
            "prev_block",
            "min_price"
        ]

class round_smra_sumSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.round_smra_sum
        fields = [
            "price",
            "activity",
            "bidder",
            "item",
        ] 
    
class round_smra_tempSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.round_smra_temp
        fields = [
            "price",
            "block",
            "bidder",
            "item",
            "prev_price",
            "prev_block",
        ]

"""class smra_roundSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.auction_summary_smra
        fields = [
            "band",
            "max_block",
            "spectrum_cap",
            "eligibility_point_per_block",
           # "bidder",
            "item_id",
            "reserved_price",
            #"prev_price",
            #"prev_block",
            "count"
        ]

class smra_bid_bidderSMRASerializer(serializers.ModelSerializer):

    class Meta:
        model = models.bid_bidder_smra
        fields = [
            "band",
            "block",
            "spectrum_cap",
            "object_id",
            "item_id",
            "bidder_id",
            "eligibility_point_per_block",
            "reserved_price",
            "available_block",
            "penawaran",
            "round",
            "prev_block",
            "prev_price",
            "min_price"
        ]"""

class undangan_SMRA_CCASerializer(serializers.ModelSerializer):

    class Meta:
        model = models.undangan_smra_cca
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
            "link_teleconference",
            "keterangan",
            "link_file",
            "owner",
        ]

class berita_acara_lelangSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.berita_acara_lelang
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
        ]