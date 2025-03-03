from rest_framework import permissions
from userman.models import bidder_user
from adm_lelang.models import bidder_lelang, item_lelang

from django.core.exceptions import FieldDoesNotExist

def has_field(model_class, field_name):
    try:
        model_class._meta.get_field(field_name)
        return True
    except FieldDoesNotExist:
        return False

class EAuctionsPErmission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        # kalau bidder, hanya boleh akses obyek yang dia punya akses terhadap item_lelang
        if hasattr(user, "user_type") and user.user_type == 'B': 
            model_name = obj._meta.object_name # get Class name of the model
            if has_field(obj,"item_lelang"):
                try:
                    bu = bidder_user.objects.get(users = user)
                    bl = bidder_lelang.objects.get(bidder = bu)
                    itl = item_lelang.objects.filter(id = bl.item_lelang)
                    if not itl.exists():
                        return False
                    return True
                except:
                    return False
        elif hasattr(user, "user_type") and user.user_type == 'C':
            model_name = obj._meta.object_name # get Class name of the model
            if has_field(obj,"item_lelang"):
                try:
                    bu = bidder_user.objects.get(users = user)
                    bl = bidder_lelang.objects.get(bidder = bu)
                    itl = item_lelang.objects.filter(id = bl.item_lelang)
                    if not itl.exists():
                        return False
                    return True
                except:
                    return False
        else:
            return True

class EAuctionsUndanganPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        # kalau bidder, hanya boleh akses obyek yang dia punya akses terhadap item_lelang
        print("Masuk sini")

        if hasattr(user, "user_type") and user.user_type == 'B': 
            model_name = obj._meta.object_name # get Class name of the model
            bu = obj.bidder_user
            is_in_bu = False  
            for b in bu:
                if b.users == user:
                    is_in_bu = True
                    break
            return is_in_bu
        else:
            return True