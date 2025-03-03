from django import template
from userman.models import tim_lelang, bidder_perwakilan, bidder, bidder_user, UserMenu, Notifikasi, Users,UserMenuGroup, viewers
from adm_lelang.models import jadwal_seleksi, auctioner_lelang, bidder_lelang, item_lelang, detail_itemlelang, viewers_lelang
from django.utils import timezone
import os
from django.contrib.sessions.backends.db import SessionStore


register = template.Library()

def repl(text):
    return text.replace('/','_')
register.filter('repl', repl)

@register.inclusion_tag('judul_bidder_template.html')
def add_judul_bidder(i, j=None, url=None, breadcrumb=None, takes_context=True):
    context = {}
    user = Users.objects.get(id = i)

    vbidder_perwakilan = bidder_user.objects.all().filter(users_id = i)
    if vbidder_perwakilan:
        bidder_id = vbidder_perwakilan[0].bidder_id
        vbidder = bidder.objects.all().filter(id = bidder_id)
        context["bidder"] = vbidder
        if j:
            vbidder_lelang = bidder_lelang.objects.all().filter(bidder = vbidder_perwakilan[0], item_lelang=j)
            user.session_data['item_lelang'] = j
            user.save()
        else:
            if user.session_data:
                j = user.session_data['item_lelang']
            vbidder_lelang = bidder_lelang.objects.all().filter(bidder = vbidder_perwakilan[0], item_lelang=j)
        dt = timezone.now()
        # f_item_lelang = vbidder_lelang[0].item_lelang
        # print('-> DEBUG: vbidder_lelang', vbidder_lelang)
        
        tahapan = None
        
        if len(vbidder_lelang) > 0:
            context["bidder_lelang"] = vbidder_lelang[0]
            context["item_lelang"] = bidder_lelang.objects.all().filter(bidder = vbidder_perwakilan[0])
            tahapan = jadwal_seleksi.objects.all().filter(item_lelang=vbidder_lelang[0].item_lelang).filter(tanggal_akhir__gte=dt).filter(tanggal_awal__lte=dt)    
            
        if tahapan:
            context["tahapan"]  = tahapan
        else:
            context["tahapan"]  = None
            context["bidder_lelang"] = None
            context["item_lelang"] = None
        
        context["bidder_id"] = bidder_id
        context['url']=url
        context['breadcrumb'] = breadcrumb
        
        return context
    return {'name': 'Rachmat Gunawan', 'tahapan': i}

@register.inclusion_tag('judul_auctioner_template.html')
def add_judul_auctioner(i, j=None, url=None, breadcrumb=None, takes_context=True):
    context = {}
    user = Users.objects.get(id = i)
    vauctioner1 = tim_lelang.objects.all().filter(users = i)
    if vauctioner1:
        auctioner_id = vauctioner1[0].id
        if j:
            vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id, item_lelang=j)
            user.session_data['item_lelang'] = j
            user.save()
        else:
            if user.session_data:
                j = user.session_data['item_lelang']
            vauctioner = auctioner_lelang.objects.all().filter(auctioner = auctioner_id, item_lelang=j)
        
        if vauctioner:
            context["auctioner"] = vauctioner[0]
        else:
            context["auctioner"] = None
        context["item_lelang"] = auctioner_lelang.objects.all().filter(auctioner = auctioner_id)
        dt = timezone.now()
        tahapan = jadwal_seleksi.objects.all().filter(item_lelang=j).filter(tanggal_akhir__gte=dt).filter(tanggal_awal__lte=dt).order_by("tanggal_awal","tahap__level")
        context['url']=url
        context['breadcrumb'] = breadcrumb
        if tahapan:
            context["tahapan"]  = tahapan
        else:
            context["tahapan"]  = None
        return context
    return {'name': 'Rachmat Gunawan', 'tahapan': i}

@register.inclusion_tag('judul_viewer_template.html')
def add_judul_viewer(i, j=None, url=None, breadcrumb=None, takes_context=True):
    user = Users.objects.get(id = i)

    context = {}
    viewer1 = viewers.objects.all().filter(users = i)
    if viewer1:
        viewer_id = viewer1[0].id
        if j:
            vviewer = viewers_lelang.objects.all().filter(viewer = viewer_id, item_lelang=j)
            user.session_data['item_lelang'] = j
            user.save()
        else:
            if user.session_data.exists():
                j = user.session_data['item_lelang']
            vviewer = viewers_lelang.objects.all().filter(viewer = viewer_id, item_lelang=j)
        
        context["viewer"] = vviewer[0]
        context["item_lelang"] = viewers_lelang.objects.all().filter(viewer = viewer_id)
        dt = timezone.now()
        tahapan = jadwal_seleksi.objects.all().filter(item_lelang=j).filter(tanggal_akhir__gte=dt).filter(tanggal_awal__lte=dt).order_by("tanggal_awal","tahap__level")
        context['url']=url
        context['breadcrumb'] = breadcrumb
        if tahapan:
            context["tahapan"]  = tahapan
        else:
            context["tahapan"]  = None
        return context
        
    return {'name': 'Rachmat Gunawan', 'tahapan': i}

@register.inclusion_tag('judul_admin_template.html')
def add_judul_admin(i, j=None, url=None, breadcrumb=None, takes_context=True):
    user = Users.objects.get(id = i)

    context = {}
    dt = timezone.now()
    context["item_lelang"] = item_lelang.objects.all()
    if j:
        context["itm_lelang"] = item_lelang.objects.get(pk=j)
        user.session_data['item_lelang'] = j
        user.save()
    else:
        if user.session_data.exists():
            j = user.session_data['item_lelang']
        context["itm_lelang"] = item_lelang.objects.get(pk=j)

    tahapan = jadwal_seleksi.objects.all().filter(item_lelang=j).filter(tanggal_akhir__gte=dt).filter(tanggal_awal__lte=dt).order_by("tanggal_awal","tahap__level")
    context['url']=url
    context['breadcrumb'] = breadcrumb
    if tahapan:
        context["tahapan"]  = tahapan
    else:
        context["tahapan"]  = None
    #print(context)
    return context

@register.inclusion_tag('undangan_auctioner.html')
def add_undangan_auctioner(item_lelang, element, current_step, subelement, auctioner):
    context = {}
    return {'item_lelang': item_lelang, "element": element, "current_step": current_step, 
    "subelement": subelement, "auctioner":auctioner}

@register.inclusion_tag('crud.html')
def add_crud(item_lelang, button_element, element, subelement, drfUrl, listUrl, modalUrl, modalUpdateUrl, auctioner):
    context = {}
    return {'item_lelang': item_lelang, "element": element, "drf_url": drfUrl, "list_url": listUrl,
    "modal_url": modalUrl,"modal_update_url": modalUpdateUrl,"subelement": subelement, "auctioner":auctioner,
    "button_element": button_element}

@register.inclusion_tag('ba_auctioner.html')
def add_ba_auctioner(item_lelang, element, current_step, subelement, auctioner):
    context = {}
    return {'item_lelang': item_lelang, "element": element, "current_step": current_step, 
    "subelement": subelement, "auctioner":auctioner}

@register.inclusion_tag('tabs.html')
def add_tabs(url, userid):
    #'/persiapan/dokumen_seleksi/'
    menu = UserMenu.objects.all().filter(link=url)
    nodes = menu[0].get_leafnodes()
    user = Users.objects.get(pk=userid)
    grp = []
    for g in user.customGroup.all():
        grp.append(g.id)
    #for p in nodes:
        #print(p.id)
    menugroup = UserMenuGroup.objects.all().filter(menu__in=nodes).filter(group__in=grp).distinct('menu')

    context = {
        'tabs': nodes,
        'menu_group': menugroup,
    }
    return context

@register.inclusion_tag('sidebar_htmx.html', takes_context=True)
def add_sidebar(context):
    request = context['request']
    userid = request.user.id
    user = Users.objects.get(pk=userid)
    grp = []
    for g in user.customGroup.all():
        grp.append(g.id)
    menugroup = UserMenuGroup.objects.values_list('menu', flat=True).all().filter(group__in=grp).distinct('menu')
    menu = UserMenu.objects.all()
    current_url = request.headers.get("Current-URL", "/")
    return {'menu': menu, 'menugroup': list(menugroup), "current_url": current_url}

@register.inclusion_tag('notifikasi.html', takes_context=True)
def add_notification(context):
    request = context['request']
    email = request.user.email
    #email = 	"budidwiprasetyo49@gmail.com"
    today =  timezone.now()
    notif_undangan = Notifikasi.objects.filter(email=email, notification_type='U', expire_date__gte = today)
    notif_ba = Notifikasi.objects.filter(email=email, notification_type='B', expire_date__gte = today)
    return {'notif_undangan': notif_undangan, 'notif_ba': notif_ba, 'count_undangan': len(notif_undangan), 'count_ba': len(notif_ba), 'count': len(notif_undangan)+len(notif_ba)}

LABEL_MAPPING = {
    "smra2": "SMRA",
    "settings": "Pengaturan Lelang",
}

@register.filter
def to_label(value):
    """Template filter to map status to custom text."""
    return LABEL_MAPPING.get(value, "Unknown Text")