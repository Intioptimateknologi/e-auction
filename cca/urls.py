from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
#router.register("jadwal_smra", api.jadwalSMRAViewSet)
router.register("round_cca", api.round_ccaViewSet, basename="round_cca")
router.register("sum_round_cca", api.sum_round_ccaViewSet, basename="sum_round_cca")
router.register("auctioner_hasil", api.auctioner_hasilViewSet, basename="auctioner_hasil")
router.register("round_detail_cca", api.round_detail_ccaViewSet, basename="round_detail_cca")
router.register("obyek_seleksi_cca", api.obyek_seleksiViewSet, basename="obyek_seleksi_cca")
router.register("kombinasi_cr", api.matrix_hasil_crViewSet, basename="kombinasi_cr")
router.register("hasil_cca", api.hasil_ccaViewSet, basename="hasil_cca")
router.register("price_increase", api.price_increaseViewSet, basename="price_increase")
router.register("matrix_cr", api.matrix_hasil_crViewSet, basename="matrix_cr")
router.register("matrix2_cr", api.matrix2_crViewSet, basename="matrix2_cr")



urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("manajemen_cca/", views.home),
    path("settings/", views.settings),
    path("cr/", views.cr),
    path("sr/", views.sr),
    path("ar/", views.ar),
    path("jadwal/", views.jadwal),
    path("dashboard_bidder/", views.dashboard_bidder),
    path("dashboard_auctioner/", views.dashboard_auctioner),
    path("putaran_cr/", views.putaran_cr),
    path("putaran_sr/", views.putaran_sr),
    path("putaran_ar/", views.putaran_ar),


    path("obyek_seleksi/<int:pk>/", views.obyek_seleksiView.as_view()),
    path("obyek_seleksi_group/<int:pk>/", views.obyek_seleksiGroupView.as_view()),
    path("obyek_seleksi_form/<int:pk>/", views.obyek_seleksiCreateView.as_view()),
    path("obyek_seleksi_update/<int:pk>/", views.obyek_seleksiUpdateView.as_view()),

    path("hasil_cca/<int:pk>/", views.hasil_ccaListView.as_view()),
    path("auctioner_hasil/<int:pk>/", views.auctioner_hasilListView.as_view()),
    path("hasil_invalidcca/<int:pk>/", views.hasil_invalidccaListView.as_view()),
    path("round_cca/<int:pk>/<int:bidder>/", views.round_ccsListView.as_view()),
    path("round_detail_cca/<int:pk>/<int:bidder>/", views.round_detail_ccsListView.as_view()),
    path("matirx_cr/<int:pk>/<int:bidder>/", views.matirx_hasil_crListView.as_view()),

    path("obyek_seleksi2/<int:pk>/", views.detail_itemlelangListView.as_view()),
    path("obyek_seleksi2_form/<int:pk>/", views.detail_itemlelangCreateView.as_view()),
    path("obyek_seleksi2_update/<int:pk>/", views.detail_itemlelangUpdateView.as_view()),

    path("price_increase/<int:pk>/", views.price_increaseListView.as_view()),
    path("price_increase_form/<int:pk>/", views.price_increaseCreateView.as_view()),
    path("price_increase_update/<int:pk>/", views.price_increaseUpdateView.as_view()),
    path('dashboard/', views.dashboard, name='pie-chart'),
    path('hasil_chart/<int:pk>/', views.hasil_chart, name='pie-chart'),
    path('hasil_chart_maxmin/<int:pk>/', views.hasil_chart_maxmin, name='pie-chart'),

)