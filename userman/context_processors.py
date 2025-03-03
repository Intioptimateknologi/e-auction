# from .models import (Users, CustomGroup,tim_lelang, bidder_user, bidder, dokumen_perusahaan, admin, viewers, bidder_list, bidder_perwakilan, UserMenu, UserMenuGroup)
 
# def menutree(request):
#     grp = []
#     user = Users.objects.get(pk=request.user.id)
#     for g in user.customGroup.all():
#         grp.append(g.id)
    
#     menugroup = UserMenuGroup.objects.values_list('menu', flat=True).all().filter(group__in=grp).distinct('menu')
#     menu = UserMenu.objects.all()
#     return {'menu': menu, 'menugroup': list(menugroup)}