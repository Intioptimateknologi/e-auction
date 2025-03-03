import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eauctions.settings")
django.setup()

from smra2 import tasks
from smra2 import models
from adm_lelang.models import detail_itemlelang
from userman.models import bidder_perwakilan, bidder_user
from django.utils import timezone
from datetime import datetime, timedelta
import argparse
from background_task.models import Task as BTask


# id_detail_itemlelang = 113
id_detail_itemlelang = 114
peserta = 3

def test_mulai():
    mulai = timezone.localtime()
    akhir = mulai + timedelta(minutes=5)
    itm = detail_itemlelang.objects.get(pk = id_detail_itemlelang)
    models.round_smra2.objects.filter(item=itm).update(status_round='STA')
    dt = timezone.localtime()
    td = str(timezone.localtime().today().isoweekday()) 
    jadwal_berikutnya = BTask.objects.filter(creator_object_id = itm.id, task_name="smra2.tasks.mulai").filter(run_at__gte=dt).order_by('run_at').first()    
    tasks.mulai(id_detail_itemlelang, verbose_name="Memulai Putaran", schedule=jadwal_berikutnya, creator = itm)

def test_nobid():
    mulai = timezone.localtime()
    akhir = mulai + timedelta(minutes=5)
    itm = detail_itemlelang.objects.get(pk = id_detail_itemlelang)
    models.round_smra2.objects.filter(item=itm).update(round=1)
    obsel = models.obyek_seleksi_smra.objects.filter(item = itm, item__disabled=False)
    for o in obsel:
        vbidder_perwakilan = bidder_perwakilan.objects.filter(bidder = o.bidder_user).first()
        updated_values = {'price':0,'block':0,'valid':True, 'berlaku': True, 'perwakilan': vbidder_perwakilan}
        putaran = 1
        print(o.bidder_user)
        hasil, created = models.hasil_smra2.objects.update_or_create(round=putaran,  bidder=o.bidder_user, item=itm, item_lelang = 100,defaults=updated_values)
        print(hasil, created)
        obj = models.round_smra2.objects.get(item=itm, bidder = o.bidder_user)
        obj.penawaran = 0
        obj.round = 1
        obj.prev_block = 0
        obj.status_round = 'STA'
        obj.save()
    tasks.selesai(100, verbose_name="Mengakhiri Putaran", schedule=mulai, creator = itm)

def test_besar1():
    mulai = timezone.localtime()
    akhir = mulai + timedelta(minutes=5)
    itm = detail_itemlelang.objects.get(pk = id_detail_itemlelang)
    #models.round_smra2.objects.filter(item=itm).update(round=1)
    obsel = models.obyek_seleksi_smra.objects.filter(item = itm, item__disabled=False)
    data = [
        {'price':3005000000, 'block':2},
        {'price':3005000000, 'block':2},
        {'price':3001000000, 'block':1},
        {'price':3002000000, 'block':1},
        {'price':3003000000, 'block':0},
        {'price':3004000000, 'block':0},
    ]
    i = 0
    for o in obsel:
        d = data[i]
        if d['block']!=0:
            print(d['price'])
            vbidder_perwakilan = bidder_perwakilan.objects.filter(bidder = o.bidder_user).first()
            updated_values = {'price':d['price'],'block':d['block'],'valid':True, 'berlaku': True, 'perwakilan': vbidder_perwakilan}
            putaran = 1
            i = i + 1
            print(o.bidder_user)
            hasil, created = models.hasil_smra2.objects.update_or_create(round=putaran,  bidder=o.bidder_user, item=itm, item_lelang = 100,defaults=updated_values)
            print(hasil, created)
            updated_values = {'price':d['price'],'valid':True, 'berlaku': True, 'perwakilan': vbidder_perwakilan}
            hasil = models.hasil2_smra.objects.update_or_create(item=itm, bidder=o.bidder_user, round = putaran, defaults=updated_values)
            obj = models.round_smra2.objects.get(item=itm, bidder = o.bidder_user)
            obj.penawaran = d['price']
            obj.prev_block = d['block']
            obj.block = d['block']
            obj.status_round = 'STA'
            obj.save()
            print(obj)
    #tasks.selesai(100, verbose_name="Mengakhiri Putaran", schedule=mulai, creator = itm)

def test_besar2():
    mulai = timezone.localtime()
    akhir = mulai + timedelta(minutes=5)
    itm = detail_itemlelang.objects.get(pk = id_detail_itemlelang)
    #models.round_smra2.objects.filter(item=itm).update(round=2)
    obsel = models.obyek_seleksi_smra.objects.filter(item = itm, item__disabled=False)
    data = [
        {'price':3007000000, 'block':1},
        {'price':3007000000, 'block':1},
        {'price':3003000000, 'block':1},
        {'price':3003000000, 'block':1},
        {'price':3003000000, 'block':0},
        {'price':3004000000, 'block':0},
    ]
    i = 0
    for o in obsel:
        d = data[i]
        if d['block']!=0:
            print(d['price'])
            vbidder_perwakilan = bidder_perwakilan.objects.filter(bidder = o.bidder_user).first()
            updated_values = {'price':d['price'],'block':d['block'],'valid':True, 'berlaku': True, 'perwakilan': vbidder_perwakilan}
            putaran = 1
            i = i + 1
            print(o.bidder_user)
            hasil, created = models.hasil_smra2.objects.update_or_create(round=putaran,  bidder=o.bidder_user, item=itm, item_lelang = 100,defaults=updated_values)
            print(hasil, created)
            updated_values = {'price':d['price'],'valid':True, 'berlaku': True, 'perwakilan': vbidder_perwakilan}
            hasil = models.hasil2_smra.objects.update_or_create(item=itm, bidder=o.bidder_user, round = putaran, defaults=updated_values)
            obj = models.round_smra2.objects.get(item=itm, bidder = o.bidder_user)
            obj.penawaran = d['price']
            obj.prev_block = d['block']
            obj.block = d['block']
        #    obj.status_round = 'STA'
            obj.save()
            print(obj)
    #tasks.selesai(100, verbose_name="Mengakhiri Putaran", schedule=mulai, creator = itm)

def test_sama(): # mestinya masuk lelang khusus dengan top price yang sama
    mulai = timezone.localtime()
    akhir = mulai + timedelta(minutes=5)
    itm = detail_itemlelang.objects.get(pk = id_detail_itemlelang)
    #models.round_smra2.objects.filter(item=itm).update(round=2)
    obsel = models.obyek_seleksi_smra.objects.filter(item = itm, item__disabled=False)
    data = [
        {'price':3008000000, 'block':1},
        {'price':3009000000, 'block':1},
        {'price':3007000000, 'block':1},
        {'price':3003000000, 'block':0},
        {'price':3003000000, 'block':0},
        {'price':3004000000, 'block':0},
    ]
    i = 0
    for o in obsel:
        d = data[i]
        if d['block']!=0:
            print(d['price'])
            vbidder_perwakilan = bidder_perwakilan.objects.filter(bidder = o.bidder_user).first()
            updated_values = {'price':d['price'],'block':d['block'],'valid':True, 'berlaku': True, 'perwakilan': vbidder_perwakilan}
            putaran = 1
            i = i + 1
            print(o.bidder_user)
            hasil, created = models.hasil_smra2.objects.update_or_create(round=putaran,  bidder=o.bidder_user, item=itm, item_lelang = 100,defaults=updated_values)

            updated_values = {'price':d['price'],'valid':True, 'berlaku': True, 'perwakilan': vbidder_perwakilan}
            hasil = models.hasil2_smra.objects.update_or_create(item=itm, bidder=o.bidder_user, round = putaran, defaults=updated_values)
            print(hasil, created)
            obj = models.round_smra2.objects.get(item=itm, bidder = o.bidder_user)
            obj.penawaran = d['price']
            obj.prev_block = d['block']
            obj.block = d['block']
            obj.status_round = 'STA'
            obj.save()
            print(obj)

def test_kecil_k1(): # mestinya masuk lelang khusus dengan top price yang sama
    mulai = timezone.localtime()
    akhir = mulai + timedelta(minutes=5)
    itm = detail_itemlelang.objects.get(pk = id_detail_itemlelang)
    #models.round_smra2.objects.filter(item=itm).update(round=2)
    obsel = models.obyek_seleksi_smra.objects.filter(item = itm, item__disabled=False)
    data = [
        {'price':3009000000, 'block':1},
        {'price':3009000000, 'block':1},
        {'price':3007000000, 'block':1},
        {'price':3003000000, 'block':0},
        {'price':3003000000, 'block':0},
        {'price':3004000000, 'block':0},
    ]
    i = 0
    for o in obsel:
        d = data[i]
        if d['block']!=0:
            print(d['price'])
            vbidder_perwakilan = bidder_perwakilan.objects.filter(bidder = o.bidder_user).first()
            updated_values = {'price':d['price'],'block':d['block'],'valid':True, 'berlaku': True, 'perwakilan': vbidder_perwakilan}
            putaran = 1
            i = i + 1
            print(o.bidder_user)
            hasil, created = models.hasil_smra2.objects.update_or_create(round=putaran,  bidder=o.bidder_user, item=itm, item_lelang = 100,defaults=updated_values)

            updated_values = {'price':d['price'],'valid':True, 'berlaku': True, 'perwakilan': vbidder_perwakilan}
            hasil = models.hasil2_smra.objects.update_or_create(item=itm, bidder=o.bidder_user, round = putaran, defaults=updated_values)
            print(hasil, created)
            obj = models.round_smra2.objects.get(item=itm, bidder = o.bidder_user)
            obj.penawaran = d['price']
            obj.prev_block = d['block']
            obj.block = d['block']
            obj.status_round = 'STA'
            obj.save()
            print(obj)
    #tasks.selesai(100, verbose_name="Mengakhiri Putaran", schedule=mulai, creator = itm)

def test_kecil_k2(): # mestinya masuk lelang khusus dengan bottom price yang sama
    mulai = timezone.localtime()
    akhir = mulai + timedelta(minutes=5)
    itm = detail_itemlelang.objects.get(pk = id_detail_itemlelang)
    #models.round_smra2.objects.filter(item=itm).update(round=2)
    obsel = models.obyek_seleksi_smra.objects.filter(item = itm, item__disabled=False)
    data = [
        {'price':3009000000, 'block':1},
        {'price':3007000000, 'block':1},
        {'price':3007000000, 'block':1},
        {'price':3003000000, 'block':0},
        {'price':3003000000, 'block':0},
        {'price':3004000000, 'block':0},
    ]
    i = 0
    for o in obsel:
        d = data[i]
        if d['block']!=0:
            print(d['price'])
            vbidder_perwakilan = bidder_perwakilan.objects.filter(bidder = o.bidder_user).first()
            updated_values = {'price':d['price'],'block':d['block'],'valid':True, 'berlaku': True, 'perwakilan': vbidder_perwakilan}
            putaran = 1
            i = i + 1
            print(o.bidder_user)
            hasil, created = models.hasil_smra2.objects.update_or_create(round=putaran,  bidder=o.bidder_user, item=itm, item_lelang = 100,defaults=updated_values)
            updated_values = {'price':d['price'],'valid':True, 'berlaku': True, 'perwakilan': vbidder_perwakilan}
            hasil = models.hasil2_smra.objects.update_or_create(item=itm, bidder=o.bidder_user, round = putaran, defaults=updated_values)
            print(hasil, created)
            obj = models.round_smra2.objects.get(item=itm, bidder = o.bidder_user)
            obj.penawaran = d['price']
            obj.prev_block = d['block']
            obj.block = d['block']
            obj.status_round = 'STA'
            obj.save()
            print(obj)

def test_kecil(): # mestinya tidak masuk lelang khusus
    mulai = timezone.localtime()
    akhir = mulai + timedelta(minutes=5)
    itm = detail_itemlelang.objects.get(pk = id_detail_itemlelang)
    #models.round_smra2.objects.filter(item=itm).update(round=2)
    obsel = models.obyek_seleksi_smra.objects.filter(item = itm, item__disabled=False)
    data = [
        {'price':3009000000, 'block':1},
        {'price':3008000000, 'block':1},
        {'price':3007000000, 'block':1},
        {'price':3003000000, 'block':0},
        {'price':3003000000, 'block':0},
        {'price':3004000000, 'block':0},
    ]
    i = 0
    for o in obsel:
        d = data[i]
        if d['block']!=0:
            print(d['price'])
            vbidder_perwakilan = bidder_perwakilan.objects.filter(bidder = o.bidder_user).first()
            updated_values = {'price':d['price'],'block':d['block'],'valid':True, 'berlaku': True, 'perwakilan': vbidder_perwakilan}
            putaran = 1
            i = i + 1
            print(o.bidder_user)
            hasil, created = models.hasil_smra2.objects.update_or_create(round=putaran,  bidder=o.bidder_user, item=itm, item_lelang = 100,defaults=updated_values)
            updated_values = {'price':d['price'],'valid':True, 'berlaku': True, 'perwakilan': vbidder_perwakilan}
            hasil = models.hasil2_smra.objects.update_or_create(item=itm, bidder=o.bidder_user, round = putaran, defaults=updated_values)
            print(hasil, created)
            obj = models.round_smra2.objects.get(item=itm, bidder = o.bidder_user)
            obj.penawaran = d['price']
            obj.prev_block = d['block']
            obj.block = d['block']
            obj.status_round = 'STA'
            obj.save()
            print(obj)
    #tasks.selesai(100, verbose_name="Mengakhiri Putaran", schedule=mulai, creator = itm)

def run_specific_test(test_name):
    """Run a specific test based on the provided name."""
    if test_name == "mulai":
        print("Running 'Mulai putaran'...")
        test_mulai()
    elif test_name == "besar1":
        print("Running 'Test Ronde 1, Demand > Supply'...")
        test_besar1()
    elif test_name == "besar2":
        print("Running 'Test Ronde 1, Demand > Supply'...")
        test_besar2()
    elif test_name == "kecil":
        print("Running 'Test Ronde 1, Demand > Supply'...")
        test_kecil()
    elif test_name == "kecil_k1":
        print("Running 'Test Ronde 1, Demand > Supply'...")
        test_kecil_k1()
    elif test_name == "kecil_k2":
        print("Running 'Test Ronde 1, Demand < Supply'...")
        test_kecil_k2()
    elif test_name == "sama":
        print("Running 'Test Ronde 1, Demand < Supply'...")
        test_sama()
    elif test_name == "nobid":
        print("Running 'Test Ronde 1 Nobid'...")
        test_nobid()
    else:
        print(f"No test found with the name: {test_name}")

def main():
    parser = argparse.ArgumentParser(description="Script to run Django environment tasks.")
    parser.add_argument(
        "--test",
        help="Skenario yang dijalankan."
    )
    parser.add_argument(
        "--item",
        help="ID Detail Item Lelang.", nargs='?', const=113, type=int,default=113
    )
    parser.add_argument(
        "--peserta",
        help="Jumlah Peserta Lelang.", nargs='?', const=3, type=int,default=3
    )
    args = parser.parse_args()
    print(args)
    id_detail_itemlelang = args.item
    peserta = args.peserta

    if args.test:
        run_specific_test(args.test)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
