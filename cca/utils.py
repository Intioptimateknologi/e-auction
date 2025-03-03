from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from . import models
from . import forms
from . import utils
from userman.models import tim_lelang, bidder_perwakilan, bidder
from adm_lelang.models import auctioner_lelang, bidder_lelang, item_lelang
from smra.models import bidding_round_smra, round_schedule_smra
from adm_lelang.models import bidder_lelang, item_lelang, detail_itemlelang
from django.utils import timezone
import json
from django.conf import settings


from cent import Client
def find(arr, val):
    for key in arr:
        if key.get(val):
            return key[val]

def check_reveal(d1, d2):
    keys_list = [list(item.keys())[0] for item in d2]
    total1 = 0
    total2 = 0
    total_kiri = 0
    total_kanan = 0
    for d in keys_list:
        dt1 = find(d1, d)
        dt2 = find(d2, d)
        print(d, dt1, dt2)
        #harga2 - #harga1 pada kombinasi 2
        total1 = total1+dt1['block']*dt1['price']
        total2 = total2+dt1['block']*dt2['price']
        print(dt1['price'], total1,dt2['price'],total2)
    total_kiri =  total2-total1
    print(total_kiri)
    total1 = 0
    total2 = 0
    for d in keys_list:
        dt1 = find(d1, d)
        dt2 = find(d2, d)
        #harga2 - #harga1 pada kombinasi 2
        total1 = total1+dt2['block']*dt1['price']
        total2 = total2+dt2['block']*dt2['price']        
        print(dt1['price'], total1,dt2['price'],total2)
    total_kanan = total2-total1
    print(total_kanan)
    return (total_kiri - total_kanan)

def ws_publish(data):
    send_event("spectrum-auctions", "message", data)
"""    if settings.CENTRIFUGO_INTERNAL:
        url = "http://"+settings.CENTRIFUGO_INTERNAL+"/api"
        api_key = "d7627bb6-2292-4911-82e1-615c0ed3eebb"
        client = Client(url, api_key=api_key, timeout=1)
        channel = "spectrum-eauctions"
        client.publish(channel, data)
"""

def rebuild_hasil(item, round, mulai, selesai):
    dtl = detail_itemlelang.objects.filter(item_lelang = item, disabled=False)
    ronde = models.round_cca.objects.filter(item_lelang = item)
    for r in ronde:
        r.mulai = mulai
        r.selesai = selesai
        r.save()
    for d in dtl:
        m = models.hasil2_detail_cca.objects.all().filter(item=d, parent__round = round, parent__valid=True).order_by("-price", "-parent__submit")
        i = 1
        for a in m:
            a.ranking_putaran = i
            a.save()
            i = i + 1
        m = models.hasil2_detail_cca.objects.all().filter(item=d, parent__valid=True).order_by("-price", "-parent__submit")
        i = 1
        for a in m:
            a.ranking_putaran = i
            a.save()
            i = i + 1


