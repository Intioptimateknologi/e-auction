from django.urls import path, include
from rest_framework import routers
from . import api
from . import views

router = routers.DefaultRouter()
router.register("integrasi_users_judul", api.tahun_judulViewSet)
router.register("rencana_jadwal_seleksi", api.rencana_jadwal_seleksiViewSet)
router.register("rencana_seleksinya", api.rencana_seleksis_seleksiViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),

    path("api/get_judulby_tahun/<tahun>/", views.api_get_judulby_tahun, name="api_get_judulby_tahun"),
)
