from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from . import forms
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import PasswordChangeView
import django_eventstream
from mfa.views import LoginView

urlpatterns = [
    path('', views.home, name='index'),
    #page accounts
#    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('accounts/ganti_password/', auth_views.PasswordChangeView.as_view(template_name='ganti_password_akun.html',success_url='/ganti_password/done/'), name='Ganti Password Akun'),
    path('change_password/', views.change_password, name='change_password'),
    path('user_details/', views.user_details, name='user_details'),
    path('ganti_password/done/', TemplateView.as_view(template_name="ganti_password_done.html"), name="ganti_password_akun_berhasil"),

    path('password_reset/', views.password_reset_request),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/otp/', TemplateView.as_view(template_name='password_reset_otp.html'), name='password_reset_otp'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    #registrasi
    path("registrasi/users/", views.register_users, name='registrasi_users'),
    path('registrasi/admin/', views.registrasi_admin, name='registrasi_admin'),
    path('registrasi/bidder/', views.registrasi_perusahaan, name='registrasi_perusahaan'),
    path('registrasi/auctioneer/', views.registrasi_auctioneer, name='registrasi_auctioneer'),
    path('registrasi/viewrs/', views.registrasi_viewrs, name='registrasi_viewrs'),
    path('registrasi/hak_akses/', views.registrasi_hak_akses, name='registrasi_hak_akses'),
    path('registrasi/judul/', views.registrasi_judul, name='registrasi_judul'),

    #setting_portal
    path('setting_portal/index_setting_portal/', views.index_setting_portal, name='index_setting_portal'),
    path('setting_portal/banner_slide/', views.banner_slide, name='banner_slide'),
    path('setting_portal/history_lelang/', views.history_lelang, name='history_lelang'),
    path('setting_portal/istilah_lelang/', views.istilah_lelang, name='istilah_lelang'),
    path('setting_portal/aturan_lelang/', views.aturan_lelang, name='aturan_lelang'),
    path('setting_portal/informasi_lelang/', views.informasi_lelang, name='informasi_lelang'),


    #rencana_seleksi
    path('rencana_seleksi/index_rencana/', views.index_rencana, name='index_rencana'),
    path('rencana_seleksi/index_rencana/rencana_seleksi/delete/<int:id>', views.deleterencanaseleksi, name='deleterencanaseleksi'),
    path('rencana_seleksi/index_rencana/rencana_seleksi/edit/<int:id>', views.editrencanaseleksi, name='editrencanaseleksi'),
    path('rencana_seleksi/objek_seleksi/', views.objek_seleksi, name='objek_seleksi'),
    path('rencana_seleksi/penanggung_jawab/', views.penanggung_jawab, name='penanggung_jawab'),
    path('rencana_seleksi/alamat/', views.alamat, name='alamat'),
    path('rencana_seleksi/persyaratan/', views.persyaratan, name='persyaratan'),
    path('rencana_seleksi/jadwal/', views.jadwal, name='jadwal'),
    path('rencana_seleksi/kegiatan/', views.kegiatan, name='kegiatan'),
    path('rencana_seleksi/edit_rencana/', views.edit_rencana, name='edit_rencana'),
    #portal
    path('portal_user/', TemplateView.as_view(template_name='new_index/konten/portal_user/portal_user.html'), name='portal'),
    path('profile/', views.profile, name='profile'),
    path('dasar_hukum/', views.dasar_hukum, name='dasar_hukum'),
    path('istilah_lelang/', views.istilah_lelang, name='istilah_lelang'),
    path('pengumuman/', views.pengumuman, name='pengumuman'),
    path('history_lelang/', views.history_lelang, name='history_lelang'),
    path('benchmark/', views.benchmark, name='benchmark'),
    path('indes', TemplateView.as_view(template_name='new_index/base1.html'), name='indes'),
    path('ganti-password/', PasswordChangeView.as_view(), name='ganti_password'),
    path('invalid-captcha/', views.invalid_captcha, name='invalid_captcha'),
    path('invalid-credentials/', views.invalid_credentials, name='invalid_credentials'),
    path('masa-berlaku/', views.masa_berlaku, name='masa_berlaku'),

    path('secure_media/<path:file_path>', views.protected_media, name='media_protected'),

    #page accounts
    path('userman/', include('userman.urls')),
    #path('gabungan/', include('gabungan.urls')),
    path('beauty_contest/', include('beauty_contest.urls')),
    path('adm_lelang/', include('adm_lelang.urls')),
    path('negosiasi/', include('negosiasi.urls')),
    path('portal/', include('portal.urls')),
    #path('cca/', include('cca.urls')),
    path('smra2/', include('smra2.urls')),
    #path('smra/', include('smra.urls')),
    path('persiapan/', include('persiapan.urls')),
    path('administrasi/', include('administrasi.urls')),
    path('pasca_seleksi/', include('pasca_seleksi.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('system/', include('sysmon.urls')),
    path("events/<channel>/", include(django_eventstream.urls)),
    path("prose/", include("prose.urls")),
    path('mfa/', include('mfa.urls', namespace='mfa')),
    path('brevohook/', views.brevo_webhook, name='benchmark')
    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


