from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("detail_itemlelang", api.detail_itemlelangViewSet, basename="detail_itemlelang")
router.register("item_lelang", api.item_lelangViewSet, basename="item_lelang")
router.register("bidder_lelang", api.bidder_lelangViewSet, basename="bidder_lelang")
router.register("auctioner_lelang", api.auctioner_lelangViewSet, basename="auctioner_lelang")
router.register("viewer_lelang", api.viewers_lelangViewSet, basename="viewer_lelang")
router.register("jadwal_seleksi", api.jadwal_seleksiViewSet, basename="jadwal_seleksi")
router.register("dasar_hukum", api.dasar_hukumViewSet, basename="dasar_hukum")
router.register("pengumuman_lelang", api.pengumuman_lelangViewSet, basename="pengumuman_lelang")
router.register("pengumuman_lelang2", api.pengumuman_lelang2ViewSet, basename="pengumuman_lelang2")
router.register("persyaratan_lelang", api.persyaratan_lelangViewSet, basename="persyaratan_lelang")
router.register("alamat_panitia", api.alamat_panitiaViewSet, basename="alamat_panitia")
router.register("template_berita_acara", api.template_berita_acaraViewSet, basename="template_berita_acara")
router.register("tahapan_lelang", api.tahapan_lelangViewSet, basename="tahapan_lelang")
router.register("undangan_lelang", api.undangan_lelangViewSet, basename="undangan_lelang")
router.register("ba", api.berita_acaraViewSet, basename="ba")
router.register("ambil_ba", api.pengambilanBAViewSet, basename="ambil_ba")
router.register("ambil_undangan", api.pengambilanUndanganViewSet, basename="ambil_undangan")
router.register("penangung_jawab", api.penangung_jawabViewSet, basename="penangung_jawab")


urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("administrasi/", views.home),
    path("info_lelang/<int:pk>/", views.info_seleksi),
    path("rekapitulasi/", views.rekap_manajemen),
    path("create_jadwal_by_template/<pk>/<tgl_awal>/", views.create_jadwal_seleksi),

    path("undangan_auctioner/<int:item_lelang>/<int:current_step>/<int:auctioner>/", views.undanganAuctionerListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    path("undangan_bidder/<int:item_lelang>/<int:current_step>/", views.undanganBidder2ListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    path("undangan_rekapitulasi/<int:item_lelang>/", views.undanganRekapitulasiListView.as_view(), name="undanganRekapitulasiListView"),
    path("pengumuman_rekapitulasi/<int:item_lelang>/", views.pengumumanRekapitulasiListView.as_view(), name="pengumumanRekapitulasiListView"),
    path("berita_acara_rekapitulasi/<int:item_lelang>/", views.beritaacaraRekapitulasiListView.as_view(), name="beritaacaraRekapitulasiListView"),
    path("doksel_rekapitulasi/<int:item_lelang>/", views.dokselRekapitulasiListView.as_view(), name="DokumenseleksiRekapitulasiListView"),
    path("email_rekapitulasi/", views.emailRekapitulasiListView.as_view(), name="EmailRekapitulasiListView"),
    # path("undangan_bidder/<int:item_lelang>/<int:current_step>/<int:bidder>/", views.undanganBidderListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    path("modal_undangan_create/<int:item_lelang>/<int:tahapan>/", views.undangan_CreateView.as_view()),
    path("modal_undangan_update/<int:pk>/", views.undangan_UpdateView.as_view()),

    path("modal_bidderlelang/<int:pk>/", views.bidderLelangCreateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("modal_bidderlelang/edit/<int:lelang>/<int:pk>/", views.bidderLelangUpdateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("modal_auctionerlelang/<int:pk>/", views.auctionerLelangCreateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("modal_auctionerlelang/edit/<int:lelang>/<int:pk>/", views.auctionerLelangUpdateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("modal_viewerlelang/<int:pk>/", views.viewerLelangCreateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("modal_viewerlelang/edit/<int:lelang>/<int:pk>/", views.viewerLelangUpdateView.as_view(), name="adm_lelang_detail_itemlelang_list"),

    path("ba_auctioner/<int:item_lelang>/<int:current_step>/<int:auctioner>/", views.BAAuctionerListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    path("ba_bidder/<int:item_lelang>/<int:current_step>/", views.BABidder2ListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    path("ba_bidder/<int:item_lelang>/<int:current_step>/<int:bidder>/", views.BABidderListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    path("modal_ba_create/<int:item_lelang>/<int:tahapan>/", views.modalCreateBA.as_view()),
    path("modal_ba_update/<int:pk>/", views.modalUpdateBA.as_view()),

    path("pengambilan_undangan/<int:pk>/", views.pengambilan_undanganListView.as_view()),
    path("pengambilan_ba/<int:pk>/", views.pengambilan_baListView.as_view()),
    path("penanggung_jawab/<int:pk>/", views.penanggung_jawabListView.as_view()),
    path("adm_lelang/itemlelang/<int:pk>/", views.itemlelangListView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("adm_lelang/detail_itemlelang/<int:pk>/", views.detail_itemlelangListView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("adm_lelang/detail_itemlelang2/<int:pk>/", views.detail_itemlelang2ListView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("adm_lelang/nilai_detail_itemlelang/<int:pk>/", views.nilai_detail_itemlelangListView.as_view(), name="adm_lelang_detail_itemlelang_list"),

    path("adm_lelang/modal_itemlelang/", views.itemLelangCreateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("adm_lelang/modal_itemlelang/<int:pk>/", views.itemlelangUpdateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("adm_lelang/modal_obyek_seleksi/<int:pk>/", views.objekSeleksiCreateView.as_view(), name="adm_lelang_modal_obyek_seleksi"),
    path("adm_lelang/modal_update_obyek_seleksi/<int:pk>/<int:id>/", views.objekSeleksiUpdateView.as_view(), name="adm_update_obyek_seleksi"),
    path("adm_lelang/modal_pengumuman_lelang/<int:pk>/", views.pengumumanLelangCreateView.as_view(), name="adm_modal_pengumuman_lelang"),
    path("adm_lelang/modal_update_pengumuman_lelang/<int:pk>/", views.pengumumanLelangUpdateView.as_view(), name="adm_modal_update_pengumuman_lelang"),
    path("adm_lelang/modal_persyaratan_lelang/<int:pk>/", views.persyaratanSeleksiCreateView.as_view(), name="adm_modal_persyaratan_lelang"),
    path("adm_lelang/modal_update_persyaratan_lelang/<int:pk>/<int:id>/", views.persyaratanSeleksiUpdateView.as_view(), name="adm_modal_update_persyaratan_lelang"),
    path("adm_lelang/modal_alamat_panitia/<int:pk>/", views.alamatPanitiaCreateView.as_view(), name="adm_modal_persyaratan_lelang"),
    path("adm_lelang/modal_update_alamat_panitia/<int:pk>/<int:id>/", views.alamatPanitiaUpdateView.as_view(), name="adm_modal_update_persyaratan_lelang"),
    path("adm_lelang/modal_jadwal_seleksi/<int:pk>/", views.jadwalSeleksiCreateView.as_view(), name="adm_modal_persyaratan_lelang"),
    path("adm_lelang/modal_update_jadwal_seleksi/<int:pk>/<int:id>/", views.jadwalSeleksiUpdateView.as_view(), name="adm_modal_update_persyaratan_lelang"),
    
    path("adm_lelang/modal_penanggung_jawab/<int:pk>/", views.PenanggungJawabCreateView.as_view()),
    path("adm_lelang/modal_update_penanggung_jawab/<int:pk>/<int:id>/", views.PenanggungJawabUpdateView.as_view()),

    path("adm_lelang/lihat_ba/<int:pk>/", views.PdfsView.as_view(), name="PdfsView"),
    path("adm_lelang/download_ba/<int:pk>/", views.docxview, name="DocxView"),

    path("adm_lelang/bidder_lelang/<int:pk>/", views.bidder_lelangListView.as_view()),
    path("adm_lelang/berita_acara/", views.template_berita_acaraListView.as_view(), name="adm_lelang_ba_list"),
    path("adm_lelang/modal_create/", views.template_berita_acaraCreateView.as_view(), name="adm_lelang_ba_list"),
    path("adm_lelang/modal_update/<int:pk>/", views.template_berita_acaraUpdateView.as_view(), name="adm_lelang_ba_list"),
    path("adm_lelang/auctioner_lelang/<int:pk>/", views.auctioner_lelangListView.as_view(), name="adm_lelang_item_lelang_list"),
    path("adm_lelang/viewer_lelang/<int:pk>/", views.viewer_lelangListView.as_view(), name="adm_lelang_item_lelang_list"),
    path("adm_lelang/alamat_panitia/<int:pk>/", views.alamat_panitiaListView.as_view(), name="adm_lelang_item_lelang_list"),
    path("adm_lelang/modal_dasar_hukum/<int:pk>/", views.dasarHukumCreateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("adm_lelang/modal_update_dasar_hukum/<int:pk>/<int:id>/", views.dasarHukumUpdateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("adm_lelang/dasar_hukum/<int:pk>/", views.dasar_hukumListView.as_view(), name="adm_dasar_hukumListView"),
    path("adm_lelang/dasar_hukum2/<int:pk>/", views.dasar_hukumListView.as_view(), name="adm_dasar_hukumListView"),
    path("adm_lelang/persyaratan_lelang/<int:pk>/", views.persyaratan_lelangListView.as_view(), name="adm_persyaratan_lelangListView"),
    path("adm_lelang/jadwal_lelang/<int:pk>/", views.jadwal_seleksiListView.as_view(), name="adm_jadwal_seleksiListView"),
    path("adm_lelang/jadwal_lelang2/<int:pk>/", views.jadwal_seleksi2ListView.as_view(), name="adm_jadwal_seleksiListView"),
    #path("adm_lelang/pengumuman_lelang/<int:pk>/<int:current_step>/", views.pengumuman_lelangListView.as_view(), name="adm_pengumuman_lelangListView"),
    path("adm_lelang/pengumuman_lelang2/<int:item_lelang>/<int:current_step>/", views.pengumuman_lelang2ListView.as_view(), name="adm_pengumuman_lelang2ListView"),
    path("adm_lelang/pengumuman_lelang3/<int:item_lelang>/<int:current_step>/", views.pengumuman_lelang3ListView.as_view(), name="adm_pengumuman_lelang3ListView"),
    path("pengumuman_auctioner/<int:item_lelang>/<int:current_step>/<int:auctioner>/", views.pengumuman_lelangListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    path("pengumuman_bidder/<int:item_lelang>/<int:current_step>/", views.pengumuman_lelang2ListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    path("modal_pengumuman/<int:pk>/<int:tahapan>/", views.pengumumanCreateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("modal_pengumuman/<int:pk>/", views.pengumumanUpdateView.as_view(), name="adm_lelang_detail_itemlelang_list"),

    # api check bidder
    path("api_check_bidder/<int:pk>/<int:objek_lelang>/", views.api_check_bidder, name='api_check_bidder'),
)