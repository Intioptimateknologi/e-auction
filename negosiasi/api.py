from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from . import serializers
from . import models
from adm_lelang.models import bidder_lelang, auctioner_lelang, viewers_lelang, item_lelang, detail_itemlelang
from userman.models import Users, bidder, tim_lelang, viewers, bidder_perwakilan
from django.template.loader import render_to_string
from rest_framework.response import Response
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from pprint import pprint

class penyampaian_penawaranViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_penawaran class"""

    queryset = models.penawaran.objects.all()
    serializer_class = serializers.penyampaian_penawaranSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item',)
    
    def perform_update(self, serializer):
        user_type = self.request.user.user_type
        if user_type == 'C':
            serializer.save(verified_by=self.request.user)
        else:
            serializer.save()

class penyampaian_penawaran2ViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_penawaran class"""

    queryset = models.revisi_penawaran.objects.all()
    serializer_class = serializers.revisi_penyampaian_penawaranSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item',)
    def perform_create(self, serializer):
        user_type = self.request.user.user_type
        if user_type == 'B':
            serializer.save(dibuat_oleh=self.request.user)
    def perform_update(self, serializer):
        user_type = self.request.user.user_type
        if user_type == 'C':
            serializer.save(verified_by=self.request.user)
        else:
            serializer.save(diubah_oleh=self.request.user)
        
    
class evaluasi_penyampaian_penawaranViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_penawaran class"""

    queryset = models.evaluasi_penawaran.objects.all()
    serializer_class = serializers.evaluasi_penawaranSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('penawaran__item',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class revisi_evaluasi_penyampaian_penawaranViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_penawaran class"""

    queryset = models.evaluasi_revisi_penawaran.objects.all()
    serializer_class = serializers.evaluasi_penawaran2Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('revisi_penawaran__item',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)
    
    @action(detail=True, methods=['get'])
    def init(self, request, pk=None):
        hasil = models.evaluasi_revisi_penawaran.objects.all().filter(revisi_penawaran__item__item_lelang__id=pk, hasil='Diterima')
        m = models.hasil_negosiasi.objects.filter(item__item_lelang__id=pk)
        m.delete()

        retval = []
        for h in hasil:
            for k in range(0,h.revisi_penawaran.blok):
                m = models.hasil_negosiasi(bidder=h.revisi_penawaran.bidder, item = h.revisi_penawaran.item, harga=h.revisi_penawaran.harga, ranking = 0)
                m.save()
#            retval.append({'item':h.revisi_penawaran.item.id, 'bidder': h.revisi_penawaran.bidder.id,'harga':h.revisi_penawaran.harga, 'blok':h.revisi_penawaran.blok})
        m = models.hasil_negosiasi.objects.filter(item__item_lelang__id=pk)
        for h in m:
            d = detail_itemlelang.objects.get(id = h.item.id)
            max_blok = d.max_block
            sub = models.hasil_negosiasi.objects.filter(item = h.item.id).order_by('-harga')
            rangking = 1
            for s in sub:
                l = models.hasil_negosiasi.objects.get(id=s.id)
                l.ranking = rangking
                l.save()
                rangking = rangking + 1
                if rangking > max_blok:
                    break

        return Response({"status":max_blok})

class obsel_negoViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_penawaran class"""

    queryset = models.obyek_seleksi_nego.objects.all()
    serializer_class = serializers.obyek_seleksi_negoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class hasil_negoViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_penawaran class"""

    queryset = models.hasil_negosiasi.objects.all()
    serializer_class = serializers.hasil_negoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item','bidder',)