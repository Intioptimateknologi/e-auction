from . import models
from rest_framework import serializers


class tahun_judulSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.tahun_integrasi_users
        fields = [
            "id",
            "id_user",
            "id_tahun_judul",
        ]

class rencana_jadwal_seleksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.jadwal_seleksinya
        fields = [
            "id",
            "nama_seleksi",
            "tanggal_mulai",
            "tanggal_selesai",
            "status"
        ]
        
class rencana_seleksis_seleksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.rencana_seleksinya
        fields = [
            "id",
            "judul",
            "tahun"
        ]
