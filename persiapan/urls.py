from django.urls import path, include
from rest_framework import routers
from . import api
from . import views

router = routers.DefaultRouter()
router.register("persiapan_dokumen", api.p_dokumenViewSet)
router.register("penyusunan_jawaban", api.penyusunan_jawabanViewSet)
router.register("aanwizing", api.aanwizingViewSet)
router.register("simulasi", api.simulasiViewSet)
router.register("addendum", api.p_addendumViewSet)
router.register("dokumen_seleksi", api.dokumen_seleksiViewSet)
router.register("pengambilan_dokumen_seleksi", api.pengambilan_dokumen_seleksiViewSet)
router.register("penyampaian_pertanyaan", api.p_pertanyaanViewSet)
router.register("berita_acara_persiapan", api.berita_acara_persiapanViewSet)
router.register("pengambilan_addendum", api.pengambilan_dokumen_addendumViewSet)
router.register("daftar_hadir", api.daftar_hadirViewSet)
urlpatterns = (
#    path("api/v1/", include(router.urls)),
    path("api/v1/", include(router.urls)),
    path("pembukaan/", views.pembukaan),
    #path("pembukaan/", views.pembukaan2),
    path("dokumen_seleksi/", views.dokumen_seleksi),
    path("pertanyaan/", views.pertanyaan),
    path("aanwizing/", views.aanwizing_doksel),
    path("simulasi/", views.simulasi),
    path("addendum_doksel/", views.addendum),
    path("get_tabs/", views.get_tabs),

    # buat tempaltetags
    path("modal_update_undangan/<int:pk>/<int:item_lelang>/", views.modalUpdateUndangan.as_view()),
    path("modal_create_undangan/<int:pk>/<int:tahapan>/", views.modalCreateUndangan.as_view()),
    path("undangan_auctioner/<int:item_lelang>/<int:current_step>/<int:auctioner>/", views.undanganAuctionerListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    path("undangan_bidder/<int:item_lelang>/<int:current_step>/<int:bidder>/", views.undanganBidderListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    
    path("modal_update_ba/<int:pk>/<int:item_lelang>/", views.modalUpdateBA.as_view()),
    path("modal_create_ba/<int:pk>/<int:tahapan>/", views.modalCreateBA.as_view()),
    path("ba_auctioner/<int:item_lelang>/<int:current_step>/<int:auctioner>/", views.BAAuctionerListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    path("ba_bidder/<int:item_lelang>/<int:current_step>/<int:bidder>/", views.BABidderListView.as_view(), name="persiapan_pengambilan_dokumen_list"),

    # table crud
    path("persiapan/pengambilan_doksel/<int:pk>/", views.pengambilan_dokselListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    path("persiapan/pengambilan_doksel2/<int:pk>/", views.pengambilan_doksel2ListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    path("persiapan/pengambilan_dokumen/<int:pk>/", views.p_dokumenListView.as_view(), name="persiapan_pengambilan_dokumen_list"),
    path("persiapan/penyusunan_jawaban/<int:pk>/", views.penyusunan_jawabanListView.as_view(), name="persiapan_penyusunan_jawaban_list"),
    path("persiapan/aanwizing/<int:pk>/", views.aanwizingListView.as_view(), name="persiapan_aanwizing_list"),
    path("persiapan/simulasi/<int:pk>/", views.simulasiListView.as_view(), name="persiapan_simulasi_list"),
    path("persiapan/p_addendum/<int:pk>/", views.p_addendumListView.as_view(), name="persiapan_p_addendum_list"),
    path("persiapan/p_dokumen_seleksi/<int:pk>/", views.p_dokumen_seleksiListView.as_view(), name="persiapan_p_dokumen_seleksi_list"),
    path("persiapan/p_pertanyaan/<int:pk>/", views.p_pertanyaanListView.as_view(), name="persiapan_p_pertanyaan_list"),
    path("persiapan/p_pertanyaanv/<int:pk>/", views.p_pertanyaanvListView.as_view(), name="persiapan_p_pertanyaan_list"),
    path("persiapan/ba_persiapan/<int:pk>/<str:code>/", views.berita_acara_persiapanListView.as_view(), name="persiapan_ba_persiapan_list"),
    path("persiapan/ba_persiapan_simulasi/<int:pk>/", views.berita_acara_persiapan_simulasiListView.as_view(), name="berita_acara_persiapan_simulasiList"),
    path("persiapan/pengambilan_addendum/<int:pk>/", views.pengambilan_addendumListView.as_view(), name="persiapan_pengambilan_dokumen_list"),

    path("persiapan/lihat_ba_doksel/<int:pk>/", views.PdfsView.as_view(), name="PdfsView"),
    path("persiapan/pengambilan_addendum_pdf/<int:pk>/", views.PdfsView_addendum.as_view(), name="PdfsView"),
    path("persiapan/download_ba_doksel/<int:pk>/", views.docxview, name="DocxView"),
    # daftar_hadir
    path("persiapan/daftar_hadir/<int:tahapan>/<int:pk>/", views.daftar_hadirListView.as_view(), name="daftar_hadirListView"),
    path("persiapan/daftar_hadir2/<int:tahapan>/<int:pk>/", views.daftar_hadirListView2.as_view(), name="daftar_hadirListView"),
    
    # table list data saja
    path("persiapan/pengambilan_dokumen2/<int:pk>/<int:code>/", views.p_dokumenList2View.as_view(), name="persiapan_pengambilan_dokumen_list2"),
        #dibawah ini yang auctioneer
    path("persiapan/pengambilan_dokumen3/<int:pk>/<str:auctioneer>/", views.p_dokumenListauctioneer2View.as_view(), name="persiapan_pengambilan_dokumen_list2"),
    
    path("persiapan/penyusunan_jawaban2/<int:pk>/", views.penyusunan_jawaban2ListView.as_view(), name="persiapan_penyusunan_jawaban_list2"),
        #dibawah ini yang auctioneer
    path("persiapan/penyusunan_jawaban3/<int:pk>/<int:code>/", views.penyusunan_jawaban3ListView.as_view(), name="persiapan_penyusunan_jawaban_list_auctioneer2"),
   
    path("persiapan/aanwizing2/<int:pk>/<int:code>/", views.aanwizing2ListView.as_view(), name="persiapan_aanwizing_list2"),
        #dibawah ini yang auctioneer
    path("persiapan/aanwizing3/<int:pk>/<int:code>/", views.aanwizing3ListView.as_view(), name="persiapan_aanwizing_list2"),
    
    path("persiapan/simulasi2/<int:pk>/<int:code>/", views.simulasi2ListView.as_view(), name="persiapan_simulasi_list2"),
    path("persiapan/simulasi3/<int:pk>/<int:code>/", views.simulasi3ListView.as_view(), name="persiapan_simulasi_list3"),
    
    path("persiapan/p_addendum2/<int:pk>/", views.p_addendum2ListView.as_view(), name="persiapan_p_addendum_list2"),
     #dibawah ini pengambilan addendum yang auctioneer
    path("persiapan/p_addendumauctioneer2/<int:pk>/<int:code>/", views.p_addendumauctioneer2ListView.as_view(), name="persiapan_p_addendum_list_auctioneer2"),
    
    path("persiapan/p_dokumen_seleksi2/<int:pk>/", views.p_dokumen_seleksi2ListView.as_view(), name="persiapan_p_dokumen_seleksi_list2"),
    path("persiapan/p_pertanyaan2/<int:pk>/", views.p_pertanyaan2ListView.as_view(), name="persiapan_p_pertanyaan_list2"),
    path("persiapan/ba_persiapan2/<int:pk>/", views.berita_acara_persiapan2ListView.as_view(), name="persiapan_ba_persiapan_list2"),
    path("persiapan/ba_persiapan_auc/<int:pk>/", views.berita_acara_persiapan2ListAuctioneerView.as_view(), name="berita_acara_persiapan2ListAuctioneerView"),
        #dibawah ini berita acara persiapan addendum yang bidder 
    path("persiapan/ba_persiapanaddendum2/<int:pk>/<str:code>/<str:bidder>/", views.berita_acara_persiapanaddendumbidder2ListView.as_view(), name="persiapan_ba_persiapan_listbidder2"),
        #dibawah ini berita acara persiapan addendum yang auctioneer
    path("persiapan/ba_persiapanaddendum3/<int:pk>/<str:code>/<str:auctioneer>/", views.berita_acara_persiapanaddendumauctioneer2ListView.as_view(), name="persiapan_ba_persiapan_listauctioneer2"),

    # lainnya
    path("persiapan/p_dokumen_seleksi3/<int:pk>/<int:code>/", views.p_dokumen_seleksi3ListView.as_view(), name="persiapan_p_dokumen_seleksi_list3"),
    path("persiapan/p_pertanyaan3/<int:pk>/", views.p_pertanyaan3ListView.as_view(), name="persiapan_p_pertanyaan_list3"),

    #modal
    path("persiapan/modal_p_pdokumen/<int:pk>/", views.p_dokumenCreateView.as_view(), name="p_dokumenCreateView"),
    path("persiapan/modal_penyusunan_jawaban/<int:pk>/", views.penyusunan_jawabanCreateView.as_view(), name="penyusunan_jawabanCreateView"),
    path("persiapan/modal_p_aanwizing/<int:pk>/", views.aanwizingCreateView.as_view(), name="aanwizingCreateView"),
    path("persiapan/modal_p_simulasi/<int:pk>/", views.simulasiCreateView.as_view(), name="simulasiCreateView"),
    path("persiapan/modal_p_addendum/<int:pk>/", views.p_addendumCreateView.as_view(), name="p_addendumCreateView"),
    path("persiapan/modal_p_dokumen_seleksi/<int:pk>/", views.p_dokumen_seleksiCreateView.as_view(), name="p_dokumen_seleksiCreateView"),
    path("persiapan/modal_p_pertanyaan/<int:pk>/", views.p_pertanyaanCreateView.as_view(), name="p_pertanyaanCreateView"),
    path("persiapan/modal_berita_acara_dokumen/<int:pk>/", views.berita_acara_dokumen_seleksiCreateView.as_view(), name="berita_acara_dokumen_seleksiCreateView"),
    path("persiapan/modal_berita_acara_simulasi/<int:pk>/", views.berita_acara_simulasiCreateView.as_view(), name="berita_acara_simulasiCreateView"),
    path("persiapan/modal_berita_acara_pertanyaan/<int:pk>/", views.berita_acara_pertanyaanCreateView.as_view(), name="berita_acara_pertanyaanCreateView"),
    path("persiapan/modal_berita_acara_addendum/<int:pk>/", views.berita_acara_addendumCreateView.as_view(), name="berita_acara_addendumCreateView"),
    path("persiapan/modal_berita_acara_aanwizing/<int:pk>/", views.berita_acara_aanwizingCreateView.as_view(), name="berita_acara_aanwizingCreateView"),
    path("persiapan/modal_daftar_hadir/<int:tahapan>/<int:pk>/", views.daftar_hadirCreateView.as_view(), name="daftar_hadirCreateView"),
    path("persiapan/pengambilan_dokumen_seleksi/<int:dokumen>/", views.pengambilan_dokumen_seleksiView.as_view(), name="pengambilan_dokumen_seleksiView"),
    path("persiapan/pengambilan_dokumen_addendum/<int:dokumen>/", views.pengambilan_dokumen_addendumView.as_view(), name="pengambilan_dokumen_seleksiView"),
    
    # Update
    path("persiapan/modal_update_p_pdokumen/<int:pk>/<int:id>/", views.p_dokumenUpdateView.as_view(), name="p_dokumenUpdateView"),
    path("persiapan/modal_update_penyusunan_jawaban/<int:pk>/<int:id>/", views.penyusunan_jawabanUpdateView.as_view(), name="penyusunan_jawabanUpdateView"),
    path("persiapan/modal_update_p_aanwizing/<int:pk>/<int:id>/", views.aanwizingUpdateView.as_view(), name="aanwizingUpdateView"),
    path("persiapan/modal_update_p_simulasi/<int:pk>/<int:id>/", views.simulasiUpdateView.as_view(), name="simulasiUpdateView"),
    path("persiapan/modal_update_p_addendum/<int:pk>/", views.p_addendumUpdateView.as_view(), name="p_addendumUpdateView"),
    path("persiapan/modal_update_p_dokumen_seleksi/<int:pk>/", views.p_dokumen_seleksiUpdateView.as_view(), name="p_dokumen_seleksiUpdateView"),
    path("persiapan/modal_update_p_pertanyaan/<int:pk>/", views.p_pertanyaanUpdateView.as_view(), name="p_pertanyaanUpdateView"),
    path("persiapan/modal_update_berita_acara_dokumen/<int:pk>/<int:id>/", views.berita_acara_dokumen_seleksiUpdateView.as_view(), name="berita_acara_dokumen_seleksiUpdateView"),
    path("persiapan/modal_update_berita_acara_simulasi/<int:pk>/<int:id>/", views.berita_acara_simulasiUpdateView.as_view(), name="berita_acara_dokumen_seleksiUpdateView"),
    path("persiapan/modal_update_berita_acara_pertanyaan/<int:pk>/<int:id>/", views.berita_acara_pertanyaanUpdateView.as_view(), name="berita_acara_dokumen_seleksiUpdateView"),
    path("persiapan/modal_update_berita_acara_addendum/<int:pk>/<int:id>/", views.berita_acara_addendumUpdateView.as_view(), name="berita_acara_dokumen_seleksiUpdateView"),
    path("persiapan/modal_update_berita_acara_aanwizing/<int:pk>/<int:id>/", views.berita_acara_aanwizingUpdateView.as_view(), name="berita_acara_dokumen_seleksiUpdateView"),
    path("persiapan/modal_update_daftar_hadir/<int:tahapan>/<int:pk>/", views.daftar_hadirUpdatedView.as_view(), name="modalUpdateUndangan"),

    path("api/api_check_addendum/<pk>/", views.api_check_addendum, name="api_delete_users_menugroup"),
)