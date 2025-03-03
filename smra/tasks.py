from background_task import background
from logging import getLogger
import datetime
from . import models
from . import forms
from userman.models import tim_lelang, bidder_perwakilan, bidder
from adm_lelang.models import auctioner_lelang, bidder_lelang, item_lelang
from smra.models import bidding_round_smra, round_schedule_smra
from adm_lelang.models import bidder_lelang, item_lelang, detail_itemlelang
from django.utils import timezone

logger = getLogger(__name__)

@background(schedule=60)
def daily_start(message):
    logger.debug('demo_task. message={0}'.format(message))

@background(schedule=60)
def daily_stop(message):
    logger.debug('demo_task. message={0}'.format(message))

@background(schedule=60)
def round_start(pk):
    item_llg = item_lelang.objects.get(id=pk)
    #round = models.bidding_round_smra.objects.all().filter(item=item_llg)
    #putaran = round[0].round_state
    br = models.bidding_round_smra.objects.all().filter(item=pk)[0]
    br.status_round = 'STA'
    br.save()
    print(br.stop_time)
    round_stop(pk, schedule=br.stop_time, verbose_name=str(pk))
    logger.debug('demo_task. message={0}'.format(pk))

@background(schedule=60)
def round_stop(pk):
    item_llg = item_lelang.objects.get(id=pk)
    round = models.bidding_round_smra.objects.all().filter(item=item_llg)
    putaran = round[0].round_state
    # increase round
    updated_values = {'round_state':putaran+1, 'status_round':'STA'}
    models.bidding_round_smra.objects.update_or_create(item=item_llg, defaults=updated_values)
    itm_llg = detail_itemlelang.objects.all().filter(item_lelang=pk)
    bidder = bidder_lelang.objects.all().filter(item_lelang=pk)
    r_smra = models.round_smra.objects.all().filter(item__in=itm_llg).filter(round=putaran)
    for bdr in r_smra:
        if bdr.block==0:
            updated_values = {'price':0, 'block':0, 'prev_price':bdr.prev_price, 'prev_block':bdr.block} # kenaikan harga role di min price
        else:
            updated_values = {'price':0, 'block':0, 'prev_price':bdr.price, 'prev_block':bdr.block,'min_price':bdr.price} # kenaikan harga role di min price
        models.round_smra.objects.update_or_create(item=bdr.item, bidder=bdr.bidder, round=putaran+1, defaults=updated_values)
    #round_start(pk, schedule=datetime.datetime.now())
    br = models.bidding_round_smra.objects.all().filter(item=pk)[0]
    br.status_round = 'STO'
    br.save()

    dt = timezone.now()
    mulai = models.round_schedule_smra.objects.all().filter(item=item_llg).filter(mulai__gte=dt).order_by('mulai').first()
    if mulai:
        br = models.bidding_round_smra.objects.all().filter(item=pk)[0]
        #print(br)
        br.status_round = 'WAI'
        print(mulai.mulai)
        br.start_time = mulai.mulai
        br.stop_time = mulai.selesai
        br.save()
        round_start(pk, schedule=mulai.mulai, verbose_name=str(pk))
        
    logger.debug('demo_task. message={0}'.format(pk))