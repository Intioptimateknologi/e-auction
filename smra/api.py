from rest_framework import generics, status, viewsets, permissions
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import filters
import json
from datetime import datetime, date
from . import serializers
from . import models
from . import tasks
from userman.models import Users, bidder, tim_lelang, viewers, bidder_perwakilan
from adm_lelang.models import bidder_lelang, auctioner_lelang, viewers_lelang, item_lelang, detail_itemlelang
from datetime import datetime
from django.utils import timezone
from channels.layers import get_channel_layer
import asyncio
from asgiref.sync import async_to_sync, sync_to_async
import django_filters.rest_framework
from background_task.models import Task as BTask
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from pprint import pprint



from django_pandas.io import read_frame
class round_cca2ViewSet(viewsets.ModelViewSet):

    queryset = models.round_cca2.objects.all().order_by('item')
    serializer_class = serializers.round_cca2Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('item_lelang','bidder', "round")
    def retrieve(self, request, *args, **kwargs):
        print(args)
        print(kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    @action(detail=True, methods=['get'])
    def create_schedule(self, request, pk=None):
        item_llg = item_lelang.objects.all().filter(id=1)[0]
        dt = timezone.now() + timedelta(minutes=10)
        delta = 3
        skip = 5
        data = round_schedule_smra.objects.all()
        for i in range(20):
            updated_values = {'mulai': dt, 'selesai': dt + timedelta(minutes=delta)}
            data = round_schedule_smra(item=item_llg, mulai= dt, selesai= dt + timedelta(minutes=delta))
            data.save()
            dt = dt + timedelta(minutes=skip)
        return Response({"statuss":"OK"})


    @action(detail=True, methods=['get'])
    def init(self, request, pk=None):
        b_task = BTask.objects.all()
        b_task.delete()
        itm_lelang = item_lelang.objects.all().filter(id=pk)[0]
        bidder = bidder_lelang.objects.all().filter(item_lelang=itm_lelang)
        for bdr in bidder:
            item_llg = detail_itemlelang.objects.all().filter(item_lelang=itm_lelang)
            for i in item_llg:
                updated_values = {'status_round':'INI','round':1, 'price':0, 'block':0, 
                    'prev_price':i.reserved_price, 'min_price':i.reserved_price,
                    'mulai': timezone.now(), 'selesai':timezone.now(),
                    'item_lelang':i.item_lelang.id, 'lock':False
                    }
                models.round_cca2.objects.update_or_create(bidder=bdr.bidder, item=i, defaults=updated_values)
                hasil = models.hasil_cca2.objects.all().filter(bidder=bdr.bidder).filter(item=i)
                hasil.delete()
        return Response({"statuss":"OK"})
    
    @action(detail=True, methods=['get'])
    def start(start, request, pk=None):
        item_llg = detail_itemlelang.objects.all().filter(id=pk)[0]
        bidder = bidder_lelang.objects.all().filter(item_lelang=item_llg.item_lelang)
        dt = timezone.now()
        round = round_schedule_smra.objects.all().filter(item=item_llg.item_lelang).filter(mulai__gte=dt).order_by('mulai').first()
        if round:
            for bdr in bidder:
                updated_values = {'status_round':'WAI', 'lock': False, 'mulai': round.mulai, 'selesai':round.selesai}
                models.round_smra2.objects.update_or_create(bidder=bdr.bidder, item=item_llg, defaults=updated_values)
            tasks.round2_start(pk, round.selesai.timestamp(), schedule=round.mulai, verbose_name=str(pk))
            #tasks.round2_stop(pk, schedule=round.selesai, verbose_name=str(pk))
            return Response({"status":"OK"})
        else:
            return Response({"status":"Tidak ada jadwal"})

    @action(detail=True, methods=['get'])
    def resume(start, request, pk=None):
        start(start, request, pk)

    @action(detail=True, methods=['get'])
    def stop(start, request, pk=None):
        b_task = BTask.objects.all()
        b_task.delete()
        item_llg = detail_itemlelang.objects.all().filter(id=pk)[0]
        bidder = bidder_lelang.objects.all().filter(item_lelang=item_llg.item_lelang)
        for bdr in bidder:
            #dt = timezone.now()
            #round = round_schedule_smra.objects.all().filter(item=item_llg.item_lelang).filter(mulai__gte=dt).order_by('mulai').first()
            updated_values = {'status_round':'STO'}
            models.round_smra2.objects.update_or_create(bidder=bdr.bidder, item=item_llg, defaults=updated_values)
        return Response({"statuss":"OK"})
    
    @action(detail=True, methods=['get'])
    def pause(start, request, pk=None):
        b_task = BTask.objects.all()
        b_task.delete()
        item_llg = detail_itemlelang.objects.all().filter(id=pk)[0]
        bidder = bidder_lelang.objects.all().filter(item_lelang=item_llg.item_lelang)
        for bdr in bidder:
            updated_values = {'status_round':'SUS'}
            models.round_smra2.objects.update_or_create(bidder=bdr.bidder, item=item_llg, defaults=updated_values)
        return Response({"statuss":"OK"})

    @action(detail=True, methods=['get'])
    def close(start, request, pk=None):
        b_task = BTask.objects.all()
        b_task.delete()
        item_llg = detail_itemlelang.objects.all().filter(id=pk)[0]
        bidder = bidder_lelang.objects.all().filter(item_lelang=item_llg.item_lelang)
        for bdr in bidder:
            updated_values = {'status_round':'CLO'}
            models.round_smra2.objects.update_or_create(bidder=bdr.bidder, item=item_llg, defaults=updated_values)
        return Response({"statuss":"OK"})

    @action(detail=True, methods=['post'])
    def submit_bid(self, request, pk=None):
        data = request.data
        item_llg = detail_itemlelang.objects.get(pk=data[0]['data']['item'])
        bdr = bidder.objects.get(pk=data[0]['data']['bidder'])
        price = []
        locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 
        for d in data:
            updated_values = {'price':locale.atof(d['price']),'valid':d['valid']}
            price.append({"block":int(d['block']), 'price':locale.atof(d['price']), 'valid':d['valid']})
            hasil = models.hasil_smra2.objects.update_or_create(block=int(d['block']), round=int(d['data']['round']),  bidder=bdr, item=item_llg, item_lelang=item_llg.item_lelang.id, defaults=updated_values)
        obj = models.round_smra2.objects.get(pk=pk)
        obj.penawaran = price
        obj.prev_price = price
        obj.lock= True
        obj.save()

        #print(item_llg)
        #item_llg = detail_itemlelang.objects.all().filter(id=data['item'])[0]
        #bdr = bidder.objects.all().filter(id=data['bidder'])[0]
        #obj = models.round_smra2.objects.all().filter(id=pk)[0]
        ##obj.price = data['price']
        #obj.block=data['block']
        #obj.lock= True
        #obj.save()
        #updated_values = {'price':float(data['price']), 'block':int(data['block']),}
        #hasil = models.hasil_smra2.objects.update_or_create(round=int(data['round']),  bidder=bdr, item=item_llg, item_lelang=item_llg.item_lelang.id, defaults=updated_values)
        return Response({"statuss":"OK"})

class hasil_cca2ViewSet(viewsets.ModelViewSet):

    queryset = models.hasil_cca2.objects.all()
    serializer_class = serializers.hasil_cca2Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('item_lelang',"bidder","round")


class jadwalSMRAViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_sanggahan class"""

    queryset = models.round_schedule_smra.objects.all()
    serializer_class = serializers.jadwalSMRASerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('item',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_create(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

"""class bidding_round_smraViewSet(viewsets.ModelViewSet):
    queryset = models.bidding_round_smra.objects.all()
    serializer_class = serializers.bidding_round_smraSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('item',)
    

    @action(detail=True, methods=['get'])
    def init(self, request, pk=None):
        b_task = BTask.objects.all()
        b_task.delete()
        item_llg = detail_itemlelang.objects.all().filter(item_lelang=pk)
        itm_llg = item_lelang.objects.get(id=pk)
        models.round_smra.objects.filter(item__in=item_llg).delete()
        # get bidder
        bidder = bidder_lelang.objects.all().filter(item_lelang=pk)
        for bdr in bidder:
            for item in item_llg:
                updated_values = {'round_state':1, 'status_round':'INI'}
                models.bidding_round_smra.objects.update_or_create(item=itm_llg, defaults=updated_values)
                updated_values = {'round':1, 'price':0, 'block':0, 'prev_price':item.reserved_price, 'min_price':item.reserved_price}
                models.round_smra.objects.update_or_create(item=item, bidder=bdr.bidder, defaults=updated_values)
        return Response({"statuss":"OK"})

    @action(detail=True, methods=['get'])
    def next_round(self, request, pk=None):
        item_llg = item_lelang.objects.get(id=pk)
        round = models.bidding_round_smra.objects.all().filter(item=item_llg)
        putaran = round[0].round_state
        # increase round
        updated_values = {'round_state':putaran+1, 'status_round':'STA'}
        models.bidding_round_smra.objects.update_or_create(item=item_llg, defaults=updated_values)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang=pk)
        bidder = bidder_lelang.objects.all().filter(item_lelang=pk)
        r_smra = models.round_smra.objects.all().filter(item__in=item_llg).filter(round=putaran)
        for bdr in r_smra:
            if bdr.block==0:
                updated_values = {'price':0, 'block':0, 'prev_price':bdr.prev_price, 'prev_block':bdr.block} # kenaikan harga role di min price
            else:
                updated_values = {'price':0, 'block':0, 'prev_price':bdr.price, 'prev_block':bdr.block,'min_price':bdr.price} # kenaikan harga role di min price
            models.round_smra.objects.update_or_create(item=bdr.item, bidder=bdr.bidder, round=putaran+1, defaults=updated_values)
        return Response({"statuss":"OK"})


    @action(detail=True, methods=['get'])
    def start(self, request, pk=None):
        item_llg = item_lelang.objects.get(id=pk)
        round = models.bidding_round_smra.objects.all().filter(item=item_llg)
        #jadwal = models.round_schedule_smra.objects.all().filter(item=item_llg)
        dt = timezone.now()
        mulai = models.round_schedule_smra.objects.all().filter(item=item_llg).filter(mulai__gte=dt).order_by('mulai').first()
        if mulai:
            putaran = round[0].round_state
            br = models.bidding_round_smra.objects.all().filter(item=pk).filter(round_state=putaran)[0]
            print(br)
            br.status_round = 'WAI'
            br.start_time = mulai.mulai
            br.stop_time = mulai.selesai
            br.save()
            #updated_values = {'status_round':'STA','start_time': mulai.mulai}
            #models.bidding_round_smra.objects.update_or_create(round_state=putaran,item=item_llg, defaults=updated_values)
            #datetime_object = datetime.strptime(mulai, '%Y-%m-%d %H:%M:%S')
            tasks.round_start(pk, schedule=mulai.mulai, verbose_name=str(pk))
            #tasks.round_stop(pk, schedule=mulai.selesai, verbose_name=str(pk))
            return Response({"status":"OK"})
        else:
            return Response({"status":"Tidak ada jadwal terdekat"})

    @action(detail=True, methods=['get'])
    def stop(self, request, pk=None):
        b_task = BTask.objects.all()
        b_task.delete()

        item_llg = item_lelang.objects.get(id=pk)
        round = models.bidding_round_smra.objects.all().filter(item=item_llg)
        putaran = round[0].round_state
        updated_values = {'status_round':'STO'}
        models.bidding_round_smra.objects.update_or_create(round_state=putaran,item=item_llg, defaults=updated_values)
        return Response({"statuss":"OK"})
"""

class round_smraViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_sanggahan class"""

    queryset = models.round_smra.objects.all()
    serializer_class = serializers.round_smraSerializer
    permission_classes = [permissions.IsAuthenticated]


class round_smra_sumViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_sanggahan class"""

    queryset = models.round_smra_sum.objects.all()
    serializer_class = serializers.round_smra_sumSerializer
    permission_classes = [permissions.IsAuthenticated]

class round_smra_tempViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_sanggahan class"""

    queryset = models.round_smra_temp.objects.all()
    serializer_class = serializers.round_smra_tempSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def test(elf, request):
        bdr = bidder_lelang.objects.all().filter(item_lelang=1)
        m = models.round_smra.objects.all().filter(bidder=45)
        df = read_frame(m)
        return Response({'status':'REVEAL', "code": 400})

    @action(detail=False, methods=['post'])
    def submit_bid(self, request):
#        itm_llg = item_lelang.objects.get(id=pk)
#        bdr = bidder_lelang.objects.all().filter(item_lelang=pk)
        item_id = 0
        bidder_id = 0
        round_data = 0
        eli = 0
        price = 0
        for data in request.data:
            bdr = bidder.objects.get(id=data['bidder_id'])
            itm_llg = detail_itemlelang.objects.get(id=data['object_id'])
            item_id = itm_llg
            bidder_id = bdr
            round_data = data['round']
            eli = eli + data['eligibility_point_per_block']*int(data['block'])
            price = price + float(data['penawaran'])*int(data['block'])
            if round_data==1:
                updated_values = {'price': float(data['penawaran']), 'block':int(data['block'])}
                models.round_smra.objects.update_or_create(bidder=bdr, round=data['round'], item=itm_llg, defaults=updated_values)
            else:
                updated_values = {'price': float(data['penawaran']), 'prev_price': float(data['prev_price']), 'block':int(data['block']),'prev_block':int(data['prev_block'])}
                models.round_smra_temp.objects.update_or_create(bidder=bdr, round=data['round'], item=itm_llg, defaults=updated_values)
        if (round_data==1):
            updated_values = {'price': price, 'activity':eli}
            models.round_smra_sum.objects.update_or_create(bidder=bidder_id, round=round_data, item=itm_llg.item_lelang, defaults=updated_values)
            return Response({'status':'OK', "code": 200})
        else:
            # check if activity higher then previous activity
            smra_sum = models.round_smra_sum.objects.all().filter(bidder=bidder_id).filter(round=round_data-1).filter(item=itm_llg.item_lelang)
            if eli>smra_sum[0].activity:
                if round_data==2:
                    selisih = 0
                    item_llg = detail_itemlelang.objects.all().values_list("id", flat=True).filter(item_lelang=itm_llg.item_lelang)
                    for i in item_llg:
                        eli_round = models.eli_round.objects.all().filter(bidder_id=bidder_id.id).filter(round=round_data).filter(item_id=i)
                        prev = eli_round[0].cbcp - eli_round[0].cbpp
                        current = eli_round[0].pbcp - eli_round[0].pbpp
                        selisih = selisih + prev-current
                    if (selisih<0): # accepted
                        updated_values = {'price': price, 'activity':smra_sum[0].activity, 'corrected':True}
                        models.round_smra_sum.objects.update_or_create(bidder=bidder_id, round=round_data, item=itm_llg.item_lelang, defaults=updated_values)
                        r_smra = models.round_smra_temp.objects.all().filter(bidder=bidder_id).filter(round=round_data)
                        for bdr in r_smra:
                            updated_values = {'block':bdr.block, 'price':bdr.price} 
                            models.round_smra.objects.update_or_create(item=bdr.item, bidder=bdr.bidder, round=round_data, defaults=updated_values)
                        return Response({'status':'OK', "code": 200})
                    else:
                        return Response({'status':'REVEAL', "code": 400})
                #
                else:
                    #bdr = bidder_lelang.objects.all().filter(item_lelang=1)
                    m = models.round_smra.objects.all().filter(bidder=bidder_id)
                    df = read_frame(m)
                    print(df)
                    data = []
                    for i in range(1, round_data):
                        data.append(df[df['round']==i])
                    m2 = models.round_smra_temp.objects.all().filter(bidder=bidder_id).filter(round=round_data)
                    df2 = read_frame(m2)
                    data.append(df2)
                    df3 = data[1]['price']*data[2]['block'].values
                    print(df3)
                    #calculate cbcp, cbpp, pbcp, pcpp.
#                    selisih = 0
#                    item_llg = detail_itemlelang.objects.all().values_list("id", flat=True).filter(item_lelang=itm_llg.item_lelang)
#                    for i in item_llg:
#                        eli_round = models.eli_round.objects.all().filter(bidder_id=bidder_id.id).filter(round=round_data).filter(item_id=i)
#                        cbcp = eli_round[0].cbcp
#                        selisih = selisih + prev-current
#                    if (selisih<0): # accepted
#                        updated_values = {'price': price, 'activity':eli}
#                        models.round_smra_sum.objects.update_or_create(bidder=bidder_id, round=round_data, item=itm_llg.item_lelang, defaults=updated_values)
#                        r_smra = models.round_smra_temp.objects.all().filter(bidder=bidder_id).filter(round=round_data)
#                        for bdr in r_smra:
#                            updated_values = {'block':bdr.block, 'price':bdr.price} 
#                            models.round_smra.objects.update_or_create(item=bdr.item, bidder=bdr.bidder, round=round_data, defaults=updated_values)
#                        return Response({'status':'OK', "code": 200})
#                    else:
#                        return Response({'status':'REVEAL', "code": 400})

                return Response({'status':'REVEAL', "code": 400})
            else:
                updated_values = {'price': price, 'activity':eli}
                models.round_smra_sum.objects.update_or_create(bidder=bidder_id, round=round_data, item=itm_llg.item_lelang, defaults=updated_values)
                r_smra = models.round_smra_temp.objects.all().filter(bidder=bidder_id).filter(round=round_data)
                for bdr in r_smra:
                    updated_values = {'block':bdr.block, 'price':bdr.price} 
                    models.round_smra.objects.update_or_create(item=bdr.item, bidder=bdr.bidder, round=round_data, defaults=updated_values)
                return Response({'status':'OK', "code": 200})

            #ret = self.validate_mybid(bidder_id, item_id, round_data, eli, price)
            return Response({'status':'OK', "code": 200})

"""class round_smraSummaryViewSet(viewsets.ModelViewSet):
    queryset = models.auction_summary_smra.objects.all()
    serializer_class = serializers.smra_roundSummarySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('item_id',)
"""
"""class smra_bid_bidderViewSet(viewsets.ModelViewSet):
    queryset = models.bid_bidder_smra.objects.all()
    serializer_class = serializers.smra_bid_bidderSMRASerializer
    permission_classes = [permissions.IsAuthenticated]
    #filter_backends = (filters.DjangoFilterBackend,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('item_id', 'bidder_id','round')"""

class berita_acara_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_sanggahan class"""
    queryset = models.berita_acara_lelang.objects.all()
    serializer_class = serializers.berita_acara_lelangSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    # filterset_fields = ('item_id', 'bidder_id','round')

class undangan_SMRA_CCAViewSet(viewsets.ModelViewSet):

    queryset = models.undangan_smra_cca.objects.all()
    serializer_class = serializers.undangan_SMRA_CCASerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('owner',)

    @action(detail=True, methods=['get'])
    def kirim_undangan(self, request, pk):
        domain = request.headers['Host']
        undangan = models.undangan_smra_cca.objects.get(pk=pk)
        item = item_lelang.objects.get(pk=undangan.item_lelang.id)
        auc_lelang = auctioner_lelang.objects.all().filter(item_lelang=item.id)
        pprint(auc_lelang)
        bdr_lelang = bidder_lelang.objects.all().filter(item_lelang=item.id)
        vwr_lelang = viewers_lelang.objects.all().filter(item_lelang=item.id)
        email_auctioner = []
        email_bidder = []
        email_viewer = []
        for a in auc_lelang:
            auc = tim_lelang.objects.get(pk=a.auctioner.id)
            email_auctioner.append(auc.users.email)
        for b in bdr_lelang:
            bdr = bidder_perwakilan.objects.all().filter(bidder_id=b.bidder.id)
            for c in bdr:
                user = Users.objects.get(pk=c.users_id)
                email_bidder.append(user.email)
        for v in vwr_lelang:
            vwr = viewers.objects.get(pk=v.viewer.id)
            email_viewer.append(vwr.users.email)
        email_auctioner.append('rachmatg@yahoo.com')
        data = {"auctioner": email_auctioner, "bidder": email_bidder, "viewer":email_viewer }
        subject = "Notifikasi Undangan"
        email_template_notif_bidder = "email_notif_bidder.html"
        email_template_notif_auctioneer = "email_notif_auctioner.html"
        email_template_notif_viewer = "email_notif_viewer.html"
        auc_email_context = {
            "email": email_auctioner,
            'domain': domain,
            'site_name': 'Spectrum E-auction',
            'judul': undangan.judul,
            'link': undangan.link_teleconference,
            'file': undangan.link_file
        }
        email = render_to_string(email_template_notif_auctioneer, auc_email_context)
        try:
            send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, email_auctioner, fail_silently=False)
        except BadHeaderError:
            return Response({"status":"Invalid header found"})
        return Response({"status":data})
