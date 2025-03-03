from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register("round_smra", api.round_smraViewSet)
router.register("sum_round_smra", api.sum_round_smraViewSet)
router.register("hasil_smra", api.hasil_smra2ViewSet)
router.register("auctioneer_hasil", api.auctioner_hasilViewSet)
router.register("price_increase", api.price_increaseViewSet)
router.register("obyek_seleksi", api.obyek_seleksiViewSet)
router.register("jadwal_smra", api.jadwalSMRAViewSet)



urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("manajemen_smra/", views.home),
    path("settings/", views.settings),
    path("dashboard_bidder/", views.dashboard_bidder),
    path("hasil_putaran_bidder/", views.hasil_putaran_bidder),
    path("hasil_putaran_auctioneer/", views.hasil_putaran_auctioneer),
    path("dashboard_auctioner/", views.dashboard_auctioner),
    path("dashboard_auctioner2/", views.dashboard_auctioner2),
    path("summary/<int:pk>/", views.round_smraPivotView.as_view()),
    path("hasil_smra2/<int:pk>/", views.hasil_smra2ListView.as_view()),
    path("hasil_smra2_auctioner/<int:pk>/", views.hasil_smra2_auctionerListView.as_view()),
    path("hasil_akhir_auctioner/<int:pk>/", views.hasil_akhir_auctionerListView.as_view()),
    path("hasil2_smra2/<int:pk>/", views.hasil2_smra2ListView.as_view()),
    path("hasil3_smra2/<int:pk>/", views.hasil3_smra2ListView.as_view()),
    path("hasil4_smra2/<int:pk>/", views.hasil4_smra2ListView.as_view()),
    path("hasil5_smra2/<int:pk>/", views.hasil5_smra2ListView.as_view()),
    
    path("jadwalbg/<int:pk>/", views.scheduler_smra2ListView.as_view()),

    path("auctioner_highest/<int:pk>/", views.auctioner_highestListView.as_view()),
    path("auctioner_hasil/<int:pk>/", views.auctioner_hasilListView.as_view()),
    path("auctioner_hasil_maxmin/<int:pk>/", views.auctioner_hasil_maxminListView.as_view()),
    path("price_increase/<int:pk>/", views.price_increaseListView.as_view()),
    path("price_increase_form/<int:pk>/", views.price_increaseCreateView.as_view()),
    path("price_increase_update/<int:pk>/", views.price_increaseUpdateView.as_view()),
    path("bid_smra2/<int:pk>/<int:bidder>/", views.bidSMRA2CreateView.as_view()),
    path("pdfview/<int:pk>/<int:bidder>/", views.PdfsView.as_view()),
    path("docview/<int:pk>/<int:bidder>/", views.docxview),

    path("obyek_seleksi/<int:pk>/", views.obyek_seleksiView.as_view()),
    path("obyek_seleksi_group/<int:pk>/", views.obyek_seleksiGroupView.as_view()),
    path("obyek_seleksi_form/<int:pk>/", views.obyek_seleksiCreateView.as_view()),
    path("obyek_seleksi_update/<int:pk>/", views.obyek_seleksiUpdateView.as_view()),
    path("obyek_seleksi2/<int:pk>/", views.detail_itemlelangListView.as_view()),
    path("obyek_seleksi2_form/<int:pk>/", views.detail_itemlelangCreateView.as_view()),
    path("obyek_seleksi2_update/<int:pk>/", views.detail_itemlelangUpdateView.as_view()),

    path('create_putaran/<int:pk>/', views.create_schedule, name='putaran-chart'),
    path('clear_putaran/<int:pk>/', views.clear_schedule, name='putaran-chart'),
    path('run_putaran/<int:pk>/', views.run_schedule, name='putaran-chart'),
    path('clear_putaranbg/<int:pk>/', views.clear_schedulebg, name='putaran-chart'),
    path('push_message/', views.push_message, name='putaran-chart'),

    path('hasil_chart/<int:pk>/', views.hasil_chart, name='pie-chart'),
    path('hasil_chart_maxmin/<int:pk>/', views.hasil_chart_maxmin, name='pie-chart'),
    path('hasil_persen/<int:pk>/', views.hasil_persen, name='pie-chart'),
    path('hasil_block/<int:pk>/', views.hasil_block, name='pie-chart'),
    path('hasil_peserta/<int:pk>/', views.hasil_peserta, name='pie-chart'),
    path('dashboard/', views.dashboard, name='pie-chart'),

    path("jadwal_putaran/<int:pk>/", views.round_scheduleListView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("jadwal_putaran2/<int:pk>/", views.round_schedule2ListView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("modal_jadwal_putaran/<int:pk>/", views.round_scheduleCreateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("modal_update_putaran/<int:pk>/", views.round_scheduleUpdateView.as_view(), name="adm_lelang_detail_itemlelang_list"),

    
)