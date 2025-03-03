from rest_framework import generics, viewsets, permissions, pagination
from django_filters import rest_framework as filters

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings


from . import serializers
from . import models
from mfa import models as mfa_models
import os
import requests
import json




class dokumen_perusahaanViewSet(viewsets.ModelViewSet):
    """ViewSet for the dokumen_perusahaan class"""

    queryset = models.dokumen_perusahaan.objects.all()
    serializer_class = serializers.dokumen_perusahaanSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)


class UsersViewSet(viewsets.ModelViewSet):
    """ViewSet for the Users class"""

    queryset = models.Users.objects.all()
    serializer_class = serializers.UsersSerializer
    permission_classes = [permissions.IsAuthenticated]
    #filter_backends = (filters.DjangoFilterBackend,)
    #filterset_fields = ('mobile_number', 'username', 'bidder', 'isactive', 'user_type',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        oldUserCustomGroup = list(instance.customGroup.all())

        # Ambil data baru dari request
        newUserCustomGroup = serializer.validated_data.get('customGroup', [])
        
        print('oldUserCustomGroup', oldUserCustomGroup)
        print('newUserCustomGroup', newUserCustomGroup)

        # Gabungkan old + new (hindari duplikasi)
        updatedCustomGroup = set(oldUserCustomGroup) | set(newUserCustomGroup)
        serializer.save(diubah_oleh=self.request.user, customGroup=updatedCustomGroup)

class UsersViewViewSet(viewsets.ModelViewSet):
    """ViewSet for the Users class"""

    queryset = models.Users.objects.all()
    serializer_class = serializers.UsersViewSerializer
    permission_classes = [permissions.IsAuthenticated]
    #filter_backends = (filters.DjangoFilterBackend,)
    #filterset_fields = ('mobile_number', 'username', 'bidder', 'isactive', 'user_type',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class tim_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the tim_lelang class"""

    queryset = models.tim_lelang.objects.all()
    serializer_class = serializers.tim_lelangSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('users',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class adminViewSet(viewsets.ModelViewSet):
    """ViewSet for the tim_lelang class"""

    queryset = models.admin.objects.all()
    serializer_class = serializers.adminSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('users',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class viewerViewSet(viewsets.ModelViewSet):
    """ViewSet for the tim_lelang class"""

    queryset = models.viewers.objects.all()
    serializer_class = serializers.viewerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('users',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class bidderlistViewSet(viewsets.ModelViewSet):
    """ViewSet for the tim_lelang class"""

    queryset = models.bidder_list.objects.all()
    serializer_class = serializers.bidderlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    #filter_backends = (filters.DjangoFilterBackend,)
    #filterset_fields = ('users',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class bidderperwakilanViewSet(viewsets.ModelViewSet):
    """ViewSet for the bidder class"""
    queryset = models.bidder_perwakilan.objects.all()
    serializer_class = serializers.bidderperwakilanSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = (filters.DjangoFilterBackend,)
   # filterset_fields = ('id','user',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)
    
    @action(detail=True, methods=['get'])
    def send_speciment(self, request, pk=None):
        ttd = models.bidder_perwakilan.objects.get(pk=pk)
        url = "http://"+settings.PERURI_DOCKER+"/v1/specimen/set"
        payload = {'profileName': ttd.profil_peruri}
        currentdir = os.getcwd()
        files=[
            ('file',('signature.png',open(currentdir + "/media/" + ttd.ttd.name,'rb'),'image/png'))
        ]
        response = requests.request("POST", url, data=payload, files=files)
        #print("Response :" ,response.text)
        data = json.loads(response.text)
        ttd.peruri_ttd = data['saveAs']
        ttd.save()
        return Response({"status":data})

    @action(detail=True, methods=['get'])
    def test_esign(self, request, pk=None):
        url1 = "http://"+settings.PERURI_DOCKER+"/v1/auth/token"
        vbidder_perwakilan = models.bidder_perwakilan.objects.get(id = 137)
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

        data_jwt = jwt["jwt"]
        # session init
        url2 = "http://"+settings.PERURI_DOCKER+"/v1/auth/session/init"
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

        return Response({"step":"session","session":session, "fileid": "a4b5a9f9-61a4-44e0-989c-ffdcc5967bc1", "jwt": jwt })

    @action(detail=True, methods=['get'])
    def otp_esign(self, request, pk=None):
        url2 = "http://"+settings.PERURI_DOCKER+"/v1/auth/session/validate"
        jwt = "eyJraWQiOiJzc29zIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJBZG1pbmlzdHJhdG9yIiwiYXVkIjoicGVydXJpIiwibmJmIjoxNzM5NDIwMzQ4LCJpc3MiOiJwZXJ1cmkiLCJleHAiOjE3Mzk1MDY3NDgsImlhdCI6MTczOTQyMDM0OH0.icitSLuu5XEzv9bkC3urpn6m3hZYj-wqRalOqpGNNrog6-YQBvem0uyvE_68JqEC4sIr3tE6V_YZmFeXFz6XlRih_lOCOtF5OGJYWWrIwrhiGt3g_CvygoAsIydDKb-Pe4wTb0cxCAWhKHBqOUkaZA7I75lSDTQMPvH9eDMmuPsHva_mMMZhVmoXRCD9CBv7QqyD2EDWVTKA_5dgKDQ9PZ6sH15IiMinCc07OXb-DSzvCTfXQ9brf3JrAyvhIGodEjoJwpva8LEnkQWnel_ocRZiiVPtVZAOi5vs_Jh6F5o83_sFMa25XLs3sN-CO7K6yodxQ3c5frs9frH84vWwwQ"
        payload = json.dumps({
            "param": {
                "email": "rachmatg@yahoo.com",
                "systemId": settings.PERURI_SYSTEM_ID,
                "tokenSession": "73465b9c09ed4005b12f5654b7b57e31",
                "otpCode": "308612"
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJraWQiOiJzc29zIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJBZG1pbmlzdHJhdG9yIiwiYXVkIjoicGVydXJpIiwibmJmIjoxNzM5NDIwMzQ4LCJpc3MiOiJwZXJ1cmkiLCJleHAiOjE3Mzk1MDY3NDgsImlhdCI6MTczOTQyMDM0OH0.icitSLuu5XEzv9bkC3urpn6m3hZYj-wqRalOqpGNNrog6-YQBvem0uyvE_68JqEC4sIr3tE6V_YZmFeXFz6XlRih_lOCOtF5OGJYWWrIwrhiGt3g_CvygoAsIydDKb-Pe4wTb0cxCAWhKHBqOUkaZA7I75lSDTQMPvH9eDMmuPsHva_mMMZhVmoXRCD9CBv7QqyD2EDWVTKA_5dgKDQ9PZ6sH15IiMinCc07OXb-DSzvCTfXQ9brf3JrAyvhIGodEjoJwpva8LEnkQWnel_ocRZiiVPtVZAOi5vs_Jh6F5o83_sFMa25XLs3sN-CO7K6yodxQ3c5frs9frH84vWwwQ'
        }

        response = requests.request("POST", url2, headers=headers, data=payload)
        session = json.loads(response.text)
        print(session)
        #if session['errorCode']=='04':
        #    return Response({"status":"NOK", "message": "Invalid OTP"}) 

        url2 = "http://"+settings.PERURI_DOCKER+"/v1/doc/shield/composite/user/sign"

        payload = json.dumps({
        "systemId": settings.PERURI_SYSTEM_ID,
        "profileName": "rachmatg@yahoo.com",
        "src": "8d3cee17-18ac-4f0d-ad51-731be2527614.pdf",
        "location": "Jakarta",
        "reason": "I agree to sign",
        "coordinate": {
            "specimenImage": "9e949fd7470cde5fa22b3712086604dfa1f4e7a2.png",
            "isBase64": False,
            "page": 1,
            "llx": 0,
            "lly": 200,
            "urx": 100,
            "ury": 100
        }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + jwt,
            'x-Gateway-APIKey': settings.PERURI_API_KEY
        }

        response = requests.request("POST", url2, headers=headers, data=payload)

        file = "a4b5a9f9-61a4-44e0-989c-ffdcc5967bc1" #os.path.splitext(a4b5a9f9-61a4-44e0-989c-ffdcc5967bc1)[0]
        url3 = "http://"+settings.PERURI_DOCKER+"/v1/doc/download?idFile="+file

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + jwt,
            'x-Gateway-APIKey': settings.PERURI_API_KEY
        }
        response2 = requests.request("GET", url3, headers=headers, data=payload)
        return Response({"status":response})

class crudbidderperwakilanViewSet(viewsets.ModelViewSet):
    """ViewSet for the bidder class"""
    queryset = models.bidder_perwakilan.objects.all()
    serializer_class = serializers.crudbidderperwakilanserializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('id','bidder',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class bidderViewSet(viewsets.ModelViewSet):
    """ViewSet for the bidder class"""
    queryset = models.bidder.objects.all()
    serializer_class = serializers.bidderSerializer
    permission_classes = [permissions.IsAuthenticated]
    #filter_backends = (filters.DjangoFilterBackend,)
    #filterset_fields = ('nama_perusahaan',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)


class usermenuViewSet(viewsets.ModelViewSet):
    """ViewSet for the smra_round class"""

    queryset = models.UserMenu.objects.all().filter(level=0)
    serializer_class = serializers.UserMenuSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = pagination.LimitOffsetPagination
    filterset_fields = ('parent',)
    
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class usermenu2ViewSet(viewsets.ModelViewSet):
    """ViewSet for the smra_round class"""

    queryset = models.UserMenu.objects.all()
    serializer_class = serializers.UserMenu2Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = pagination.LimitOffsetPagination
    filterset_fields = ('parent',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class usermenugroupViewSet(viewsets.ModelViewSet):
    """ViewSet for the smra_round class"""

    queryset = models.UserMenuGroup.objects.all()
    serializer_class = serializers.UserMenuGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = pagination.LimitOffsetPagination
    filterset_fields = ('group',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

    @action(detail=True, methods=['get'])
    def update_group(self, request, pk=None):
        if request.GET.get('g'):
            g = request.GET.get('g')
            menu = models.UserMenu.objects.get(pk=pk)
            menugroup = models.UserMenuGroup.objects.all().filter(menu=pk, group=g)
            if (menugroup):
                menugroup[0].delete()
            else:
                grp = models.CustomGroup.objects.get(pk = g)
                umg = models.UserMenuGroup(group=grp, menu=menu)
                umg.save()

            return Response({"status":"OK"})
        else:
            return Response({"status":"GROUP NOT FOUND"})

class groupViewSet(viewsets.ModelViewSet):
    """ViewSet for the smra_round class"""

    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class costumgroupViewSet(viewsets.ModelViewSet):
    """ViewSet for the smra_round class"""

    queryset = models.CustomGroup.objects.all()
    serializer_class = serializers.CostumGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class userViewSet(viewsets.ModelViewSet):
    """ViewSet for the smra_round class"""

    queryset = models.Users.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class admin2ViewSet(viewsets.ModelViewSet):
    """ViewSet for the smra_round class"""

    queryset = models.Users.objects.all().filter(user_type='A')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class BidderUserViewSet(viewsets.ModelViewSet):
    """ViewSet for the smra_round class"""

    queryset = models.bidder_user.objects.all()
    serializer_class = serializers.BidderUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class BidderUser2ViewSet(viewsets.ModelViewSet):
    """ViewSet for the smra_round class"""

    queryset = models.bidder_user.objects.all()
    serializer_class = serializers.BidderUser2Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('users',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)
        
    def perform_destroy(self, instance):
        instance.delete()

class groupMapViewSet(viewsets.ModelViewSet):
    """ViewSet for the smra_round class"""

    queryset = models.menugroup_map.objects.raw(
        """SELECT row_number() OVER () AS id,
            a.menu_id,
            a.group_id,
            b.name,
            b.id AS menuid,
            b.parent_id
        FROM userman_usermenu b
            LEFT OUTER JOIN
            (select menu_id, group_id from userman_usermenugroup where group_id = 8) a 
        on a.menu_id = b.id"""
    )
    serializer_class = serializers.GroupMapSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    #filterset_fields = ('group',)

class mfaKeyMonitoringViewSet(viewsets.ModelViewSet):
    queryset = mfa_models.MFAKey.objects.all()
    serializer_class = serializers.MFAKeyMonitoringSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class notifikasiViewSet(viewsets.ModelViewSet):
    queryset = models.Notifikasi.objects.all()
    serializer_class = serializers.NotifikasiSerializer
    permission_classes = [permissions.IsAuthenticated]
    