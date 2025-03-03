from rest_framework import generics, viewsets, permissions
from django_filters import rest_framework as filters

from . import serializers
from . import models


class tahun_judulViewSet(viewsets.ModelViewSet):
    """ViewSet for the Users class"""

    queryset = models.tahun_integrasi_users.objects.all()
    serializer_class = serializers.tahun_judulSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('id_user',)
    
class rencana_jadwal_seleksiViewSet(viewsets.ModelViewSet):
    """ViewSet for the Users class"""

    queryset = models.jadwal_seleksinya.objects.all()
    serializer_class = serializers.rencana_jadwal_seleksiSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ('tahun',)
    
class rencana_seleksis_seleksiViewSet(viewsets.ModelViewSet):
    """ViewSet for the Users class"""

    queryset = models.rencana_seleksinya.objects.all()
    serializer_class = serializers.rencana_seleksis_seleksiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('tahun',)
