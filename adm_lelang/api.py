from django.utils.text import capfirst
from rest_framework import viewsets, permissions, generics, pagination, status
from django_filters import rest_framework as filters
from django_filters import FilterSet
from rest_framework.decorators import action
from userman.models import UserMenu, Users, bidder_user, viewers, tim_lelang, Notifikasi
from . import serializers
from . import models
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.utils import timezone
from rest_framework.filters import BaseFilterBackend
from django.db import connection
from rest_framework.response import Response

class detail_itemlelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the detail_itemlelang class"""

    queryset = models.detail_itemlelang.objects.all()
    serializer_class = serializers.detail_itemlelangSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang','disabled')
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.disabled=True
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        """Filter products based on user"""
        return models.detail_itemlelang.objects.filter(disabled=False)


class item_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the item_lelang class"""

    queryset = models.item_lelang.objects.all()
    serializer_class = serializers.item_lelangSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)


class bidder_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the item_lelang class"""

    queryset = models.bidder_lelang.objects.all()
    serializer_class = serializers.bidder_lelangSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('bidder', 'item_lelang')
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)


class auctioner_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the item_lelang class"""

    queryset = models.auctioner_lelang.objects.all()
    serializer_class = serializers.auctioner_lelangSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('auctioner', 'item_lelang')
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class viewers_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the item_lelang class"""

    queryset = models.viewers_lelang.objects.all()
    serializer_class = serializers.viewers_lelangSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('viewer', 'item_lelang')
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class jadwal_seleksiViewSet(viewsets.ModelViewSet):
    """ViewSet for the jadwal_seleksi class"""

    queryset = models.jadwal_seleksi.objects.all()
    serializer_class = serializers.jadwal_seleksiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang', 'tahap',)
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class dasar_hukumViewSet(viewsets.ModelViewSet):
    """ViewSet for the dasar_hukum class"""

    queryset = models.dasar_hukum.objects.all()
    serializer_class = serializers.dasar_hukumSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class pengumuman_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the pengumuman_lelang class"""
    dt = timezone.localtime()
    queryset = models.pengumuman.objects.all()
    serializer_class = serializers.pengumuman_lelangSerializer
    permission_classes = [permissions.AllowAny]

    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class pengumuman_lelang2ViewSet(viewsets.ModelViewSet):
    """ViewSet for the dasar_hukum class"""
    dt = timezone.localtime()
    queryset = models.pengumuman.objects.all()
    serializer_class = serializers.pengumuman_lelangSerializer
    
    

class persyaratan_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the dasar_hukum class"""

    queryset = models.persyaratan_lelang.objects.all()
    serializer_class = serializers.persyaratan_lelangSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class alamat_panitiaViewSet(viewsets.ModelViewSet):
    """ViewSet for the dasar_hukum class"""

    queryset = models.alamat_panitia.objects.all()
    serializer_class = serializers.alamat_panitiaSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class template_berita_acaraViewSet(viewsets.ModelViewSet):
    """ViewSet for the dasar_hukum class"""

    queryset = models.template_berita_acara.objects.all()
    serializer_class = serializers.template_berita_acaraSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('template_code_menu', 'template_code_sub')
    # def perform_create(self, serializer):
    #     serializer.save(dibuat_oleh=self.request.user)

    # def perform_update(self, serializer):
    #     serializer.save(diubah_oleh=self.request.user)

class tahapan_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the dasar_hukum class"""

    queryset = models.tahapan_lelang2.objects.all()
    serializer_class = serializers.tahapan2_Serializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = None
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)


class undangan_lelangViewSet(viewsets.ModelViewSet):
    """ViewSet for the dasar_hukum class"""

    queryset = models.undangan.objects.all()
    serializer_class = serializers.undanganSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang', 'tahapan')

    def get_queryset(self):
        """Filter products based on user"""
        user = self.request.user

        if user.user_type == 'B':
            bu = bidder_user.objects.filter(users = user)
            return models.undangan.objects.filter(bidder_user__in=bu)
        elif user.user_type == 'C':
            au = tim_lelang.objects.filter(users = user)
            return models.undangan.objects.filter(auctioneer__in =au)
        elif user.user_type == 'V':
            au = viewers.objects.filter(users = user)
            return models.undangan.objects.filter(viewer__in =au)
        else:
            return models.undangan.objects.all()

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)
    
    @action(detail=True, methods=['get'])
    def kirim_undangan(self, request, pk):
        domain = request.headers['Host']
        undangan = models.undangan.objects.get(pk=pk)
        item = models.item_lelang.objects.get(pk=undangan.item_lelang.id)
        tahapan = undangan.tahapan
        jadwal = models.jadwal_seleksi.objects.filter(tahap = tahapan)
        if (not jadwal.exists()):
            return Response({'status': "Error", 'reason': "Jadwal tidak ada"})
        batas_akhir = jadwal[0].tanggal_akhir        
        path = request.GET.get('pathname', '')
        menu = UserMenu.objects.filter(link=path).first()
        menu_name = "-"
        
        if menu is not None:
            if menu.parent is not None:
                menu_name = menu.parent.name + ' ' + menu.name
            else:
                menu_name = menu.name
        
        auc_lelang = undangan.auctioneer.all()
        bdr_lelang = undangan.bidder_user.all()
        vwr_lelang = undangan.viewer.all()
        email_auctioner = []
        email_bidder = []
        email_viewer = []
        subject = "Notifikasi Undangan: #" + str(undangan.id) + ", " + undangan.judul
        email_template_notif_bidder = "email_notif_auctioner.html"
        email_template_notif_auctioneer = "email_notif_auctioner.html"
        email_template_notif_viewer = "email_notif_auctioner.html"
        for a in auc_lelang:
            try:
                auc_email_context = {
                    "email": [a.users.email],
                    'domain': domain,
                    'site_name': item.nama_lelang,
                    'judul': undangan.judul,
                    'link': undangan.link_teleconference,
                    'file': undangan.file,
                    'menu': menu_name,
                }
                email = render_to_string(email_template_notif_auctioneer, auc_email_context )
                send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [a.users.email], fail_silently=False)
                notif = Notifikasi(email=a.users.email, notification_type="U", expire_date = batas_akhir, id_undangan=undangan.id, subyek=subject, notifikasi=email,email_status="Sending")
                notif.save()
            except BadHeaderError:
                None
        for b in bdr_lelang:
            try:
                auc_email_context = {
                    "email": [b.users.email],
                    'domain': domain,
                    'site_name': item.nama_lelang,
                    'judul': undangan.judul,
                    'link': undangan.link_teleconference,
                    'file': undangan.file,
                    'menu': menu_name,
                }
                email = render_to_string(email_template_notif_bidder, auc_email_context )
                send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [b.users.email], fail_silently=False)
                notif = Notifikasi(email=b.users.email, notification_type="U", expire_date = batas_akhir, id_undangan=undangan.id, subyek=subject, notifikasi=email,email_status="Sending")
                notif.save()
            except BadHeaderError:
                None
        for v in vwr_lelang:
            try:
                auc_email_context = {
                    "email": [v.users.email],
                    'domain': domain,
                    'site_name': item.nama_lelang,
                    'judul': undangan.judul,
                    'link': undangan.link_teleconference,
                    'file': undangan.file,
                    'menu': menu_name,
                }
                email = render_to_string(email_template_notif_viewer, auc_email_context )
                send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [v.users.email], fail_silently=False)
                notif = Notifikasi(email=b.users.email, notification_type="U", expire_date = batas_akhir, id_undangan=undangan.id, subyek=subject, notifikasi=email,email_status="Sending")
                notif.save()
            except BadHeaderError:
                None
        return Response({'menu': menu_name, 'path': path})

class berita_acaraViewSet(viewsets.ModelViewSet):

    queryset = models.berita_acara.objects.all()
    serializer_class = serializers.berita_acaraSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

    @action(detail=True, methods=['get'])
    def kirim_undangan(self, request, pk):
        domain = request.headers['Host']
        undangan = models.berita_acara.objects.get(pk=pk)
        item = models.item_lelang.objects.get(pk=undangan.item_lelang.id)
        tahapan = undangan.tahapan
        jadwal = models.jadwal_seleksi.objects.filter(tahap = tahapan)
        if (not jadwal.exists()):
            return Response({'status': "Error", 'reason': "Jadwal tidak ada"})
        batas_akhir = jadwal[0].tanggal_akhir        
        path = request.GET.get('pathname', '')
        menu = UserMenu.objects.filter(link=path).first()
        menu_name = "-"
        
        if menu is not None:
            if menu.parent is not None:
                menu_name = menu.parent.name + ' ' + menu.name
            else:
                menu_name = menu.name
        
        auc_lelang = undangan.auctioneer.all()
        bdr_lelang = undangan.bidder_user.all()
        vwr_lelang = undangan.viewer.all()
        email_auctioner = []
        email_bidder = []
        email_viewer = []
        subject = "Notifikasi Berita Acara: #" + str(undangan.id) + ", " + undangan.judul
        email_template_notif_auctioneer = "email_template_notif_auctioneer_ba.html"
        email_template_notif_bidder = "email_template_notif_auctioneer_ba.html"
        email_template_notif_viewer = "email_template_notif_auctioneer_ba.html"

        for a in auc_lelang:
            try:
                auc_email_context = {
                    "email": [a.users.email],
                    'domain': domain,
                    'site_name': item.nama_lelang,
                    'judul': undangan.judul,
                    'file': undangan.file,
                    'menu': menu_name,
                }
                email = render_to_string(email_template_notif_auctioneer, auc_email_context )
                send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [a.users.email], fail_silently=False)
                notif = Notifikasi(email=a.users.email, notification_type="B", expire_date = batas_akhir, id_ba=undangan.id, subyek=subject, notifikasi=email,email_status="Sending")
                notif.save()
            except BadHeaderError:
                None
        for b in bdr_lelang:
            try:
                auc_email_context = {
                    "email": [b.users.email],
                    'domain': domain,
                    'site_name': item.nama_lelang,
                    'judul': undangan.judul,
                    'file': undangan.file,
                    'menu': menu_name,
                }
                email = render_to_string(email_template_notif_bidder, auc_email_context )
                send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [b.users.email], fail_silently=False)
                notif = Notifikasi(email=b.users.email, notification_type="B", expire_date = batas_akhir, id_ba=undangan.id, subyek=subject, notifikasi=email,email_status="Sending")
                notif.save()
            except BadHeaderError:
                None
        for v in vwr_lelang:
            try:
                auc_email_context = {
                    "email": [v.users.email],
                    'domain': domain,
                    'site_name': item.nama_lelang,
                    'judul': undangan.judul,
                    'file': undangan.file,
                    'menu': menu_name,
                }
                email = render_to_string(email_template_notif_viewer, auc_email_context )
                send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [v.users.email], fail_silently=False)
                notif = Notifikasi(email=b.users.email, notification_type="B", expire_date = batas_akhir, id_ba=undangan.id, subyek=subject, notifikasi=email,email_status="Sending")
                notif.save()
            except BadHeaderError:
                None
        return Response({'menu': menu_name, 'path': path})

class pengambilanBAViewSet(viewsets.ModelViewSet):
    queryset = models.pengambilan_ba.objects.all()
    serializer_class = serializers.pengambilan_baSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = None
    @action(detail=False, methods=['get'], url_path=r'update_undangan/(?P<undangan>\d+)/(?P<bdr>\d+)')
    def update_undangan(self, request, undangan, bdr):
        undangan = models.berita_acara.objects.get(id=undangan)
        user = Users.objects.get(pk=bdr)
        a_undangan = models.pengambilan_ba(ba = undangan, user = user) 
        a_undangan.save()    
        return Response({"status":"OK"})   

class pengambilanUndanganViewSet(viewsets.ModelViewSet):
    queryset = models.pengambilan_undangan.objects.all()
    serializer_class = serializers.pengambilan_undanganSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = None

    @action(detail=False, methods=['get'], url_path=r'update_undangan/(?P<undangan>\d+)/(?P<bdr>\d+)')
    def update_undangan(self, request, undangan, bdr):
        undangan = models.undangan.objects.get(id=undangan)
        user = Users.objects.get(pk=bdr)
        a_undangan = models.pengambilan_undangan(undangan = undangan, user = user) 
        a_undangan.save()    
        return Response({"status":"OK"})   
        

class penangung_jawabViewSet(viewsets.ModelViewSet):
    """ViewSet for the dasar_hukum class"""

    queryset = models.penangung_jawab_seleksi.objects.all()
    serializer_class = serializers.penangung_jawabSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

        