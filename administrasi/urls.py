from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
#router.register("undangan_pemeriksaan_kelengkapan", api.undangan_pemeriksaan_kelengkapanViewSet)
router.register("form_pemeriksaan", api.form_pemeriksaanViewSet)
router.register("berita_acara", api.berita_acara_allViewSet)
#router.register("undangan_verifikasi", api.undangan_verifikasiViewSet)
router.register("permohonan_keikutsertaan", api.permohonan_keikutsertaanViewSet)
##router.register("undangan_evaluasi", api.undangan_evaluasiViewSet)
#router.register("undangan_sanggahan", api.undangan_sanggahanViewSet)
#router.register("undangan_akun", api.undangan_akunViewSet)
router.register("form_verifikasi", api.form_verifikasiViewSet)
router.register("form_evaluasi", api.form_evaluasiViewSet)
router.register("form_sanggahan", api.form_sanggahanViewSet)
router.register("hasil_evaluasi", api.hasil_evaluasiViewSet)
router.register("jawaban_sanggahan", api.jawaban_sanggahanViewSet)
router.register("hasil_kesimpulan", api.hasilKesimpulanViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("akun_lelang/", views.akun_lelang),
    path("evaluasi/", views.hasil_evaluasi),
    path("kelengkapan/", views.pemeriksaan),
    path("keikutsertaan/", views.permohonan),
    path("sanggahan/", views.sanggahan),
    path("verifikasi/", views.verifikasi),
    path("pengumuman/", views.pengumuman),

   # path("administrasi/undangan_p_kelengkapan/<int:pk>/", views.undangan_p_kelengkapanView.as_view(), name="undangan_pemeriksaan_kelengkapan"),
    path("administrasi/form_pemeriksaan/<int:pk>/", views.form_pemeriksaan_kView.as_view(), name="form_pemeriksaan"),
    path("administrasi/berita_acara/<int:pk>/", views.berita_acara_allView.as_view(), name="form_pemeriksaan"),
    path("administrasi/p_keikutsertaan/<int:pk>/", views.pkeikutsertaan_allView.as_view(), name="adm_p_keikutserta"),
    path("administrasi/pengambilan_keikutsertaan/<int:pk>/", views.PdfsView_keikutsertaan.as_view(), name="PdfsView"),
    
    # LIST DATA TABLE
    #path("administrasi/undangans_p_kelengkapan/<int:pk>/", views.undgn_pemeriksaan_klngkpnListView.as_view(), name="undgn_pemeriksaan_klngkpnListView"),
    #path("administrasi/undangans_p_kelengkapan2/<int:pk>/<int:code>/", views.undgn_pemeriksaan_klngkpn2ListView.as_view(), name="undgn_pemeriksaan_klngkpn2ListView"),
    #path("administrasi/undgn_evaluasi/<int:pk>/", views.undgn_evaluasiListView.as_view(), name="undgn_evaluasiListView"),
    #path("administrasi/undgn_evaluasi2/<int:pk>/<int:code>/", views.undgn_evaluasi2ListView.as_view(), name="undgn_evaluasi2ListView"),
    #path("administrasi/undgn_verifikasi/<int:pk>/", views.undgn_verifikasiListView.as_view(), name="undgn_verifikasiListView"),
    #path("administrasi/undgn_verifikasi2/<int:pk>/", views.undgn_verifikasi2ListView.as_view(), name="undgn_verifikasi2ListView"),
    #path("administrasi/undgn_sanggahan/<int:pk>/", views.undgn_sanggahanListView.as_view(), name="undgn_sanggahanListView"),
    #path("administrasi/undgn_sanggahan2/<int:pk>/", views.undgn_sanggahan2ListView.as_view(), name="undgn_sanggahan2ListView"),
    #path("administrasi/undgn_akun/<int:pk>/", views.undgn_akunListView.as_view(), name="undgn_akunListView"),
    #path("administrasi/undgn_akun2/<int:pk>/", views.undgn_akun2ListView.as_view(), name="undgn_akun2ListView"),
    path("administrasi/form_pemeriksaan/<int:pk>/", views.form_pemeriksaanListView.as_view(), name="form_pemeriksaanListView"),
    path("administrasi/form_pemeriksaan2/<int:pk>/", views.form_pemeriksaan2ListView.as_view(), name="form_pemeriksaan2ListView"),
    path("administrasi/form_verifikasi/<int:pk>/", views.form_verifikasiListView.as_view(), name="form_verifikasiListView"),
    path("administrasi/form_verifikasi2/<int:pk>/", views.form_verifikasi2ListView.as_view(), name="form_verifikasi2ListView"),
    path("administrasi/form_evaluasi/<int:pk>/", views.form_evaluasiListView.as_view(), name="form_evaluasiListView"),
    path("administrasi/form_evaluasi2/<int:pk>/", views.form_evaluasi2ListView.as_view(), name="form_evaluasi2ListView"),
    path("administrasi/form_sanggahan/<int:pk>/", views.form_sanggahanListView.as_view(), name="form_sanggahanListView"),
    path("administrasi/form_sanggahan2/<int:pk>/", views.form_sanggahan2ListView.as_view(), name="form_sanggahan2ListView"),
    path("administrasi/permohonan_keikutsertaan/<int:pk>/", views.permohonan_keikutsertaanListView.as_view(), name="permohonan_keikutsertaanListView"),
    path("administrasi/permohonan_keikutsertaan2/<int:pk>/", views.permohonan_keikutsertaan2ListView.as_view(), name="permohonan_keikutsertaan2ListView"),
    path("administrasi/permohonan_keikutsertaan3/<int:pk>/", views.permohonan_keikutsertaan3ListView.as_view(), name="permohonan_keikutsertaan3ListView"),
    path("administrasi/hasil_evaluasi/<int:pk>/", views.hasil_evaluasiListView.as_view(), name="hasil_evaluasiListView"),
    path("administrasi/hasil_evaluasi2/<int:pk>/", views.hasil_evaluasi2ListView.as_view(), name="hasil_evaluasi2ListView"),
    path("administrasi/hasil_evaluasi3/<int:pk>/", views.hasil_evaluasi3ListView.as_view(), name="hasil_evaluasi3ListView"),
    path("administrasi/hasil_evaluasi4/<int:pk>/", views.hasil_evaluasi4ListView.as_view(), name="hasil_evaluasi4ListView"),
    path("administrasi/ba_administrasi/<int:pk>/<str:code>/", views.ba_administrasiListView.as_view(), name="ba_administrasiListView"),
    path("administrasi/ba_administrasi2/<int:pk>/<str:code>/", views.ba_administrasi2ListView.as_view(), name="ba_administrasi2ListView"),
    path("administrasi/jawaban_sanggahan2/<int:pk>/", views.jawaban_sanggahan2ListView.as_view(), name="ba_administrasi2ListView"),
    path("administrasi/jawaban_sanggahan/<int:pk>/", views.jawaban_sanggahanListView.as_view(), name="ba_administrasi2ListView"),
     path("administrasi/pengumuman/<int:pk>/", views.pengumuman_hasil_evaluasiListView.as_view(), name="pengumuman_hasil_evaluasiListView"),
    
    # MODAL
    #path("administrasi/modal_undangans_p_kelengkapan/<int:pk>/", views.undgn_pemeriksaan_klngkpnCreateView.as_view(), name="modal_undgn_pemeriksaan_klngkpnCreateView"),
    #path("administrasi/modal_undgn_evaluasi/<int:pk>/", views.undangan_evaluasiCreateView.as_view(), name="modal_undgn_evaluasiCreateView"),
    #path("administrasi/modal_undgn_verifikasi/<int:pk>/", views.undangan_verifikasiCreateView.as_view(), name="modal_undgn_verifikasiCreateView"),
    #path("administrasi/modal_undgn_sanggahan/<int:pk>/", views.undangan_sanggahanCreateView.as_view(), name="modal_undgn_sanggahanCreateView"),
    #path("administrasi/modal_undgn_akun/<int:pk>/", views.undangan_akunCreateView.as_view(), name="modal_undgn_akunCreateView"),
    path("administrasi/modal_form_pemeriksaan/<int:pk>/", views.form_pemeriksaanCreateView.as_view(), name="modal_form_pemeriksaanCreateView"),
    path("administrasi/modal_form_verifikasi/<int:pk>/", views.form_verifikasiCreateView.as_view(), name="modal_form_verifikasiCreateView"),
    path("administrasi/modal_form_evaluasi/<int:pk>/", views.form_evaluasiCreateView.as_view(), name="modal_form_evaluasiCreateView"),
    path("administrasi/modal_form_sanggahan/<int:pk>/", views.form_sanggahanCreateView.as_view(), name="modal_form_sanggahanCreateView"),
    path("administrasi/modal_permohonan_keikutsertaan/<int:pk>/", views.permohonan_keikutsertaanCreateView.as_view(), name="modal_permohonan_keikutsertaanCreateView"),
    path("administrasi/modal_hasil_evaluasi/<int:pk>/", views.hasil_evaluasiCreateView.as_view(), name="modal_hasil_evaluasiCreateView"),
    path("administrasi/modal_ba_penyerahan/<int:pk>/", views.ba_penyerahanCreateView.as_view(), name="modal_ba_penyerahanCreateView"),
    path("administrasi/modal_ba_permohonan_keikutsertaan/<int:pk>/", views.ba_permohonan_keikutsertaanCreateView.as_view(), name="modal_ba_permohonan_keikutsertaanCreateView"),
    path("administrasi/modal_ba_verifikasi_permohonan/<int:pk>/", views.ba_verifikasi_permohonanCreateView.as_view(), name="modal_ba_verifikasi_permohonanCreateView"),
    path("administrasi/modal_ba_sanggahan/<int:pk>/", views.ba_sanggahanCreateView.as_view(), name="modal_ba_sanggahanCreateView"),
    path("administrasi/modal_ba_hasil_evaluasi/<int:pk>/", views.ba_hasil_evaluasiCreateView.as_view(), name="modal_ba_hasil_evaluasiCreateView"),
    path("administrasi/modal_ba_evaluasi/<int:pk>/", views.ba_evaluasiCreateView.as_view(), name="modal_ba_evaluasiCreateView"),
    path("administrasi/modal_jawaban_sanggahan/<int:pk>/", views.jawaban_sanggahanCreateView.as_view(), name="modal_ba_evaluasiCreateView"),
    
    # UPDATE
    #path("administrasi/modal_update_undangans_p_kelengkapan/<int:pk>/", views.PemeriksaanKelengkapanUpdateView.as_view(), name="modal_undgn_pemeriksaan_klngkpnUpdateView"),
    #path("administrasi/modal_update_undgn_evaluasi/<int:pk>/", views.EvaluasiUpdateView.as_view(), name="modal_undgn_evaluasiUpdateView"),
    #path("administrasi/modal_update_undgn_verifikasi/<int:pk>/", views.VerifikasiUpdateView.as_view(), name="modal_undgn_verifikasiUpdateView"),
    #path("administrasi/modal_update_undgn_sanggahan/<int:pk>/", views.sanggahanUpdateView.as_view(), name="modal_undgn_sanggahanUpdateView"),
    #path("administrasi/modal_update_undgn_akun/<int:pk>/", views.AkunFormUpdateView.as_view(), name="modal_undgn_akunUpdateView"),
    path("administrasi/modal_update_form_pemeriksaan/<int:pk>/", views.FormPemeriksaanUpdateView.as_view(), name="modal_form_pemeriksaanUpdateView"),
    path("administrasi/modal_update_form_verifikasi/<int:pk>/", views.FormVerifikasiUpdateView.as_view(), name="modal_form_verifikasiUpdateView"),
    path("administrasi/modal_update_form_evaluasi/<int:pk>/", views.FormEvaluasiUpdateView.as_view(), name="modal_form_evaluasiUpdateView"),
    path("administrasi/modal_update_form_sanggahan/<int:pk>/", views.FormSanggahanUpdateView.as_view(), name="modal_form_sanggahanUpdateView"),
    path("administrasi/modal_update_permohonan_keikutsertaan/<int:pk>/", views.PermohonanKeikutsertaanUpdateView.as_view(), name="modal_permohonan_keikutsertaanUpdateView"),
    path("administrasi/modal_update_hasil_evaluasi/<int:pk>/", views.hasil_evaluasiUpdateView.as_view(), name="modal_hasil_evaluasiUpdateView"),
    path("administrasi/modal_update_ba_penyerahan/<int:pk>/", views.ba_penyerahanUpdateView.as_view(), name="modal_ba_penyerahanUpdateView"),
    path("administrasi/modal_update_ba_permohonan_keikutsertaan/<int:pk>/", views.ba_permohonan_keikutsertaanUpdateView.as_view(), name="modal_ba_permohonan_keikutsertaanUpdateView"),
    path("administrasi/modal_update_ba_verifikasi_permohonan/<int:pk>/", views.ba_verifikasi_permohonanUpdateView.as_view(), name="modal_ba_verifikasi_permohonanUpdateView"),
    path("administrasi/modal_update_ba_sanggahan/<int:pk>/", views.ba_sanggahanUpdateView.as_view(), name="modal_ba_sanggahanUpdateView"),
    path("administrasi/modal_update_ba_hasil_evaluasi/<int:pk>/", views.ba_hasil_evaluasiUpdateView.as_view(), name="modal_ba_hasil_evaluasiUpdateView"),
    path("administrasi/modal_update_ba_evaluasi/<int:pk>/", views.ba_evaluasiUpdateView.as_view(), name="modal_ba_evaluasiUpdateView"),
    path("administrasi/modal_update_jawaban_sanggahan/<int:pk>/", views.JawabanSanggahanUpdateView.as_view(), name="modal_ba_evaluasiUpdateView"),

    # api
    path("api/api_check_keikutsertaan/<pk>/", views.api_check_keikutsertaan, name="api_delete_users_menugroup"),
    path("api/api_check_sanggahan/<pk>/", views.api_check_sanggahan, name="api_check_sanggahan"),
)