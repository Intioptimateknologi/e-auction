
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import PasswordChangeForm as AuthPasswordChangeForm

class SendInBluePasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email` using
        `anymail.backends.postmark.EmailBackend`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        print("MASUK SINI")
        body = loader.render_to_string(email_template_name, context)

        email_backend = get_connection('anymail.backends.sendinblue.EmailBackend')

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email], connection=email_backend)
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

class PasswordChangeForm(AuthPasswordChangeForm):
    pass  # You can customize this form further if needed
# from django import forms
# from . import models

# class penyampaian_penawaranForm(forms.ModelForm):
#     class Meta:
#         model = models.penyampaian_penawaran
#         fields = [
#             "dokumen_penawaran",
#             "harga",
#             "bidder",
#             "penawaran",
#             "item_lelang",
#         ]


# class berita_acara_negoForm(forms.ModelForm):
#     class Meta:
#         model = models.berita_acara_nego
#         fields = [
#             "dokumen_ba",
#             "item_lelang",
#         ]