from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register("jadwal_smra", api.jadwalSMRAViewSet)
router.register("hasil_cca2", api.hasil_cca2ViewSet)
router.register("round_cca2", api.round_cca2ViewSet)
router.register("round_smra", api.round_smraViewSet)
router.register("round_smra_sum", api.round_smra_sumViewSet)
router.register("round_smra_temp", api.round_smra_tempViewSet)
#router.register("bidding_round_smra", api.bidding_round_smraViewSet)
#router.register("auction_smra_summary", api.round_smraSummaryViewSet)
#router.register("bid_bidder", api.smra_bid_bidderViewSet)
router.register("undangan_smra_cca", api.undangan_SMRA_CCAViewSet)
router.register("berita_acara_lelang", api.berita_acara_lelangViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("manajemen_smra/", views.home),
    path("jadwal/", views.jadwal),
    path("dashboard_bidder/", views.dashboard_bidder),
    path("dashboard_auctioner/", views.dashboard_auctioner),
    #path("modal_bidderlelang/<int:pk>/", views.bidderLelangCreateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    #path("modal_auctionerlelang/<int:pk>/", views.auctionerLelangCreateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    #path("modal_viewerlelang/<int:pk>/", views.viewerLelangCreateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("jadwal_putaran/<int:pk>/", views.round_scheduleListView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("jadwal_putaran2/<int:pk>/", views.round_schedule2ListView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("modal_jadwal_putaran/<int:pk>/", views.round_scheduleCreateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("modal_viewerlelang/<int:pk>/", views.viewerLelangCreateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    path("modal_update_putaran/<int:pk>/", views.round_scheduleUpdateView.as_view(), name="adm_lelang_detail_itemlelang_list"),
    # tabel undangan
    path("undangan_smra_cca/<int:pk>/<str:code>/", views.undangan_smra_ccaListView.as_view(), name="undangan_smra_ccaListView"),
    path("undangan_smra_cca2/<int:pk>/<str:code>/<int:id>/", views.undangan_smra_cca2ListView.as_view(), name="undangan_smra_cca2ListView"),
    path("undangan_smra_cca_bid/<int:pk>/<str:code>/<int:id>/", views.undangan_smra_ccabidListView.as_view(), name="undangan_smra_cca2ListView"),
    path("undangan_smra_cca_auc/<int:pk>/<str:code>/<int:id>/", views.undangan_smra_ccaaucListView.as_view(), name="undangan_smra_cca2ListView"),
    # modal smra
    path("modal_undangan_smra/<int:pk>/", views.undangan_smraCreateView.as_view(), name="undangan_smraCreateView"),
    path("modal_update_undangan_smra/<int:pk>/<int:id>/", views.undangan_smraUpdateView.as_view(), name="undangan_smraUpdateView"),

)