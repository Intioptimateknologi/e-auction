from rest_framework import generics, status, viewsets, permissions
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import filters
import json
from django import core
from datetime import datetime, date
from datetime import datetime, timedelta
from django.utils import timezone
from . import serializers
from . import models
from . import tasks
from . import utils
from userman.models import Users, bidder, bidder_perwakilan, bidder_user
from smra.models import round_schedule_smra, bidding_round_smra, bidding_round_smra
from adm_lelang.models import bidder_lelang, item_lelang, detail_itemlelang
from datetime import datetime
from channels.layers import get_channel_layer
import asyncio
from asgiref.sync import async_to_sync, sync_to_async
import django_filters.rest_framework
from background_task.models import Task as BTask
from django.db import connection
from django.db import reset_queries
import locale
from terbilang import Terbilang
import django_renderpdf
from django.core.files.base import ContentFile, File
import os
import requests
from django.conf import settings


class sum_round_ccaViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_sanggahan class"""

    queryset = models.sum_round_cca.objects.all()
    serializer_class = serializers.sum_round_ccaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend ]
    filterset_fields = ('item_lelang',)
    pagination_class = None

class round_ccaViewSet(viewsets.ModelViewSet):
    """ViewSet for the penyampaian_sanggahan class"""

    queryset = models.round_cca.objects.all()
    serializer_class = serializers.round_ccaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend ]
    filterset_fields = ('bidder','item_lelang')
    pagination_class = None

    @action(detail=True, methods=['get'])
    def init(self, request, pk=None):
        itm_llg = item_lelang.objects.get(id=pk)
        b_task = BTask.objects.all().filter(task_name = "cca.tasks.round2_start", creator_object_id = itm_llg.id	)
        b_task.delete()
        b_task = BTask.objects.all().filter(task_name = "cca.tasks.round2_stop", creator_object_id = itm_llg.id	)
        b_task.delete()
        # get bidder
        obyek = models.obyek_seleksi_cca.objects.all().filter(item=itm_llg)
        for ob in obyek:
            updated_values = {'round':1, 'status_round':'INI',"eli_point": ob.eli_awal}
            (obj, created) = models.round_cca.objects.update_or_create(item_lelang=ob.item, bidder=ob.bidder_user, defaults=updated_values)
            item_llg = detail_itemlelang.objects.all().filter(item_lelang=ob.item, disabled=False)
            models.round_detail_cca.objects.filter(parent=obj).delete()
            for i in item_llg:
                updated_values = {'price':0, 'block':0,"prev_price": i.harga_minimal, "prev_block":0, "eli_per_block": i.eligibility_point_per_block, 
                "spectrum_cap": i.spectrum_cap, "max_blok": i.max_block, "harga_minimal":i.harga_minimal,"valid": False}
                models.round_detail_cca.objects.update_or_create(item=i, parent = obj, defaults=updated_values)


        hasil2 = models.hasil_detail_cca.objects.all().filter(item__item_lelang__id=itm_llg.id)
        hasil2.delete()
        hasil2 = models.hasil2_detail_cca.objects.all().filter(item__item_lelang__id=itm_llg.id)
        hasil2.delete()
        hasil = models.hasil_cca.objects.all().filter(item_lelang=itm_llg.id)
        hasil.delete()
        utils.ws_publish({"sender":"start","message":"status_changed"})
        return Response({"statuss":"OK"})

    @action(detail=True, methods=['get'])
    def start(start, request, pk=None):
        itm_llg = item_lelang.objects.get(id=pk)
        obyek = models.obyek_seleksi_cca.objects.all().filter(item=itm_llg)
        dt = timezone.localtime().time()
        td = str(timezone.localtime().today().isoweekday())    
        round = round_schedule_smra.objects.all().filter(item=itm_llg).filter(hari=td).filter(mulai__gte=dt).order_by('mulai').first()
        if round:
            mulai = timezone.make_aware(datetime.combine(timezone.localtime().today(),round.mulai))
            selesai = timezone.make_aware(datetime.combine(timezone.localtime().today(), round.selesai))
            for ob in obyek:
                updated_values = {'status_round':'WAI', 'lock': False, 'mulai': mulai, 'selesai':selesai}
                models.round_cca.objects.update_or_create(bidder=ob.bidder_user, item_lelang=itm_llg, defaults=updated_values)
            selesai = round.selesai.isoformat()

            tasks.round2_start(pk, selesai, schedule=mulai, verbose_name=str(pk), creator=itm_llg)
            #tasks.round2_stop(pk, schedule=round.selesai, verbose_name=str(pk))
            utils.ws_publish({"sender":"start","message":"status_changed"})
            return Response({"status":"OK"})
        else:
            return Response({"status":"Hari ini tidak ada jadwal"})

    @action(detail=True, methods=['get'])
    def start2(start, request, pk=None):
        itm_llg = item_lelang.objects.get(id=pk)
        obyek = models.obyek_seleksi_cca.objects.all().filter(item=itm_llg)
        dt = timezone.localtime().time()
        td = str(timezone.localtime().today().isoweekday())    
        round = round_schedule_smra.objects.all().filter(item=itm_llg).filter(hari=td).filter(mulai__gte=dt).order_by('mulai').first()
        if round:
            mulai = timezone.make_aware(datetime.combine(timezone.localtime().today(),round.mulai))
            selesai = timezone.make_aware(datetime.combine(timezone.localtime().today(), round.selesai))
            putaran = models.round_cca.objects.filter(item_lelang=itm_llg)[0]
            for ob in obyek:
                updated_values = {'status_round':'WAI', 'lock': False, 'mulai': mulai, 'selesai':selesai, 'jenis':'SUPLE', 'round': putaran.round+1}
                models.round_cca.objects.update_or_create(bidder=ob.bidder_user, item_lelang=itm_llg, defaults=updated_values)
            selesai = round.selesai.isoformat()

            tasks.round3_start(pk, selesai, schedule=mulai, verbose_name=str(pk), creator=itm_llg)
            #tasks.round2_stop(pk, schedule=round.selesai, verbose_name=str(pk))
            utils.ws_publish({"sender":"start","message":"status_changed"})
            return Response({"status":"OK"})
        else:
            return Response({"status":"Hari ini tidak ada jadwal"})

    @action(detail=True, methods=['get'])
    def resume(start, request, pk=None):
        itm_llg = item_lelang.objects.get(id=pk)
        obyek = models.obyek_seleksi_cca.objects.all().filter(item=itm_llg)
        dt = timezone.now()
        td = str(date.today().isoweekday())    
        round = round_schedule_smra.objects.all().filter(item=itm_llg).filter(hari=td).filter(mulai__gte=dt).order_by('mulai').first()
        if round:
            mulai = datetime.combine(date.today(),round.mulai)
            selesai = datetime.combine(date.today(), round.selesai)
            for bdr in bidder:
                updated_values = {'status_round':'WAI', 'lock': False, 'mulai': mulai, 'selesai':selesai}
                models.round_cca.objects.update_or_create(bidder=bdr.bidder, item_lelang=pk, defaults=updated_values)
        #   tasks.round2_start(pk, selesai.timestamp(), schedule=mulai, verbose_name=str(pk))
            #tasks.round2_stop(pk, schedule=round.selesai, verbose_name=str(pk))
            return Response({"status":"OK"})
        else:
            return Response({"status":"Hari ini tidak ada jadwal"})

    @action(detail=True, methods=['get'])
    def next_round(start, request, pk=None):
        #item_lelang = item_lelang.objects.get(pk=pk)
        bidder = bidder_lelang.objects.all().filter(item_lelang=pk)
        dt = timezone.now()
        td = str(date.today().isoweekday())    
        round = round_schedule_smra.objects.all().filter(item=pk).filter(hari=td).filter(mulai__gte=dt).order_by('mulai').first()
        if round:
            mulai = datetime.combine(date.today(),round.mulai)
            selesai = datetime.combine(date.today(), round.selesai)
            putaran = models.round_cca.objects.all().filter(item_lelang=pk)[0]
            for bdr in bidder:
                updated_values = {'round':putaran.round+1, 'status_round':'WAI', 'lock': False, 'mulai': mulai, 'selesai':selesai}
                models.round_cca.objects.update_or_create(bidder=bdr.bidder, item_lelang=pk, defaults=updated_values)
            return Response({"status":"OK"})
        else:
            return Response({"status":"Hari ini tidak ada jadwal"})


    @action(detail=True, methods=['get'])
    def run_now(start, request, pk=None):
        bidder = bidder_lelang.objects.all().filter(item_lelang=pk)
        for bdr in bidder:
            updated_values = {'status_round':'STA'}
            models.round_cca.objects.update_or_create(bidder=bdr.bidder, item_lelang=pk, defaults=updated_values)
        return Response({"statuss":"OK"})

    @action(detail=True, methods=['get'])
    def reset_round(start, request, pk=None):
        itm_llg = item_lelang.objects.get(id=pk)
        b_task = BTask.objects.all().filter(task_name = "cca.tasks.round2_start", creator_object_id = itm_llg.id	)
        b_task.delete()
        b_task = BTask.objects.all().filter(task_name = "cca.tasks.round2_stop", creator_object_id = itm_llg.id	)
        b_task.delete()
        if request.GET.get('r'):
            r = request.GET.get('r')
        else:
            r = 1
        bidder = models.obyek_seleksi_cca.objects.all().filter(item=pk)
        for bdr in bidder:
            m = models.round_cca.objects.get(bidder=bdr.bidder_user, item_lelang=pk)
            m.status_round = 'WAI'
            m.save()
            parent = models.hasil_cca.objects.all().filter(bidder=bdr.bidder_user, item_lelang=pk, round=m.round)
            if parent:
                hasil2 = models.hasil_detail_cca.objects.all().filter(parent=parent)
                hasil2.delete()
                hasil2 = models.hasil2_detail_cca.objects.all().filter(parent=parent)
                hasil2.delete()
                parent.delete()

        return Response({"statuss":"OK"})

    @action(detail=True, methods=['get'])
    def stop(start, request, pk=None):
        itm_llg = item_lelang.objects.get(id=pk)
        b_task = BTask.objects.all().filter(task_name = "cca.tasks.round2_start", creator_object_id = itm_llg.id	)
        b_task.delete()
        b_task = BTask.objects.all().filter(task_name = "cca.tasks.round2_stop", creator_object_id = itm_llg.id	)
        b_task.delete()
        tasks.round_stop(pk, timezone.now())
        obyek = models.obyek_seleksi_cca.objects.all().filter(item=itm_llg)
        for ob in obyek:
            updated_values = {'status_round':'STO'}
            models.round_cca.objects.update_or_create(bidder=ob.bidder_user, item_lelang=itm_llg, defaults=updated_values)
        utils.ws_publish({"sender":"start","message":"status_changed"})
        return Response({"statuss":"OK"})

    
    @action(detail=True, methods=['get'])
    def pause(start, request, pk=None):
        itm_llg = item_lelang.objects.get(id=pk)
        b_task = BTask.objects.all().filter(task_name = "cca.tasks.round2_start", creator_object_id = itm_llg.id	)
        b_task.delete()
        b_task = BTask.objects.all().filter(task_name = "cca.tasks.round2_stop", creator_object_id = itm_llg.id	)
        b_task.delete()
        obj = models.round_cca.objects.filter(item_lelang=itm_llg).first()
        r = obj.round

        obyek = models.obyek_seleksi_cca.objects.all().filter(item=itm_llg)
        for ob in obyek:
            updated_values = {'status_round':'INI','round':r,
                'item_lelang':itm_llg, 'lock':False
                }
            models.round_cca.objects.update_or_create(bidder=ob.bidder_user, item_lelang=itm_llg, defaults=updated_values)
            hasil = models.hasil_cca.objects.all().filter(bidder=ob.bidder_user, item_lelang=pk, round=r)
        return Response({"statuss":"OK"})

    @action(detail=True, methods=['get'])
    def close(start, request, pk=None):
        itm_llg = item_lelang.objects.get(id=pk)
        b_task = BTask.objects.all().filter(task_name = "cca.tasks.round2_start", creator_object_id = itm_llg.id	)
        b_task.delete()
        b_task = BTask.objects.all().filter(task_name = "cca.tasks.round2_stop", creator_object_id = itm_llg.id	)
        b_task.delete()
        obj = models.round_cca.objects.filter(item_lelang=itm_llg).first()
        r = obj.round
        tasks.round_stop(pk, timezone.now())
        bidder = models.obyek_seleksi_cca.objects.all().filter(item=pk)
        for bdr in bidder:
            updated_values = {'status_round':'CLO','round':r}
            models.round_cca.objects.update_or_create(bidder=bdr.bidder_user, item_lelang=pk, defaults=updated_values)
        return Response({"statuss":"OK"})

    @action(detail=False, methods=['post'])
    def submit_bid(self, request):
        def find(arr, val):
            for key in arr:
                if key.get(val):
                    return key[val]

        def check_reveal(d1, d2):
            keys_list = [list(item.keys())[0] for item in d1]
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

        peruri_docker_url = settings.PERURI_DOCKER
        from pdfminer.high_level import extract_pages
        from pdfminer.layout import LTTextContainer
        data = request.data['data']
        eli_err = request.data['eli_err']
        eli = request.data['eli']
        assignment = False
        if request.data.get('assignment'):
            assignment = True
        perwakilan = request.data['perwakilan']
        activity = request.data['activity']
        wakil_id = request.data['perwakilan']['id']
        item_lelang = request.data['item_lelang']
        locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
        accepted = False
        putaran = 1
        bdr = bidder_user.objects.get(users__id=request.user.id)
        if assignment:
            eli_err = False
        #save hasilnya duluan
        if eli_err:
            #construct summary
            summary = {}
            json_agg = []
            putaran = int(data[0]['round'])
            for d in data:
                json_agg.append({str(d['item']) : {'block':int(d['block']),'price':float(d['price'])}})
            #summary = {"json_agg": json_agg}
            #print(summary)
            if putaran == 1:
                # check reveal ke 1
                m = models.matrix_hasil_cr.objects.all().filter(parent__item_lelang = item_lelang, parent__bidder = bdr, parent__round=1)
                s1 = m[0].json_agg
                s2 = json_agg

                if (utils.check_reveal(s1,s2))> 0:
                    accepted = True
            else:
                s2 = json_agg
                accepted = True
                for i in range(1,putaran):
                    m = models.matrix_hasil_cr.objects.all().filter(parent__item_lelang = item_lelang, parent__bidder = bdr, parent__round=i)
                    if m[0].parent.eli > m[0].parent.activity:
                        s1 = m[0].json_agg
                        ret = check_reveal(s1,s2)
                        accepted = accepted and (ret > 0)
            return Response({"step":"reveal", "status":'gagal'})
        else:
            accepted = True
        if assignment:
            accepted = True


        if accepted:
            vbidder = 0
            vitem = 0
            data_template = []
            putaran = 1
            total = 0
            t = Terbilang()
            dt = timezone.localtime().now()
            total_eli = 0
            #round_c = models.round_cca.objects.filter(item=request.data['item_lelang']).first()

            parent = None
            for d in data:
                obj = models.round_detail_cca.objects.get(pk=d['id'])
                obj.block = int(d['block'])
                obj.price = float(d['price'])
                obj.activity = int(d['block'])*int(d['eli_per_block'])
                obj.prev_block = int(d['block'])
                obj.prev_price = float(d['price'])
                parent = obj.parent
                putaran = int(data[0]['round'])
                obj.save()
                vbidder = bdr
                vitem = d['item']
                item_llg = detail_itemlelang.objects.get(pk=d['item'])
                total = total + float(d['price'])*int(d['block'])
                data_template.append({
                    'price':float(d['price']),
                    'block':int(d['block']),
                    'putaran':putaran, 
                    'band':item_llg.band,
                    'tblock': t.parse(int(d['block'])).getresult(),
                    'tputaran': t.parse(putaran).getresult(),
                })
            parent.lock = True
            parent.save()

            updated_values = {'eli_point': activity}
            (parent, create) = models.round_cca.objects.update_or_create(bidder=bdr, item_lelang=item_lelang, defaults=updated_values)
            if assignment:
                updated_values = {"jenis": 'ASSI','activity': activity, 'eli': eli, 'revelaled':eli_err}
            else:
                updated_values = {"jenis": 'CLOCK','activity': activity, 'eli': eli, 'revelaled':eli_err}
            (parent, create) = models.hasil_cca.objects.update_or_create(bidder=bdr, round=putaran, item_lelang=item_lelang, defaults=updated_values)

            for d in data:
                dtl=detail_itemlelang.objects.get(pk = d['item'])
                updated_values = {"block":int(d['block']), "price":float(d['price'])}
                (obj, create) = models.hasil_detail_cca.objects.update_or_create(parent=parent, item=dtl, defaults=updated_values)

            obj = models.hasil_detail_cca.objects.filter(parent=parent)
            models.hasil2_detail_cca.objects.filter(parent=parent).delete()
            for o in obj:
                blok = o.block
                for i in range(0,blok):
                    newob = models.hasil2_detail_cca(parent = parent, item = o.item, price = o.price, submit = o.submit)
                    newob.save()

            currentdir = os.getcwd()
            filename = "ba_cca_"+str(vitem)+"_"+ str(vbidder) + "_"+ str(putaran) + ".pdf"
            pathname = currentdir + "/media/upload/bidder/" + filename
            with open(pathname,"wb") as my_file:
                context = {}
                user = self.request.user
                harga = float(d['price'])
                block = int(d['block'])
                vbidder_perwakilan = bidder_perwakilan.objects.all().get(id = perwakilan['id'])
                if vbidder_perwakilan:
                    bidder_id = vbidder_perwakilan.bidder_id
                    vbidder = bidder.objects.all().filter(id = bidder_id)
                    context["bidder"] = bdr.bidder
                    vbidder_lelang = bidder_lelang.objects.all().filter(bidder = bidder_id)
                    context["bidder_lelang"] = vbidder_lelang
                    context["bidder_id"] = bidder_id
                    context["wakil"] = vbidder_perwakilan.nama_lengkap
                    context["tahun"] = item_llg.item_lelang.tahun
                    context["seleksi"] = item_llg.item_lelang
                    context["obyek"] = data_template
                    context["total"] = total
                    context["ttotal"] = t.parse(int(total)).getresult()
                    context["putaran"] = putaran
                    context["tputaran"] = t.parse(putaran).getresult()
                django_renderpdf.helpers.render_pdf(template= ["ba_putaran_cca.html"], file_= my_file, context= context)
                my_file.close()
                updated_values = {'valid':False, 'perwakilan': vbidder_perwakilan}
                #putaran = int(d['data']['round'])
                hasil, created = models.hasil_cca.objects.update_or_create(round=putaran,  bidder__id=bidder_id, item_lelang=item_lelang, defaults=updated_values)
                with open(pathname, "rb") as f:
                    myfile = File(f)
                    hasil.berita_acara_unsigned.save(filename, myfile, save=True)


            bbox = ()
            for page_layout in extract_pages(pathname):
                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        if hasattr(element, 'bbox'):
                            if element.get_text().startswith("Jakarta"):
                                bbox = element.bbox
                                print(element.bbox)

            url = "http://"+settings.PERURI_DOCKER+"/v1/doc/upload"
            payload = {'profileName': vbidder_perwakilan.profil_peruri}
            files=[
                ('file',(filename,open(pathname,'rb'),'application/pdf'))
            ]
            response = requests.request("POST", url, files=files)
            data = json.loads(response.text)
            if data['errorCode']!="0":
                return Response({"step":"document", "status":data})
            else:
                fileId = data['saveAs']
                url1 = settings.PERURI_CLOUD+"gateway/jwtSandbox/1.0/getJsonWebToken/v1"
                payload = json.dumps({
                    "param": {
                        "systemId": "PERURI-DEPLOY-HASH"
                    }
                })
                headers = {
                    'Content-Type': 'application/json',
                    'x-Gateway-APIKey': settings.PERURI_API_KEY
                }
                response = requests.request("POST", url1, headers=headers, data=payload)
                jwt = json.loads(response.text)
                #data_jwt = jwt.data.jwt
                data_jwt = jwt["data"]["jwt"]
                # session init
                url2 = settings.PERURI_CLOUD+"gateway/digitalSignatureOnPremise/1.0/sessionInitiate/v1"
                payload = json.dumps({
                "param": {
                    "email": vbidder_perwakilan.profil_peruri,
                    "systemId": "PERURI-DEPLOY-HASH",
                    "sendEmail": "0",
                    "sendSms": "0",
                    "sendWhatsapp": "1"
                }
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + jwt["data"]["jwt"],
                    'x-Gateway-APIKey': settings.PERURI_API_KEY
                }
                response = requests.request("POST", url2, headers=headers, data=payload)
                session = json.loads(response.text)

                return Response({"step":"session","email": vbidder_perwakilan.profil_peruri, "bbox":'-'.join([str(value) for value in bbox]), "session":session, "putaran": putaran, "bidder": bdr.id, "wakil": perwakilan['id'], "item_lelang": item_lelang,"session":session, "fileid": fileId, "jwt": jwt["data"]["jwt"] })

                #return Response({"step":"session","putaran": putaran, "bidder": bdr.id, "item_lelang": item_llg.item_lelang.id,"session":session, "fileid": fileId, "jwt": jwt["data"]["jwt"] })

    @action(detail=False, methods=['post'])
    def submit_bid_sr(self, request):
        def find(arr, val):
            for key in arr:
                if key.get(val):
                    return key[val]

        def check_reveal(d1, d2):
            keys_list = [list(item.keys())[0] for item in d1]
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

        peruri_docker_url = settings.PERURI_DOCKER
        from pdfminer.high_level import extract_pages
        from pdfminer.layout import LTTextContainer
        data = request.data['data']
        eli_err = request.data['eli_err']
        eli = request.data['eli']
        parent = request.data['parent']
        perwakilan = request.data['perwakilan']
        activity = request.data['activity']
        wakil_id = request.data['perwakilan']['id']
        item_lelang = request.data['item_lelang']
        locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
        accepted = False
        putaran = int(request.data['round'])
        bdr = bidder_user.objects.get(users__id=request.user.id)

        #save hasilnya duluan
        if eli_err:
            #construct summary
            summary = {}
            json_agg = []
            putaran = int(data[0]['round'])
            for d in data:
                json_agg.append({str(d['item']) : {'block':int(d['block']),'price':float(d['price'])}})
            #summary = {"json_agg": json_agg}
            #print(summary)
            if putaran == 1:
                # check reveal ke 1
                m = models.matrix_hasil_cr.objects.all().filter(parent__item_lelang = item_lelang, parent__bidder = bdr, parent__round=1)
                s1 = m[0].json_agg
                s2 = json_agg

                if (utils.check_reveal(s1,s2))> 0:
                    accepted = True
            else:
                s2 = json_agg
                accepted = True
                for i in range(1,putaran):
                    m = models.matrix_hasil_cr.objects.all().filter(parent__item_lelang = item_lelang, parent__bidder = bdr, parent__round=i)
                    if m[0].parent.eli > m[0].parent.activity:
                        s1 = m[0].json_agg
                        ret = check_reveal(s1,s2)
                        accepted = accepted and (ret > 0)
            return Response({"step":"reveal", "status":'gagal'})
        else:
            accepted = True


        if accepted:
            vbidder = 0
            vitem = 0
            data_template = []
            total = 0
            t = Terbilang()
            dt = timezone.localtime().now()
            total_eli = 0
            #round_c = models.round_cca.objects.filter(item=request.data['item_lelang']).first()

            #parent = None
            for d in data:
                obj = models.hasil_detail_cca.objects.filter(parent = parent)
#                obj = models.round_detail_cca.objects.get(pk=d['id'])
#                obj.block = int(d['block'])
#                obj.price = float(d['price'])
#                obj.activity = int(d['block'])*int(d['eli_per_block'])
#                obj.prev_block = int(d['block'])
#                obj.prev_price = float(d['price'])
                parent = obj[0].parent
#                obj.save()
                vbidder = bdr
                vitem = d['item_id']
                item_llg = detail_itemlelang.objects.get(pk=d['item_id'])
                total = total + float(d['price'])*int(d['block'])
                data_template.append({
                    'price':float(d['price']),
                    'block':int(d['block']),
                    'putaran':putaran, 
                    'band':item_llg.band,
                    'tblock': t.parse(int(d['block'])).getresult(),
                    'tputaran': t.parse(putaran).getresult(),
                })

            updated_values = {'eli_point': activity}
            (parent, create) = models.round_cca.objects.update_or_create(bidder=bdr, item_lelang=item_lelang, defaults=updated_values)
            updated_values = {"jenis": 'SUPLE','activity': activity, 'eli': eli, 'revelaled':eli_err}
            (parent, create) = models.hasil_cca.objects.update_or_create(bidder=bdr, round=putaran, item_lelang=item_lelang, defaults=updated_values)
            print(parent, create, bdr, item_lelang, putaran, updated_values)
            for d in data:
                dtl=detail_itemlelang.objects.get(pk = d['item_id'])
                updated_values = {"block":int(d['block']), "price":float(d['price'])}
                (obj, create) = models.hasil_detail_cca.objects.update_or_create(parent=parent, item=dtl, defaults=updated_values)

            obj = models.hasil_detail_cca.objects.filter(parent=parent)
            models.hasil2_detail_cca.objects.filter(parent=parent).delete()
            for o in obj:
                blok = o.block
                for i in range(0,blok):
                    newob = models.hasil2_detail_cca(parent = parent, item = o.item, price = o.price, submit = o.submit)
                    newob.save()

            currentdir = os.getcwd()
            filename = "ba_cca_"+str(vitem)+"_"+ str(vbidder) + "_"+ str(putaran) + ".pdf"
            pathname = currentdir + "/media/upload/bidder/" + filename
            with open(pathname,"wb") as my_file:
                context = {}
                user = self.request.user
                harga = float(d['price'])
                block = int(d['block'])
                vbidder_perwakilan = bidder_perwakilan.objects.all().get(id = perwakilan['id'])
                if vbidder_perwakilan:
                    bidder_id = vbidder_perwakilan.bidder_id
                    vbidder = bidder.objects.all().filter(id = bidder_id)
                    context["bidder"] = bdr.bidder
                    vbidder_lelang = bidder_lelang.objects.all().filter(bidder = bidder_id)
                    context["bidder_lelang"] = vbidder_lelang
                    context["bidder_id"] = bidder_id
                    context["wakil"] = vbidder_perwakilan.nama_lengkap
                    context["tahun"] = item_llg.item_lelang.tahun
                    context["seleksi"] = item_llg.item_lelang
                    context["obyek"] = data_template
                    context["total"] = total
                    context["ttotal"] = t.parse(int(total)).getresult()
                    context["putaran"] = putaran
                    context["tputaran"] = t.parse(putaran).getresult()
                django_renderpdf.helpers.render_pdf(template= ["ba_putaran_cca.html"], file_= my_file, context= context)
                my_file.close()
                updated_values = {'valid':False, 'perwakilan': vbidder_perwakilan}
                #putaran = int(d['data']['round'])
                hasil, created = models.hasil_cca.objects.update_or_create(round=putaran,  bidder__id=bidder_id, item_lelang=item_lelang, defaults=updated_values)
                with open(pathname, "rb") as f:
                    myfile = File(f)
                    hasil.berita_acara_unsigned.save(filename, myfile, save=True)


            bbox = ()
            for page_layout in extract_pages(pathname):
                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        if hasattr(element, 'bbox'):
                            if element.get_text().startswith("Jakarta"):
                                bbox = element.bbox
                                print(element.bbox)

            url = "http://"+peruri_docker_url+"/v1/doc/upload"
            payload = {'profileName': vbidder_perwakilan.profil_peruri,}
            files=[
                ('file',(filename,open(pathname,'rb'),'application/pdf'))
            ]
            response = requests.request("POST", url, files=files)
            data = json.loads(response.text)
            if data['errorCode']!="0":
                return Response({"step":"document", "status":data})
            else:
                fileId = data['saveAs']
                url1 = settings.PERURI_CLOUD+"gateway/jwtSandbox/1.0/getJsonWebToken/v1"
                payload = json.dumps({
                    "param": {
                        "systemId": "PERURI-DEPLOY-HASH"
                    }
                })
                headers = {
                    'Content-Type': 'application/json',
                    'x-Gateway-APIKey': settings.PERURI_API_KEY
                }
                response = requests.request("POST", url1, headers=headers, data=payload)
                jwt = json.loads(response.text)
                #data_jwt = jwt.data.jwt
                data_jwt = jwt["data"]["jwt"]
                # session init
                url2 = settings.PERURI_CLOUD+"gateway/digitalSignatureOnPremise/1.0/sessionInitiate/v1"
                payload = json.dumps({
                "param": {
                    "email": vbidder_perwakilan.profil_peruri,
                    "systemId": "PERURI-DEPLOY-HASH",
                    "sendEmail": "0",
                    "sendSms": "0",
                    "sendWhatsapp": "1"
                }
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + jwt["data"]["jwt"],
                    'x-Gateway-APIKey': settings.PERURI_API_KEY
                }
                response = requests.request("POST", url2, headers=headers, data=payload)
                session = json.loads(response.text)

                return Response({"step":"session","email":vbidder_perwakilan.profil_peruri,"bbox":'-'.join([str(value) for value in bbox]), "session":session, "putaran": putaran, "bidder": bdr.id, "wakil": perwakilan['id'], "item_lelang": item_lelang,"session":session, "fileid": fileId, "jwt": jwt["data"]["jwt"] })

    @action(detail=True, methods=['get'])
    def optim(self, request, pk=None):
        import numpy
        from itertools import chain, combinations, product
        def approach5_1(list_of_arrays):
            num_of_array = len(list_of_arrays)
            #print(num_of_array)
            datatype = numpy.result_type(*list_of_arrays)
            array = numpy.empty([len(a) for a in list_of_arrays] + [num_of_array], dtype=datatype)
            for i, a in enumerate(numpy.ix_(*list_of_arrays)):
                array[...,i] = a
            return array.reshape(-1, num_of_array)
        def calc_price(arr):
            retval = []
            parent = []
            k = {}
            for a in arr:
                item = 0
                max_block = 0
                block = 0
                price = 0
                parent.append(a.parent.id)
                #print(a.json_agg)
                for j in a.json_agg:
                    idx = str(j['item_id'])
                    if  k.get(idx):
                        k[idx]['price'] = k[idx]['price'] + j['price']
                        k[idx]['block'] = k[idx]['block'] + j['block']
                        k[idx]['max_block'] = j['max_block']
                    else:
                        k[idx]  = {'price':0, 'block': 0, 'max_block' :0}
                        k[idx]['price'] = k[idx]['price'] + j['price']
                        k[idx]['block'] = k[idx]['block'] + j['block']
                        k[idx]['max_block'] = j['max_block']
            hasilnya = {'parent':parent, 'item': k}
            key = hasilnya['item'].keys()
            total = 0
            valid = True
            for ret in key:
                block = hasilnya['item'][ret]['block']
                max_block = hasilnya['item'][ret]['max_block']
                total = total + hasilnya['item'][ret]['price']*hasilnya['item'][ret]['block']
                if (max_block >= block):
                    hasilnya['item'][ret]['valid'] = True
                    valid = valid and True
                else:
                    hasilnya['item'][ret]['valid'] = False
                    valid = valid and False
            retval.append({'parent':parent, 'item': k, 'total': total, 'valid': valid})
            return retval

        itm_llg = item_lelang.objects.get(id=pk)
        obyek = models.obyek_seleksi_cca.objects.all().filter(item=itm_llg)
        dt = timezone.localtime().time()
        td = str(timezone.localtime().today().isoweekday())    
        round = round_schedule_smra.objects.all().filter(item=itm_llg).filter(hari=td).filter(mulai__gte=dt).order_by('mulai').first()
        if round:
            mulai = timezone.make_aware(datetime.combine(timezone.localtime().today(),round.mulai))
            selesai = timezone.make_aware(datetime.combine(timezone.localtime().today(), round.selesai))
            dtl=detail_itemlelang.objects.filter(item_lelang = pk, disabled=False)
            parent = models.round_cca.objects.filter(item_lelang=pk)
            ronde = parent[0].round
            
            hasil = models.hasil_cca.objects.all().filter(item_lelang = pk).distinct('bidder')
            m = []
            jumlah_bidder = len(hasil)
            for a in hasil:
                m.append(numpy.array(models.matrix2_cr.objects.all().filter(parent__item_lelang = pk, parent__bidder=a.bidder).distinct('kombinasi').order_by('kombinasi','-parent__round')))
            combs = []
            kombinasi = []
            for i in range(1,jumlah_bidder+1):
                b = combinations(range(1,jumlah_bidder+1),i)
                combs.append(list(b))
            for c in combs:
                for d in c:
                    l = []
                    e = numpy.asarray(d)
                    for f in e:     
                        l.append(m[f-1])
                    Output = approach5_1(l)
                    kombinasi.append(Output)
            hasil = []
            for k in kombinasi:
                for l in k:
                    a = calc_price(l)
                    if (a[0]['valid']):
                        hasil.append(a)

            #urutkan dengan nilai tertinggi
            hasil.sort(key=lambda x: x[0]['total'], reverse=True)    
            data_optim = hasil[0]
            for d in dtl:
                for prn in parent:
                    prn.status_round='WAI'
                    prn.mulai = mulai
                    prn.selesai = selesai
                    prn.round = ronde + 1
                    prn.jenis = 'ASSI'
                    prn.save()
                    r = models.round_detail_cca.objects.all().filter(parent=prn, item=d)
                    r[0].block = 0
                    r[0].prev_blok = 0
                    r[0].lock = False
                    r[0].save()

            
            prn_hasil = data_optim[0]['parent']
            item_hasil = data_optim[0]['item'].keys()
            for a in prn_hasil:
                for b in item_hasil:
                    p = models.hasil_cca.objects.get(id = a)
                    r = models.round_detail_cca.objects.all().filter(item=int(b), parent__bidder = p.bidder, parent__round = ronde+1)
                    if r:
                        q = models.hasil_detail_cca.objects.get(parent=p, item=int(b))
                        print(q.price)
                        r[0].block = q.block
                        r[0].price = q.price
                        r[0].prev_price = q.price
                        r[0].prev_blok = q.block
                        r[0].lock = False
                        r[0].save()
            tasks.round3_start(pk, selesai.time().isoformat(), schedule=mulai, verbose_name=str(pk), creator=itm_llg)
            utils.ws_publish({"sender":"start","message":"status_changed"})
            return Response({"status":"OK"})
        else:
            return Response({"status":"Hari ini tidak ada jadwal"})


    @action(detail=True, methods=['get'])
    def send_document(self, request, pk=None):
        url = "http://localhost:9044/v1/doc/upload"
        payload = {'profileName': 'bayu.poc104@yopmail.com'}
        files=[
            ('file',('signature.png',open('/home/auction/kominfo2/media/upload/bidder/porter.pdf','rb'),'image/png'))
        ]
        response = requests.request("POST", url, files=files)
        data = json.loads(response.text)
        return Response({"status":data})

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
            "email": "bayu.poc104@yopmail.com",
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
        payload = {'profileName': 'bayu.poc104@yopmail.com'}
        files=[
            ('file',('signature.png',open('/home/auction/kominfo2/media/upload/bidder/porter.pdf','rb'),'image/png'))
        ]
        response = requests.request("POST", url, files=files)
        data = json.loads(response.text)'''
        return Response({"session":session, "jwt": jwt["data"]["jwt"] })

    @action(detail=True, methods=['get'])
    def sign(self, request, pk=None):
        peruri_docker_url = settings.PERURI_DOCKER
        user = request.user

        jwt = request.GET.get('jwt')
        fileid = request.GET.get('fileid')
        otp = request.GET.get('otp')
        token = request.GET.get('token')
        putaran = request.GET.get('putaran')
        bidder_id = request.GET.get('bidder')
        item_lelang_id = request.GET.get('item_lelang')
        wakil = request.GET.get('wakil')
        bbox = request.GET.get('bbox').split('-')
        vbidder_perwakilan = bidder_perwakilan.objects.all().get(pk = int(wakil))

        bidder_id = vbidder_perwakilan.bidder.id
        #item_llg = item_lelang.objects.get(pk=item_lelang_id)
        bdr = bidder_user.objects.get(pk=bidder_id)

        parent= models.hasil_cca.objects.filter(bidder=bdr, round=putaran, item_lelang=item_lelang_id)
        if parent:
            parent[0].valid = True
            parent[0].save()

        return Response({"status":"OK"})

        #validate token
        url2 = settings.PERURI_CLOUD+"gateway/digitalSignatureOnPremise/1.0/sessionValidation/v1"

        payload = json.dumps({
            "param": {
                "email": vbidder_perwakilan.profil_peruri,
                "systemId": "PERURI-DEPLOY-HASH",
                "tokenSession": token,
                "otpCode": otp
            }
        })
        headers = {
            '$resourceID': 'voluptate Lorem eu Excepteur',
            '$path': 'voluptate Lorem eu Excepteur',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + jwt
        }

        response = requests.request("POST", url2, headers=headers, data=payload)
        session = json.loads(response.text)
        print(session)
        if session['resultCode']=='04':
            return Response({"status":"NOK", "message": "Invalid OTP"}) 
        user = request.user
        vbidder_perwakilan = bidder_perwakilan.objects.all().filter(users_id = user.id)
        bidder_id = vbidder_perwakilan[0].bidder_id
        ttd = signature2.objects.all().filter(bidder=bidder_id)[0]

        url2 = "http://"+settings.PERURI_DOCKER+":9044/v1/doc/sign"

        payload = json.dumps({
        "systemId": "PERURI-DEPLOY-HASH",
        "profileName":vbidder_perwakilan.profil_peruri,
        "src": fileid,
        "docPass": "",
        "location": "Jakarta",
        "reason": "I agree to sign",
        "coordinate": {
            "specimenImage": ttd.uid,
            "page": 1,
            "llx": 7,
            "lly": 61,
            "urx": 51,
            "ury": 105
        }
        })
        headers = {
        '$resourceID': 'voluptate Lorem eu Excepteur',
        '$path': 'voluptate Lorem eu Excepteur',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + jwt,
        'x-Gateway-APIKey': settings.PERURI_API_KEY
        }

        response = requests.request("POST", url2, headers=headers, data=payload)
        file = os.path.splitext(fileid)[0]
        url3 = "http://"+settings.PERURI_DOCKER+":9044/v1/doc/download?idFile="+file

        payload = {}
        headers = {
        '$resourceID': 'voluptate Lorem eu Excepteur',
        '$path': 'voluptate Lorem eu Excepteur',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + jwt,
        'x-Gateway-APIKey': settings.PERURI_API_KEY
        }
        response = requests.request("GET", url3, headers=headers, data=payload)
        item_llg = detail_itemlelang.objects.all().filter(item_lelang=item_lelang_id)
        bdr = bidder.objects.get(pk=bidder_id)
        for i in item_llg:
            hasil = models.hasil_cca.objects.all().filter(round=putaran).filter(bidder=bdr).filter(item=i)[0]
            hasil.berita_acara.save(fileid, ContentFile(response.content))
            hasil.valid = True
            hasil.save()

        return Response({"status":"OK"})

class hasil_ccaViewSet(viewsets.ModelViewSet):
     """ViewSet for the penyampaian_sanggahan class"""

     queryset = models.hasil_cca.objects.all()
     serializer_class = serializers.hasil_ccaSerializer
     permission_classes = [permissions.IsAuthenticated]
     filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
     filterset_fields = ('bidder','item_lelang')

class round_detail_ccaViewSet(viewsets.ModelViewSet):
     """ViewSet for the penyampaian_sanggahan class"""

     queryset = models.round_detail_cca.objects.all()
     serializer_class = serializers.round_detail_ccaSerializer
     permission_classes = [permissions.IsAuthenticated]
     filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]
     filterset_fields = ('item','parent__bidder','parent__item_lelang','parent__round')
     ordering = ['item__urutan']
     ordering_fields = ['item__urutan']

class auctioner_hasilViewSet(viewsets.ModelViewSet):

    queryset = models.auctioner_hasil_cca.objects.all()
    serializer_class = serializers.auctioner_hasilSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('item_lelang',"round")



class obyek_seleksiViewSet(viewsets.ModelViewSet):

    queryset = models.obyek_seleksi_cca.objects.all()
    serializer_class = serializers.obyek_seleksiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_create(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class matrix_hasil_crViewSet(viewsets.ModelViewSet):

    queryset = models.matrix_hasil_cr.objects.all()
    serializer_class = serializers.matrix_hasil_crSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

class matrix2_crViewSet(viewsets.ModelViewSet):

    queryset = models.matrix2_cr.objects.all()
    serializer_class = serializers.matrix2_crSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('parent__bidder','parent__item_lelang','parent__round')

class price_increaseViewSet(viewsets.ModelViewSet):

    queryset = models.cca_price_increase.objects.all()
    serializer_class = serializers.price_increaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_create(self, serializer):
        serializer.save(diubah_oleh=self.request.user)


# from django_pandas.io import read_frame

# class jadwalSMRAViewSet(viewsets.ModelViewSet):
#     """ViewSet for the penyampaian_sanggahan class"""

#     queryset = models.round_schedule_smra.objects.all()
#     serializer_class = serializers.jadwalSMRASerializer
#     permission_classes = [permissions.IsAuthenticated]
#     filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
#     filterset_fields = ('item',)

# class bidding_round_smraViewSet(viewsets.ModelViewSet):
#     """ViewSet for the penyampaian_sanggahan class"""

#     queryset = models.bidding_round_smra.objects.all()
#     serializer_class = serializers.bidding_round_smraSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
#     filterset_fields = ('item',)

#     @action(detail=True, methods=['get'])
#     def init(self, request, pk=None):
#         b_task = BTask.objects.all()
#         b_task.delete()
#         itm_llg = item_lelang.objects.get(id=pk)
#         updated_values = {'round_state':1, 'status_round':'INI'}
#         models.bidding_round_smra.objects.update_or_create(item=itm_llg, defaults=updated_values)
#         item_llg = detail_itemlelang.objects.all().filter(item_lelang=pk)
#         models.round_smra.objects.filter(item__in=item_llg).delete()
#         # get bidder
#         bidder = bidder_lelang.objects.all().filter(item_lelang=pk)
#         for bdr in bidder:
#             for item in item_llg:
#                 updated_values = {'round':1, 'price':0, 'block':0, 'prev_price':item.reserved_price, 'min_price':item.reserved_price}
#                 models.round_smra.objects.update_or_create(item=item, bidder=bdr.bidder, defaults=updated_values)
#         return Response({"statuss":"OK"})

#     @action(detail=True, methods=['get'])
#     def next_round(self, request, pk=None):
#         item_llg = item_lelang.objects.get(id=pk)
#         round = models.bidding_round_smra.objects.all().filter(item=item_llg)
#         putaran = round[0].round_state
#         # increase round
#         updated_values = {'round_state':putaran+1, 'status_round':'STA'}
#         models.bidding_round_smra.objects.update_or_create(item=item_llg, defaults=updated_values)
#         item_llg = detail_itemlelang.objects.all().filter(item_lelang=pk)
#         bidder = bidder_lelang.objects.all().filter(item_lelang=pk)
#         r_smra = models.round_smra.objects.all().filter(item__in=item_llg).filter(round=putaran)
#         for bdr in r_smra:
#             if bdr.block==0:
#                 updated_values = {'price':0, 'block':0, 'prev_price':bdr.prev_price, 'prev_block':bdr.block} # kenaikan harga role di min price
#             else:
#                 updated_values = {'price':0, 'block':0, 'prev_price':bdr.price, 'prev_block':bdr.block,'min_price':bdr.price} # kenaikan harga role di min price
#             models.round_smra.objects.update_or_create(item=bdr.item, bidder=bdr.bidder, round=putaran+1, defaults=updated_values)
#         return Response({"statuss":"OK"})


#     @action(detail=True, methods=['get'])
#     def start(self, request, pk=None):
#         item_llg = item_lelang.objects.get(id=pk)
#         round = models.bidding_round_smra.objects.all().filter(item=item_llg)
#         jadwal = models.round_schedule_smra.objects.all().filter(item=item_llg)
#         mulai = "{} {}".format(date.today(),jadwal[0].harian_mulai)
#         #print(mulai)
#         putaran = round[0].round_state
#         sekarang = datetime.now()
#         dmulai = datetime.strptime(mulai, '%Y-%m-%d %H:%M:%S')
#         if dmulai>sekarang:
#             updated_values = {'status_round':'STA','start_time': sekarang}
#         else:
#             updated_values = {'status_round':'STA'}
#         models.bidding_round_smra.objects.update_or_create(round_state=putaran,item=item_llg, defaults=updated_values)
#         datetime_object = datetime.strptime(mulai, '%Y-%m-%d %H:%M:%S')
#         tasks.round_start(pk, schedule=datetime_object)
#         return Response({"statuss":"OK"})

#     @action(detail=True, methods=['get'])
#     def stop(self, request, pk=None):
#         b_task = BTask.objects.all()
#         b_task.delete()

#         item_llg = item_lelang.objects.get(id=pk)
#         round = models.bidding_round_smra.objects.all().filter(item=item_llg)
#         putaran = round[0].round_state
#         updated_values = {'status_round':'STO'}
#         models.bidding_round_smra.objects.update_or_create(round_state=putaran,item=item_llg, defaults=updated_values)
#         return Response({"statuss":"OK"})

# class round_smraViewSet(viewsets.ModelViewSet):
#     """ViewSet for the penyampaian_sanggahan class"""

#     queryset = models.round_smra.objects.all()
#     serializer_class = serializers.round_smraSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class round_smra_sumViewSet(viewsets.ModelViewSet):
#     """ViewSet for the penyampaian_sanggahan class"""

#     queryset = models.round_smra_sum.objects.all()
#     serializer_class = serializers.round_smra_sumSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class round_smra_tempViewSet(viewsets.ModelViewSet):
#     """ViewSet for the penyampaian_sanggahan class"""

#     queryset = models.round_smra_temp.objects.all()
#     serializer_class = serializers.round_smra_tempSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     @action(detail=False, methods=['get'])
#     def test(elf, request):
#         bdr = bidder_lelang.objects.all().filter(item_lelang=1)
#         m = models.round_smra.objects.all().filter(bidder=45)
#         df = read_frame(m)
#         return Response({'status':'REVEAL', "code": 400})

#     @action(detail=False, methods=['post'])
#     def submit_bid(self, request):
# #        itm_llg = item_lelang.objects.get(id=pk)
# #        bdr = bidder_lelang.objects.all().filter(item_lelang=pk)
#         item_id = 0
#         bidder_id = 0
#         round_data = 0
#         eli = 0
#         price = 0
#         for data in request.data:
#             bdr = bidder.objects.get(id=data['bidder_id'])
#             itm_llg = detail_itemlelang.objects.get(id=data['object_id'])
#             item_id = itm_llg
#             bidder_id = bdr
#             round_data = data['round']
#             eli = eli + data['eligibility_point_per_block']*int(data['block'])
#             price = price + float(data['penawaran'])*int(data['block'])
#             if round_data==1:
#                 updated_values = {'price': float(data['penawaran']), 'block':int(data['block'])}
#                 models.round_smra.objects.update_or_create(bidder=bdr, round=data['round'], item=itm_llg, defaults=updated_values)
#             else:
#                 updated_values = {'price': float(data['penawaran']), 'prev_price': float(data['prev_price']), 'block':int(data['block']),'prev_block':int(data['prev_block'])}
#                 models.round_smra_temp.objects.update_or_create(bidder=bdr, round=data['round'], item=itm_llg, defaults=updated_values)
#         if (round_data==1):
#             updated_values = {'price': price, 'activity':eli}
#             models.round_smra_sum.objects.update_or_create(bidder=bidder_id, round=round_data, item=itm_llg.item_lelang, defaults=updated_values)
#             return Response({'status':'OK', "code": 200})
#         else:
#             # check if activity higher then previous activity
#             smra_sum = models.round_smra_sum.objects.all().filter(bidder=bidder_id).filter(round=round_data-1).filter(item=itm_llg.item_lelang)
#             if eli>smra_sum[0].activity:
#                 if round_data==2:
#                     selisih = 0
#                     item_llg = detail_itemlelang.objects.all().values_list("id", flat=True).filter(item_lelang=itm_llg.item_lelang)
#                     for i in item_llg:
#                         eli_round = models.eli_round.objects.all().filter(bidder_id=bidder_id.id).filter(round=round_data).filter(item_id=i)
#                         prev = eli_round[0].cbcp - eli_round[0].cbpp
#                         current = eli_round[0].pbcp - eli_round[0].pbpp
#                         selisih = selisih + prev-current
#                     if (selisih<0): # accepted
#                         updated_values = {'price': price, 'activity':smra_sum[0].activity, 'corrected':True}
#                         models.round_smra_sum.objects.update_or_create(bidder=bidder_id, round=round_data, item=itm_llg.item_lelang, defaults=updated_values)
#                         r_smra = models.round_smra_temp.objects.all().filter(bidder=bidder_id).filter(round=round_data)
#                         for bdr in r_smra:
#                             updated_values = {'block':bdr.block, 'price':bdr.price} 
#                             models.round_smra.objects.update_or_create(item=bdr.item, bidder=bdr.bidder, round=round_data, defaults=updated_values)
#                         return Response({'status':'OK', "code": 200})
#                     else:
#                         return Response({'status':'REVEAL', "code": 400})
#                 #
#                 else:
#                     #bdr = bidder_lelang.objects.all().filter(item_lelang=1)
#                     m = models.round_smra.objects.all().filter(bidder=bidder_id)
#                     df = read_frame(m)
#                     print(df)
#                     data = []
#                     for i in range(1, round_data):
#                         data.append(df[df['round']==i])
#                     m2 = models.round_smra_temp.objects.all().filter(bidder=bidder_id).filter(round=round_data)
#                     df2 = read_frame(m2)
#                     data.append(df2)
#                     df3 = data[1]['price']*data[2]['block'].values
#                     print(df3)
#                     #calculate cbcp, cbpp, pbcp, pcpp.
# #                    selisih = 0
# #                    item_llg = detail_itemlelang.objects.all().values_list("id", flat=True).filter(item_lelang=itm_llg.item_lelang)
# #                    for i in item_llg:
# #                        eli_round = models.eli_round.objects.all().filter(bidder_id=bidder_id.id).filter(round=round_data).filter(item_id=i)
# #                        cbcp = eli_round[0].cbcp
# #                        selisih = selisih + prev-current
# #                    if (selisih<0): # accepted
# #                        updated_values = {'price': price, 'activity':eli}
# #                        models.round_smra_sum.objects.update_or_create(bidder=bidder_id, round=round_data, item=itm_llg.item_lelang, defaults=updated_values)
# #                        r_smra = models.round_smra_temp.objects.all().filter(bidder=bidder_id).filter(round=round_data)
# #                        for bdr in r_smra:
# #                            updated_values = {'block':bdr.block, 'price':bdr.price} 
# #                            models.round_smra.objects.update_or_create(item=bdr.item, bidder=bdr.bidder, round=round_data, defaults=updated_values)
# #                        return Response({'status':'OK', "code": 200})
# #                    else:
# #                        return Response({'status':'REVEAL', "code": 400})

#                 return Response({'status':'REVEAL', "code": 400})
#             else:
#                 updated_values = {'price': price, 'activity':eli}
#                 models.round_smra_sum.objects.update_or_create(bidder=bidder_id, round=round_data, item=itm_llg.item_lelang, defaults=updated_values)
#                 r_smra = models.round_smra_temp.objects.all().filter(bidder=bidder_id).filter(round=round_data)
#                 for bdr in r_smra:
#                     updated_values = {'block':bdr.block, 'price':bdr.price} 
#                     models.round_smra.objects.update_or_create(item=bdr.item, bidder=bdr.bidder, round=round_data, defaults=updated_values)
#                 return Response({'status':'OK', "code": 200})

#             #ret = self.validate_mybid(bidder_id, item_id, round_data, eli, price)
#             return Response({'status':'OK', "code": 200})

# class round_smraSummaryViewSet(viewsets.ModelViewSet):
#     """ViewSet for the penyampaian_sanggahan class"""
#     queryset = models.auction_summary_smra.objects.all()
#     serializer_class = serializers.smra_roundSummarySerializer
#     permission_classes = [permissions.IsAuthenticated]
#     filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
#     filterset_fields = ('item_id',)

# class smra_bid_bidderViewSet(viewsets.ModelViewSet):
#     """ViewSet for the penyampaian_sanggahan class"""
#     queryset = models.bid_bidder_smra.objects.all()
#     serializer_class = serializers.smra_bid_bidderSMRASerializer
#     permission_classes = [permissions.IsAuthenticated]
#     #filter_backends = (filters.DjangoFilterBackend,)
#     filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
#     filterset_fields = ('item_id', 'bidder_id','round')