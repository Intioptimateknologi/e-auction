from django.urls import path, include
from rest_framework import routers

from . import views
from . import api

router = routers.DefaultRouter()
router.register("penawaran", api.penyampaian_penawaranViewSet)
router.register("evaluasi", api.evaluasi_penyampaian_penawaranViewSet)
router.register("obyek_seleksi", api.obsel_sampul2ViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("management/", views.home),
    path("evaluasi_penawaran/<int:pk>", views.evaluasi_penawaran),
    path("penawaran/<int:pk>", views.penawaran),
    path("settings/<int:pk>", views.setting),
   

    path("sampul2/obsel/<int:pk>/", views.obselListView.as_view(), name="sampul2_penyampaian_penawaran_list"),
    path("sampul2/kirim_obsel/<int:pk>/", views.ObyekSeleksiCreateView.as_view(), name="sampul2_penyampaian_penawaran_create"),
    path("sampul2/update_obsel/<int:pk>/", views.ObyekSeleksiUpdateView.as_view(), name="sampul2_penyampaian_penawaran_create"),

    path("sampul2/penawaran/<int:pk>/", views.penawaranListView.as_view(), name="sampul2_penyampaian_penawaran_list"),
    path("sampul2/kirim_penawaran/<int:pk>/", views.PenawaranCreateView.as_view(), name="sampul2_penyampaian_penawaran_create"),
    path("sampul2/update_penawaran/<int:pk>/", views.PenawaranUpdateView.as_view(), name="sampul2_penyampaian_penawaran_create"),
    path("sampul2/verifikasi_penawaran/<int:pk>/", views.verifikasiPenawaranUpdateView.as_view(), name="sampul2_penyampaian_penawaran_create"),
    path("sampul2/hasil_pemasukan_penawaran/<int:pk>/", views.hasil_pemasukanPenawaranListView.as_view(), name="sampul2_penyampaian_penawaran_create"),
    
    path("sampul2/evaluasi_penawaran/<int:pk>/", views.evaluasiPenawaranListView.as_view(), name="sampul2_penyampaian_penawaran_list"),
    path("sampul2/kirim_evaluasi_penawaran/<int:pk>/", views.EvaluasiPenawaranCreateView.as_view(), name="sampul2_penyampaian_penawaran_create"),
    path("sampul2/update_evaluasi_penawaran/<int:pk>/", views.EvaluasiPenawaranUpdateView.as_view(), name="sampul2_penyampaian_penawaran_create"),
    
)