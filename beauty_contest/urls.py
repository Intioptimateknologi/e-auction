from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("parameter_evaluasi", api.parameter_evaluasiViewSet)
router.register("dokumen_bc", api.dokumen_bcViewSet)
router.register("format_dokumen_bc", api.format_dokumen_bcViewSet)
router.register("input_penilaian", api.input_penilaian_bcViewSet)
router.register("sum_penilaian", api.sum_penilaianViewSet)
router.register("obyek_seleksi", api.obyek_seleksiViewSet)
router.register("hasil", api.hasil_bcViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("management/", views.home),
    path("penawaran/", views.penawaran),
    path("penilaian/", views.penilaian),

    path("beauty_contest/parameter_evaluasi/<int:pk>/", views.kriteria_evaluasiListView.as_view(), name="kriteria_evaluasiListView"),
    path("beauty_contest/parameter_evaluasi_group/<int:pk>/", views.kriteria_evaluasibcGroupView.as_view(), name="kriteria_evaluasiListView"),
    path("beauty_contest/dokumen_bc/<int:pk>/", views.dokumen_bcListView.as_view(), name="dokumen_bcListView"),
    path("beauty_contest/dokumen_bc2/<int:pk>/", views.dokumen_bcListView2.as_view(), name="beauty_contest_dokumen_bc_list2"),
    path("beauty_contest/input_penilaian_bc/<int:pk>/", views.input_penilaianListView.as_view(), name="input_penilaianListView"),
    path("beauty_contest/input_penilaian_bc2/<int:pk>/", views.input_penilaianListView2.as_view(), name="input_penilaianListView2"),
    path("beauty_contest/sum_penilaian/<int:pk>/", views.sum_penilaianListView2.as_view(), name="input_penilaianListView2"),
    path("beauty_contest/sum_penilaian2/<int:pk>/<int:code>/", views.sum_penilaianListView.as_view(), name="input_penilaianListView"),
    # path("beauty_contest/kirim_undangan/<int:pk>/", views.kirim_undangan_bcListView.as_view(), name="kirim_undanganListView"),
    path("obyek_seleksi/<int:pk>/", views.obyek_seleksibcView.as_view()),
    path("obyek_seleksi_group/<int:pk>/", views.obyek_seleksibcGroupView.as_view()),
    path("obyek_seleksi_form/<int:pk>/", views.obyek_seleksibcCreateView.as_view()),
    path("obyek_seleksi_update/<int:pk>/", views.obyek_seleksibcUpdateView.as_view()),
    path("penilaian_group/<int:pk>/", views.input_penilaianGroupView.as_view()),
    path("hasil_bc/<int:pk>/", views.hasilListView.as_view()),

    path("beauty_contest/dokumenpersyaratan/<int:pk>/", views.dokumen_persyaratanListView.as_view(), name="dokumen_persyaratanListView"),
    path("beauty_contest/dokumenpersyaratan2/<int:pk>/", views.dokumen_persyaratanListView2.as_view(), name="beauty_contest_dokumen_persyaratan_list2"),
    path("beauty_contest/daftarbuktipeersyaratan/<int:pk>/", views.dokumen_persyaratanListView3.as_view(), name="beauty_contest_dokumen_persyaratan_list3"),
    # modal
    path("beauty_contest/modal_parameter_evaluasi/<int:pk>/", views.parameterevaluasiCreateView.as_view(), name="beauty_contest_modal_parameter_evaluasi"),
    path("beauty_contest/modal_dokumen_bc/<int:pk>/", views.dokumenbcCreateView.as_view(), name="beauty_contest_modal_dokumenbc"),
    path("beauty_contest/modal_dokumenpersyaratan/<int:pk>/", views.dokumenpersyaratanCreateView.as_view(), name="beauty_contest_modal_persyaratan"),
    path("beauty_contest/modal_penilaian_bc/<int:pk>/", views.penilaianbcreateView.as_view(), name="beauty_contest_modal_penilaianbc"),
    #update
    path("beauty_contest/modal_update_parameter_evaluasi/<int:pk>/", views.parameterevaluasiUpdateView.as_view(), name="beauty_contest_modal_update_parameter_evaluasi"),
    path("beauty_contest/modal_update_dokumen_bc/<int:pk>/", views.dokumenbcUpdateView.as_view(), name="beauty_contest_modal_update_dokumenbc"),
    path("beauty_contest/modal_update_dokumenpersyaratan/<int:pk>/", views.dokumenpersyaratanUpdateView.as_view(), name="beauty_contest_modal_update_dokumenbc"),
    path("beauty_contest/modal_update_penilaian_bc/<int:pk>/", views.penilaianbUpdateView.as_view(), name="beauty_contest_modal_update_penilaianbc"),
    
#    path("beauty_contest/parameter_evaluasi/", views.parameter_evaluasiListView.as_view(), name="beauty_contest_parameter_evaluasi_list"),
#    path("beauty_contest/parameter_evaluasi/create/", views.parameter_evaluasiCreateView.as_view(), name="beauty_contest_parameter_evaluasi_create"),
#    path("beauty_contest/parameter_evaluasi/detail/<int:pk>/", views.parameter_evaluasiDetailView.as_view(), name="beauty_contest_parameter_evaluasi_detail"),
#    path("beauty_contest/parameter_evaluasi/update/<int:pk>/", views.parameter_evaluasiUpdateView.as_view(), name="beauty_contest_parameter_evaluasi_update"),
#    path("beauty_contest/parameter_evaluasi/delete/<int:pk>/", views.parameter_evaluasiDeleteView.as_view(), name="beauty_contest_parameter_evaluasi_delete"),
#    path("beauty_contest/dokumen_bc/", views.dokumen_bcListView.as_view(), name="beauty_contest_dokumen_bc_list"),
#    path("beauty_contest/dokumen_bc/create/", views.dokumen_bcCreateView.as_view(), name="beauty_contest_dokumen_bc_create"),
#    path("beauty_contest/dokumen_bc/detail/<int:pk>/", views.dokumen_bcDetailView.as_view(), name="beauty_contest_dokumen_bc_detail"),
#    path("beauty_contest/dokumen_bc/update/<int:pk>/", views.dokumen_bcUpdateView.as_view(), name="beauty_contest_dokumen_bc_update"),
#    path("beauty_contest/dokumen_bc/delete/<int:pk>/", views.dokumen_bcDeleteView.as_view(), name="beauty_contest_dokumen_bc_delete"),
    
)