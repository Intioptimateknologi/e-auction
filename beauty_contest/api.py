from rest_framework import viewsets, permissions

from rest_framework.decorators import action
from adm_lelang.models import bidder_lelang, item_lelang, detail_itemlelang
from rest_framework.response import Response
from django_filters import rest_framework as filters
from . import serializers
from . import models
import json
import django_filters.rest_framework
from userman.models import bidder_user



class parameter_evaluasiViewSet(viewsets.ModelViewSet):
    """ViewSet for the parameter_evaluasi class"""

    queryset = models.parameter_evaluasi.objects.all()
    serializer_class = serializers.parameter_evaluasiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class dokumen_bcViewSet(viewsets.ModelViewSet):
    """ViewSet for the dokumen_bc class"""

    queryset = models.dokumen_bc.objects.all()
    serializer_class = serializers.dokumen_bcSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class format_dokumen_bcViewSet(viewsets.ModelViewSet):
    """ViewSet for the dokumen_bc class"""

    queryset = models.format_dokumen_bc.objects.all()
    serializer_class = serializers.format_dokumen_bcSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)


class sum_penilaianViewSet(viewsets.ModelViewSet):
    """ViewSet for the pengumuman_bc class"""

    queryset = models.sum_penilaian.objects.all()
    serializer_class = serializers.sum_penilaianSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

class hasil_bcViewSet(viewsets.ModelViewSet):
    """ViewSet for the pengumuman_bc class"""

    queryset = models.hasil_beauty_contest.objects.all()
    serializer_class = serializers.hasil_beautycontestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)

    @action(detail=True, methods=['get'])
    def init(self, request, pk=None):
        itm_lelang = models.penilaian_bc.objects.all().filter(item__item_lelang__id=pk)
        #.distinct("bidder")
        id = []
        for it in itm_lelang:
            id.append(it.item.id)
        models.hasil_beauty_contest.objects.all().filter(item__id__in=id).delete()
        obj = models.obyek_seleksi_bc.objects.all().filter(item__id__in=id)
        for i in obj:

        #for i in itm_lelang:
            #obj = models.obyek_seleksi_bc.objects.all().filter(item=i.item)
            #for b in obj:
            nilai = models.penilaian_bc.objects.all().filter(bidder=i.bidder_user, item=i.item)
            total = 0
            for n in nilai:
                total = total + n.penilaian*n.bobot
            #ob = models.obyek_seleksi_bc.objects.all().filter(item = i.item, bidder_user = i.bidder_user)[0]
            if i.block:
                for k in range(0,i.block):
                    a = models.hasil_beauty_contest(item = i.item, bidder = i.bidder_user, penilaian=total/100.0)
                    a.save()
            m = models.hasil_beauty_contest.objects.all().filter(item=i.item).order_by("-penilaian")
            i = 1
            for a in m:
                a.ranking = i
                a.save()
                i = i + 1

        

        return Response({"status":"Ok"})


class input_penilaian_bcViewSet(viewsets.ModelViewSet):
    """ViewSet for the pengumuman_bc class"""

    queryset = models.penilaian_bc.objects.all().order_by("parameter")
    serializer_class = serializers.input_penialianSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

    @action(detail=True, methods=['get'])
    def init(self, request, pk=None):
        itm_lelang = models.obyek_seleksi_bc.objects.all().filter(item__item_lelang__id=pk)
        id = []
        for it in itm_lelang:
            id.append(it.item.id)
        models.penilaian_bc.objects.all().filter(item__id__in=id).delete()
        #bidder = models.obyek_seleksi_bc.objects.all().filter(item__in=itm_lelang)
        #print(bidder)
        for i in itm_lelang:
            bdr = models.obyek_seleksi_bc.objects.all().filter(item=i.item)
            for b in bdr:
                parameter = models.parameter_evaluasi.objects.all().filter(item=i.item)
                for p in parameter:
                    updated_values = {'penilaian':0, 'bobot':p.bobot}
                    models.penilaian_bc.objects.update_or_create(bidder=b.bidder_user, item=i.item, parameter=p, defaults=updated_values)   
        return Response({"status":"Ok"})

    @action(detail=False, methods=['post'])
    def submit_bid(self, request):
        data = request.data
        print(data)
        for d in data:
            for i in d:
                js = i['key']
                id = js['id']
                penilaian = js['penilaian']
                updated_values = {'penilaian':penilaian}
                models.penilaian_bc.objects.update_or_create(id=id, defaults=updated_values)

        return Response({"status":data})

class obyek_seleksiViewSet(viewsets.ModelViewSet):

    queryset = models.obyek_seleksi_bc.objects.all()
    serializer_class = serializers.obyek_seleksibcSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)
