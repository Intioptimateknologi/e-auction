from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register("penawaran", api.penyampaian_penawaranViewSet)
router.register("revisi_penawaran", api.penyampaian_penawaran2ViewSet)
router.register("evaluasi", api.evaluasi_penyampaian_penawaranViewSet)
router.register("evaluasi_revisi", api.revisi_evaluasi_penyampaian_penawaranViewSet)
router.register("obyek_seleksi", api.obsel_negoViewSet)
router.register("hasil_nego", api.hasil_negoViewSet)


urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("management/", views.home),
    path("setting/", views.setting),
    path("penawaran/", views.penawaran),
    path("evaluasi_penawaran/", views.evaluasi_penawaran),
    path("revisi_penawaran/", views.revisi_penawaran),
    path("evaluasi_revisi_penawaran/", views.evaluasi_revisi_penawaran),

    path("nego/obsel/<int:pk>/", views.obselListView.as_view(), name="nego_penyampaian_penawaran_list"),
    path("nego/kirim_obsel/<int:pk>/", views.ObyekSeleksiCreateView.as_view(), name="nego_penyampaian_penawaran_create"),
    path("nego/update_obsel/<int:pk>/", views.ObyekSeleksiUpdateView.as_view(), name="nego_penyampaian_penawaran_create"),

    path("nego/penawaran/<int:pk>/", views.penawaranListView.as_view(), name="nego_penyampaian_penawaran_list"),
    path("nego/kirim_penawaran/<int:pk>/", views.PenawaranCreateView.as_view(), name="nego_penyampaian_penawaran_create"),
    path("nego/update_penawaran/<int:pk>/", views.PenawaranUpdateView.as_view(), name="nego_penyampaian_penawaran_create"),
    path("nego/verifikasi_penawaran/<int:pk>/", views.verifikasiPenawaranUpdateView.as_view(), name="nego_penyampaian_penawaran_create"),
    path("nego/hasil_pemasukan_penawaran/<int:pk>/", views.hasil_pemasukanPenawaranListView.as_view(), name="nego_penyampaian_penawaran_create"),
    
    path("nego/evaluasi_penawaran/<int:pk>/", views.evaluasiPenawaranListView.as_view(), name="nego_penyampaian_penawaran_list"),
    path("nego/kirim_evaluasi_penawaran/<int:pk>/", views.EvaluasiPenawaranCreateView.as_view(), name="nego_penyampaian_penawaran_create"),
    path("nego/update_evaluasi_penawaran/<int:pk>/", views.EvaluasiPenawaranUpdateView.as_view(), name="nego_penyampaian_penawaran_create"),
    
    path("nego/evaluasi_revisi/<int:pk>/", views.evaluasiRevisiPenawaranListView.as_view(), name="nego_penyampaian_penawaran_list"),
    path("nego/kirim_evaluasi_revisi/<int:pk>/", views.EvaluasiRevisiPenawaranCreateView.as_view(), name="nego_penyampaian_penawaran_detail"),
    path("nego/update_evaluasi_resisi/<int:pk>/", views.EvaluasiRevisiPenawaranUpdateView.as_view(), name="nego_penyampaian_penawaran_update"),
    
    path("nego/revisi/<int:pk>/", views.revisiPenawaranListView.as_view(), name="nego_penyampaian_penawaran_list"),
    path("nego/kirim_revisi/<int:pk>/", views.RevisiPenawaranCreateView.as_view(), name="nego_penyampaian_penawaran_detail"),
    path("nego/update_revisi/<int:pk>/", views.RevisiPenawaranUpdateView.as_view(), name="nego_penyampaian_penawaran_update"),
    path("nego/verifikasi_revisi_penawaran/<int:pk>/", views.verifikasirevisiPenawaranUpdateView.as_view(), name="nego_penyampaian_penawaran_create"),
    path("nego/hasil_pemasukan_revisi_penawaran/<int:pk>/", views.hasil_revisiPenawaranListView.as_view(), name="nego_penyampaian_penawaran_create"),
    
    #add new code for table hasilevrevpenawaran
    path("nego/hasil_evaluasi_revisi_penawaran/<int:pk>/", views.hasilevrevpenawaranListView.as_view(), name="hasil_rev_ev_pen_table"),
    path("nego/hasil_negosiasi/<int:pk>/", views.hasil_negosiasiListView.as_view(), name="hasil_negosiasi"),
)