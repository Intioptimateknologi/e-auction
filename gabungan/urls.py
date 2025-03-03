from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("penentuan_parameter", api.penentuan_parameterViewSet)
router.register("ba_gabungan", api.ba_gabunganViewSet)
router.register("penilaian_gabungan", api.penilaian_gabunganViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("management/", views.home),
    path("penilaian/",views.penilaian ),
    # modal
    path("gabungan/modal_ba_gabungan/<int:pk>/", views.bagabunganCreateView.as_view(), name="gabungan_modal_ba_gabungan"),
    path("gabungan/modal_p_gabungan/<int:pk>/", views.pgabunganCreateView.as_view(), name="gabungan_modal_p_gabungan"),
    path("gabungan/modal_p_parameter/<int:pk>/", views.pparameterCreateView.as_view(), name="gabungan_modal_p_parameter"),
    path("gabungan/modal_undangan/<int:pk>/", views.undangan_gabunganCreateView.as_view(), name="gabungan_modal_p_parameter"),
    #update
    path("gabungan/modal_update_ba_gabungan/<int:pk>/<int:id>/", views.bagabunganUpdateView.as_view(), name="gabungan_modal_update_ba_gabungan"),
    path("gabungan/modal_update_p_gabungan/<int:id>/", views.pgabunganUpdateView.as_view(), name="gabungan_modal_update_p_gabungan"),
    path("gabungan/modal_update_p_parameter/<int:pk>/", views.pparameterUpdateView.as_view(), name="gabungan_modal_update_p_parameter"),
    path("gabungan/modal_update_undangan/<int:pk>/<int:id>/", views.undangan_gabunganUpdateView.as_view(), name="gabungan_modal_update_p_parameter"),
    

#    path("gabungan/sum_gabungan/<int:pk>/", views.sum_gabunganListView.as_view(), name="gabungan_penentuan_parameter_list"),
#    path("gabungan/sum_gabungan/<int:pk>/<int:code>/", views.sum_gabungan2ListView.as_view(), name="gabungan_penentuan_parameter_list"),
    path("gabungan/penentuan_parameter/<int:pk>/", views.penentuan_parameterListView.as_view(), name="gabungan_penentuan_parameter_list"),
    path("gabungan/penentuan_parameter/create/", views.penentuan_parameterCreateView.as_view(), name="gabungan_penentuan_parameter_create"),
    path("gabungan/penentuan_parameter/detail/<int:pk>/", views.penentuan_parameterDetailView.as_view(), name="gabungan_penentuan_parameter_detail"),
    path("gabungan/penentuan_parameter/update/<int:pk>/", views.penentuan_parameterUpdateView.as_view(), name="gabungan_penentuan_parameter_update"),
    path("gabungan/penentuan_parameter/delete/<int:pk>/", views.penentuan_parameterDeleteView.as_view(), name="gabungan_penentuan_parameter_delete"),
    path("gabungan/ba_gabungan/<int:pk>/", views.ba_gabunganListView.as_view(), name="gabungan_ba_gabungan_list"),
    path("gabungan/ba_gabungan2/<int:pk>/", views.ba_gabunganList2View.as_view(), name="gabungan_ba_gabungan_list"),
    path("gabungan/ba_gabungan/create/", views.ba_gabunganCreateView.as_view(), name="gabungan_ba_gabungan_create"),
    path("gabungan/ba_gabungan/detail/<int:pk>/", views.ba_gabunganDetailView.as_view(), name="gabungan_ba_gabungan_detail"),
    path("gabungan/ba_gabungan/update/<int:pk>/", views.ba_gabunganUpdateView.as_view(), name="gabungan_ba_gabungan_update"),
    path("gabungan/ba_gabungan/delete/<int:pk>/", views.ba_gabunganDeleteView.as_view(), name="gabungan_ba_gabungan_delete"),
    path("gabungan/nilai_gabungan/<int:pk>/", views.penilaian_gabunganListView.as_view(), name="gabungan_penilaian_gabungan_list"),
    path("gabungan/nilai_gabungan/create/", views.penilaian_gabunganCreateView.as_view(), name="gabungan_penilaian_gabungan_create"),
    path("gabungan/nilai_gabungan/detail/<int:pk>/", views.penilaian_gabunganDetailView.as_view(), name="gabungan_penilaian_gabungan_detail"),
    path("gabungan/nilai_gabungan/update/<int:pk>/", views.penilaian_gabunganUpdateView.as_view(), name="gabungan_penilaian_gabungan_update"),
    path("gabungan/nilai_gabungan/delete/<int:pk>/", views.penilaian_gabunganDeleteView.as_view(), name="gabungan_penilaian_gabungan_delete"),

    path("gabungan/hasil_gabungan/<int:pk>/", views.hasil_gabunganListView.as_view(), name="gabungan_penilaian_gabungan_list"),

)