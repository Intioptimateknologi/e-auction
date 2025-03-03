from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("banner", api.bannerViewSet, basename='banner')
router.register("aturan_lelang", api.aturan_lelangViewSet, basename='aturan_lelang')
router.register("history_lelang", api.history_lelangViewSet, basename='history_lelang')
router.register("portal_block", api.portal_blockViewSet, basename='portal_block')
router.register("lelang_mancanegara", api.lelang_mancanegaraViewSet, basename='lelang_mancanegara')
router.register("istilah_lelang", api.istilah_lelangViewSet, basename='istilah_lelang')
router.register("notice_lelang", api.notice_lelangViewSet, basename='notice_lelang')
router.register("profil", api.profilViewSet, basename='profil')
router.register("aturan_lelang2", api.aturan_lelang2ViewSet, basename='aturan_lelang2')
router.register("history_lelang2", api.history_lelang2ViewSet, basename='history_lelang2')
router.register("lelang_mancanegara2", api.lelang_mancanegara2ViewSet, basename='lelang_mancanegara2')

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("home/", views.home, name="portal_banner_list"),
    
    path("manage/", views.manage, name="manage_portal"),
    path("manage_banner/", views.manage_banner, name="manage banner"),
    path("banner_table/", views.BannerTableView.as_view(), name="manage banner"),
    path("get_front_banner/", views.get_front_banner, name="portal_banner_list"),
    path("get_istilah_lelang/", views.get_istilah_lelang, name="portal_banner_list"),
    path("get_history_lelang/", views.get_history_lelang, name="portal_history_lelang"),
    path("get_aturan_lelang/", views.get_aturan_lelang, name="portal_aturan_lelang"),
    path("get_notice_lelang/", views.get_notice_lelang, name="portal_notice_lelang"),
    path("lelang_mancanegara/", views.get_lelang_by_country, name="portal_banner_list"),
    path("banner/", views.bannerListView.as_view(), name="portal_banner_list"),
    path('index_istilah/', views.index_istilah_lelang, name='istilah_lelang'),
    path('get_pengumuman/', views.get_pengumuman, name='p_umum'),
    path('get_pengumuman2/', views.get_pengumuman2, name='p_umum'),
    path('get_pengumuman3/', views.get_pengumuman3, name='p_umum'),
    path('get_profile/', views.get_profile, name='profil'),

    path("portal/profil/update/<int:pk>/", views.profilUpdateView.as_view(), name="portal_banner_update"),
    path("portal/istilah_lelang/update/<int:pk>/", views.istilahUpdateView.as_view(), name="portal_istilah_lelang_update"),
    path("banner/create/", views.bannerCreateView.as_view(), name="portal_banner_create"),
    path("banner/detail/<int:pk>/", views.bannerDetailView.as_view(), name="portal_banner_detail"),
    path("portal/banner/update/<int:pk>/", views.bannerslideUpdateView.as_view(), name="portal_banner_update"),
    path("portal/banner/delete/<int:pk>/", views.bannerDeleteView.as_view(), name="portal_banner_delete"),
    # notice penting
    path("portal/notice_lelang/", views.notice_lelangListView.as_view(), name="portal_notice_lelang_list"),
    path("portal/notice_lelang/create/", views.notice_lelangCreateView.as_view(), name="portal_notice_lelang_create"),
    path("portal/notice_lelang/detail/<int:pk>/", views.notice_lelangDetailView.as_view(), name="portal_notice_lelang_detail"),
    path("portal/notice_lelang/update/<int:pk>/", views.notice_lelangUpdateView.as_view(), name="portal_notice_lelang_update"),
    path("portal/notice_lelang/delete/<int:pk>/", views.notice_lelangDeleteView.as_view(), name="portal_notice_lelang_delete"),
    # aturan
    path("portal/aturan_lelang/", views.aturan_lelangListView.as_view(), name="portal_aturan_lelang_list"),
    path("portal/aturan_lelang/create/", views.aturan_lelangCreateView.as_view(), name="portal_aturan_lelang_create"),
    path("portal/aturan_lelang/detail/<int:pk>/", views.aturan_lelangDetailView.as_view(), name="portal_aturan_lelang_detail"),
    path("portal/aturan_lelang/update/<int:pk>/", views.aturan_lelangUpdateView.as_view(), name="portal_aturan_lelang_update"),
    path("portal/aturan_lelang/delete/<int:pk>/", views.aturan_lelangDeleteView.as_view(), name="portal_aturan_lelang_delete"),
    # history
    path("portal/history_lelang/", views.history_lelangListView.as_view(), name="portal_history_lelang_list"),
    path("portal/history_lelang/create/", views.history_lelangCreateView.as_view(), name="portal_history_lelang_create"),
    path("portal/history_lelang/detail/<int:pk>/", views.history_lelangDetailView.as_view(), name="portal_history_lelang_detail"),
    path("portal/history_lelang/update/<int:pk>/", views.history_lelangUpdateView.as_view(), name="portal_history_lelang_update"),
    path("portal/history_lelang/delete/<int:pk>/", views.history_lelangDeleteView.as_view(), name="portal_history_lelang_delete"),
    # blok
    path("portal/portal_block/", views.portal_blockListView.as_view(), name="portal_portal_block_list"),
    path("portal/portal_block_table/", views.portal_blockTableView.as_view(), name="portal_portal_block_list"),
    path("portal/portal_block/create/", views.portal_blockCreateView.as_view(), name="portal_portal_block_create"),
    path("portal/portal_block/detail/<int:pk>/", views.portal_blockDetailView.as_view(), name="portal_portal_block_detail"),
    path("portal/portal_block/update/<int:pk>/", views.portal_blockUpdateView.as_view(), name="portal_portal_block_update"),
    path("portal/portal_block/delete/<int:pk>/", views.portal_blockDeleteView.as_view(), name="portal_portal_block_delete"),
    # manca
    path("portal/lelang_mancanegara/", views.lelang_mancanegaraListView.as_view(), name="portal_lelang_mancanegara_list"),
    path("portal/lelang_mancanegara/create/", views.lelang_mancanegaraCreateView.as_view(), name="portal_lelang_mancanegara_create"),
    path("portal/lelang_mancanegara/detail/<int:pk>/", views.lelang_mancanegaraDetailView.as_view(), name="portal_lelang_mancanegara_detail"),
    path("portal/lelang_mancanegara/update/<int:pk>/", views.lelangmancaUpdateView.as_view(), name="portal_lelang_mancanegara_update"),
    path("portal/lelang_mancanegara/delete/<int:pk>/", views.lelang_mancanegaraDeleteView.as_view(), name="portal_lelang_mancanegara_delete"),
    # istilah
    path("portal/istilah_lelang/", views.istilah_lelangListView.as_view(), name="portal_istilah_lelang_list"),
    path("portal/istilah_lelang/create/", views.IstilahTambahView.as_view(), name="portal_istilah_lelang_create"),
    path("portal/istilah_lelang/detail/<int:pk>/", views.istilah_lelangDetailView.as_view(), name="portal_istilah_lelang_detail"),
    path("portal/istilah_lelang/delete/<int:pk>/", views.istilah_lelangDeleteView.as_view(), name="portal_istilah_lelang_delete"),

    # tabel
    path("portal/istilah_lelang_table/", views.istilah_lelangTableView.as_view(), name="portal_istilah_lelang_list"),
    path("portal/histori_lelangtable/", views.histori_lelangTableView.as_view(), name="portal_histori_lelang_list"),
    path("portal/lelang_manca_table/", views.lelang_mancaTableView.as_view(), name="portal_lelang_manca_list"),
    path("portal/aturan_lelang_table/", views.aturan_lelangTableView.as_view(), name="portal_aturan_lelang_list"),
    path("portal/banner_table/", views.BannerTableView.as_view(), name="banner_slide"),
    path("portal/profil/", views.ProfilTableView.as_view()),
)