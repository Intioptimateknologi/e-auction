from background_task import background
from background_task.tasks import tasks
from logging import getLogger
from datetime import datetime, date
from . import models
from . import forms
from . import utils
from userman.models import tim_lelang, bidder_perwakilan, bidder
from adm_lelang.models import auctioner_lelang, bidder_lelang, item_lelang
from smra.models import bidding_round_smra, round_schedule_smra
from adm_lelang.models import bidder_lelang, item_lelang, detail_itemlelang
from django.utils import timezone
import json
from django.core.serializers.json import DjangoJSONEncoder
import math
from django.db.models import Sum

logger = getLogger(__name__)

def check_putaran():
    # check penawaran

    return True

def round_start(pk, selesai, schedule):
    obj = item_lelang.objects.get(pk=pk)
    round2_start(pk, selesai, schedule=schedule, creator = obj)

def round_stop(pk, schedule):
    obj = item_lelang.objects.get(pk=pk)
    round2_stop(pk, schedule=schedule, creator=obj )

def round3_stop(pk, schedule):
    obj = item_lelang.objects.get(pk=pk)
    round3_stop(pk, schedule=schedule, creator=obj )

@background(remove_existing_tasks=True)
def round2_start(pk, selesai):
    bidder = models.obyek_seleksi_cca.objects.all().filter(item__id=pk)
    for bdr in bidder:
        r = models.round_cca.objects.all().get(bidder=bdr.bidder_user, item_lelang=bdr.item)
        r.status_round='STA'
        r.lock = False
        r.save()
    
    sls = datetime.strptime(selesai, "%H:%M:%S").time()
    utils.ws_publish({"sender":"background","message":"status_time_end","time_end": selesai})
    ts = timezone.make_aware(datetime.combine(timezone.localtime().today(), sls))
    print("call stop at", ts)
    round_stop(pk, ts)
    logger.debug('demo_task. message={0}'.format(pk))

@background(remove_existing_tasks=True)
def round3_start(pk, selesai):
    bidder = models.obyek_seleksi_cca.objects.all().filter(item__id=pk)
    for bdr in bidder:
        r = models.round_cca.objects.all().get(bidder=bdr.bidder_user, item_lelang=bdr.item)
        r.status_round='STA'
        r.lock = False
        r.save()
    
    sls = datetime.strptime(selesai, "%H:%M:%S").time()
    utils.ws_publish({"sender":"background","message":"status_time_end","time_end": selesai})
    ts = timezone.make_aware(datetime.combine(timezone.localtime().today(), sls))
    print("call stop at", ts)
    round_stop3(pk, ts)
    logger.debug('demo_task. message={0}'.format(pk))

@background(remove_existing_tasks=True)
def round2_stop(pk):
    bidder = models.obyek_seleksi_cca.objects.all().filter(item__id=pk)
    round_finish = False
    next_mulai = timezone.localtime().time()
    item_llg = item_lelang.objects.all().get(id=pk)
    for bdr in bidder:
        r = models.round_cca.objects.all().get(bidder=bdr.bidder_user, item_lelang=bdr.item)
        r.status_round='STO'
        r.lock = False
        r.save()

    dt = timezone.localtime().time()
    td = str(timezone.localtime().today().isoweekday())    
    round = round_schedule_smra.objects.all().filter(item=item_llg).filter(hari=td).filter(mulai__gte=dt).order_by('mulai').first()
    if round:
        # cek permintaan vs penawaran
        parent = models.round_cca.objects.all().filter(item_lelang=pk).first()
        obyek = models.round_detail_cca.objects.filter(parent=parent)
        hasil_parent = models.hasil_cca.objects.all().filter(item_lelang=pk, round=parent.round)
        ronde_lanjut = True
        mulai = timezone.make_aware(datetime.combine(timezone.localtime().today(),round.mulai))
        selesai = timezone.make_aware(datetime.combine(timezone.localtime().today(), round.selesai))
        total_permintaan = 0
        for ob in obyek:
            # diperbaiki
            hasil_detil = models.hasil_detail_cca.objects.all().filter(parent__item_lelang = pk, item = ob.item).aggregate(Sum('block'))
            total_permintaan = hasil_detil["block__sum"]
            print(ob.max_blok,total_permintaan)
            if ob.max_blok < total_permintaan:
                ronde_lanjut = True
            else:
                ronde_lanjut = False
        if ronde_lanjut:
            dtl=detail_itemlelang.objects.filter(item_lelang = pk, disabled=False)
            parent = models.round_cca.objects.filter(item_lelang=pk)
            ronde = parent[0].round
            for d in dtl:
                print("masuk d ",d)
                hasil_detil = models.hasil_detail_cca.objects.all().filter(parent__round = ronde, parent__item_lelang = pk, item = d).aggregate(Sum('block'))
                total_permintaan = hasil_detil["block__sum"]
                price_inc = models.cca_price_increase.objects.all().filter(detail_item=d, rentang_max__gt=total_permintaan,rentang_min__lte=total_permintaan)
                max_price = models.round_detail_cca.objects.all().filter(parent=parent[0], item=d).order_by('-price')[0]
                for prn in parent:
                    print("masuk prn ",prn)
                    prn.status_round='WAI'
                    prn.mulai = mulai
                    prn.selesai = selesai
                    prn.round = ronde + 1
                    prn.save()
                    r = models.round_detail_cca.objects.all().filter(parent=prn, item=d)
                    if r:
                        print("masuk r ",r)
                        r[0].block = 0
                        r[0].price = 0
                        r[0].lock = False
                        print(max_price.price, total_permintaan)
                        if (price_inc):
                            print(price_inc[0].kenaikan, max_price.price, total_permintaan)
                            r[0].prev_price = math.ceil(float(max_price.price)*(1.0 + float(price_inc[0].kenaikan)/100.0)/1000000.0)*1000000.0+1000000.0
                        r[0].save()

                utils.rebuild_hasil(d, ronde, mulai, selesai)
            utils.ws_publish({"sender":"background","message":"status_changed"})
            print("call start at", mulai)
            round_start(pk, selesai.time().isoformat(), mulai)
        else:
            round_finish=True
            parent = models.round_cca.objects.all().filter(item_lelang=pk).first()
            utils.rebuild_hasil(d, ronde, mulai, selesai)
            for prn in parent:
                r = models.round_cca.objects.all().get(id = prn.id)
                r.status_round='FIN'
                r.lock = True
                r.save()
            utils.ws_publish({"sender":"background","message":"status_changed"})
        
    else:
        round_finish=True
        ronde = models.round_cca.objects.all().filter(item_lelang=pk)[0]
        utils.rebuild_hasil(item_llg, ronde.round, round.mulai, round.selesai)
        for bdr in bidder:
            r = models.round_cca.objects.all().get(bidder=bdr.bidder_user, item_lelang=bdr.item)
            r.status_round='CLO'
            r.lock = True
            r.save()
        utils.ws_publish({"sender":"background","message":"status_changed"})

@background(remove_existing_tasks=True)
def round3_stop(pk):
    bidder = models.obyek_seleksi_cca.objects.all().filter(item__id=pk)
    round_finish = False
    next_mulai = timezone.localtime().time()
    item_llg = item_lelang.objects.all().get(id=pk)
    for bdr in bidder:
        r = models.round_cca.objects.all().get(bidder=bdr.bidder_user, item_lelang=bdr.item)
        r.status_round='STO'
        r.lock = False
        r.save()

    dt = timezone.localtime().time()
    td = str(timezone.localtime().today().isoweekday())    
    round_finish=True
    ronde = models.round_cca.objects.all().filter(item_lelang=pk)[0]
    #utils.rebuild_hasil(item_llg, ronde.round)
    for bdr in bidder:
        r = models.round_cca.objects.all().get(bidder=bdr.bidder_user, item_lelang=bdr.item)
        r.status_round='CLO'
        r.lock = True
        r.save()
    utils.ws_publish({"sender":"background","message":"status_changed"})



