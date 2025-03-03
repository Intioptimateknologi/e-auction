from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from adm_lelang.models import item_lelang
from rest_framework.response import Response

from . import serializers
from . import models


class form_pemeriksaanViewSet(viewsets.ModelViewSet):

    queryset = models.form_pemeriksaan.objects.all()
    serializer_class = serializers.form_pemeriksaanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class berita_acara_allViewSet(viewsets.ModelViewSet):

    queryset = models.berita_acara_administrasi.objects.all()
    serializer_class = serializers.berita_acara_allSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('owner',)

class hasilKesimpulanViewSet(viewsets.ModelViewSet):

    queryset = models.hasil_kesimpulan.objects.all()
    serializer_class = serializers.hasilKesimpulanSerialiser
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class permohonan_keikutsertaanViewSet(viewsets.ModelViewSet):

    queryset = models.permohonan_keikutsertaan.objects.all()
    serializer_class = serializers.permohonan_keikutsertaanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang','perwakilan',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user, bidder=self.request.user.bidder_user)
        
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class form_verifikasiViewSet(viewsets.ModelViewSet):

    queryset = models.form_verifikasi.objects.all()
    serializer_class = serializers.form_verifikasiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class form_evaluasiViewSet(viewsets.ModelViewSet):

    queryset = models.form_evaluasi.objects.all()
    serializer_class = serializers.form_evaluasiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)
    
    @action(detail=True, methods=['get'])
    def init(self, request, pk=None):
        itm_lelang = item_lelang.objects.all().get(pk =pk)
        """      form_pemeriksaan = models.form_evaluasi.objects.all().filter(item_lelang__id = pk)
                form_verifikasi = models.form_verifikasi.objects.all().filter(item_lelang__id = pk)
                bdr_lelang = model_admlelang.bidder_lelang.objects.all().filter(item_lelang__id = pk)
                id_bdr_lelang = []
                for bl in bdr_lelang:
                    id_bdr_lelang.append(bl.bidder.id)
                bdr = model_userman.bidder_users.objects.all().filter(id__in = id_bdr_lelang)
        """
        form_kesimpulan = models.hasil_kesimpulan.objects.all().filter(item_lelang = itm_lelang)
        print(form_kesimpulan)
        for f in form_kesimpulan:
            updated_values = {'keterangan':'',
                    "hasil_pemeriksaan":False
                }
            print(f.bidder)
            models.form_evaluasi.objects.update_or_create(bidder=f.bidder, item_lelang = itm_lelang, defaults=updated_values)
        return Response({"status":"OK"})

class form_sanggahanViewSet(viewsets.ModelViewSet):

    queryset = models.form_sanggahan.objects.all()
    serializer_class = serializers.form_sanggahanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang','bidder',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class hasil_evaluasiViewSet(viewsets.ModelViewSet):

    queryset = models.hasil_evaluasi.objects.all()
    serializer_class = serializers.hasil_evaluasiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class jawaban_sanggahanViewSet(viewsets.ModelViewSet):

    queryset = models.jawaban_sanggahan.objects.all()
    serializer_class = serializers.jawaban_sanggahanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)
