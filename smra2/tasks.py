from background_task import background
from background_task.tasks import tasks
from background_task.models import Task as BTask
from logging import getLogger
from datetime import datetime, date
from datetime import datetime, timedelta
from . import models
from . import forms
from . import utils
from . import tasks
from userman.models import tim_lelang, bidder_perwakilan, bidder
from adm_lelang.models import auctioner_lelang, bidder_lelang, item_lelang
#from smra.models import bidding_round_smra, round_schedule_smra
from adm_lelang.models import bidder_lelang, item_lelang, detail_itemlelang
from django.utils import timezone
import json
from django.core.serializers.json import DjangoJSONEncoder
import math
from django.db.models import Sum,Count, Max
import time

logger = getLogger(__name__)

def print_auctioneer(mes):
# def print_auctioneer(item, mes):
    print(mes)
    utils.ws_publish_auctioneer(mes)
    # utils.ws_publish_auctioneer(item, mes)
    logger.info(json.dumps(mes))

def print_bidder(item, mes):
    #print(mes)
    utils.ws_publish_bidder(item, mes)
    #logger.info(json.dumps(mes))


def roundx_start(pk, selesai, schedule):
    obj = detail_itemlelang.objects.get(pk=pk)
    round2x_start(pk, selesai, schedule=schedule, creator = obj)


def change_start_to_stop(o):
    models.round_smra2.objects.filter(status_round="STA", item = o.item).update(status_round='STO')

def change_to_finish(o):
    r.status_round='FIN'
    r.save()
    mesg = {"sender":"background","message":"<br><b>2. lelang selesai karena tidak ada penawaran di round "+o.round+" </b>", "detail_item_lelang":o.item.id}
    print_auctioneer(mesg)

def check_permintaan(o):
    # cek permintaan vs penawaran
    #itm_lelang = detail_itemlelang.objects.all().get(id=rsmra.item.id)

    objs = models.obyek_seleksi_smra.objects.filter(item__id=o.item.id, item__disabled=False)
    lanjutkan = True
    total_blok = 0
    for obj in objs:
        r1 = models.round_smra2.objects.all().get(bidder=obj.bidder_user, item__id=o.item.id)
        r2 = models.hasil_smra2.objects.all().filter(bidder=obj.bidder_user, item__id=o.item.id, round = r1.round, valid=True).first()
        if (r2 and r1.status_round == 'STO') :
            total_blok = total_blok + r2.block

#    sum_permintaan = models.round_smra2.objects.all().filter(item=o.item, status_round='STO', penawaran__gt=0).aggregate(Sum('prev_block'))
#    print(sum_permintaan)
    #if  sum_permintaan['prev_block__sum'] is None:
    #    sum_permintaan['prev_block__sum']=0
    ronde = o.round

    permintaan = total_blok #sum_permintaan['prev_block__sum']
    penawaran = o.item.max_block

    #notifikasi hasil pengecekan permintaan dan penawaran
    mesg = {"sender":"background","message":"<br><b>1. cek supply vs demand" +"</b><br> ... penawaran = "+str(penawaran)+" vs permintaan = " + str(permintaan) + " pada ronde:" + str(ronde), "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    return {"permintaan": permintaan, "penawaran": penawaran, "putaran": ronde}

def next_round(o):
    dt = timezone.localtime()
    td = str(timezone.localtime().today().weekday()) 
    round_schedule = models.round_schedule_smra2.objects.all().filter(item=o.item.item_lelang).filter(hari=td).filter(mulai__gte=dt).order_by('mulai').first()
    if round_schedule:
        jadwal_berikutnya = BTask.objects.filter(creator_object_id = round_schedule.id, task_name="smra2.tasks.mulai").first()
        if not jadwal_berikutnya: #jadwal berikutnya tidak ditemukan
            models.round_smra2.objects.all().filter(item__id=o.item.id, status_round='STO').update(status_round='NSC')
            time.sleep(2)
            mesg = {"sender":"background","message":"Tidak Jadwal Putaran Berikut nya, Status NSC", "detail_item_lelang":str(o.item.id)}
            print_auctioneer(mesg)
        else:
            #jadwal_berakhir_berikutnya = BTask.objects.filter(creator_object_id = round_schedule.id, task_name="smra2.tasks.selesai").filter(run_at__gte=jadwal_berikutnya.run_at).order_by('run_at').first()
            mesg = {"sender":"background","message":"Ada Jadwal Putaran Berikut nya", "detail_item_lelang":str(o.item.id)}
            print_auctioneer(mesg)        
            # buat jadwal putaran baru
            sls = json.loads(jadwal_berikutnya.task_params)
            itm = detail_itemlelang.objects.get(pk = o.item.id)
            mulai = jadwal_berikutnya.run_at
            lama = sls[1]['extra_param']['lama']
            selesai =  mulai + timedelta(minutes=int(lama))
            #notifikasi set jadwal baru untuk yg egible masuk
            print("set jadwal baru untuk yg egible masuk")
            models.round_smra2.objects.all().filter(item__id=o.item.id, status_round="STO").update(status_round='WAI',mulai = mulai,selesai = selesai)
            # models.sum_round_smra2.objects.all().filter(item_lelang__id=o.item.id, status_round="STO").update(status_round='WAI',mulai1 = mulai,selesai1 = selesai)
            #notifikasi jadwal round berikutnya
            time.sleep(2)
            mesg = {"sender":"background","message":"<br>+  Set Jadwal Putaran Berikut nya untuk untuk round "+ str(o.round + 1) + " mulai : " + str(mulai) + " berakhir :" + str(selesai), "detail_item_lelang":str(o.item.id)}
            print_auctioneer(mesg)  
    else:
        models.round_smra2.objects.all().filter(item__id=o.item.id, status_round='STO').update(status_round='NSC')
        time.sleep(2)
        mesg = {"sender":"background","message":"Tidak Jadwal Putaran Berikut nya, Status NSC", "detail_item_lelang":str(o.item.id)}
        print_auctioneer(mesg)


def penawaran_kurang_dari_permintaan(o, penawaran, permintaan):
        # notifikasi jika penawaran < permintaan
    mesg = {"sender":"background","message":"***jumlah maks blok < jumlah penawaran yaitu "+ str(penawaran)+" > "+str(permintaan)+" lanjutkan", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    
    #notifikasi penentuan peringkat putaran
    mesg = {"sender":"background","message":"penentuan peringkat putaran", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)

    #penentuan peringkat putaran
    hasil2bid = models.hasil2_smra.objects.all().filter(item__id=o.item.id, round = o.round, valid=True, berlaku=True).order_by("-price", "submit")
    i = 1
    for a in hasil2bid:
        a.ranking_putaran = i
        a.save()
        i = i + 1

    bb = models.hasil_smra2.objects.all().filter(item__id=o.item.id)
    for a in bb:
        a.fin = True
        a.save()

    #notifikasi penentuan kenaikan penawaran
    mesg = {"sender":"background","message":"penentuan kenaikan penawaran dan putaran baru", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)

    #kebutuhan db untuk increment
    rsmrabid = models.round_smra2.objects.all().filter(item__id=o.item.id, penawaran__isnull=False).order_by("-penawaran")[0]
    mesg = {"sender":"background","message":"penentuan kenaikan penawaran dan putaran baru " + str(rsmrabid.penawaran), "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    price_inc = models.price_increase.objects.all().filter(detail_item__id=o.item.id, rentang_max__gte=rsmrabid.penawaran,rentang_min__lte=rsmrabid.penawaran)
    
    #penentuan harga minimum dan putaran baru
    objs = models.obyek_seleksi_smra.objects.filter(item__id=o.item.id, item__disabled=False)
    lanjutkan = True
    total_blok = 0
    for obj in objs:
        r = models.round_smra2.objects.all().get(bidder=obj.bidder_user, item__id=o.item.id)

        #berlaku untuk semua yang bidding di round tsb maka lanjut
        if (r.block > 0 and r.status_round == 'STO'):
            rr = r.round
            r.round = rr + 1   # naikan putaran
            block_r = r.block
            penawaran_r = r.penawaran 
            r.block = 0 # 0 kan block
            r.penawaran = 0 # 0 kan penawaran
            r.prev_price = penawaran_r #simpan penawaran sebelumnya
            r.prev_block = block_r #simpan blok sebelumnya
            
            #set min penawaran
            if (price_inc):
                r.prev_price = math.ceil(float(rsmrabid.penawaran)*(1.0 + float(price_inc[0].kenaikan)/100.0)/1000000.0)*1000000.0+1000000.0
                r.ext_data = {'min_price': r.prev_price}
            else:
                r.prev_price = math.ceil(float(rsmrabid.penawaran))
                r.ext_data = {'min_price': r.prev_price}
            r.lock = False
            total_blok = total_blok + r.prev_block
            r.save()

            #notifikasi penawaran bidder
            mesg = {"sender":"background","message":"<br>+ set bidder =" + str(obj.bidder_user) + " r = " + str(r.round) + " min " + str(r.prev_price), "detail_item_lelang":str(o.item.id)}
            print_auctioneer(mesg)

        #jika tidak bid, maka tidak bisa ikut berikutnya
        else :
            r.status_round='CLO'
            r.lock = True
            r.vi = False
            r.save()

            #notifikasi penawaran bidder
            mesg = {"sender":"background","message":"<br>+ set bidder =" + str(obj.bidder_user) + " r = " + str(r.round) + " CLOSED ", "detail_item_lelang":str(o.item.id)}
            print_auctioneer(mesg)
        
    #cek jadwal round berikutnya
    print(total_blok, penawaran)
    if total_blok > penawaran:
        next_round(o)
    time.sleep(2)
    mesg = {"sender":"background","message":"Validasi selesai", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    print_bidder(o.item.item_lelang.id,mesg)

def process_lelang_khusus(o, penawaran, values, bidder_group):
    #masuk ke lelang khusus
    #notifikasi bahwa masuk ke lelang khusus
    time.sleep(2)
    mesg = {"sender":"background","message":"Masuk ke Lelang Khusus, persiapkan kebutuhan, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + "</b>", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)

    #parameter untuk lelang khusus        
    i = 0
    j = 0
    harga_sblmnya = 0
    cukup = False
    lvalues=list(values)

    #set kebutuhan lelang khussu
    for k in values:
        if (cukup == False) :
            #notifikasi bidding unix
            mesg = {"sender":"background","message":"<br>+ group "+str(i)+" bidding "+ str(k)+" bidder "+str(len(bidder_group[i])), "detail_item_lelang":str(o.item.id)}
            print_auctioneer(mesg)
            #jika di group bidding, ada lebih dari 1 bidder, masuk ke round khusus
            if len(bidder_group[i])>1:
                bidders = bidder_group[i]
                for b in bidders:
                    #update di db round_smra2
                    rowa = models.round_smra2.objects.get(bidder__id=b, item__id=o.item.id)
                    rowb = models.hasil_smra2.objects.filter(bidder__id=b, item__id=o.item.id, berlaku=True, valid=True).order_by('-round').first()
                    rowa.khusus = True # status khusus menjadi true
                    #rowa.round = rowa.round + 1 # tambah putaran
                    block_r = rowb.block
                    penawaran_r = rowa.penawaran 
                    rowa.block = 0 # 0 kan blok
                    rowa.lock = False
                    rowa.penawaran = 0 # 0 kan penawaran
                    rowa.prev_price = penawaran_r
                    #if mblok[b]>0 :
                    #    rowa.prev_block = str(mblok[b])
                    rowa.prev_block = block_r
                    rowa.block = 0 # 0 kan block
                    j = j + rowb.block

                    if i == 0 :
                        rowa.ext_data = {'min_price': lvalues[i] }
                        rowa.prev_price = lvalues[i]
                        mesg = {"sender":"background","message":"<br>+ bidder "+rowa.bidder.users.username+" round "+ str(rowa.round)+" blok "+str(rowa.prev_block)+" min price  = "+ str(lvalues[i]), "detail_item_lelang":str(o.item.id)}
                        print_auctioneer(mesg)
                    else:
                        rowa.ext_data = {'min_price': lvalues[i],'max_price':harga_sblmnya }
                        rowa.prev_price = lvalues[i]
                        mesg = {"sender":"background","message":"<br>+ bidder "+rowa.bidder.users.username+" round "+str(rowa.round)+" blok "+str(rowa.prev_block) + " min price  = " + str(lvalues[i]) + " max price = " + str(harga_sblmnya), "detail_item_lelang":str(o.item.id)}
                        print_auctioneer(mesg)
                    rowa.save()

                    if (j >= penawaran) :
                        cukup = True

            #jika di group bidding, hanya ada 1 bidder, tak masuk round khusus
            else :
                b=bidder_group[i][0]
                rowb = models.hasil_smra2.objects.filter(bidder__id=b, item__id=o.item.id, berlaku=True, valid=True).order_by('-round').first()
                rowa = models.round_smra2.objects.get(bidder__id=b, item__id=o.item.id) 
                rowa.status_round='CLO'
                rowa.lock = True
                rowa.vi= False
                
                rowa.save()
                j = j + rowb.block
                if (j >= penawaran) :
                    cukup = True
                    
            i = i + 1
        
        #peserta round khusus sudah memenuhi quota
        else :
            print(" group bid ",k," gak ikut serta karena sudah cukup ")
        
        harga_sblmnya = k
    # berhentikan sisa yang tidak ikut lelang khusus
    ## populate yang tidak ikut lelang khusus
    models.round_smra2.objects.filter(item__id=o.item.id).exclude(khusus =True).update(status_round='FIN')
    # models.round_smra2.objects.filter(item__id=o.item.id).include(khusus =True).update(status_round='STOP')
    # coba cobi
    # models.round_smra2.objects.filter(item__id=o.item.id).exclude(khusus =True).update(status_round='STO')
    # models.sum_round_smra2.objects.filter(item_lelang__id=o.item.id).update(status_round='STO')
    #cek jadwal round berikutnya
    next_round(o)
    mesg = {"sender":"background","message":"Proses Validasi Seleksi", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    print_bidder(o.item.item_lelang.id,mesg)

def tidak_lelang_khusus(o):
    time.sleep(2)
    mesg = {"sender":"background","message":"penentuan peringkat akhir, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + "</b>", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    #penentuan peringkat akhir

    hasil2 = models.hasil2_smra.objects.all().filter(item__id=o.item.id, valid=True, berlaku=True).order_by("-price", "submit")
    i = 1
    for a in hasil2:
        a.ranking = i
        i = i + 1
        a.save()
        
    time.sleep(2)
    mesg = {"sender":"background","message":"7. ubah status menjadi final, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + "</b>", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    objs = models.obyek_seleksi_smra.objects.all().filter(item__id=o.item_id)

    #ubah status final
    for obj in objs:
        models.round_smra2.objects.filter(bidder=obj.bidder_user, item__id=o.item_id).update(status_round='FIN')

    time.sleep(2)
    mesg = {"sender":"background","message":"Proses Validasi Selesai, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + "</b>", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    print_bidder(o.item.item_lelang.id,mesg)

def permintaan_kurang_dari_penawaran(o, penawaran, permintaan):
    time.sleep(2)
    mesg = {"sender":"background","message":"***jumlah maks blok >= jumlah penawaran yaitu "+ str(penawaran)+" < "+str(permintaan)+" lanjutkan, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + "</b>", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    
    #notifikasi penentuan peringkat putaran
    time.sleep(2)
    mesg = {"sender":"background","message":"2. penentuan peringkat putaran, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + "</b>", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)

    #penentuan peringkat
    hasil2bid = models.hasil2_smra.objects.all().filter(item__id=o.item.id, round = o.round, valid=True, berlaku=True).order_by("-price", "submit")
    i = 1
    for a in hasil2bid:
        a.ranking_putaran = i
        a.save()
        i = i + 1

    bb = models.hasil_smra2.objects.all().filter(item__id=o.item.id)
    for a in bb:
        a.fin = True
        a.save()

    #notifikasi cek lelang khusus
    time.sleep(2)
    mesg = {"sender":"background","message":"3. Pengecekan Apakah Masuk ke Lelang khusus, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + "</b>", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    
    #logika lelang khusus / tidak
    hasil2bidder = models.hasil2_smra.objects.values('bidder').annotate(harga=Max('price')).filter(item__id=o.item.id, berlaku=True).order_by("-price", "bidder")
    values = sorted(set(map(lambda x:x['harga'], hasil2bidder)), reverse=True)
    values.sort(reverse=True)
    print("  penawaran unik ",str(values))
    bidder_group = [[y['bidder'] for y in hasil2bidder if y['harga']==x] for x in values]
    print("  bidder unik ",str(bidder_group))
    #parameter awal
    lelang_khusus = False
    ckp1 = False
    ckp2 = False
    i = 0
    j = 0
    sisab = penawaran
    mblok = {}
    
    #cek masuk ke lelang khusus/tidak
    for k in values:
        if (ckp1 == False) :
            print ("  cek group ke ", i)
            bidders = bidder_group[i]
            for b in bidders:
                rowa = models.hasil_smra2.objects.filter(bidder__id=b, item__id=o.item.id, berlaku=True, valid=True).first()
                if rowa:
                    j = j + rowa.block
                    
                print (" group ke ", i, " bidder ", b, " jumlah blok ", rowa.block)
                if (j >= penawaran) :
                    ckp1 = True 
                    print("  ckp 1 terpenuhi saat i = ",i)
                    
                #if (rowa.block <= sisab ) :
                #    mblok[b]=rowa.block
                #    print(" bidder ",b," blok ",rowa.block," dari sisab ",sisab)
                #else :
                #    if (sisab > 0) :
                #        mblok[b]=sisab
                #        print(" bidder ",b," blok ",sisab," dari sisab ",sisab )

            #sisab = penawaran - j
            #print("sisab jadi ",sisab)

            if len(bidder_group[i])>1:
                ckp2 = True
                
        i = i + 1

    #hasil akhir pengecekan 
    if (ckp1 == True and ckp2 == True) : 
        lelang_khusus = True
        mesg = {"sender":"background","message":"dapat ditentukan urutan pemenang maka masuk ke round khusus, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + "</b>", "detail_item_lelang":str(o.item.id)}
        print_auctioneer(mesg)
    else :
        mesg = {"sender":"background","message":"Tidak Dapat ditentukan urutan pemenang maka tidak masuk ke round khusus, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + "</b>", "detail_item_lelang":str(o.item.id)}
        print_auctioneer(mesg)

    return {"lelang_khusus": lelang_khusus, "values": values, "bidder_group": bidder_group}     

def proses_permintaan_ronde1(o):
    mesg = {"sender":"background","message":"2. lelang Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + " selesai karena tidak ada penawaran di round 1", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    print_bidder(o.item.item_lelang.id,mesg)
    models.round_smra2.objects.filter(status_round="STO", item = o.item).update(status_round='FIN')

def selesai_lelang_khusus(o):
    mesg = {"sender":"background","message":"3. ***proses lelang khusus sudah selesai, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + "</b>", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)

    #notifikasi penentuan peringkat putaran
    time.sleep(2)
    mesg = {"sender":"background","message":"2. penentuan peringkat putaran, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + "</b>", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    
    #penentuan peringkat
    hasil2 = models.hasil2_smra.objects.all().filter(item__id=o.item.id, round = o.round, valid=True, berlaku=True).order_by("-price", "submit")
    i = 1
    for a in hasil2:
        a.ranking_putaran = i
        
        # check ronde khusus
        check_rounde = models.round_smra2.objects.filter(
            item__id=a.item.id,
            round=a.round,
            item_lelang=a.item_lelang,
            penawaran=a.price,
            bidder__id=a.bidder.id
        )

        if check_rounde.exists() and check_rounde.first().khusus:
            a.jenis = "KHUSUS"
        else:
            a.jenis = "NORMAL"
        # a.jenis = "KHUSUS"
        a.save()
        i = i + 1
    
    bb = models.hasil_smra2.objects.all().filter(item__id=o.item.id)
    for a in bb:
        a.jenis = "KHUSUS"
        a.fin = True
        a.save()
    
    #notifikasi penentuan peringkat putaran
    time.sleep(2)
    mesg = {"sender":"background","message":"2. penentuan peringkat putaran akhir, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + "</b>", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)

    #penentuan peringkat akhir
    hasil2 = models.hasil2_smra.objects.all().filter(item__id=o.item.id, valid=True, berlaku=True).order_by("-price", "submit")
    i = 1
    for a in hasil2:
        a.ranking = i
        a.save()
        i = i + 1
    
    #notifikasi lelang selelsai
    time.sleep(2)
    mesg = {"sender":"background","message":"3. Lelang, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan + " Berakhir", "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)

    objs = models.obyek_seleksi_smra.objects.all().filter(item__id=o.item.id)
    #perubahan status menjadi final / selesai
    for obj in objs:
        r = models.round_smra2.objects.all().get(bidder=obj.bidder_user, item__id=o.item.id)
        r.status_round='FIN'
        #r.lock = True
        r.save()
    
    time.sleep(2)
    mesg = {"sender":"background","message":"4.  Proses Validasi Seleksi, Obyek Seleksi: " + o.item.band + "-" + o.item.cakupan, "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    print_bidder(o.item.item_lelang.id,mesg)

#@background(remove_existing_tasks=True)
def process_selesai(o):
    mesg = {"sender":"background","message": "Menyelesaikan putaran, obyek Seleksi: " + o.item.band + "-" + o.item.cakupan, "detail_item_lelang":str(o.item.id)}
    print_auctioneer(mesg)
    print_bidder(o.item.item_lelang.id,mesg)
    change_start_to_stop(o)
    permintaan_penawaran = check_permintaan(o)
    permintaan = permintaan_penawaran['permintaan']
    penawaran = permintaan_penawaran['penawaran']
    putaran = permintaan_penawaran['putaran']
    if permintaan == 0 and putaran == 1:
        proses_permintaan_ronde1(o)
    else:
        if (not o.khusus):
            if (penawaran < permintaan):
                penawaran_kurang_dari_permintaan(o, penawaran, permintaan)
            else:
                lelang_khusus = permintaan_kurang_dari_penawaran(o, penawaran, permintaan)
                if (lelang_khusus['lelang_khusus']):
                    process_lelang_khusus(o, penawaran, lelang_khusus['values'],lelang_khusus['bidder_group'])
                else:
                    tidak_lelang_khusus(o)
        else:
            selesai_lelang_khusus(o)
    #change_stop_to_wait(pk, rsmra)


@background(remove_existing_tasks=True)
def mulai(item_lelang, **kwargs):
    print_auctioneer({"sender":"background","message":"Mulai......","detail_item_lelang": item_lelang})
    print_bidder(item_lelang, {"sender":"background","message":"Mulai......","detail_item_lelang": item_lelang})
    objs = models.obyek_seleksi_smra.objects.all().filter(item__item_lelang__id = item_lelang, item__disabled=False).values("item").distinct()
    obyek_seleksi = []
    for o in objs:
        obyek_seleksi.append(o['item'])
    models.round_smra2.objects.filter(status_round="WAI", item__in = obyek_seleksi).update(status_round='STA')
    #print_auctioneer({"sender":"background","message":"START RONDE = " + str(r.round) + " untuk obyek seleksi: " + item_lelang , "detail_item_lelang":obyek_seleksi})

from django.core import serializers

@background(remove_existing_tasks=True)
def selesai(item_lelang, **kwargs):
    objs = models.sum_round_smra2.objects.filter(item__item_lelang__id=item_lelang, item__disabled=False).order_by("item").distinct("item")
    #objs = models.obyek_seleksi_smra.objects.all().filter(item__item_lelang__id = item_lelang, item__disabled=False).values("item").distinct()
    for o in objs:
        if o.status_round == "STA":
            process_selesai(o)
            print_auctioneer({"sender":"background","message":"status_time_end","detail_item_lelang":o.item.id})
            print_bidder(item_lelang, {"sender":"background","message":"status_time_end","detail_item_lelang":o.item.id})

def roundx_stop(pk, schedule):
    obj = detail_itemlelang.objects.get(pk=pk)
    round2x_stop(pk, schedule=schedule, creator=obj )

@background(remove_existing_tasks=True)
def round2x_start(pk, selesai):
    
    rsmra = models.round_smra2.objects.all().filter(item__id=pk).order_by('-round')[0] 

    objs = models.obyek_seleksi_smra.objects.all().filter(item__id=pk)
    for obj in objs:
        r = models.round_smra2.objects.all().get(bidder=obj.bidder_user, item__id=pk)
        if (r.status_round=='WAI') :
            r.status_round='STA'
            #r.lock = False
            r.save()

    print_auctioneer("START RONDE = " + str(rsmra.round))
    print("===============================START RONDE = ", rsmra.round, "===========")
    
    ts=timezone.localtime().today()
    sls = datetime.strptime(selesai, "%H:%M:%S").time()
    utils.ws_publish({"sender":"background","message":"status_time_end","time_end": selesai})
    tsls = timezone.make_aware(datetime.combine(ts, sls))
    roundx_stop(pk, tsls )

@background(remove_existing_tasks=True)
def round2x_cek(pk):
    utils.ws_publish({"sender":"master","message":"ceksch"})

@background(remove_existing_tasks=True)
def round2x_stop(pk):
    
    # persiapkan database
    itm_lelang = detail_itemlelang.objects.all().get(id=pk)
    itm_lelang1 = detail_itemlelang.objects.all().filter(id=pk)
    rsmra = models.round_smra2.objects.all().filter(item__id=pk).order_by("-round")[0]
    jml_peserta = models.obyek_seleksi_smra.objects.filter(item__id=pk).count()
    objs = models.obyek_seleksi_smra.objects.all().filter(item__id=pk)

    #notifikasi Penawaran telah Usai
    time.sleep(1)
    msg="STOP RONDE = " + str(rsmra.round)
    print_auctioneer(msg)
    print("===============================STOP RONDE = ", rsmra.round, "===========")
    
    #notifikasi validasi dimulasi
    time.sleep(1)
    mesg="<b>VALIDASI RONDE = "+str(rsmra.round)+"</b>"
    print_auctioneer(mesg)
    print("======== VALIDASI RONDE = ",str(rsmra.round))
   
    #ubdah status bidder aktif (STA) menjadi STO
    for obj in objs:
        r = models.round_smra2.objects.all().get(bidder=obj.bidder_user, item__id=pk)
        if (r.status_round=='STA') :
            r.status_round='STO'
            r.save()

        #notifikasi daftar bidding
        mesg = mesg + "<br>+ round "+ str(r.round) + ": bidder " + str(r.bidder) + " bid (" + str(r.block) + ") "+ str(r.penawaran)
        print_auctioneer(mesg)
        print("item ",r.item_id," bidder ",r.bidder," bidding (",r.block,") ",r.penawaran)

    #publish bahwa status berubah
    utils.ws_publish({"sender":"background","message":"status_changed"})

    # cek permintaan vs penawaran
    sum_permintaan = models.round_smra2.objects.all().filter(item__id=pk, penawaran__gt=0, status_round='STO').aggregate(Sum('block'))
    if  sum_permintaan['block__sum'] is None:
        sum_permintaan['block__sum']=0

    permintaan = sum_permintaan['block__sum']
    penawaran = itm_lelang1[0].max_block

    #notifikasi hasil pengecekan permintaan dan penawaran
    time.sleep(2) 
    print("1. cek supply vs demand yaitu max block", penawaran, " vs  ", permintaan," pada ronde ",rsmra.round)
    mesg = mesg + "<br><b>1. cek supply vs demand" +"</b><br> ... penawaran = "+str(penawaran)+" vs permintaan = " + str(permintaan)
    print_auctioneer(mesg)
    
    #jika permintaan 0 round 1 maka lelang selesai karena tidak ada yang nawar di round 1
    if permintaan==0 and rsmra.round==1:
        
        #notifikasi bahwa lelang sudah selesai
        time.sleep(1)
        mesg = mesg + "<br><b>2. lelang selesai karena tidak ada penawaran di round 1</b>"
        print("2. lelang selesai karena tidak ada penawaran di round 1")
        print_auctioneer(mesg)
        
        #ubah status menjadi finish
        for obj in objs:
            r = models.round_smra2.objects.all().get(bidder=obj.bidder_user, item__id=pk)
            r.status_round='FIN'
            r.save()
    
        #notifiaksi bahwa lelang udah selesai
        time.sleep(2)
        print("3. Validasi Selesai")
        print("====================================================================================================================")
        mesg = mesg + "<br><b>3. Validasi Selesai</b>"
        print_auctioneer(mesg)

        #publsih dan notifikasi status berubah
        time.sleep(1)
        utils.ws_publish({"sender":"background","message":"status_changed"})
        utils.ws_publish({"sender":"graphmon","message":"status_changed"})
    
    else :
        #kondisi tidak khusus
        if (rsmra.khusus == False):

            # penawaran < permintaan
            if (penawaran < permintaan) :
                
                # notifikasi jika penawaran < permintaan
                time.sleep(2)
                mesg=mesg+"<br>.. jumlah penawaran < permintaan, lanjut ke round berikutnya"
                print(" ***jumlah maks blok < jumlah penawaran yaitu ", penawaran," < ",permintaan," lanjutkan")
                print_auctioneer(mesg)
                
                #notifikasi penentuan peringkat putaran
                time.sleep(2)
                mesg=mesg+"<br><b>2. penentuan peringkat putaran</b>"
                print("2. penentuan peringkat putaran")
                print_auctioneer(mesg)

                #penentuan peringkat putaran
                hasil2bid = models.hasil2_smra.objects.all().filter(item__id=pk, round = rsmra.round, valid=True, berlaku=True).order_by("-price", "submit")
                i = 1
                for a in hasil2bid:
                    a.ranking_putaran = i
                    a.save()
                    i = i + 1

                bb = models.hasil_smra2.objects.all().filter(item__id=pk)
                for a in bb:
                    a.fin = True
                    a.save()
                utils.ws_publish({"sender":"graphmon","message":"status_changed"})

                #notifikasi penentuan kenaikan penawaran
                time.sleep(2)
                print ("3.penentuan kenaikan penawaran dan putaran baru")
                mesg=mesg+"<br><b>3.penentuan kenaikan penawaran dan putaran baru</b>"
                print_auctioneer(mesg)

                #kebutuhan db untuk increment
                rsmrabid = models.round_smra2.objects.all().filter(item__id=pk, penawaran__isnull=False).order_by("-penawaran")[0]
                price_inc = models.price_increase.objects.all().filter(detail_item__id=pk, rentang_max__gte=rsmrabid.penawaran,rentang_min__lte=rsmrabid.penawaran)
                
                #penentuan harga minimum dan putaran baru
                for obj in objs:
                    r = models.round_smra2.objects.all().get(bidder=obj.bidder_user, item__id=pk)

                    #berlaku untuk semua yang bidding di round tsb maka lanjut
                    if (r.block > 0 and r.status_round == 'STO') :
                        rr = r.round
                        r.round = rr + 1   # naikan putaran
                        block_r = r.block
                        penawaran_r = r.penawaran 
                        r.block = 0 # 0 kan block
                        r.penawaran = 0 # 0 kan penawaran
                        r.prev_price = penawaran_r #simpan penawaran sebelumnya
                        r.prev_block = block_r #simpan blok sebelumnya
                        
                        #set min penawaran
                        if (price_inc):
                            r.prev_price = math.ceil(float(rsmrabid.penawaran)*(1.0 + float(price_inc[0].kenaikan)/100.0)/1000000.0)*1000000.0+1000000.0
                            r.ext_data = {'min_price': r.prev_price}
                            r.save()

                        #notifikasi penawaran bidder
                        mesg = mesg + "<br>+ set bidder =" + str(obj.bidder_user) + " r = " + str(r.round) + " min " + str(r.prev_price)
                        print_auctioneer(mesg)

                    #jika tidak bid, maka tidak bisa ikut berikutnya
                    else :
                        r.status_round='CLO'
                        r.lock = True
                        r.vi = False
                        r.save()

                        #notifikasi penawaran bidder
                        mesg = mesg + "<br>+ set bidder =" + str(obj.bidder_user) + " r = " + str(r.round) + " CLOSED "
                        print_auctioneer(mesg)
                    
                #cek jadwal round berikutnya
                dt = timezone.localtime().time()
                td = str(timezone.localtime().today().isoweekday()) 
                jdwl = round_schedule_smra.objects.all().filter(item=itm_lelang.item_lelang).filter(hari=td).filter(mulai__gte=dt).order_by('mulai').first()

                #notifikasi jadwal round berikutnya
                mesg = mesg + "<br><b>4. Pengecekan Jadwal Putaran Berikut nya </b>"
                print_auctioneer(mesg)

                if jdwl:
                    mesg = mesg + "<br>+  Ada Jadwal Putaran Berikut nya "
                    print_auctioneer(mesg)
                    
                    # buat jadwal putaran baru
                    mulai = timezone.make_aware(datetime.combine(timezone.localtime().today(),jdwl.mulai))
                    selesai = timezone.make_aware(datetime.combine(timezone.localtime().today(), jdwl.selesai))


                    #notifikasi set jadwal baru untuk yg egible masuk
                    for obj in objs:
                        r = models.round_smra2.objects.all().get(bidder=obj.bidder_user, item__id=pk)
                        if (r.status_round == 'STO') :
                            r.status_round='WAI'
                            r.mulai = mulai # set waktu mulai
                            r.selesai = selesai #set waktu selesai
                            #r.lock = False
                            r.save()
                    
                    #notifikasi jadwal round berikutnya
                    time.sleep(2)
                    print ("<b>+ set jadwal berikutnya untuk round ", str(rsmra.round + 1) ," mulai : ", mulai," berakhir :",selesai)
                    mesg = mesg + "<br>+  Set  Jadwal Putaran Berikut nya untuk untuk round "+ str(rsmra.round + 1) + " mulai : " + str(mulai) + " berakhir :" + str(selesai)
                    print_auctioneer(mesg)
                    
                    roundx_start(pk, selesai.time().isoformat(), mulai)

                else :

                    # tidak ada jadwal putaran baru
                    for obj in objs:
                        r = models.round_smra2.objects.all().get(bidder=obj.bidder_user, item__id=pk, status_round='STO')
                        r.status_round='NSCH'
                        #r.lock = True
                        r.save()

                    #notifikasi tidak ada jadwal
                    time.sleep(2)
                    print ("4. jadwal hari ini tidak ada")
                    mesg = mesg + "<br>+  Tidak Jadwal Putaran Berikut nya, Status NSCH "
                    print_auctioneer(mesg)

                time.sleep(2)
                print("5. Validasi Selesai")
                print("====================================================================================================================")
                mesg = mesg + "<br><b>4.  Proses Validasi Seleksi </b>"
                print_auctioneer(mesg)

                utils.ws_publish({"sender":"background","message":"status_changed"})
                

            else :
                # penawaran <= perminataan
                
                # notifikasi jika penawaran < permintaan
                time.sleep(2)
                mesg=mesg+"<br>.. jumlah penawaran >= permintaan, lanjut ke round berikutnya"
                print(" ***jumlah maks blok >= jumlah penawaran yaitu ", penawaran," < ",permintaan," lanjutkan")
                print_auctioneer(mesg)
                
                #notifikasi penentuan peringkat putaran
                time.sleep(2)
                mesg=mesg+"<br><b>2. penentuan peringkat putaran</b>"
                print("2. penentuan peringkat putaran")
                print_auctioneer(mesg)

                #penentuan peringkat
                hasil2bid = models.hasil2_smra.objects.all().filter(item__id=pk, round = rsmra.round, valid=True, berlaku=True).order_by("-price", "submit")
                i = 1
                for a in hasil2bid:
                    a.ranking_putaran = i
                    a.save()
                    i = i + 1

                bb = models.hasil_smra2.objects.all().filter(item__id=pk)
                for a in bb:
                    a.fin = True
                    a.save()
                utils.ws_publish({"sender":"graphmon","message":"status_changed"})

                #notifikasi cek lelang khusus
                time.sleep(2)
                print("4. cek apakah masuk ke lelang khusus atau ga")
                mesg=mesg+"<br><b>3. Pengecekan Apakah Masuk ke Lelang khusu</b>"
                print_auctioneer(mesg)
                
                
                #logika lelang khusus / tidak
                hasil2bidder = models.hasil2_smra.objects.values('bidder').annotate(harga=Max('price')).filter(item__id=pk, berlaku=True).order_by("-price", "bidder")
                values = sorted(set(map(lambda x:x['harga'], hasil2bidder)), reverse=True)
                values.sort(reverse=True)
                print("  penawaran unik ",str(values))
                bidder_group = [[y['bidder'] for y in hasil2bidder if y['harga']==x] for x in values]
                print("  bidder unik ",str(bidder_group))
                #parameter awal
                lelang_khusus = False
                ckp1 = False
                ckp2 = False
                i = 0
                j = 0
                sisab = penawaran
                mblok = {}
                
                #cek masuk ke lelang khusus/tidak
                for k in values:
                    if (ckp1 == False) :
                        print ("  cek group ke ", i)
                        bidders = bidder_group[i]
                        for b in bidders:
                            rowa = models.hasil_smra2.objects.get(bidder__id=b, item__id=pk, berlaku=True, valid=True)
                            j = j + rowa.block
                            
                            print (" group ke ", i, " bidder ", b, " jumlah blok ", rowa.block)
                            if (j >= penawaran) :
                                ckp1 = True 
                                print("  ckp 1 terpenuhi saat i = ",i)
                            
                            #if (rowa.block <= sisab ) :
                            #    mblok[b]=rowa.block
                            #    print(" bidder ",b," blok ",rowa.block," dari sisab ",sisab)
                            #else :
                            #    if (sisab > 0) :
                            #        mblok[b]=sisab
                            #        print(" bidder ",b," blok ",sisab," dari sisab ",sisab )

                        #sisab = penawaran - j
                        #print("sisab jadi ",sisab)

                        if len(bidder_group[i])>1:
                            ckp2 = True
                            
                    i = i + 1

                #hasil akhir pengecekan 
                if (ckp1 == True and ckp2 == True) : 
                    lelang_khusus = True
                    mesg=mesg+"<br> Tidak dapat ditentukan urutan pemenang maka masuk ke round khusus"
                    print_auctioneer(mesg)
                else :
                    mesg=mesg+"<br> Dapat ditentukan urutan pemenang maka tidak masuk ke round khusus"
                    print_auctioneer(mesg)     
               
                #persiapan untuk lelang khusus       
                if (lelang_khusus == True) :
                    #masuk ke lelang khusus
                    
                    #notifikasi bahwa masuk ke lelang khusus
                    time.sleep(2)
                    print("5. Set kebutuhan lelang khusus")
                    mesg=mesg+"<br><b>4. Masuk ke Lelang Khusus, persiapkan kebutuhan</b>"
                    print_auctioneer(mesg)

                    #parameter untuk lelang khusus        
                    i = 0
                    j = 0
                    harga_sblmnya = 0
                    cukup = False
                    lvalues=list(values)

                    #set kebutuhan lelang khussu
                    for k in values:
                        if (cukup == False) :
                            #notifikasi bidding unix
                            mesg=mesg+"<br>+ group "+str(i)+" bidding "+ str(k)+" bidder "+str(len(bidder_group[i]))
                            print_auctioneer(mesg)

                            #jika di group bidding, ada lebih dari 1 bidder, masuk ke round khusus
                            if len(bidder_group[i])>1:
                                bidders = bidder_group[i]
                                for b in bidders:
                                    #update di db round_smra2
                                    rowa = models.round_smra2.objects.get(bidder__id=b, item__id=pk)
                                    rowb = models.hasil_smra2.objects.get(bidder__id=b, item__id=pk, berlaku=True, valid=True)
                                    rowa.khusus = True # status khusus menjadi true
                                    rowa.round = rsmra.round + 1 # tambah putaran
                                    block_r = rowb.block
                                    penawaran_r = rowa.penawaran 
                                    rowa.block = 0 # 0 kan blok
                                    rowa.lock = False
                                    rowa.penawaran = 0 # 0 kan penawaran
                                    rowa.prev_price = penawaran_r
                                    #if mblok[b]>0 :
                                    #    rowa.prev_block = str(mblok[b])
                                    rowa.prev_block = block_r
                                    rowa.block = 0 # 0 kan block
                                    j = j + rowb.block
 
                                    if i == 0 :
                                        rowa.ext_data = {'min_price': lvalues[i] }
                                        mesg=mesg+"<br>+ bidder "+str(b)+" round "+ str(rowa.round)+" blok "+str(rowa.prev_block)+" min price  = "+ str(lvalues[i])
                                        print_auctioneer(mesg)
                                    else:
                                        rowa.ext_data = {'min_price': lvalues[i],'max_price':harga_sblmnya }
                                        mesg=mesg+"<br>+ bidder "+str(b)+" round "+str(rowa.round)+" blok "+str(rowa.prev_block) + " min price  = " + str(lvalues[i]) + " max price = " + str(harga_sblmnya)
                                        print_auctioneer(mesg)
                                    rowa.save()

                                    if (j >= penawaran) :
                                        cukup = True

                            #jika di group bidding, hanya ada 1 bidder, tak masuk round khusus
                            else :
                                b=bidder_group[i][0]
                                rowb = models.hasil_smra2.objects.get(bidder__id=b, item__id=pk, berlaku=True, valid=True)
                                rowa = models.round_smra2.objects.get(bidder__id=b, item__id=pk) 
                                rowa.status_round='CLO'
                                rowa.lock = True
                                rowa.vi= False
                               
                                rowa.save()
                                j = j + rowb.block
                                if (j >= penawaran) :
                                    cukup = True
                                   
                            i = i + 1
                        
                        #peserta round khusus sudah memenuhi quota
                        else :
                            print(" group bid ",k," gak ikut serta karena sudah cukup ")
                        
                        harga_sblmnya = k

                    #cek jadwal round berikutnya
                    dt = timezone.localtime().time()
                    td = str(timezone.localtime().today().isoweekday()) 
                    jdwl = round_schedule_smra.objects.all().filter(item=itm_lelang.item_lelang).filter(hari=td).filter(mulai__gte=dt).order_by('mulai').first()

                    #notifikasi jadwal round berikutnya
                    mesg = mesg + "<br><b>4. Pengecekan Jadwal Putaran Berikut nya </b>"
                    print_auctioneer(mesg)

                    if jdwl:
                        #notifikasi jadwal round berikutnya
                        mesg = mesg + "<br>+  Ada Jadwal Putaran Berikut nya "
                        print_auctioneer(mesg)
                        
                        # buat jadwal putaran baru
                        mulai = timezone.make_aware(datetime.combine(timezone.localtime().today(),jdwl.mulai))
                        selesai = timezone.make_aware(datetime.combine(timezone.localtime().today(), jdwl.selesai))


                        #set jadwal baru untuk yg egible masuk
                        for obj in objs:
                            r = models.round_smra2.objects.all().get(bidder=obj.bidder_user, item__id=pk)
                            if (r.status_round == 'STO') :
                                r.status_round = 'WAI'
                                r.mulai = mulai # set waktu mulai
                                r.selesai = selesai #set waktu selesai
                                #r.lock = True
                                r.save()
                        
                        roundx_start(pk, selesai.time().isoformat(), mulai)

                    else :

                        # tidak ada jadwal putaran baru
                        for obj in objs:
                            r = models.round_smra2.objects.all().get(bidder=obj.bidder_user, item__id=pk, status_round='STO')
                            r.status_round='NSCH'
                            #r.lock = True
                            r.save()

                        #notifikasi tidak ada jadwal
                        time.sleep(2)
                        print ("4. jadwal hari ini tidak ada")
                        mesg = mesg + "<br>+  Tidak Jadwal Putaran Berikut nya, Status NSCH "
                        print_auctioneer(mesg)

                    
                    time.sleep(2)
                    print("5. Validasi Selesai")
                    print("====================================================================================================================")
                    mesg = mesg + "<br><b>4.  Proses Validasi Seleksi </b> "
                    print_auctioneer(mesg)

                    utils.ws_publish({"sender":"background","message":"status_changed"})
                            
                else:
                    #tidak masuk ke lelang khusus
                   
                    time.sleep(2)
                    print("6. penentuan peringkat akhir")
                    print_auctioneer("6. penentuan peringkat akhir")
                    #penentuan peringkat akhir

                    hasil2 = models.hasil2_smra.objects.all().filter(item__id=pk, valid=True, berlaku=True).order_by("-price", "submit")
                    i = 1
                    for a in hasil2:
                        a.ranking = i
                        a.save()
                        i = i + 1
                        
                    time.sleep(2)
                    print("7. ubah status menjadi final")
                    print_auctioneer("7. ubah status menjadi final")
                    #ubah status final
                    for obj in objs:
                        r = models.round_smra2.objects.all().get(bidder=obj.bidder_user, item__id=pk)
                        r.status_round='FIN'
                        #r.lock = True
                        r.save()
                
                    time.sleep(2)
                    print("5. Validasi Selesai")
                    print("====================================================================================================================")
                    mesg = mesg + "<br><b>4.  Proses Validasi Seleksi </b> "
                    print_auctioneer(mesg)

                    utils.ws_publish({"sender":"background","message":"status_changed"})
        
        else :
            #notifikasi penentuan peringkat putaran
            print(" ***proses lelang khusus sudah selesai")
            print_auctioneer(" ***proses lelang khusus sudah selesai")

            #notifikasi penentuan peringkat putaran
            time.sleep(2)
            mesg=mesg+"<br><b>2. penentuan peringkat putaran</b>"
            print("2. penentuan peringkat putaran")
            print_auctioneer(mesg)
            
            #penentuan peringkat
            hasil2 = models.hasil2_smra.objects.all().filter(item__id=pk, round = rsmra.round, valid=True, berlaku=True).order_by("-price", "submit")
            i = 1
            for a in hasil2:
                a.ranking_putaran = i
                a.save()
                i = i + 1
            
            bb = models.hasil_smra2.objects.all().filter(item__id=pk)
            for a in bb:
                a.fin = True
                a.save()
            utils.ws_publish({"sender":"graphmon","message":"status_changed"})
            
            #notifikasi penentuan peringkat putaran
            time.sleep(2)
            mesg=mesg+"<br><b>2. penentuan peringkat putaran akhir</b>"
            print("2. penentuan peringkat putaran akhir")
            print_auctioneer(mesg)

            #penentuan peringkat akhir
            hasil2 = models.hasil2_smra.objects.all().filter(item__id=pk, valid=True, berlaku=True).order_by("-price", "submit")
            i = 1
            for a in hasil2:
                a.ranking = i
                a.save()
                i = i + 1
            
            #notifikasi lelang selelsai
            time.sleep(2)
            mesg=mesg+"<br><b>3. Lelang Berakhir</b>"
            print("2. penentuan peringkat putaran akhir")
            print_auctioneer(mesg)

            #perubahan status menjadi final / selesai
            for obj in objs:
                r = models.round_smra2.objects.all().get(bidder=obj.bidder_user, item__id=pk)
                r.status_round='FIN'
                #r.lock = True
                r.save()
            
            time.sleep(2)
            print("5. Validasi Selesai")
            print("====================================================================================================================")
            mesg = mesg + "<br><b>4.  Proses Validasi Seleksi </b> "
            print_auctioneer(mesg)

            utils.ws_publish({"sender":"background","message":"status_changed"})