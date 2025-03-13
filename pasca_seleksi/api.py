from rest_framework import viewsets, permissions, status
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from adm_lelang.models import bidder_lelang, item_lelang, detail_itemlelang
from smra2.models import hasil2_smra
from userman.models import bidder
from django.shortcuts import get_object_or_404
#from beauty_contest.models import hasil_beauty_contest
#from gabungan.models import hasil_gabungan
#from negosiasi.models import hasil_negosiasi
#from cca.models import hasil2_detail_cca
from rest_framework.response import Response
import django_filters
from rest_framework.exceptions import ValidationError

from . import serializers
from . import models
from . import utils

class blokViewSet(viewsets.ModelViewSet):

    queryset = models.blok.objects.all()
    serializer_class = serializers.blokSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

class pemilihan_blok_pasca_seleksiViewSet(viewsets.ModelViewSet):

    queryset = models.pemilihan_blok_pasca_seleksi.objects.all()
    serializer_class = serializers.pemilihan_blok_pasca_seleksiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

    def partial_update(self, request, pk=None):
        pilblok = get_object_or_404(models.pemilihan_blok_pasca_seleksi, pk=pk)
        serializer = self.get_serializer(pilblok, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            utils.ws_publish_auctioneer({"sender":"paska_seleksi_pilih_blok", "message": "Bidder sudah memilih"})
            return Response(serializer.data, status=status.HTTP_200_OK)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        


    @action(detail=True, methods=['get'])
    def init(self, request, pk=None):
        #itm_lelang = item_lelang.objects.get(pk=pk)
        itm_llg = detail_itemlelang.objects.all().filter(item_lelang__id=pk, disabled=False)
        models.pemilihan_blok_pasca_seleksi.objects.all().filter(item__item_lelang__id=pk).delete()
        source = request.GET.get('source', None)
        id = []
        for itm in itm_llg:
            id.append(itm)
        #data = None
        #print(source)
        if source=='SMRA':
            for i in id:
                sum_penawaran = detail_itemlelang.objects.all().get(pk=i.id)
                max_block = sum_penawaran.max_block
                dt = hasil2_smra.objects.all().filter(item = i).order_by('-price', 'submit')[:max_block]
                rank = 1
                for j in dt:
                    a = models.pemilihan_blok_pasca_seleksi(bidder = j.bidder, item = j.item, ranking = rank, penawaran = j.price)
                    a.save()
                    rank += 1
        elif source == 'BC':
            for i in id:
                sum_penawaran = detail_itemlelang.objects.all().get(pk=i.id)
                max_block = sum_penawaran.max_block
                data = hasil_beauty_contest.objects.all().filter(item = i).order_by('-penilaian')[:max_block]
                #print(i.id)
                for j in data:
                    a = models.pemilihan_blok_pasca_seleksi(bidder = j.bidder, item = j.item, ranking = j.ranking)
                    a.save()
        elif source == 'GAB':
            for i in id:
                sum_penawaran = detail_itemlelang.objects.all().get(pk=i.id)
                max_block = sum_penawaran.max_block
                data = hasil_gabungan.objects.all().filter(item = i).order_by('-total')[:max_block]
                #print(data)
                for j in data:
                    a = models.pemilihan_blok_pasca_seleksi(bidder = j.bidder, item = j.item, ranking = j.ranking)
                    a.save()

        elif source == 'NEGO':
            for i in id:
                sum_penawaran = detail_itemlelang.objects.all().get(pk=i.id)
                max_block = sum_penawaran.max_block
                data = hasil_negosiasi.objects.all().filter(item = i).order_by('-harga')[:max_block]
                #print(data)
                for j in data:
                    a = models.pemilihan_blok_pasca_seleksi(bidder = j.bidder, item = j.item, ranking = j.ranking)
                    a.save()

        elif source == 'CCA':
            for i in id:
                sum_penawaran = detail_itemlelang.objects.all().get(pk=i.id)
                max_block = sum_penawaran.max_block
                data = hasil2_detail_cca.objects.all().filter(item = i).order_by('-parent__round','-price')[:max_block]
                #print(data)
                for j in data:
                    a = models.pemilihan_blok_pasca_seleksi(bidder = j.parent.bidder, item = j.item, ranking = j.ranking_putaran)
                    a.save()            

        return Response({"status":"Ok"})

    @action(detail=True, methods=['get'])
    def toggle1(self, request, pk=None):
        data = models.pemilihan_blok_pasca_seleksi.objects.get(pk=pk)
        data.pilih_blok = not data.pilih_blok
        utils.ws_publish_bidder({"sender":"paska_seleksi_pilih_blok", "message": data.pilih_blok})
        data.save()
        return Response({"status":"Ok"})

    @action(detail=True, methods=['get'])
    def reset(self, request, pk=None):
        data = models.pemilihan_blok_pasca_seleksi.objects.get(pk=pk)
        data.pilih_blok = False
        data.persetujuan = False
        data.blok = None
        utils.ws_publish_bidder({"sender":"paska_seleksi_pilih_blok", "message": data.pilih_blok})
        data.save()
        return Response({"status":"Ok"})
        
    @action(detail=True, methods=['get'])
    def toggle2(self, request, pk=None):
        data = models.pemilihan_blok_pasca_seleksi.objects.get(pk=pk)
        data.persetujuan = not data.persetujuan
        utils.ws_publish_bidder({"sender":"paska_seleksi_persetujuan_blok", "message": data.persetujuan})
        data.save()
        return Response({"status":"Ok"})

    @action(detail=True, methods=['patch'])
    def edit_keterangan(self, request, pk=None):
        data = models.pemilihan_blok_pasca_seleksi.objects.get(pk=pk)
        data.keterangan = request.data['keterangan']
        data.save()
        return Response({"status":"Ok"})


class seleksiViewSet(viewsets.ModelViewSet):

    queryset = models.seleksi.objects.all()
    serializer_class = serializers.seleksiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

class sanggahanViewSet(viewsets.ModelViewSet):

    queryset = models.sanggahan.objects.all()
    serializer_class = serializers.sanggahanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

class sanggahan_jawabanViewSet(viewsets.ModelViewSet):

    queryset = models.sanggahan_jawaban.objects.all()
    serializer_class = serializers.sanggahan_jawabanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

class jawaban_atas_sanggahanViewSet(viewsets.ModelViewSet):

    queryset = models.jawaban_atas_sanggahan.objects.all()
    serializer_class = serializers.jawaban_atas_sanggahanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

class pemenangViewSet(viewsets.ModelViewSet):

    queryset = models.pemenang.objects.all()
    serializer_class = serializers.pemenangSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class pengumuman_pemenangViewSet(viewsets.ModelViewSet):

    queryset = models.pengumuman_pemenang.objects.all()
    serializer_class = serializers.pengumuman_pemenangSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

class berita_acara_pasca_seleksiViewSet(viewsets.ModelViewSet):

    queryset = models.berita_acara_pasca_seleksi.objects.all()
    serializer_class = serializers.berita_acara_pasca_seleksiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('owner',)

class form_ps_sanggahanViewSet(viewsets.ModelViewSet):

    queryset = models.form_ps_sanggahan.objects.all()
    serializer_class = serializers.form_ps_sanggahanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang','bidder',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)
        
class undangan_ps_sanggahanViewSet(viewsets.ModelViewSet):

    queryset = models.undangan_ps_sanggahan.objects.all()
    serializer_class = serializers.undangan_ps_sanggahanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

class jawaban_ps_sanggahanViewSet(viewsets.ModelViewSet):

    queryset = models.jawaban_ps_sanggahan.objects.all()
    serializer_class = serializers.jawaban_ps_sanggahanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class blok_paska_seleksiViewSet(viewsets.ModelViewSet):

    queryset = models.blok_pasca_seleksi.objects.all()
    serializer_class = serializers.blok_paska_seleksiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item',)

    def perform_create(self, serializer):
        item = serializer.validated_data.get('item')
        itm_lelang = detail_itemlelang.objects.get(id=item.id if hasattr(item, 'id') else item)
        current_count = models.blok_pasca_seleksi.objects.filter(item=item).count()
        if current_count >= itm_lelang.max_block:
            raise ValidationError("Blok telah mencapai limit untuk Obyek Seleksi "+itm_lelang.band +"/"+itm_lelang.cakupan+".")
        serializer.save()

    @action(detail=True, methods=['get'])
    def toggle1(self, request, pk=None):
        data = models.blok_pasca_seleksi.objects.get(pk=pk)
        bid = request.GET.get('bidder', 1)
        bdr = bidder.objects.get(pk=bid)
        data.pilih_blok = not data.pilih_blok
        if data.pilih_blok:
            data.bidder = bdr
        else:
            data.bidder = None
        data.save()
        return Response({"status":"Ok"})

    @action(detail=True, methods=['get'])
    def toggle2(self, request, pk=None):
        data = models.blok_pasca_seleksi.objects.get(pk=pk)
        data.sudah_pilih = not data.sudah_pilih
        bid = request.GET.get('bidder', 1)
        bdr = bidder.objects.get(pk=bid)
        if data.pilih_blok:
            data.owner = bdr.id
        else:
            data.owner = None

        data.save()
        return Response({"status":"Ok"})

    @action(detail=True, methods=['get'])
    def toggle3(self, request, pk=None):
        data = models.blok_pasca_seleksi.objects.get(pk=pk)
        data.approved = not data.approved
        bid = request.GET.get('bidder', 1)
        bdr = bidder.objects.get(pk=bid)
        data.save()
        return Response({"status":"Ok"})

class pemenang_blok_paska_seleksiViewSet(viewsets.ModelViewSet):

    queryset = models.pemilihan_blok_pasca_seleksi.objects.all()
    serializer_class = serializers.pemenang_blok_pasca_seleksiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang','item','bidder','ranking',"penawaran","keterangan")

    