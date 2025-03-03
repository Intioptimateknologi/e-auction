from rest_framework import generics, viewsets, permissions, pagination
from django_filters import rest_framework as filters

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers
from . import models


class bannerViewSet(viewsets.ModelViewSet):
    """ViewSet for the banner class"""

    queryset = models.banner.objects.all()
    serializer_class = serializers.bannerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
            serializer.save(dibuat_oleh=self.request.user)
    def perform_update(self, serializer):
            serializer.save(updated_by=self.request.user)


class aturan_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the aturan_lelang class"""

    queryset = models.aturan_lelang.objects.all()
    serializer_class = serializers.aturan_lelangSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
            serializer.save(dibuat_oleh=self.request.user)
    def perform_update(self, serializer):
            serializer.save(updated_by=self.request.user)

class aturan_lelang2ViewSet(viewsets.ModelViewSet):
    """ViewSet for the aturan_lelang class"""

    queryset = models.aturan_lelang.objects.all()
    serializer_class = serializers.aturan_lelangSerializer
    
class notice_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the aturan_lelang class"""

    queryset = models.notice_lelang.objects.all()
    serializer_class = serializers.notice_lelangSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
            serializer.save(dibuat_oleh=self.request.user)
    def perform_update(self, serializer):
            serializer.save(updated_by=self.request.user)

class history_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the history_lelang class"""

    queryset = models.history_lelang.objects.all()
    serializer_class = serializers.history_lelangSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class history_lelang2ViewSet(viewsets.ModelViewSet):
    """ViewSet for the history_lelang class"""

    queryset = models.history_lelang.objects.all()
    serializer_class = serializers.history_lelangSerializer
    

class portal_blockViewSet(viewsets.ModelViewSet):
    """ViewSet for the portal_block class"""

    queryset = models.portal_block.objects.all()
    serializer_class = serializers.portal_blockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)

class lelang_mancanegaraViewSet(viewsets.ModelViewSet):
    """ViewSet for the lelang_mancanegara class"""

    queryset = models.lelang_mancanegara.objects.all()
    serializer_class = serializers.lelang_mancanegaraSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class lelang_mancanegara2ViewSet(viewsets.ModelViewSet):
    """ViewSet for the lelang_mancanegara class"""

    queryset = models.lelang_mancanegara.objects.all()
    serializer_class = serializers.lelang_mancanegaraSerializer
    

class istilah_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the istilah_lelang class"""

    queryset = models.istilah_lelang.objects.all()
    serializer_class = serializers.istilah_lelangSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class profilViewSet(viewsets.ModelViewSet):
    """ViewSet for the istilah_lelang class"""

    queryset = models.profil.objects.all()
    serializer_class = serializers.profilSerializer
    permission_classes = [permissions.IsAuthenticated]