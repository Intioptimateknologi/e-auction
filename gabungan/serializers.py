from rest_framework import serializers

from . import models


class penentuan_parameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.penentuan_parameter
        fields = [
            "id",
            "created",
            "obyek_bc",
            "bobot",
            "obyek_smra",
            "bobot2",
            "item",
            "last_updated",
        ]

class ba_gabunganSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ba_gabungan
        fields = [
            "last_updated",
            "created",
            "dokumen_ba",
            "item_lelang",
        ]
        
class penilaian_gabunganSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.penilaian_gabungan
        fields = [
            "last_updated",
            "created",
            "penilaian",
            "bobot",
            "bidder",
            "parameter",
            "item_lelang",
        ]