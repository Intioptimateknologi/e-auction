from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth import logout

class MFAEnforceMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            user = request.user
            maber1 = user.masaberlaku1
            maber2 = user.masaberlaku2
            today = now().date()

            if (maber1 > today) or (maber2 < today):
            # Suspend account (set inactive)
                user.is_active = False
                user.save()

            # Force logout with a message
                messages.error(request, "Akun sudah nonaktif. Hubungi Administrator.")
                logout(request)
                return redirect('/masa-berlaku/')
        if (
            not getattr(view_func, 'mfa_public', False)
            and request.user.is_authenticated
            and not request.user.mfakey_set.exists()
        ):
            return redirect('mfa:list')