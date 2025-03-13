from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseNotFound
from userman import models 
from pprint import pprint
from portal import templates
from django.db.models import Q
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django import forms
from userman.models import Users, bidder_perwakilan, bidder_user, Notifikasi
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from  django.core.mail import BadHeaderError, send_mail
from portal.models import istilah_lelang as IstilahLelang
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView
from django.urls import reverse_lazy
from mfa import models as mfa_models
import pyotp
import json
import re
import os
import mimetypes



class UsernamePasswordResetForm(PasswordResetForm):
        username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
        class Meta:
                model = Users
                fields = ("username")

def password_reset_request(request):
    if request.method == "POST":
        domain = request.headers['Host']
        password_reset_form = UsernamePasswordResetForm(request.POST)
        if password_reset_form.is_valid():

            data = password_reset_form.cleaned_data['username']
            users = models.Users.objects.all()
            associated_users = None
            for u in users:
                if u.username == data:
                    associated_users = u
                    break
            if associated_users:
                subject = "Password Reset Requested"
                email_template_name = "new_index/password_reset_email.html"
                c = {
                "email": associated_users.email,
                'domain': domain,
                'site_name': 'Spectrum E-auction',
                "uid": urlsafe_base64_encode(force_bytes(associated_users.pk)),
                "user": associated_users,
                'token': default_token_generator.make_token(associated_users),
                'protocol': 'https',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [associated_users.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect("/password_reset/done/")
    password_reset_form = UsernamePasswordResetForm()
    return render(request=request, template_name="password_reset_form.html",
                  context={"form": password_reset_form})
    
def send_email_notification_bidder_to_admin(user):
    subject = "Notifikasi Bidder Update Password"
    email_context = {
        'bidder': user.username
    }
    
    email_template = 'email_notif_changed_password.html'
    
    email_bid = render_to_string(email_template, email_context)
    
    list_target_email = [user.email for user in Users.objects.filter(user_type='A')] + ['uat_admin@somelora.com']
    
    try:
        send_mail(subject, email_bid, settings.DEFAULT_FROM_EMAIL, list_target_email, fail_silently=False)
    except Exception as e:
        print('-> ERROR sending notification email to admin after bidder changes its password: ', e)

def home(request):
        form = PasswordChangeForm(user=request.user)
        
        if not request.user:
                return render(request, 'new_index/konten/portal_user/portal_user_viewer.html')
        
        if not request.user.is_authenticated:
                return render(request, 'new_index/konten/portal_user/portal_user.html')
            
        is_bidder = request.user.user_type == 'B'
        
        if request.user.first_login is False and request.user.is_authenticated :
                
                if request.user.masaberlaku2 <= datetime.now().date():
                        return render(request, 'change_password.html', {'form': form, 'message': "2"})
                
                if request.method == 'POST':
                        form = PasswordChangeForm(user=request.user, data=request.POST)
                        new_password = request.POST.get('new_password1')
                        
                        """ NOTIFIKASI BAHWA BIDDER SUDAH UPDATE PASSWORD KE ADMIN """
                        if is_bidder:
                            print('-> DEBUG: send_email_notification_bidder_to_admin')
                            send_email_notification_bidder_to_admin(request.user)
                        
                        if form.is_valid():
                                user = form.save()
                                user.first_login = True
                                user.pending = True
                                user.password_terlihat = new_password
                                user.save()
                                return redirect('accounts/login')
        
                # return render(request, 'change_password.html', {'form' : form})
                return render(request, 'change_password.html', {'form': form, 'message': "1"})

        return render(request, 'new_index/konten/portal_user/portal_user.html')        

def change_password(request):
        user = request.user
        pprint(user)
        return HttpResponse('Done')

"""from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def protected_media(request, file_path):
    response = HttpResponse()
    response["X-Accel-Redirect"] = f"/protected/{file_path}"  # Nginx serves the file
    return response

"""
"""
nginx 
location /media/ {
    internal;
    alias /path/to/media/;
}
"""

# invalid captcha
def invalid_captcha(request):
        return render(request, 'invalid_captcha.html')

# invalid credentials
def invalid_credentials(request):
        return render(request, 'invalid_credential.html')

# masa berlaku
def masa_berlaku(request):
        return render(request, 'masa_berlaku.html')

def protected_media(request, file_path):
    """Serve media files securely, only for authenticated users."""
    protected_folder = ['upload/files', 'upload/bidder', 'uploads']
    
    # Get the absolute file path
    absolute_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    # Check that the file is within one of the allowed folders
    if any(os.path.abspath(absolute_path).startswith(os.path.abspath(os.path.join(settings.MEDIA_ROOT, folder)))
               for folder in protected_folder):
        # check for login
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        else:
                if os.path.exists(absolute_path):
                    return FileResponse(open(absolute_path, 'rb'))
                else:
                    return HttpResponseNotFound("File not found.")
    else:
        if os.path.exists(absolute_path):
            return FileResponse(open(absolute_path, 'rb'))
        else:
            return HttpResponseNotFound("File not found.")


def extract_id_and_type(text):
    # Extract notification type
    match_type = re.search(r"Notifikasi (Undangan|Berita Acara)", text)
    notif_type = match_type.group(1) if match_type else "Unknown"
    type_mapping = {"Undangan": "U", "Berita Acara": "B"}
    notif_type_short = type_mapping.get(notif_type, "Unknown")

    # Extract ID
    match_id = re.search(r"#(\d+)", text)
    notif_id = int(match_id.group(1)) if match_id else None

    return {"id": notif_id, "type": notif_type_short}

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def brevo_webhook(request):
    value = json.loads(request.body.decode("utf-8"))
    email = value['email']
    subyek = value['subject']
    email_status = value['event']
    match = extract_id_and_type(subyek)
    if not match['id'] == None:
        id = match['id']
        notif_type = match['type']
        if notif_type=="U":
            notif = models.Notifikasi.objects.filter(email=email, id_undangan = id).update(email_status=email_status)
        if notif_type=="B":
            notif = models.Notifikasi.objects.filter(email=email, id_ba = id).update(email_status=email_status)

#     return HttpResponse('Done')
    return HttpResponse(request)
        
@login_required
def register_users(request):
        return render(request, 'new_index/konten/registrasi/registrasi_users.html')

@login_required
def registrasi_admin(request):
        return render(request, 'new_index/konten/registrasi/registrasi_admin.html')
    
@login_required
def registrasi_perusahaan(request):
        return render(request, 'new_index/konten/registrasi/registrasi_bidder.html')
    
@login_required
def registrasi_auctioneer(request):
        return render(request, 'new_index/konten/registrasi/registrasi_auctioneer.html')

@login_required
def registrasi_viewrs(request):
        return render(request, 'new_index/konten/registrasi/registrasi_viewer.html')

@login_required
def registrasi_hak_akses(request):
        return render(request, 'new_index/konten/registrasi/registrasi_hak_akses.html')

@login_required
def registrasi_judul(request):
        return render(request, 'new_index/konten/registrasi/registrasi_judul.html')
# registrasi

@login_required
def index_setting_portal(request):
        return render(request, 'new_index/konten/seting_portal/index_setting_portal.html')

@login_required
def banner_slide(request):
        return render(request, 'new_index/konten/seting_portal/banner-slide.html')

@login_required
def history_lelang(request):
        return render(request, 'new_index/konten/seting_portal/history-lelang.html')

#@login_required
#def istilah_lelang(request):
#        return render(request, 'new_index/konten/seting_portal/istilah-lelang.html')

@login_required
def aturan_lelang(request):
        return render(request, 'new_index/konten/seting_portal/aturan-lelang.html')

@login_required
def informasi_lelang(request):
        return render(request, 'new_index/konten/seting_portal/informasi-lelang.html')        

@login_required
def seleksi_dasar_hukum(request):
        return render(request, 'new_index/konten/rencana_seleksi/index_rencana_seleksi.html')       

@login_required
def objek_seleksi(request):
        return render(request, 'new_index/konten/rencana_seleksi/objek_seleksi.html')       

@login_required
def penanggung_jawab(request):
        return render(request, 'new_index/konten/rencana_seleksi/penanggung_jawab.html')

@login_required
def alamat(request):
        return render(request, 'new_index/konten/rencana_seleksi/alamat.html')    

@login_required
def persyaratan(request):
        return render(request, 'new_index/konten/rencana_seleksi/persyaratan.html')  

@login_required
def jadwal(request):
        return render(request, 'new_index/konten/rencana_seleksi/jadwal.html')  

@login_required
def reportbro(request):
        return render(request, 'new_index/reportbro.html')  

@login_required
def kegiatan(request):
        return render(request, 'new_index/konten/rencana_seleksi/kegiatan.html') 

def index_rencana(request):
    formjadwalseleksi = RencanaSeleksiForm()
   
    if request.method == 'POST':
        formjadwalseleksi = RencanaSeleksiForm(request.POST)
      
        if formjadwalseleksi.is_valid():
            formjadwalseleksi.save()
            return redirect('/rencana_seleksi/index_rencana/')
       
    jadwal_seleksis = jadwal_seleksinya.objects.all()
    rencana_seleksis = rencana_seleksinya.objects.all()
    

    context = {
        'list_jadwal': jadwal_seleksis,
        'list_rencana': rencana_seleksis,
        'form_rencana': formjadwalseleksi,
        
    }
    return render(request, 'new_index/konten/rencana_seleksi/index_rencana_seleksi.html', context)

@login_required
def editrencanaseleksi(request, id):
        getrencanaseleksi = rencana_seleksinya.objects.get(id=id)
        edit = RencanaSeleksiForm(request.POST or None, instance=getrencanaseleksi)
        if request.method == 'POST':
                if edit.is_valid():
                        edit.save()
                        return redirect('/rencana_seleksi/index_rencana/')
        context = {
        'getdata': getrencanaseleksi,
        'editrencana': edit,
        }
        return render(request, 'new_index/konten/rencana_seleksi/editrencana.html', context)

@login_required
def deleterencanaseleksi(request, id):
    jadwalseleksi = rencana_seleksinya.objects.get(id=id)
    jadwalseleksi.delete()
    return redirect('index_rencana')

@login_required
def edit_rencana(request):
        return render(request, 'new_index/konten/rencana_seleksi/edit.html') 

def profile (request):
        return render(request,'new_index/konten/portal_user/profile.html')
def dasar_hukum (request):
        return render(request,'new_index/konten/portal_user/dasar_hukum.html')
def istilah_lelang (request):
        istilah = IstilahLelang.objects.all().order_by('nama_istilah')
        #return render(request, 'new_index/konten/seting_portal/istilah-lelang.html', {'istilah': istilah})
        return render(request,'new_index/konten/portal_user/istilah_lelang.html', {'istilah': istilah})
def pengumuman (request):
        return render(request,'new_index/konten/portal_user/pengumuman.html')
def history_lelang (request):
        return render(request,'new_index/konten/portal_user/history_lelang.html')
def benchmark (request):
        return render(request,'new_index/konten/portal_user/benchmark.html')

class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'ganti_password.html'
    success_url = reverse_lazy('profile')  # Redirect after successful password change

@login_required
def user_details (request):
    qr_code = mfa_models.MFAKey.objects.all().filter(user=request.user, method='TOTP')
    if len(qr_code)>0:
        mfa_keys = mfa_models.MFAKey.objects.all().filter(user=request.user)
        totp = pyotp.TOTP(qr_code[0].secret)
        url = totp.provisioning_uri(
                request.user.username,
                issuer_name=settings.MFA_SITE_TITLE,
        )
        return render(request, 'users_detail.html', {'url': url, 'mfa_keys' : mfa_keys})
    else:
        return render(request, 'users_detail.html')
        # return redirect("/mfa/create/TOTP/")


def dapet_server_time(request):
    server_time = datetime.now().strftime("%H:%M:%S")
    return JsonResponse({'current_time': server_time})
        