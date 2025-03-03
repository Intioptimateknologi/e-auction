from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from . import serializers
from . import models
from adm_lelang.models import bidder_lelang, auctioner_lelang, viewers_lelang, item_lelang, detail_itemlelang
from userman.models import Users, bidder, tim_lelang, viewers, bidder_perwakilan, UserMenu
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from pprint import pprint

class p_dokumenViewSet(viewsets.ModelViewSet):

    queryset = models.p_dokumen.objects.all()
    serializer_class = serializers.p_dokumenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_create(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

    @action(detail=True, methods=['get'])
    def kirim_undangan(self, request, pk):
        domain = request.headers['Host']
        undangan = models.p_dokumen.objects.get(pk=pk)
        item = item_lelang.objects.get(pk=undangan.item_lelang.id)
        
        auc_lelang = undangan.auctioneer.all()
        bdr_lelang = undangan.bidder.all()
        vwr_lelang = viewers_lelang.objects.all().filter(item_lelang=item.id)
        email_auctioner = []
        email_bidder = []
        email_viewer = []
        for a in auc_lelang:
            auc = tim_lelang.objects.get(pk=a.id)
            email_auctioner.append(auc.users.email)
        for b in bdr_lelang:
            bdr = bidder_perwakilan.objects.all().filter(bidder_id=b.id)
            for c in bdr:
                user = Users.objects.get(pk=c.users_id)
                email_auctioner.append(user.email)
        for v in vwr_lelang:
            vwr = viewers.objects.get(pk=v.viewer.id)
            email_viewer.append(vwr.users.email)
        # email_auctioner.append('rachmatg@yahoo.com')
        data = {"auctioner": email_auctioner, "bidder": email_bidder, "viewer":email_viewer }
        subject = "Notifikasi Undangan"
        email_template_notif_bidder = "email_notif_bidder.html"
        email_template_notif_auctioneer = "email_notif_auctioner.html"
        email_template_notif_viewer = "email_notif_viewer.html"
        auc_email_context = {
            "email": email_auctioner,
            'domain': domain,
            'site_name': item.nama_lelang,
            'judul': undangan.judul,
            'link': undangan.link_teleconference,
            'file': undangan.file
        }
        email = render_to_string(email_template_notif_auctioneer, auc_email_context)
        try:
            send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, email_auctioner, fail_silently=False)
        except BadHeaderError:
            return Response({"status":"Invalid header found"})
        return Response({"status":data})

    @action(detail=True, methods=['get'])
    def get_tabs(self, request, pk):
        url = '/persiapan/pembukaan/'
        menu = UserMenu.objects.all().filter(link=url)
        #print(menu[0].get_leafnodes())
        return Response({"status":"ok"})


class penyusunan_jawabanViewSet(viewsets.ModelViewSet):

    queryset = models.penyusunan_jawaban.objects.all()
    serializer_class = serializers.penyusunan_jawabanSerializer
    permission_classes = [permissions.IsAuthenticated]

class aanwizingViewSet(viewsets.ModelViewSet):

    queryset = models.aanwizing.objects.all()
    serializer_class = serializers.aanwizingSerializer
    permission_classes = [permissions.IsAuthenticated]

class simulasiViewSet(viewsets.ModelViewSet):

    queryset = models.simulasi.objects.all()
    serializer_class = serializers.simulasiSerializer
    permission_classes = [permissions.IsAuthenticated]

class p_addendumViewSet(viewsets.ModelViewSet):

    queryset = models.p_addendum.objects.all()
    serializer_class = serializers.p_addendumSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class dokumen_seleksiViewSet(viewsets.ModelViewSet):

    queryset = models.dokumen_seleksi.objects.all()
    serializer_class = serializers.dokumen_seleksiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class pengambilan_dokumen_seleksiViewSet(viewsets.ModelViewSet):

    queryset = models.pengambilan_dokumen_seleksi.objects.all()
    serializer_class = serializers.pengambilan_dokumen_seleksiSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('id','bidder_perwakilan')

class pengambilan_dokumen_addendumViewSet(viewsets.ModelViewSet):
    queryset = models.pengambilan_dokumen_addendum.objects.all()
    serializer_class = serializers.pengambilan_dokumen_addendumSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('id','bidder_perwakilan')

class daftar_hadirViewSet(viewsets.ModelViewSet):
    queryset = models.daftar_hadir.objects.all()
    serializer_class = serializers.daftar_hadirSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang',)

    def perform_create(self, serializer):
        user = self.request.user
        tgl_kehadiran = serializer.validated_data.get('tgl_kehadiran')
        
        sudah_hadir = models.daftar_hadir.objects.filter(
            dibuat_oleh=user,
            tgl_kehadiran=tgl_kehadiran
        ).exists()
        
        if sudah_hadir:
            raise ValidationError({
                "type": "warning",
                "message": "Pengguna sudah terdaftar pada tanggal ini."
            })
        
        serializer.save(dibuat_oleh=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class p_pertanyaanViewSet(viewsets.ModelViewSet):

    queryset = models.p_pertanyaan.objects.all()
    serializer_class = serializers.p_pertanyaanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('item_lelang','bidder',)

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)

    def perform_update(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

class berita_acara_persiapanViewSet(viewsets.ModelViewSet):

    queryset = models.berita_acara_persiapan.objects.all()
    serializer_class = serializers.berita_acara_persiapanSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('owner',)

    def perform_create(self, serializer):
        serializer.save(diubah_oleh=self.request.user)

    @action(detail=True, methods=['get'])
    def kirim_undangan(self, request, pk):
        domain = request.headers['Host']
        undangan = models.berita_acara_persiapan.objects.get(pk=pk)
        item = item_lelang.objects.get(pk=undangan.item_lelang.id)
        
        auc_lelang = undangan.auctioneer.all()
        bdr_lelang = undangan.bidder.all()
        vwr_lelang = viewers_lelang.objects.all().filter(item_lelang=item.id)
        email_auctioner = []
        email_bidder = []
        email_viewer = []
        for a in auc_lelang:
            auc = tim_lelang.objects.get(pk=a.id)
            email_auctioner.append(auc.users.email)
        for b in bdr_lelang:
            bdr = bidder_perwakilan.objects.all().filter(bidder_id=b.id)
            for c in bdr:
                user = Users.objects.get(pk=c.users_id)
                email_auctioner.append(user.email)
        for v in vwr_lelang:
            vwr = viewers.objects.get(pk=v.viewer.id)
            email_viewer.append(vwr.users.email)
        # email_auctioner.append('budidwiprasetyo49@.gmail.com')
        data = {"auctioner": email_auctioner, "bidder": email_bidder, "viewer":email_viewer }
        subject = "Notifikasi Berita Acara"
        email_template_notif_bidder = "email_notif_bidder.html"
        email_template_notif_auctioneer = "email_template_notif_auctioneer_ba.html"
        email_template_notif_viewer = "email_notif_viewer.html"
        auc_email_context = {
            "email": email_auctioner,
            'domain': domain,
            'site_name': item.nama_lelang,
            'judul': undangan.judul,
            'file': undangan.file
        }
        email = render_to_string(email_template_notif_auctioneer, auc_email_context)
        try:
            send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, email_auctioner, fail_silently=False)
        except BadHeaderError:
            return Response({"status":"Invalid header found"})
        return Response({"status":data})