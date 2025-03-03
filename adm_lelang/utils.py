
from django.shortcuts import redirect
from userman.models import tim_lelang, bidder_perwakilan, bidder, UserMenu, Users, UserMenuGroup, bidder_user, viewers
from userman.serializers import UserMenu2Serializer
from adm_lelang.models import auctioner_lelang, bidder_lelang, jadwal_seleksi, item_lelang, pengumuman, viewers_lelang
from datetime import datetime, timedelta
from django.utils import timezone
import requests

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_judul_context_admin(request):
    context = {}
    if request.GET.get("id"):
        request.session['id_judul'] = request.GET.get("id")
        context["item_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) 
    else:
        if request.session.get('id_judul'):
            context["item_lelang"] = item_lelang.objects.get(pk=request.session.get("id_judul")) 
        else:
            context["item_lelang"] = item_lelang.objects.all()[0]
    context['user_type'] = request.user.user_type
    context['hasil_user_type'] ="Admin" 
    return context

# def get_judul_context_auctioneer(request):
#     context = {}

#     auc = tim_lelang.objects.filter(users_id=request.user.id)

#     if auc:
#         context['auctioner'] = auc.first()

#         if request.GET.get("id"):
#             request.session['id_judul'] = request.GET.get("id")
#             auc_lelang = auctioner_lelang.objects.all().filter(auctioner = context['auctioner'] , item_lelang=request.GET.get("id"))
#             context["item_lelang"] = auc_lelang.first().item_lelang
#         else:
#             if request.session.get('id_judul'):
#                 auc_lelang = auctioner_lelang.objects.all().filter(auctioner = context['auctioner'], item_lelang=request.user.session_data['item_lelang'])
#             else:
#                 auc_lelang = auctioner_lelang.objects.all().filter(auctioner = context['auctioner']).order_by('created')
#             context["item_lelang"] = auc_lelang.first().item_lelang

#         context['user_type'] = request.user.user_type
#         context['hasil_user_type'] = "Auctioner"

#         return context
#     else:
#         return {
#             "bidder_perwakilan": None,
#             "bidder": None,
#             "bidder_lelang": None,
#             "bidder_id": None,
#             "item_lelang": None,
#             "tahapan": None
#         }

def get_judul_context_auctioneer(request):
    context = {}

    auc = tim_lelang.objects.filter(users_id=request.user.id)
    
    if auc.exists():
        context['auctioner'] = auc.first()
        auctioner = context['auctioner']
        
        item_lelang_id = request.GET.get("id") or request.session.get('id_judul')

        if item_lelang_id:
            request.session['id_judul'] = item_lelang_id
            auc_lelang = auctioner_lelang.objects.filter(auctioner=auctioner, item_lelang=item_lelang_id)
        else:
            auc_lelang = auctioner_lelang.objects.filter(auctioner=auctioner).order_by('created')

        context["item_lelang"] = auc_lelang.first().item_lelang if auc_lelang.exists() else None

        context['user_type'] = request.user.user_type
        context['hasil_user_type'] = "Auctioner"

        return context
    else:
        return {
            "bidder_perwakilan": None,
            "bidder": None,
            "bidder_lelang": None,
            "bidder_id": None,
            "item_lelang": None,
            "tahapan": None
        }



# def get_judul_context_auctioneer(request):
#     context = {}
#     auc = tim_lelang.objects.all().filter(users_id = request.user.id)
#     if auc:
#         context['auctioner'] = auc[0]
#         if request.GET.get("id"):
#             request.session['id_judul'] = request.GET.get("id")
#             context["item_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) #bidder_lelang.objects.all().filter(bidder = bidder_id)
#         else:
#             if request.session.get('id_judul'):
#                 context["item_lelang"] = item_lelang.objects.get(pk=request.session.get("id_judul")) #bidder_lelang.objects.all().filter(bidder = bidder_id)
#             else:
#                 auc_lelang = auctioner_lelang.objects.all().filter(auctioner = auc[0].id).order_by('created')
#                 context["item_lelang"] = auc_lelang[0].item_lelang #bidder_lelang.objects.all().filter(bidder = bidder_id)
#         context['user_type'] = request.user.user_type
#         context['hasil_user_type'] ="Auctioner"     
#         user = request.user
#         return context
#     else:
#         return {"bidder_perwakilan": None, "bidder": None, "bidder_lelang": None, "bidder_id": None, "item_lelang": None, "tahapan": None}
    
def get_judul_context_viewers(request):
    context = {}
    vie = viewers.objects.all().filter(users_id = request.user.id)
    if vie:
        context['viewers'] = vie[0]
        if request.GET.get("id"):
            request.session['id_judul'] = request.GET.get("id")
            context["item_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) #bidder_lelang.objects.all().filter(bidder = bidder_id)
        else:
            if request.session.get('id_judul'):
                context["item_lelang"] = item_lelang.objects.get(pk=request.session.get('id_judul')) #bidder_lelang.objects.all().filter(bidder = bidder_id)
            else:
                vie_lelang = viewers_lelang.objects.all().filter(viewer = vie[0].id).order_by('created')
                context["item_lelang"] = vie_lelang[0].item_lelang #bidder_lelang.objects.all().filter(bidder = bidder_id)
        context['user_type'] = request.user.user_type    
        context['hasil_user_type'] ="Viewer"  
        user = request.user
        #print(context)
        return context
    else:
        return {"bidder_perwakilan": None, "bidder": None, "bidder_lelang": None, "bidder_id": None, "item_lelang": None, "tahapan": None}

def get_judul_context_bidder(request):
    vbidder_perwakilan = bidder_user.objects.all().filter(users_id = request.user.id)
    context={}
    if vbidder_perwakilan:
#        print(vbidder_perwakilan)
        context = {}
        bidder_id = vbidder_perwakilan[0].bidder_id
        vbidder = bidder.objects.all().filter(id = bidder_id)
        context["bidder_perwakilan"] = vbidder_perwakilan
        context["bidder"] = vbidder
        if request.GET.get("id"):
            request.session['id_judul'] = request.GET.get("id")
            vbidder_lelang = bidder_lelang.objects.all().filter(bidder = vbidder_perwakilan[0], item_lelang=request.GET.get("id"))
        else:
            if request.session.get('id_judul'):
                vbidder_lelang = bidder_lelang.objects.all().filter(bidder = vbidder_perwakilan[0], item_lelang=request.user.session_data['item_lelang'])
            else:
                vbidder_lelang = bidder_lelang.objects.all().filter(bidder = vbidder_perwakilan[0]).order_by('created')
#        print(vbidder_lelang)
        context["bidder_lelang"] = vbidder_lelang[0]
        
        # try:
        #     context["bidder_lelang"] = vbidder_lelang[0]
        # except Exception as e:
        #     print('error', e)
        #     return redirect('/')
        
        context["bidder_id"] = vbidder_perwakilan[0].id
        context["ip_address"] = get_client_ip(request)
        context["item_lelang"] = vbidder_lelang[0].item_lelang #bidder_lelang.objects.all().filter(bidder = bidder_id)
        dt = timezone.now()
        tahapan = jadwal_seleksi.objects.all().filter(item_lelang=vbidder_lelang[0].item_lelang).filter(tanggal_akhir__gte=dt).filter(tanggal_awal__lte=dt)
        if tahapan:
            context["tahapan"]  = tahapan[0]
        else:
            context["tahapan"]  = None
        context['user_type'] = request.user.user_type   
        context['hasil_user_type'] ="Bidder"   
        #print(context)
        return context
    else:
        return {"bidder_perwakilan": None, "bidder": None, "bidder_lelang": None, "bidder_id": None, "item_lelang": None, "tahapan": None}


def get_tab_context(request, url, item_lelang=70):
    menu = UserMenu.objects.all().filter(link=url)
    nodes = menu[0].get_leafnodes() #.order_by('order')
    user = Users.objects.get(pk=request.user.id)
    context = {}
    #context['user_type'] = user.user_type
    if user.user_type=='A':
        if request.GET.get("id"):
            #context["itm_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) 
            None
            #context["item_lelang"] = item_lelang.objects.all()
        else:
            None
            #context["item_lelang"] = item_lelang.objects.all()
            #context["itm_lelang"] = item_lelang.objects.all()[0]
    elif user.user_type=='B':
        bdr = bidder_user.objects.all().filter(users_id = request.user.id)
        if request.GET.get("id"):
            #context["itm_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) 
            bdr_lelang = bidder_lelang.objects.all().filter(bidder = bdr[0].id).order_by('created')
            #context["item_lelang"] = bdr_lelang[0].item_lelang
        else:
            bdr_lelang = bidder_lelang.objects.all().filter(bidder = bdr[0].id).order_by('created')
            #context["item_lelang"] = bdr_lelang[0].item_lelang
            #context["itm_lelang"] = bdr_lelang[0].item_lelang[0]
    elif user.user_type=='C':
        auc = tim_lelang.objects.all().filter(users_id = request.user.id)
        if request.GET.get("id"):
            #context["itm_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) 
            auc_lelang = auctioner_lelang.objects.all().filter(auctioner = auc[0].id).order_by('created')
            #context["item_lelang"] = auc_lelang[0].item_lelang
        else:
            auc_lelang = auctioner_lelang.objects.all().filter(auctioner = auc[0].id).order_by('created')
            #context["item_lelang"] = auc_lelang[0].item_lelang
            #context["itm_lelang"] = auc_lelang[0].item_lelang[0]
    else:
        vwr = viewers.objects.all().filter(users_id = request.user.id)
        if request.GET.get("id"):
            #context["itm_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) 
            viewer_lelang = viewers_lelang.objects.all().filter(viewer = vwr[0].id).order_by('created')
            #context["item_lelang"] = bdr_lelang[0].item_lelang
        else:
            vwr_lelang = viewers_lelang.objects.all().filter(viewer = vwr[0].id).order_by('created')
            #context["item_lelang"] = vwr_lelang[0].item_lelang
            #context["itm_lelang"] = vwr_lelang[0].item_lelang[0]

    dt = timezone.now()
    #jadwal_tahapan = jadwal_seleksi.objects.all().filter(item_lelang=context["itm_lelang"]).filter(tanggal_akhir__gte=dt).filter(tanggal_awal__lte=dt).order_by("tanggal_awal","tahap__level")
    #context['url']=url
    #if jadwal_tahapan:
    #    context["jadwal_tahapan"]  = jadwal_tahapan
    #else:
    #    context["jadwal_tahapan"]  = None

    grp = []
    for g in user.customGroup.all():
        grp.append(g.id)
    menugroup = UserMenuGroup.objects.all().filter(menu__in=nodes).filter(group__in=grp).distinct('menu')
    tahapan = []
    menu_group = []

    for grp in menugroup:
        jad_sel = jadwal_seleksi.objects.all().filter(item_lelang=item_lelang, tahap = grp.menu.tahapan)
        status = {}
        if jad_sel:
            if jad_sel[0].tanggal_awal > dt:
                status = {"text":"Belum berlangsung","flag":"B"}
            if jad_sel[0].tanggal_akhir < dt:
                status = {"text":"Sudah berlangsung","flag":"L"}
                
            if jad_sel[0].tanggal_akhir > dt and jad_sel[0].tanggal_awal < dt:
                status = {"text":"Sedang berlangsung","flag":"N"}
        menu_group.append({'id':grp.menu.order,'menu':grp.menu, 'tahapan':jad_sel[0] if jad_sel else jad_sel, 'status': status})
        #print(menu_group)
    def extract_order(json):
        try:
            return int(json['id'])
        except KeyError:
            return 0

    menu_group.sort(key=extract_order)

    context['menu_group']= menu_group
    return context    

def get_tab_context2(request, url, item_lelang=70, pk=1):
    menu = UserMenu.objects.all().filter(link=url)
    nodes = menu[0].get_leafnodes() #.order_by('order')
    user = Users.objects.get(pk=request.user.id)
    context = {}
    #context['user_type'] = user.user_type
    if user.user_type=='A':
        if request.GET.get("id"):
            #context["itm_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) 
            None
            #context["item_lelang"] = item_lelang.objects.all()
        else:
            None
            #context["item_lelang"] = item_lelang.objects.all()
            #context["itm_lelang"] = item_lelang.objects.all()[0]
    elif user.user_type=='B':
        bdr = bidder_user.objects.all().filter(users_id = request.user.id)
        if request.GET.get("id"):
            #context["itm_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) 
            bdr_lelang = bidder_lelang.objects.all().filter(bidder = bdr[0].id).order_by('created')
            #context["item_lelang"] = bdr_lelang[0].item_lelang
        else:
            bdr_lelang = bidder_lelang.objects.all().filter(bidder = bdr[0].id).order_by('created')
            #context["item_lelang"] = bdr_lelang[0].item_lelang
            #context["itm_lelang"] = bdr_lelang[0].item_lelang[0]
    elif user.user_type=='C':
        auc = tim_lelang.objects.all().filter(users_id = request.user.id)
        if request.GET.get("id"):
            #context["itm_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) 
            auc_lelang = auctioner_lelang.objects.all().filter(auctioner = auc[0].id).order_by('created')
            #context["item_lelang"] = auc_lelang[0].item_lelang
        else:
            auc_lelang = auctioner_lelang.objects.all().filter(auctioner = auc[0].id).order_by('created')
            #context["item_lelang"] = auc_lelang[0].item_lelang
            #context["itm_lelang"] = auc_lelang[0].item_lelang[0]
    else:
        vwr = viewers.objects.all().filter(users_id = request.user.id)
        if request.GET.get("id"):
            #context["itm_lelang"] = item_lelang.objects.get(pk=request.GET.get("id")) 
            viewer_lelang = viewers_lelang.objects.all().filter(viewer = vwr[0].id).order_by('created')
            #context["item_lelang"] = bdr_lelang[0].item_lelang
        else:
            vwr_lelang = viewers_lelang.objects.all().filter(viewer = vwr[0].id).order_by('created')
            #context["item_lelang"] = vwr_lelang[0].item_lelang
            #context["itm_lelang"] = vwr_lelang[0].item_lelang[0]

    dt = timezone.now()
    #jadwal_tahapan = jadwal_seleksi.objects.all().filter(item_lelang=context["itm_lelang"]).filter(tanggal_akhir__gte=dt).filter(tanggal_awal__lte=dt).order_by("tanggal_awal","tahap__level")
    #context['url']=url
    #if jadwal_tahapan:
    #    context["jadwal_tahapan"]  = jadwal_tahapan
    #else:
    #    context["jadwal_tahapan"]  = None

    grp = []
    for g in user.customGroup.all():
        grp.append(g.id)
    menugroup = UserMenuGroup.objects.all().filter(menu__in=nodes).filter(group__in=grp).distinct('menu')
    tahapan = []
    menu_group = []
    udah=True

    for grp in menugroup:
        if pk==0 and udah:
           pk = grp.menu.id
           udah=False
        
        jad_sel = jadwal_seleksi.objects.all().filter(item_lelang=item_lelang, tahap = grp.menu.tahapan, tanggal_awal__isnull = False)
        status = {}
        # print("aya")
        # print(grp.menu.id)
        # print("aya")
        
        if jad_sel :
            if jad_sel[0].tanggal_awal > dt:
                status = {"text":"Belum berlangsung","flag":"B"}
                if grp.menu.id==pk :
                   request.session['kada']="B"
               
            if jad_sel[0].tanggal_akhir < dt:
                status = {"text":"Sudah berlangsung","flag":"L"}
                if grp.menu.id==pk :
                   request.session['kada']="L"

            if jad_sel[0].tanggal_akhir > dt and jad_sel[0].tanggal_awal < dt:
                status = {"text":"Sedang berlangsung","flag":"N"}
                if grp.menu.id==pk :
                   request.session['kada']="N"

        menu_group.append({'id':grp.menu.order,'menu':grp.menu, 'tahapan':jad_sel[0] if jad_sel else jad_sel, 'status': status})

        #print(menu_group)
 

    def extract_order(json):
        try:
            return int(json['id'])
        except KeyError:
            return 0

    menu_group.sort(key=extract_order)
    context['id']= pk
    context['menu_group']= menu_group
    return context