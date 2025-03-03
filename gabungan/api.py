from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from adm_lelang.models import bidder_lelang, item_lelang, detail_itemlelang
from rest_framework.response import Response

from . import serializers
from . import models
from beauty_contest.models import sum_penilaian
from smra2.models import hasil_highest, hasil2_smra
from django_filters import rest_framework as filters
import json



class penentuan_parameterViewSet(viewsets.ModelViewSet):
    """ViewSet for the penentuan_parameter class"""

    queryset = models.penentuan_parameter.objects.all()
    serializer_class = serializers.penentuan_parameterSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item',)


class ba_gabunganViewSet(viewsets.ModelViewSet):
    """ViewSet for the ba_gabungan class"""

    queryset = models.ba_gabungan.objects.all()
    serializer_class = serializers.ba_gabunganSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

class penilaian_gabunganViewSet(viewsets.ModelViewSet):
    """ViewSet for the ba_gabungan class"""

    queryset = models.penilaian_gabungan.objects.all()
    serializer_class = serializers.penilaian_gabunganSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

    @action(detail=True, methods=['get'])
    def init(self, request, pk=None):
        #itm_lelang = item_lelang.objects.get(pk=pk)
        models.penilaian_gabungan.objects.all().filter(item__item_lelang__id=pk).delete()
        models.hasil_gabungan.objects.all().filter(item__item_lelang__id=pk).delete()
        models.hasil2_gabungan.objects.all().filter(item__item_lelang__id=pk).delete()
        #bidder = bidder_lelang.objects.all().filter(item__item_lelang__id=pk)
        bobot = models.penentuan_parameter.objects.all().filter(item__id=pk)

        for bbt in bobot:
            #high_price_smra = hasil_highest.objects.all().filter(item=bbt.obyek_smra).order_by('-price')[0]
            smra = hasil_highest.objects.all().filter(item=bbt.obyek_smra).order_by('-price')
            highest_price = 1
            if smra:
                highest_price = smra[0].price
            for s in smra:
                updated_values = {'penilaian':s.price/highest_price*100, "bobot":bbt.bobot2}
                models.penilaian_gabungan.objects.update_or_create(bidder=s.bidder, item=bbt.obyek_smra, parameter='1', defaults=updated_values)   

            bc = sum_penilaian.objects.all().filter(item=bbt.obyek_bc)
            for b in bc:
                updated_values = {'penilaian':b.sum, "bobot":bbt.bobot}
                models.penilaian_gabungan.objects.update_or_create(bidder=b.bidder, item=bbt.obyek_bc, parameter='3', defaults=updated_values)   
        
        itm_lelang = detail_itemlelang.objects.filter(item_lelang__id=pk)
        for i in itm_lelang:
            sum_penawaran = detail_itemlelang.objects.all().get(id=i.id)
            max_block = sum_penawaran.max_block
            hasil = hasil2_smra.objects.all().filter(item=i,valid=True,ranking__isnull=False).order_by('-round','ranking')[:max_block]
            for h in hasil:
                nilai_smra = models.penilaian_gabungan.objects.all().filter(bidder=h.bidder, item=i, parameter='1')
                nilai_bc = models.penilaian_gabungan.objects.all().filter(bidder=h.bidder, item=i, parameter='3')
                if nilai_smra and nilai_bc:
                    bobot = models.penentuan_parameter.objects.all().filter(obyek_smra=i)[0]
                    a = models.hasil_gabungan(item = i, bidder = h.bidder, harga=h.price, total = nilai_smra[0].penilaian * bobot.bobot2/100.0 + nilai_bc[0].penilaian * bobot.bobot/100.0)
                    a.save()

            m = models.hasil_gabungan.objects.all().filter(item=i).order_by("-total")
            i = 1
            for a in m:
                a.ranking = i
                a.save()
                i = i + 1

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
                #models.penilaian_bc.objects.update_or_create(id=id, defaults=updated_values)

        return Response({"status":data})