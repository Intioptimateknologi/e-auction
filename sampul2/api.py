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

class obsel_sampul2ViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_penawaran class"""

    queryset = models.obyek_seleksi_sampul2.objects.all()
    serializer_class = serializers.obyek_seleksi_sampul2Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class hasil_sampul2ViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_penawaran class"""

    queryset = models.hasil_sampul2.objects.all()
    serializer_class = serializers.hasil_sampul2Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item','bidder',)
