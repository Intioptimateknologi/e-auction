from rest_framework import generics, status, viewsets, permissions
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import filters
import json
import os
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date
from . import serializers
from . import models
from . import tasks
from . import utils
from userman.models import Users, bidder
from userman.serializers import BidderUserSerializer
from adm_lelang.models import bidder_lelang, item_lelang, detail_itemlelang
from userman.models import tim_lelang, bidder_perwakilan, bidder, bidder_user
#from smra.models import round_schedule_smra
from datetime import datetime, timedelta
from django.utils import timezone
import asyncio
from asgiref.sync import async_to_sync, sync_to_async
import django_filters.rest_framework
from background_task.models import Task as BTask
from django.db.models import Count
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.db import connection
from django.db import reset_queries
import locale
from terbilang import Terbilang
import django_renderpdf
from django.core.files.base import ContentFile, File
from django.conf import settings
from django.db.models import Max

import requests


from django import core

class round_smraViewSet(viewsets.ModelViewSet):

    queryset = models.round_smra2.objects.all().order_by('item')
    serializer_class = serializers.round_smraSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('item_lelang','bidder', "round")

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'B':
            bu = bidder_user.objects.filter(users = user)
            return models.round_smra2.objects.filter(bidder__in=bu).order_by('item')
        else:
            return models.round_smra2.objects.all().order_by('item')



    # initialize client instance.
    @action(detail=True, methods=['get'])
    def init_all(self, request, pk=None):
        itm = detail_itemlelang.objects.all().filter(item_lelang__id = pk, disabled=False)
        models.round_smra2.objects.filter(item_lelang=pk).delete()
        id = []
        for i in itm:
            id.append(i.id)
        bdr = models.obyek_seleksi_smra.objects.all().filter(item__in=itm, item__disabled=False)
        for b in bdr:
            item = detail_itemlelang.objects.get(id = b.item.id)
            updated_values = {'status_round':'INI','round':1, 'price':0, 'block':b.blok_awal, 
                'prev_block':b.blok_awal, 
                'prev_price':item.harga_minimal, 'min_price':item.harga_minimal,
                'price':0,'penawaran':0,
                'mulai': timezone.now(), 'selesai':timezone.now(),
                'item_lelang':pk, 'lock':False, 'lock':False, 'khusus':False,'ext_data':{'min_price':str(item.harga_minimal)} 
                }
            models.round_smra2.objects.update_or_create(bidder=b.bidder_user, item=item, defaults=updated_values)
        hasil = models.hasil_smra2.objects.all().filter(item__item_lelang=pk)
        hasil.delete()
        hasil2 = models.hasil2_smra.objects.all().filter(item__item_lelang=pk)
        hasil2.delete()
        return Response({"statuss":"OK"})
        
    @action(detail=True, methods=['get'])
    def init(self, request, pk=None):
       
        item_llg = detail_itemlelang.objects.get(id=pk)

        itm = detail_itemlelang.objects.get(pk = pk)
        bdr = models.obyek_seleksi_smra.objects.all().filter(item=itm, item__disabled=False)
        for b in bdr:
            updated_values = {'status_round':'INI','round':1, 'price':0, 'block':0, 
                'prev_block':b.blok_awal, 
                'prev_price':itm.harga_minimal, 'min_price':itm.harga_minimal,
                'price': 0,'penawaran':0,
                'mulai': timezone.now(), 'selesai':timezone.now(),
                'item_lelang':itm.item_lelang.id, 'lock':False, 'khusus':False,'ext_data':{'min_price':str(itm.harga_minimal)} 
                }
            models.round_smra2.objects.update_or_create(bidder=b.bidder_user, item=itm, defaults=updated_values)
        hasil = models.hasil_smra2.objects.all().filter(item=itm)
        hasil.delete()
        hasil2 = models.hasil2_smra.objects.all().filter(item=itm)
        hasil2.delete()
        utils.ws_publish({"sender":"auctioneer","message":"status_changed: init"})
        td = datetime.now()
        dt = td + timedelta(seconds = 2)
#        tasks.round2x_cek(pk,schedule=dt)
        return Response({"status":"OK"})

    @action(detail=True, methods=['get'])
    def create_schedule(self, request, pk=None):
        itm = detail_itemlelang.objects.get(pk = pk)
        dt = timezone.localtime()
        td = str(timezone.localtime().today().isoweekday())    
        delta = 3
        skip = 2
        hari = str(timezone.localtime().today().isoweekday())
        data = round_schedule_smra.objects.all()
        for i in range(100):
            waktu_mulai = datetime.strptime(dt.strftime("%H:%M"),"%H:%M")
            waktu_selesai = waktu_mulai + timedelta(minutes=delta)
            data = round_schedule_smra(hari = hari, item=itm.item_lelang, mulai= waktu_mulai, selesai= waktu_selesai)
            data.save()
            dt = waktu_mulai + timedelta(minutes=skip+delta)
        return Response({"status":"OK"})
    
    @action(detail=True, methods=['get'])
    def create_schedule1(self, request, pk=None):
        itm = detail_itemlelang.objects.get(pk = pk)
        dt = timezone.localtime()
        td = str(timezone.localtime().today().isoweekday())    
        delta = 1
        skip = 1
        hari = str(timezone.localtime().today().isoweekday())
        data = round_schedule_smra.objects.all()
        for i in range(100):
            waktu_mulai = datetime.strptime(dt.strftime("%H:%M"),"%H:%M")
            waktu_selesai = waktu_mulai + timedelta(minutes=delta)
            data = round_schedule_smra(hari = hari, item=itm.item_lelang, mulai= waktu_mulai, selesai= waktu_selesai)
            data.save()
            dt = waktu_mulai + timedelta(minutes=skip+delta)
        return Response({"status":"OK"})

    @action(detail=True, methods=['get'])
    def create_schedule2(self, request, pk=None):
        itm = detail_itemlelang.objects.get(pk = pk)
        dt = timezone.localtime()
        td = str(timezone.localtime().today().isoweekday())    
        delta = 2
        skip = 1
        hari = str(timezone.localtime().today().isoweekday())
        data = round_schedule_smra.objects.all()
        for i in range(100):
            waktu_mulai = datetime.strptime(dt.strftime("%H:%M"),"%H:%M")
            waktu_selesai = waktu_mulai + timedelta(minutes=delta)
            data = round_schedule_smra(hari = hari, item=itm.item_lelang, mulai= waktu_mulai, selesai= waktu_selesai)
            data.save()
            dt = waktu_mulai + timedelta(minutes=skip+delta)
        return Response({"status":"OK"})

    @action(detail=True, methods=['get'])
    def start(start, request, pk=None):
        dt = timezone.localtime()
        td = str(timezone.localtime().today().weekday())   
        itm = detail_itemlelang.objects.get(pk = pk)
#        round = BTask.objects.filter(task_name="smra2.tasks.mulai",run_at__gte=dt, creator_object_id=itm.item_lelang.id).first()
        round_schedule = models.round_schedule_smra2.objects.filter(hari = td, mulai__gte= dt, item = itm.item_lelang).first()
        if round_schedule:
            round = BTask.objects.filter(task_name="smra2.tasks.mulai",creator_object_id=round_schedule.id).first()
            if round:
                sls = json.loads(round.task_params)
                itm = detail_itemlelang.objects.get(pk = pk)
                bidder = models.obyek_seleksi_smra.objects.all().filter(item=itm)
                td = str(timezone.localtime().today().isoweekday())   
                mulai = round.run_at
                lama = sls[1]['extra_param']['lama']
                selesai =  mulai + timedelta(minutes=int(lama))
                putaran = models.round_smra2.objects.all().filter(item__id=round.creator_object_id).first()
                ronde = 1
                if putaran:
                    ronde = putaran.round
                for bdr in bidder:
                    updated_values = {'status_round':'WAI', 'round':ronde,'lock': False, 'mulai': mulai, 'selesai':selesai}
                    models.round_smra2.objects.update_or_create(bidder=bdr.bidder_user, item=itm, defaults=updated_values)
                #selesai = round.selesai.isoformat()
                print("start lelang untuk ",pk," mulai ",mulai," selesai",selesai)
                utils.ws_publish({"sender":"auctioneer","message":"status_changed: start"})
                return Response({"status":"OK"})
            else:
                return Response({"status":"Hari ini tidak ada jadwal"})
        else:
            return Response({"status":"Hari ini tidak ada jadwal"})

    @action(detail=True, methods=['get'])
    def resume(start, request, pk=None):
        itm = detail_itemlelang.objects.get(pk = pk)
        bidder = models.obyek_seleksi_smra.objects.all().filter(item=itm)
        dt = timezone.localtime().time()
        td = str(timezone.localtime().today().weekday())   
        round_schedule = models.round_schedule_smra2.objects.all().filter(item=itm.item_lelang).filter(hari=td).filter(mulai__gte=dt).order_by('mulai').first()
        if round_schedule:
            round = BTask.objects.filter(task_name="smra2.tasks.mulai",creator_object_id=round_schedule.id).first()
            if round:
                sls = json.loads(round.task_params)
                itm = detail_itemlelang.objects.get(pk = pk)
                bidder = models.obyek_seleksi_smra.objects.all().filter(item=itm)
                mulai = round.run_at
                lama = sls[1]['extra_param']['lama']
                selesai =  mulai + timedelta(minutes=int(lama))
                putaran = models.round_smra2.objects.all().filter(item__id=round.creator_object_id).first()
                ronde = 1
                if putaran:
                    ronde = putaran.round
                for bdr in bidder:
                    updated_values = {'status_round':'WAI', 'round':ronde-1,'lock': False, 'mulai': mulai, 'selesai':selesai}
                    models.round_smra2.objects.update_or_create(bidder=bdr.bidder_user, item=itm, defaults=updated_values)
                utils.ws_publish({"sender":"auctioneer","message":"status_changed: resume"})
                return Response({"status":"OK"})
            else:
                return Response({"status":"Hari ini tidak ada jadwal"})
        else:
            return Response({"status":"Hari ini tidak ada jadwal"})

    @action(detail=True, methods=['get'])
    def resumex(start, request, pk=None):
        itm = detail_itemlelang.objects.get(pk = pk)
        bidder = models.obyek_seleksi_smra.objects.all().filter(item=itm)
        dt = timezone.localtime()
        td = str(timezone.localtime().today().isoweekday())    
        round = round_schedule_smra.objects.all().filter(item=itm.item_lelang).filter(hari=td).filter(mulai__gte=dt).order_by('mulai').first()
        if round:
            mulai = timezone.make_aware(datetime.combine(timezone.localtime().today(),round.mulai))
            selesai =  timezone.make_aware(datetime.combine(timezone.localtime().today(), round.selesai))
            for bdr in bidder:
                updated_values = {'status_round':'WAI', 'lock': False, 'mulai': mulai, 'selesai':selesai}
                models.round_smra2.objects.update_or_create(bidder=bdr.bidder_user, item=itm, defaults=updated_values)
            return Response({"status":"OK"})
            utils.ws_publish({"sender":"auctioneer","message":"status_changed: resumex"})
        else:
            return Response({"status":"Hari ini tidak ada jadwal"})


    @action(detail=True, methods=['get'])
    def resumelanjut(start, request, pk=None):
       
        td = datetime.now()
        dt = td + timedelta(seconds = 10)
        return Response({"status":"OK"})
    
        
   
    @action(detail=True, methods=['get'])
    def startnow(start, request, pk=None):
        itm = detail_itemlelang.objects.get(pk = pk)
        bidder = models.obyek_seleksi_smra.objects.all().filter(item=itm)
        for bdr in bidder:
            updated_values = {'status_round':'STA', 'lock': False}
            models.round_smra2.objects.update_or_create(bidder=bdr.bidder_user, item=itm, defaults=updated_values)
        return Response({"status":"OK"})

    @action(detail=True, methods=['get'])
    def reset_round(start, request, pk=None):
        item_llg = detail_itemlelang.objects.get(id=pk)
        bidder = models.obyek_seleksi_smra.objects.all().filter(item=item_llg)
        dt = timezone.localtime().time()
        td = str(timezone.localtime().today().weekday())   
        round_schedule = models.round_schedule_smra2.objects.all().filter(item=item_llg.item_lelang).filter(hari=td).filter(mulai__gte=dt).order_by('mulai').first()
        if round_schedule:
            round = BTask.objects.filter(task_name="smra2.tasks.mulai",creator_object_id=round_schedule.id).first()
            if round:
                sls = json.loads(round.task_params)
                itm = detail_itemlelang.objects.get(pk = pk)
                bidder = models.obyek_seleksi_smra.objects.all().filter(item=itm)
                mulai = round.run_at
                lama = sls[1]['extra_param']['lama']
                selesai =  mulai + timedelta(minutes=int(lama))
                for bdr in bidder:
                    obj = models.round_smra2.objects.filter(item=item_llg, bidder= bdr.bidder_user).order_by('-round').first()

                    updated_values = {'status_round':'WAI', 'price':0, 'penawaran': 0,                
                        'mulai': mulai, 'selesai':selesai,
                        'item_lelang':item_llg.item_lelang.id, 'lock':False
                        }
                    models.round_smra2.objects.update_or_create(bidder=bdr.bidder_user, item=item_llg, round=obj.round, defaults=updated_values)
                    hasil = models.hasil_smra2.objects.all().filter(bidder=bdr.bidder_user).filter(item=item_llg).filter(round=obj.round)
                    hasil.delete()
                    hasil = models.hasil2_smra.objects.all().filter(bidder=bdr.bidder_user).filter(item=item_llg).filter(round=obj.round)
                    hasil.delete()
                utils.ws_publish({"sender":"auctioneer","message":"status_changed: reset"})

                return Response({"status":"OK"})
            else:
                return Response({"status":"Hari ini tidak ada jadwal"})
        else:
            return Response({"status":"Hari ini tidak ada jadwal"})
        

    @action(detail=True, methods=['get'])
    def stop(start, request, pk=None):
        item_llg = detail_itemlelang.objects.get(id=pk)
        bidder = models.obyek_seleksi_smra.objects.all().filter(item=item_llg)
        for bdr in bidder:
            updated_values = {'status_round':'STO'}
            models.round_smra2.objects.update_or_create(bidder=bdr.bidder_user, item=item_llg, defaults=updated_values)
        utils.ws_publish({"sender":"auctioneer","message":"status_changed: stop"})
        return Response({"status":"OK"})
    
    @action(detail=True, methods=['get'])
    def pause(start, request, pk=None):
        item_llg = detail_itemlelang.objects.get(id=pk)
        bidder = models.obyek_seleksi_smra.objects.all().filter(item=item_llg)
        for bdr in bidder:
            updated_values = {'status_round':'SUS'}
            models.round_smra2.objects.update_or_create(bidder=bdr.bidder_user, item=item_llg, defaults=updated_values)
        utils.ws_publish({"sender":"auctioneer","message":"status_changed: pause"})
        return Response({"status":"OK"})

    @action(detail=True, methods=['get'])
    def close(start, request, pk=None):
        item_llg = detail_itemlelang.objects.get(id=pk)
        bidder = models.obyek_seleksi_smra.objects.all().filter(item=item_llg)
        for bdr in bidder:
            updated_values = {'status_round':'CLO'}
            models.round_smra2.objects.update_or_create(bidder=bdr.bidder_user, item=item_llg, defaults=updated_values)
        utils.ws_publish({"sender":"auctioneer","message":"status_changed: close"})
        return Response({"status":"OK"})

    @action(detail=True, methods=['post'])
    def submit_bid(self, request, pk=None):
        from pdfminer.high_level import extract_pages
        from pdfminer.layout import LTTextContainer
        data = request.data
        #print("masuksini")
        wakil_id = data[0]['perwakilan']['id']
        item_llg = detail_itemlelang.objects.get(pk=data[0]['data']['item'])
        bdr = bidder_user.objects.get(pk=data[0]['data']['bidder'])
        wakil = data[0]['perwakilan']
        obj = models.round_smra2.objects.get(pk=pk)
        lt = timezone.localtime()
        if obj.selesai < lt:
            return Response({"step":"document", "status":"Waktu Habis"})
        if obj.prev_price > data[0]['price']:
            return Response({"step":"document", "status":"Harga lebih kecil dari minimal penawaran"})
        putaran = 1
        currentdir = os.getcwd()
        filename = "ba_"+str(data[0]['data']['item'])+"_"+ str(data[0]['data']['bidder']) + "_"+ str(putaran) + ".pdf"
        pathname = currentdir + "/media/upload/bidder/" + filename
        hasil = []
        updated_values = []
        with open(pathname,"wb") as my_file:
            t = Terbilang()
            context = {}
            user = request.user

            for d in data:
                harga = float(d['price'])
                block = int(d['block'])
                putaran = int(d['data']['round'])
                vbidder_perwakilan = bidder_perwakilan.objects.get(id = d['perwakilan']['id'])
                if vbidder_perwakilan:
                    bidder_id = bdr.id
                    vbidder = bdr.bidder
                    context["bidder"] = vbidder
                    vbidder_lelang = bidder_lelang.objects.all().filter(bidder = bidder_id)
                    context["bidder_id"] = bidder_id
                    context["harga"] = int(harga)
                    context["wakil"] = vbidder_perwakilan.nama_lengkap
                    context["tahun"] = item_llg.item_lelang.tahun
                    context["seleksi"] = item_llg.item_lelang.nama_lelang
                    context["item"] = item_llg
                    context["block"] = block
                    context["block_t"] = t.parse(block).getresult()
                    context["putaran"] = putaran
                    context["putaran_t"] = t.parse(putaran).getresult()
                    context["terbilang"] = t.parse(int(harga)).getresult()
                #print(context)
                django_renderpdf.helpers.render_pdf(template= ["ba_putaran.html"], file_= my_file, context= context)
                my_file.close()
                updated_values = {'price':d['price'],'block':int(d['block']),'valid':False, 'perwakilan': vbidder_perwakilan}
                #updated_values = {'price':d['price'],'block':int(d['block']),'valid':True, 'perwakilan': vbidder_perwakilan}
                putaran = int(d['data']['round'])
                hasil, created = models.hasil_smra2.objects.update_or_create(round=int(d['data']['round']),  bidder=bdr, item=item_llg, item_lelang=item_llg.item_lelang.id, defaults=updated_values)
                #tambahan
                #hasil, created = models.hasil2_smra.objects.update_or_create(round=int(d['data']['round']),  bidder=bdr, item=item_llg, item_lelang=item_llg.item_lelang.id, defaults=updated_values)  
                
                with open(pathname, "rb") as f:
                    myfile = File(f)
                    hasil.berita_acara_unsigned.save(filename, myfile, save=True)

        obj.penawaran = d['price']
        obj.block = int(d['block'])
        obj.save()

        bbox = ()
        for page_layout in extract_pages(pathname):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    if hasattr(element, 'bbox'):
                        if element.get_text().startswith("Jakarta"):
                            bbox = element.bbox
                            #print(element.bbox)
        
        url = "http://"+settings.PERURI_DOCKER+"/v1/doc/upload"
        #payload = {'profileName': vbidder_perwakilan.profil_peruri}
        files=[
            ('file',(filename,open(pathname,'rb'),'application/pdf'))
        ]
        response = requests.request("POST", url, files=files)
        data = json.loads(response.text)
        if data['errorCode']!="0":
            return Response({"step":"document", "status":data})
        else:
            fileId = data['saveAs']
            url1 = "http://" + settings.PERURI_DOCKER+"/v1/auth/token"
            payload = json.dumps({
                "param": {
                    "systemId": settings.PERURI_RESOURCE_ID
                }
            })
            headers = {
                'Content-Type': 'application/json',
                'x-Gateway-APIKey': settings.PERURI_API_KEY
            }
            response = requests.request("POST", url1, headers=headers, data=payload)
            jwt = json.loads(response.text)
            if jwt['status']=="error":
#                rollback()
                return Response({"step":"document", "status":jwt['message']})
            print(jwt)
            #data_jwt = jwt.data.jwt
            data_jwt = jwt["jwt"]
            # session init
            url2 = "http://" + settings.PERURI_DOCKER+"/v1/auth/session/init"
            payload = json.dumps({
            "param": {
                "email": vbidder_perwakilan.profil_peruri,
                "systemId": settings.PERURI_SYSTEM_ID,
                "sendEmail": "1",
                "sendSms": "1",
#                "sendWhatsapp": "1"
            }
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + jwt["jwt"],
                'x-Gateway-APIKey': settings.PERURI_API_KEY
            }
            response = requests.request("POST", url2, headers=headers, data=payload)
            session = json.loads(response.text)
            if session['status']=="error":#                rollback()
                return Response({"step":"document", "status":session['message']})
            
            return Response({"step":"session","bbox":'-'.join([str(value) for value in bbox]), "putaran": putaran, "bidder": bdr.id, "wakil": wakil_id, "item_lelang": item_llg.id,"session":session, "fileid": fileId, "jwt": jwt })
        
        #return Response({"step":"session","bbox":'-'.join([str(value) for value in bbox]), "putaran": putaran, "bidder": bdr.id, "wakil": wakil_id, "item_lelang": item_llg.id,"session":"0", "fileid": "fileId", "jwt": "jwt" })

#        return Response({"step":"session", "status":data})

    @action(detail=True, methods=['get'])
    def send_document(self, request, pk=None):
        vbidder_perwakilan = bidder_perwakilan.objects.get(id = pk)
        url = "http://"+settings.PERURI_DOCKER+"/v1/doc/upload"
        payload = {'profileName': vbidder_perwakilan.profil_peruri}
        files=[
            ('file',(vbidder_perwakilan.ttd.filename,open('/home/auction/kominfo2/media/upload/bidder/porter.pdf','rb'),'image/png'))
        ]
        response = requests.request("POST", url, files=files)
        data = json.loads(response.text)
        return Response({"status":data})

    @action(detail=True, methods=['get'])
    def next_round(start, request, pk=None):
        item_llg = detail_itemlelang.objects.get(id=pk)
        bidder = models.obyek_seleksi_smra.objects.all().filter(item=item_llg)
        dt = timezone.localtime()
        td = str(timezone.localtime().today().isoweekday())    
        #print(td)
        #print(dt)
        round = round_schedule_smra.objects.all().filter(item=item_llg.item_lelang).filter(hari=td).filter(mulai__gte=dt).order_by('mulai').first()
        if round:
            mulai = datetime.combine(date.today(),round.mulai)
            selesai = datetime.combine(date.today(), round.selesai)
            putaran = models.round_smra2.objects.all().filter(item=pk)[0]
            for bdr in bidder:
                updated_values = {'round':putaran.round+1, 'status_round':'WAI', 'lock': False, 'mulai': mulai, 'selesai':selesai, 'item_lelang': item_llg.item_lelang.id}
                models.round_smra2.objects.update_or_create(bidder=bdr.bidder_user, item=item_llg, defaults=updated_values)
            return Response({"status":"OK"})
        else:
            return Response({"status":"Hari ini tidak ada jadwal"})

    @action(detail=True, methods=['get'])
    def esign(self, request, pk=None):
        # first: get jwt
        url1 = "https://apgdev.peruri.co.id:9044/gateway/jwtSandbox/1.0/getJsonWebToken/v1"
        payload = json.dumps({
            "param": {
                "systemId": "PERURI-DEPLOY-HASH"
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'x-Gateway-APIKey': 'e3aadac6-57fb-4491-b810-b998fa8c0de8'
        }
        response = requests.request("POST", url1, headers=headers, data=payload)
        jwt = json.loads(response.text)
        #data_jwt = jwt.data.jwt
        #print(jwt["data"]["jwt"])
        # session init
        url2 = "https://apgdev.peruri.co.id:9044/gateway/digitalSignatureOnPremise/1.0/sessionInitiate/v1"
        payload = json.dumps({
        "param": {
            "email": vbidder_perwakilan.profil_peruri,
            "systemId": "PERURI-DEPLOY-HASH",
            "sendEmail": "1",
            "sendSms": "0",
            "sendWhatsapp": "0"
        }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + jwt["data"]["jwt"]
        }
        response = requests.request("POST", url2, headers=headers, data=payload)
        session = json.loads(response.text)

        '''url = "http://localhost:9044/v1/doc/upload"
        payload = {'profileName': vbidder_perwakilan.profil_peruri}
        files=[
            ('file',('signature.png',open('/home/auction/kominfo2/media/upload/bidder/porter.pdf','rb'),'image/png'))
        ]
        response = requests.request("POST", url, files=files)
        data = json.loads(response.text)'''
        return Response({"session":session, "jwt": jwt["data"]["jwt"] })


    @action(detail=True, methods=['get'])
    def sign(self, request, pk=None):
        # first: get jwt
        user = request.user

        jwt = request.GET.get('jwt')
        fileid = request.GET.get('fileid')
        otp = request.GET.get('otp')
        token = request.GET.get('token')
        putaran = int(request.GET.get('putaran'))
        bidder_id = request.GET.get('bidder')
        wakil = request.GET.get('wakil')
        item_lelang_id = request.GET.get('item_lelang')
        bbox = request.GET.get('bbox').split('-')
        vbidder_perwakilan = bidder_perwakilan.objects.all().get(pk = int(wakil))

        #validate token
        url2 = "http://"+settings.PERURI_DOCKER+"/v1/auth/session/validate"

        payload = json.dumps({
            "param": {
                "email": vbidder_perwakilan.profil_peruri,
                "systemId": settings.PERURI_SYSTEM_ID,
                "tokenSession": token,
                "otpCode": otp
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + jwt,
            'x-Gateway-APIKey': settings.PERURI_API_KEY
        }

        response = requests.request("POST", url2, headers=headers, data=payload)
        session = json.loads(response.text)
        #print(session)
        if session['errorCode']!='0':
            return Response(session) 

        url2 = "http://"+settings.PERURI_DOCKER+"/v1/doc/shield/composite/user/sign"

        payload = json.dumps({
        "systemId": settings.PERURI_SYSTEM_ID,
        "profileName": vbidder_perwakilan.profil_peruri,
        "src": fileid,
        "location": "Jakarta",
        "reason": "I agree to sign",
        "coordinate": {
            "specimenImage": vbidder_perwakilan.peruri_ttd,
            "page": 1,
            "llx": float(bbox[0]),
            "lly": float(bbox[1]) - 120,
            "urx": float(bbox[0])+100,
            "ury": float(bbox[1]) - 20
        }
        })
        print(payload)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + jwt,
            'x-Gateway-APIKey': settings.PERURI_API_KEY
        }

        response_signed = requests.request("POST", url2, headers=headers, data=payload)
        retval = json.loads(response_signed.text)
        retval["position"] = "signing"
        if retval['errorCode']!='0':
            return Response(retval) 

        file = os.path.splitext(fileid)[0]
        url3 = "http://"+settings.PERURI_DOCKER+"/v1/doc/download?idFile="+file

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + jwt,
            'x-Gateway-APIKey': settings.PERURI_API_KEY
        }
        resp = requests.request("GET", url3, data=payload)

        #bdr = bidder.objects.get(pk=bidder_id)
        bidder_id = vbidder_perwakilan.bidder.id
        ttd = vbidder_perwakilan.ttd
        item_llg = detail_itemlelang.objects.get(pk=item_lelang_id)
        bdr = bidder_user.objects.get(pk=bidder_id)
        # yang lama dibuat tidak berlaku
        hasil = models.hasil_smra2.objects.all().filter(round=putaran - 1).filter(bidder=bdr).filter(item=item_llg)
        if hasil:
            hasil[0].berlaku = False
            hasil[0].save()
        hasil2 = models.hasil2_smra.objects.all().filter(round=putaran - 1).filter(bidder=bdr).filter(item=item_llg)
        if hasil2:
            for h in hasil2:
                h.berlaku = False
                h.save()
        hasil = models.hasil_smra2.objects.all().filter(round=putaran).filter(bidder=bdr).filter(item=item_llg)
        if hasil:
        #print(hasil)
            hasil[0].valid = False # dibuat False dulu
            hasil[0].berlaku = False # dibuat False dulu
            hasil[0].save()
        #---------- salin ke hasil 2
            num_blok = hasil[0].block
            for i in range(0,num_blok):
                hasil2 = models.hasil2_smra(price = hasil[0].price, item = hasil[0].item, item_lelang = hasil[0].item_lelang,
                    submit = hasil[0].submit, valid = hasil[0].valid, bidder = hasil[0].bidder, perwakilan = hasil[0].perwakilan,
                    round = hasil[0].round, jenis = hasil[0].jenis, berlaku=True)
                hasil2.save()

        hasil = models.hasil_smra2.objects.all().filter(round=putaran).filter(bidder__id=bidder_id).filter(item=item_llg)
        hasil.update(valid = True, berlaku = True)
        resp.encoding = 'utf-8'
        hasil[0].berita_acara.save(fileid, ContentFile( resp.content   ))
        hasil[0].save()

        hasil2 = models.hasil2_smra.objects.all().filter(round=putaran).filter(bidder_id=bidder_id).filter(item=item_llg).update(valid=True, berlaku=True)

        #---------- lock kalau sudah berhasil di sign
        obj = models.round_smra2.objects.all().get(bidder = bdr, item=hasil[0].item)
        obj.lock = True
        obj.save()

        return Response({"status":response, "retval": retval, "session": session})


class sum_round_smraViewSet(viewsets.ModelViewSet):

    queryset = models.sum_round_smra2.objects.all().order_by('item')
    serializer_class = serializers.sum_round_smra2Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('item_lelang',"round")
    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'B':
            bu = bidder_lelang.objects.filter(bidder__users = user)
            itm_lelang = []
            for i in bu:
                itm_lelang.append(i.item_lelang.id)
            return models.sum_round_smra2.objects.filter(item_lelang__in =itm_lelang).order_by('item')
        else:
            return models.sum_round_smra2.objects.all().order_by('item')       

class hasil_smra2ViewSet(viewsets.ModelViewSet):

    queryset = models.hasil_smra2.objects.all()
    serializer_class = serializers.hasil_smra2Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('item_lelang',"bidder","round")
    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'B':
            bu = bidder_lelang.objects.filter(bidder__users = user)
            itm_lelang = []
            for i in bu:
                itm_lelang.append(i.item_lelang.id)
            return models.hasil_smra2.objects.filter(item_lelang__in =itm_lelang).order_by('item')
        else:
            return models.hasil_smra2.objects.all().order_by('item')       
        
class auctioner_hasilViewSet(viewsets.ModelViewSet):

    queryset = models.auctioner_hasil.objects.all()
    serializer_class = serializers.auctioner_hasilSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('item_lelang',"round")
    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'B':
            bu = bidder_lelang.objects.filter(bidder__users = user)
            itm_lelang = []
            for i in bu:
                itm_lelang.append(i.item_lelang.id)
            return models.auctioner_hasil.objects.filter(item_lelang__in =itm_lelang).order_by('item')
        else:
            return models.auctioner_hasil.objects.all().order_by('item')       
        

class price_increaseViewSet(viewsets.ModelViewSet):

    queryset = models.price_increase.objects.all()
    serializer_class = serializers.price_increaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_create(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'B':
            bu = bidder_lelang.objects.filter(bidder__users = user)
            itm_lelang = []
            for i in bu:
                itm_lelang.append(i.item_lelang)
            return models.price_increase.objects.filter(item__in=itm_lelang).order_by('item')
        else:
            return models.price_increase.objects.all().order_by('item')           

class obyek_seleksiViewSet(viewsets.ModelViewSet):

    queryset = models.obyek_seleksi_smra.objects.all()
    serializer_class = serializers.obyek_seleksiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_create(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

    @action(methods=['get'], detail=False, url_path='check_bidder/(?P<pk>\d+)')
    def check_bidder(self, request, pk=None):
        available_bidder_users = bidder_user.objects.exclude(
            id__in=models.obyek_seleksi_smra.objects.filter(item=pk).values('bidder_user')
        )
        serializer = serializers.bidder_usersSerializer(available_bidder_users, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'B':
            bu = bidder_user.objects.filter(users = user).first()
            return models.obyek_seleksi_smra.objects.filter(bidder_user=bu).order_by('item')
        else:
            return models.obyek_seleksi_smra.objects.all().order_by('item')   

class jadwalSMRAViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_sanggahan class"""

    queryset = models.round_schedule_smra2.objects.all()
    serializer_class = serializers.jadwalSMRASerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('item',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_create(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        BTask.objects.filter(creator_object_id = instance.id).delete()
        models.round_schedule_smra2.objects.filter(id = instance.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'B':
            bu = bidder_lelang.objects.filter(bidder__users = user)
            itm_lelang = []
            for i in bu:
                itm_lelang.append(i.item_lelang)
            return models.round_schedule_smra2.objects.filter(item__in=itm_lelang).order_by('item')
        else:
            return models.round_schedule_smra2.objects.all().order_by('item')
