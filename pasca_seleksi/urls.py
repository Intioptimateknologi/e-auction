from django.urls import path, include
from rest_framework import routers

from . import views
from . import api

router = routers.DefaultRouter()
router.register("pemilihan_blok", api.pemilihan_blok_pasca_seleksiViewSet, basename="pemilihan_blok")
router.register("blok", api.blokViewSet, basename="blok")
router.register("seleksi", api.seleksiViewSet, basename="seleksi")
router.register("sanggahan", api.sanggahanViewSet, basename="sanggahan")
router.register("sanggahan_jawaban", api.sanggahan_jawabanViewSet, basename="sanggahan_jawaban")
router.register("jawaban_atas_sanggahan", api.jawaban_atas_sanggahanViewSet, basename="jawaban_atas_sanggahan")
router.register("pemenang", api.pemenangViewSet, basename="pemenang")
router.register("pengumuman_pemenang", api.pengumuman_pemenangViewSet, basename="pengumuman_pemenang")
router.register("berita_acara", api.berita_acara_pasca_seleksiViewSet, basename="berita_acara")
router.register("form_sanggahan", api.form_ps_sanggahanViewSet, basename="form_sanggahan")
router.register("undangan_sanggahan", api.undangan_ps_sanggahanViewSet, basename="undangan_sanggahan")
router.register("jawaban_ps_sanggahan", api.jawaban_ps_sanggahanViewSet, basename="jawaban_ps_sanggahan")
router.register("blok_pasca_seleksi", api.blok_paska_seleksiViewSet, basename="blok_pasca_seleksi")
router.register("pemenang_blok_pasca_seleksi", api.pemenang_blok_paska_seleksiViewSet, basename="pemenang_blok_pasca_seleksi")
urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("hasil_seleksi/", views.hasil_seleksi),
    path("pemilihan_blok/", views.pemilihan_blok),
    path("penetapan_pemenang/", views.penetapan_pemenang),
    path("sanggahan/", views.sanggahan),
    path("settings/", views.settings),
    
    
    #TABLE
    path("pasca_seleksi/undangan_p_blok/<int:pk>/", views.ps_u_p_blokListView.as_view(), name="pascaseleksi_undangan_p_blok_list"),
    path("pasca_seleksi/pemilihan_blok/<int:pk>/", views.ps_pemilihan_blokListView.as_view(), name="pascaseleksi_pemilihan_blok_list"),
    path("pasca_seleksi/hasil_seleksi/<int:pk>/", views.ps_seleksiListView.as_view(), name="pascaseleksi_hasil_seleksi_list"),
    path("pasca_seleksi/sanggahan/<int:pk>/", views.ps_sanggahanListView.as_view(), name="pascaseleksi_sanggahan_list"),
    path("pasca_seleksi/sanggahan_jawaban/<int:pk>/", views.ps_sanggahan_jawabanListView.as_view(), name="pascaseleksi_sanggahan_jawaban_list"),
    path("pasca_seleksi/jawaban_a_sanggahan/<int:pk>/", views.ps_j_a_sanggahanListView.as_view(), name="pascaseleksi_jawaban_atas_sanggahan_list"),
    path("pasca_seleksi/pemenang/<int:pk>/", views.ps_pemenangListView.as_view(), name="pascaseleksi_pemenang_list"),
    path("pasca_seleksi/pengumuman_pemenang/<int:pk>/", views.ps_p_pemenangListView.as_view(), name="pascaseleksi_p_pemenang_list"),
    path("pasca_seleksi/berita_acara/<int:pk>/<str:code>/", views.ps_berita_acaraListView.as_view(), name="pascaseleksi_berita_acara_list"),
    path("pasca_seleksi/blok_paska_seleksi/<int:pk>/", views.blok_pasca_seleksiListView.as_view(), name="pascaseleksi_berita_acara_list"),
    path("pasca_seleksi/pemenang_blok_paska_seleksi/<int:pk>/", views.pemenang_blok_pasca_seleksiListView.as_view(), name="pemenang_pascaseleksi_berita_acara_list"),
    
        # update sanggahannya
    path("pasca_seleksi/form_ps_sanggahan/<int:pk>/", views.ps_form_sanggahannewListView.as_view(), name="pascaseleksi_ps_sanggahan_list"),
    path("pasca_seleksi/form_kirim_sanggahan/<int:pk>/", views.ps_undg_sanggahannewListView.as_view(), name="pascaseleksi_ps_kirim_sanggahan_list"),
    path("pasca_seleksi/jawab_sanggahan/<int:pk>/", views.ps_jawaban_sanggahannewListView.as_view(), name="pascaseleksi_ps_jawab_sanggahan_list"),
    
    #ONLY TABLE WITHOUT CRUD
    path("pasca_seleksi/undangan_p_blok2/<int:pk>/<int:code>/", views.ps_u_p_blok2ListView.as_view(), name="pascaseleksi_undangan_p_blok_list2"),
    path("pasca_seleksi/pemilihan_blok2/<int:pk>/", views.ps_pemilihan_blok2ListView.as_view(), name="pascaseleksi_pemilihan_blok_list2"),

    path("pasca_seleksi/pemilihan_blok3/<int:pk>/", views.ps_pemilihan_blok3ListView.as_view(), name="pascaseleksi_pemilihan_blok_list2"),

    path("pasca_seleksi/hasil_seleksi2/<int:pk>/", views.ps_seleksi2ListView.as_view(), name="pascaseleksi_hasil_seleksi_list2"),
    path("pasca_seleksi/sanggahan2/<int:pk>/", views.ps_sanggahan2ListView.as_view(), name="pascaseleksi_sanggahan_list2"),
    path("pasca_seleksi/sanggahan_jawaban2/<int:pk>/", views.ps_sanggahan_jawaban2ListView.as_view(), name="pascaseleksi_sanggahan_jawaban_list2"),
    path("pasca_seleksi/jawaban_a_sanggahan2/<int:pk>/<int:code>/", views.ps_j_a_sanggahan2ListView.as_view(), name="pascaseleksi_jawaban_atas_sanggahan_list2"),
    path("pasca_seleksi/pemenang2/<int:pk>/", views.ps_pemenang2ListView.as_view(), name="pascaseleksi_pemenang_list2"),
    path("pasca_seleksi/pengumuman_pemenang2/<int:pk>/", views.ps_p_pemenang2ListView.as_view(), name="pascaseleksi_p_pemenang_list2"),
    path("pasca_seleksi/berita_acara2/<int:pk>/<str:code>/", views.ps_berita_acara2ListView.as_view(), name="pascaseleksi_berita_acara_list2"),
        # update sanggahannya
    path("pasca_seleksi/form_ps_sanggahan2/<int:pk>/", views.ps_form_sanggahannew2ListView.as_view(), name="pascaseleksi_ps_sanggahan_list2"),
    path("pasca_seleksi/form_kirim_sanggahan2/<int:pk>/", views.ps_undg_sanggahannew2ListView.as_view(), name="pascaseleksi_ps_kirim_sanggahan_list2"),
    path("pasca_seleksi/jawab_sanggahan2/<int:pk>/", views.ps_jawaban_sanggahannew2ListView.as_view(), name="pascaseleksi_ps_jawab_sanggahan_list2"),
    

    #Special Case 
    path("pasca_seleksi/pemilihan_blok3/<int:pk>/", views.ps_pemilihan_blok3ListView.as_view(), name="pascaseleksi_pemilihan_blok_list3"),
    
    #MODAL-MODAL
    path("pasca_seleksi/modal_undangan_p_blok/<int:pk>/", views.ps_undangan_p_blokCreateView.as_view(), name="pascaseleksi_undangan_p_blok_create"),
    path("pasca_seleksi/modal_pemilihan_blok/<int:pk>/", views.ps_pemilihan_blokCreateView.as_view(), name="pascaseleksi_pemilihan_blok_create"),
    path("pasca_seleksi/modal_hasil_seleksi/<int:pk>/", views.ps_seleksiCreateView.as_view(), name="pascaseleksi_hasil_seleksi_create"),
    path("pasca_seleksi/modal_sanggahan/<int:pk>/", views.ps_sanggahanCreateView.as_view(), name="pascaseleksi_sanggahan_create"),
    path("pasca_seleksi/modal_sanggahan_jawaban/<int:pk>/", views.ps_sanggahanjawabanCreateView.as_view(), name="pascaseleksi_sanggahan_jawaban_create"),
    path("pasca_seleksi/modal_jawaban_a_sanggahan/<int:pk>/", views.ps_jawaban_atas_sanggahanCreateView.as_view(), name="pascaseleksi_jawaban_atas_sanggahan_create"),
    path("pasca_seleksi/modal_pemenang/<int:pk>/", views.ps_pemenangCreateView.as_view(), name="pascaseleksi_pemenang_create"),
    path("pasca_seleksi/modal_pengumuman_pemenang/<int:pk>/", views.ps_p_pemenangCreateView.as_view(), name="pascaseleksi_p_pemenang_create"),
    path("pasca_seleksi/modal_ba_p_blok/<int:pk>/", views.ps_berita_acaraCreateView.as_view(), name="pascaseleksi_berita_acara_create"),
    path("pasca_seleksi/modal_ba_sanggahan/<int:pk>/", views.ps_berita_acara_sanggahanCreateView.as_view(), name="pascaseleksi_berita_acara_sanggahan_create"),
    path("pasca_seleksi/modal_ba_h_seleksi/<int:pk>/", views.ps_berita_acara_hasil_seleksiCreateView.as_view(), name="pascaseleksi_berita_acara_h_seleksi_create"),
    path("pasca_seleksi/block_paska_seleksi/<int:pk>/", views.blok_paska_seleksiCreateView.as_view(), name="pascaseleksi_berita_acara_h_seleksi_create"),
    path("pasca_seleksi/pemenang_block_paska_seleksi/<int:pk>/", views.pemenang_blok_paska_seleksiCreateView.as_view(), name="pemenang_pascaseleksi_berita_acara_h_seleksi_create"),
    
    path("pasca_seleksi/update_block_paska_seleksi/<int:pk>/", views.blok_paska_seleksiUpdateView.as_view(), name="pascaseleksi_berita_acara_h_seleksi_create"),
    path("pasca_seleksi/update_pemenang_block_paska_seleksi/<int:pk>/", views.pemenang_blok_paska_seleksiUpdateView.as_view(), name="pemenang_pascaseleksi_berita_acara_h_seleksi_create"),

    path("pasca_seleksi/modal_bidder_pemilihan_blok/<int:pk>/", views.pemilihan_blokUpdateView.as_view(), name="pascaseleksi_pemilihan_blok_create"),

        # update sanggahannya
    path("pasca_seleksi/modal_form_ps_sanggahan/<int:pk>/", views.form_ps_sanggahanCreateView.as_view(), name="pascaseleksi_ps_sanggahan_create"),
    path("pasca_seleksi/modal_form_kirim_sanggahan/<int:pk>/", views.kirim_undg_sanggahanCreateView.as_view(), name="pascaseleksi_ps_kirim_sanggahan_create"),
    path("pasca_seleksi/modal_jawab_sanggahan/<int:pk>/", views.jawab_pasca_sanggahanCreateView.as_view(), name="pascaseleksi_ps_jawab_sanggahan_create"),
    
    #UPDATE
    path("pasca_seleksi/modal_update_undangan_p_blok/<int:pk>/<int:id>/", views.ps_undangan_blokUpdateView.as_view(), name="pascaseleksi_undangan_p_blok_update"),
    path("pasca_seleksi/modal_update_pemilihan_blok/<int:pk>/<int:id>/", views.ps_pemilihan_blokUpdateView.as_view(), name="pascaseleksi_pemilihan_blok_update"),
    path("pasca_seleksi/modal_update_hasil_seleksi/<int:pk>/<int:id>/", views.ps_seleksiUpdateView.as_view(), name="pascaseleksi_hasil_seleksi_update"),
    path("pasca_seleksi/modal_update_sanggahan/<int:pk>/<int:id>/", views.ps_sanggahanUpdateView.as_view(), name="pascaseleksi_sanggahan_update"),
    path("pasca_seleksi/modal_update_sanggahan_jawaban/<int:pk>/<int:id>/", views.ps_sanggahan_jawabanUpdateView.as_view(), name="pascaseleksi_sanggahan_jawaban_update"),
    path("pasca_seleksi/modal_update_jawaban_a_sanggahan/<int:pk>/<int:id>/", views.ps_jawaban_atas_sanggahanUpdateView.as_view(), name="pascaseleksi_jawaban_atas_sanggahan_update"),
    path("pasca_seleksi/modal_update_pemenang/<int:pk>/", views.ps_pemenangUpdateView.as_view(), name="pascaseleksi_pemenang_update"),
    path("pasca_seleksi/modal_update_pengumuman_pemenang/<int:pk>/", views.ps_pengumuman_pemenangUpdateView.as_view(), name="pascaseleksi_p_pemenang_update"),
    path("pasca_seleksi/modal_update_ba_p_blok/<int:pk>/<int:id>/", views.ps_berita_acaraUpdateView.as_view(), name="pascaseleksi_berita_acara_update"),
    path("pasca_seleksi/modal_update_ba_h_seleksi/<int:pk>/<int:id>/", views.ps_berita_acara_hasil_seleksiUpdateView.as_view(), name="pascaseleksi_berita_acara_h_seleksi_update"),
    path("pasca_seleksi/modal_update_ba_sanggahan/<int:pk>/<int:id>/", views.ps_berita_acara_sanggahanUpdateView.as_view(), name="pascaseleksi_berita_acara_sanggahan_update"),
    
        # update sanggahannya
    path("pasca_seleksi/modal_update_form_ps_sanggahan/<int:pk>/", views.ps_form_sanggahanUpdateView.as_view(), name="pascaseleksi_ps_sanggahan_update"),
    path("pasca_seleksi/modal_update_form_kirim_sanggahan/<int:pk>/", views.ps_undg_sanggahanUpdateView.as_view(), name="pascaseleksi_ps_kirim_sanggahan_update"),
    path("pasca_seleksi/modal_update_jawab_sanggahan/<int:pk>/", views.ps_jawab_sanggahanUpdateView.as_view(), name="pascaseleksi_ps_jawab_sanggahan_update"),

    # api
    path("api/api_check_ps_sanggahan/<pk>/", views.api_check_ps_sanggahan, name="api_check_ps_sanggahan"),
)