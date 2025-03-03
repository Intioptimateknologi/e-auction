from django.urls import path, include
from rest_framework import routers

from . import api
from . import views
from . import htmx

router = routers.DefaultRouter()
router.register("dokumen_perusahaan", api.dokumen_perusahaanViewSet, basename="dokumen_perusahaan")
router.register("Users", api.UsersViewSet, basename="Users")
router.register("UsersView", api.UsersViewViewSet, basename="UsersView")
router.register("admin2", api.admin2ViewSet, basename="admin2")
router.register("tim_lelang", api.tim_lelangViewSet, basename="tim_lelang")
router.register("admin", api.adminViewSet, basename="admin")
router.register("bidder", api.bidderViewSet, basename="bidder")
router.register("viewrs", api.viewerViewSet, basename="viewrs")
router.register("bidder_list", api.bidderlistViewSet, basename="bidder_list")
router.register("bidder_perwakilan", api.bidderperwakilanViewSet, basename="bidder_perwakilan")
router.register("usermenu", api.usermenuViewSet, basename="usermenu")
router.register("usermenu2", api.usermenu2ViewSet, basename="usermenu2")
router.register("usermenugroup", api.usermenugroupViewSet, basename="usermenugroup")
router.register("group", api.groupViewSet, basename="group")
router.register("costumgroup", api.costumgroupViewSet, basename="costumgroup")
router.register("groupmap", api.groupMapViewSet, basename="groupmap")
router.register("user", api.userViewSet, basename="user")
router.register("bidder_users", api.BidderUserViewSet, basename="bidder_users")
# dibuat untuk crud saja
router.register("bidder_users2", api.BidderUser2ViewSet, basename="bidder_users2")
router.register("crudbidderperwakilanViewSet", api.crudbidderperwakilanViewSet, basename="crudbidderperwakilanViewSet")
router.register("mfakeymonitoring", api.mfaKeyMonitoringViewSet, basename="mfakeymonitoring")
router.register("notifikasi", api.notifikasiViewSet, basename="notifikasi")

urlpatterns = (
    # path('users/', views.UserListViews.as_view(), name='users_list'),
    path("api/v1/", include(router.urls)),
    path("sidebar", views.sidebar, name="sidebar"),

    path("menuman/", views.menu_manager),
    path("tahapman/", views.tahapan_manager),
    path("menulist/", views.menuCreateView.as_view()),
    path("menulist/<int:pk>/", views.menuUpdateView.as_view()),
    path("listmodule/<int:pk>/", views.listmodule),
    path("listmoduletree/", views.listmoduletree),

    path("userman/dokumen_perusahaan/", views.dokumen_perusahaanListView.as_view(), name="userman_dokumen_perusahaan_list"),
    path("userman/dokumen_perusahaan/create/", views.dokumen_perusahaanCreateView.as_view(), name="userman_dokumen_perusahaan_create"),
    path("userman/dokumen_perusahaan/detail/<int:pk>/", views.dokumen_perusahaanDetailView.as_view(), name="userman_dokumen_perusahaan_detail"),
    path("userman/dokumen_perusahaan/update/<int:pk>/", views.dokumen_perusahaanUpdateView.as_view(), name="userman_dokumen_perusahaan_update"),
    path("userman/dokumen_perusahaan/delete/<int:pk>/", views.dokumen_perusahaanDeleteView.as_view(), name="userman_dokumen_perusahaan_delete"),
    path("userman/Users/", views.UsersListView.as_view(), name="userman_Users_list"),
    path("userman/Users/create/", views.UsersCreateView.as_view(), name="userman_Users_create"),
    path("userman/Users/detail/<int:pk>/", views.UsersDetailView.as_view(), name="userman_Users_detail"),
    path("userman/Users/update/<int:pk>/", views.UsersUpdateView.as_view(), name="userman_Users_update"),
    path("userman/Users/delete/<int:pk>/", views.UsersDeleteView.as_view(), name="userman_Users_delete"),
    path("userman/tim_lelang/", views.tim_lelangListView.as_view(), name="userman_tim_lelang_list"),
    path("userman/tim_lelang/create/", views.tim_lelangCreateView.as_view(), name="userman_tim_lelang_create"),
    path("userman/tim_lelang/detail/<int:pk>/", views.tim_lelangDetailView.as_view(), name="userman_tim_lelang_detail"),
    path("userman/tim_lelang/update/<int:pk>/", views.tim_lelangUpdateView.as_view(), name="userman_tim_lelang_update"),
    path("userman/tim_lelang/delete/<int:pk>/", views.tim_lelangDeleteView.as_view(), name="userman_tim_lelang_delete"),
    
    #register
    path("register/edit_bidder", views.edit_bidder, name="edit_bidder"),
    path("register/admin_biodata", views.admin_biodata, name="admin_biodata"),
    path("register/lihat_biodata", views.lihat_biodata, name="lihat_biodata"),
    path("register/biodata_bidder", views.biodata_bidder, name="biodata_bidder"),
    path("register/list_akun", views.edit_bidder, name="list_akun"),
    path("register/tambah_akun", views.tambah_akun, name="tambah_akun"),

    # bidder
    path("bidder_home/", views.bidder_home, name="bidder_home"),
    path("modal_users/", views.users2CreateView.as_view(), name="adm_lelang_modal_obyek_seleksi"),
    path("modal_users/<int:pk>/", views.users2UpdateView.as_view(), name="adm_update_obyek_seleksi"),
    path("modal_users_group/<int:pk>/", views.usersgroup2UpdateView.as_view(), name="adm_update_obyek_seleksi"),
    path("modal_customgroup/", views.custom_groupCreateView.as_view(), name="adm_lelang_modal_obyek_seleksi"),
    path("modal_customgroup/<int:pk>/", views.custom_groupUpdateView.as_view(), name="adm_update_obyek_seleksi"),
    path("modal_bidder/", views.bidderCreateView.as_view(), name="adm_lelang_modal_obyek_seleksi"),
    path("modal_bidder/<int:pk>/", views.bidderUpdateView.as_view(), name="adm_update_obyek_seleksi"),
    path("modal_bidder_user/", views.bidder_userCreateView.as_view(), name="adm_lelang_modal_obyek_seleksi"),
    path("modal_bidder_user/<int:pk>/", views.bidder_userUpdateView.as_view(), name="adm_update_obyek_seleksi"),
    path("list_bidder_user/", views.bidder_userListView.as_view(), name="adm_update_obyek_seleksi"),
    path("modal_bidder_perwakilan/", views.bidder_perwakilanCreateView.as_view(), name="adm_lelang_modal_obyek_seleksi"),
    path("modal_bidder_perwakilan/<int:pk>/", views.bidder_perwakilanUpdateView.as_view(), name="adm_update_obyek_seleksi"),
    path("list_bidder_perwakilan/", views.bidder_perwakilanListView.as_view(), name="adm_update_obyek_seleksi"),
    path("cetak_password/<int:pk>/", views.cetakPassword.as_view(), name="adm_update_obyek_seleksi"),
    path("modal_tahapan/", views.tahapanCreateView.as_view(), name="adm_lelang_modal_obyek_seleksi"),
    path("modal_tahapan/<int:pk>/", views.tahapanUpdateView.as_view(), name="adm_update_obyek_seleksi"),

    path("list_bidder_perwakilan2/<int:pk>/", views.bidder_perwakilan2ListView.as_view(), name="adm_update_obyek_seleksi"),
    path("modal_bidder_perwakilan2/", views.bidder_perwakilan2CreateView.as_view(), name="adm_lelang_modal_obyek_seleksi"),
    path("modal_bidder_perwakilan2/<int:pk>/", views.bidder_perwakilan2UpdateView.as_view(), name="adm_update_obyek_seleksi"),
    

    # admin
    path("modal_admin/", views.adminCreateView.as_view(), name="adminCreateView"),
    path("modal_admin/<int:pk>/", views.adminUpdateView.as_view(), name="adminUpdateView"),
    # auctioneer
    path("modal_auctioneer/", views.auctioneerCreateView.as_view(), name="auctioneerCreateView"),
    path("modal_auctioneer/<int:pk>/", views.auctioneerUpdateView.as_view(), name="auctioneerUpdateView"),
    # viewer
    path("modal_viewer/", views.viewerCreateView.as_view(), name="auctioneerCreateView"),
    path("modal_viewer/<int:pk>/", views.viewerUpdateView.as_view(), name="auctioneerUpdateView"),
    # costumgroup
    path("modal_costumgroup/", views.costumgroupCreateView.as_view(), name="auctioneerCreateView"),
    path("modal_costumgroup/<int:pk>/", views.costumgroupUpdateView.as_view(), name="auctioneerUpdateView"),

    # users
    #path("users/", views.users, name="users"),
    path("users/add/", views.users_add, name="users_add"),
    path("users/add/bidder", views.users_add_bidder, name="users_add_bidder"),
    path("users/add/bidder/add", views.users_add_bidder_add, name="users_add_bidder_add"),
    path("users/add/bidder/edit", views.users_add_bidder_edit, name="users_add_bidder_edit"),
    path("users/edit/", views.users_edit, name="users_edit"),
    
    path("users/user_lelang", views.lelang_biodata, name="lelang_biodata"),
    path("users/user_lelang_view", views.lelang_view, name="lelang_view"),
    path("users/user_lelang_edit", views.lelang_edit, name="lelang_edit"),

    path("users/user_view", views.user_view, name="user_view"),
    path("users/user_edit", views.user_edit, name="user_edit"),
    path("users/user_biodata", views.user_biodata, name="user_biodata"),
    
    # tim lelang
    path("tim_lelang/", views.tim_lelang, name="tim_lelang"),
    path("tim_lelang/add/", views.tim_lelang_add, name="tim_lelang_add"),
    path("tim_lelang/edit/", views.tim_lelang_edit, name="tim_lelang_edit"),

    # api delete
    path("api/api_delete_users/<id>/", views.api_delete_users, name="api_delete_users"),
)
