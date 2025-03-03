from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from userman.models import Users, bidder_perwakilan
from django.utils.deprecation import MiddlewareMixin
from asgiref.sync import iscoroutinefunction, markcoroutinefunction, sync_to_async
from asgiref.sync import async_to_sync

class AccountEligibilityMiddleware:
    async_capable = False
    sync_capable = True

    def __init__(self, get_response):
        self.get_response = get_response
#        if iscoroutinefunction(self.get_response):
#            markcoroutinefunction(self)

    def __call__(self, request):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return self.get_response(request)

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
                return redirect('/accounts/login/')


    
# class BidderPerwakilanIpValidationMiddleware:
#     """
#     Middleware untuk memvalidasi apakah IP pengguna yang login cocok dengan IP yang ada di bidder_perwakilan.
#     Jika tidak ada kecocokan, pengguna akan dikeluarkan (logout).
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             user_ip = self.get_client_ip(request)
#             if not bidder_perwakilan.objects.filter(bidder__users=request.user, ip_address=user_ip).exists():
#                 logout(request)
#                 return redirect('/accounts/login/')

#         response = self.get_response(request)
#         return response

#     def get_client_ip(self, request):
#         """Mengambil IP pengguna dari request."""
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]  # Ambil IP pertama jika ada multiple IP
#         else:
#             ip = request.META.get('REMOTE_ADDR')  # Ambil IP dari remote address
#         return ip

# # class BidderPerwakilanIpValidationMiddleware:
# #     def __init__(self, get_response):
# #         self.get_response = get_response

# #     def __call__(self, request):
# #         # Allow access to login and logout URLs
# #         if not request.user.is_authenticated:
# #             return self.get_response(request)

# #         # Check if user is authenticated
# #         if request.user.is_authenticated:
# #             user = request.user
            
# #             if not user.user_type == 'B':
# #                 return self.get_response(request)
            
# #             list_bidder_perwakilan = 
            
# #             # today = now().date()
# #             # # Check if the user is active
# #             # if not user.pending:
# #             #     messages.error(request, "Akun anda masih pending. Hubungi Administrator.")
# #             #     return redirect('/accounts/logout/')

# #             # if (user.masaberlaku1 and user.masaberlaku1 > today) or (user.masaberlaku2 and user.masaberlaku2 < today):
# #             # # Suspend account (set inactive)