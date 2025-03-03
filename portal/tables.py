import django_tables2 as tables
from django_tables2 import TemplateColumn
from . import models

class BannerTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="banner_update btn btn-sm btn-warning"><i class="fa fa-edit circle-icon"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="banner_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    last_updated = TemplateColumn(template_code='<span>{{ record.last_updated|date:"d F Y H:i:s" }}</span>')
    last_updated = TemplateColumn(template_code='<span>{{ record.last_updated|date:"d F Y H:i:s" }}</span>')
    updated_by = TemplateColumn(template_code='<span>{{ record.updated_by.username }}</span>')
    image = tables.TemplateColumn(
        '<a href="{{ record.image.url }}" target="_blank"><img src="{{ record.image.url }}" class="thumbnail" width="300" height="300"></a>',
        verbose_name=u'Image',
    )
    class Meta:
        model = models.banner
        template_name = "django_tables2/bootstrap5.html"
        attrs = {"class": "table table-striped table-dark"}
        fields = [
            "nama_banner",
            "caption",
            "image",
           
            "last_updated",
            "updated_by",
        ]

class portal_blockTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="profil_update btn btn-warning text-white btn-sm"><i class="fa fa-pen-to-square"> </i>&nbsp;&nbsp;Ubah Data</button></div>')
    last_updated = TemplateColumn(verbose_name="Tanggal Diubah",template_code='<span>{{ record.last_updated|date:"d F Y H:i:s" }}</span>')
    created = TemplateColumn(verbose_name="Tanggal Dibuat", template_code='<span>{{ record.created|date:"d F Y " }}</span>')
    updated_by = TemplateColumn(template_code='<span>{{ record.updated_by.username }}</span>')
    judul = TemplateColumn(template_code='<span style="font-weight:bold;">{{ record.judul }}</span>')
    class Meta:
        model = models.portal_block
        template_name = "tables/table_profile.html"
        attrs = {
            "class": "table table-striped",
            "thead": {
                "class": "table2;",   
            }
        }
        fields = [
            "judul",
            "content",
            "last_updated",
            "created",
            "updated_by",
            "order",
        ]
        order_by = ('order')


class istilah_lelangTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="istilah_update btn btn-warning btn-sm"><i class="fa fa-pen-to-square"></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="istilah_delete btn btn-sm btn-danger"><i class="fa fa-trash"></button></div>')
    last_updated = TemplateColumn(template_code='<span>{{ record.last_updated|date:"d F Y H:i:s" }}</span>')
    updated_by = TemplateColumn(template_code='<span>{{ record.updated_by.username }}</span>')
   
    class Meta:
        model = models.istilah_lelang
        template_name = "django_tables2/bootstrap5.html"
        attrs = {
            "class": "table table-striped table-dark",
            "thead": {
                "class": "thead-custom",    # Custom class for thead
                "style": "background-color: inherit; cursor: default;",   # Custom CSS styles for thead
            }
        }
        fields = [
            "nama_istilah",
            "penjelasan",
            "last_updated",
            "updated_by",
            
        ]
       
        
        
class history_lelangTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="histori_update btn btn-warning btn-sm"><i class="fa fa-pen-to-square"></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="histori_delete btn btn-sm btn-danger"><i class="fa fa-trash"></button></div>')
    last_updated = TemplateColumn(template_code='<span>{{ record.last_updated|date:"d F Y H:i:s" }}</span>')
    updated_by = TemplateColumn(template_code='<span>{{ record.updated_by.username }}</span>')
    image = tables.TemplateColumn(
        '<a href="{{ record.image.url }}" target="_blank"><img src="{{ record.image.url }}" class="thumbnail" width="300" height="300"></a>',
        verbose_name=u'Image',
    )
    class Meta:
        model = models.history_lelang
        template_name = "django_tables2/bootstrap5.html"
        attrs = {
            "class": "table table-striped table-dark",
            "thead": {
                "class": "thead-custom",    # Custom class for thead
                "style": "background-color: inherit; cursor: default;",   # Custom CSS styles for thead
            }
        }
        fields = [
            
            "tahun",
            "pita",
            "bandwidth",
            "penyelenggaraan",
            "keterangan",
            "image",
            "last_updated",
            "updated_by",
            
        ]
        
        
class lelang_mancaTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="lelang_manca_update btn btn-warning btn-sm"><i class="fa fa-pen-to-square"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="lelang_manca_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    last_updated = TemplateColumn(template_code='<span>{{ record.last_updated|date:"d F Y H:i:s" }}</span>')
    updated_by = TemplateColumn(template_code='<span>{{ record.updated_by.username }}</span>')
    image = tables.TemplateColumn(
        '<a href="{{ record.image.url }}" target="_blank"><img src="{{ record.image.url }}" class="thumbnail" width="300" height="300"></a>',
        verbose_name=u'Image',
    )
    class Meta:
        model = models.lelang_mancanegara
        template_name = "django_tables2/bootstrap5.html"
        attrs = {
            "class": "table table-striped table-dark",
            "thead": {
                "class": "thead-custom",    # Custom class for thead
                "style": "background-color: inherit; cursor: default;",   # Custom CSS styles for thead
            }
        }
        fields = [
            "negara",
            "tahun",
            "pita",
            "bandwidth",
            "keterangan",
            "image",
            "last_updated",
            "updated_by",
            
        ]
        
class aturan_lelangTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="aturan_update btn btn-sm btn-warning"><i class="fa fa-pen-to-square"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="aturan_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    last_updated = TemplateColumn(template_code='<span>{{ record.last_updated|date:"d F Y H:i:s" }}</span>')
    updated_by = TemplateColumn(template_code='<span>{{ record.updated_by.username }}</span>')
    class Meta:
        model = models.aturan_lelang
        template_name = "django_tables2/bootstrap5.html"
        attrs = {
            "class": "table table-striped table-dark",
            "thead": {
                "class": "thead-custom",    # Custom class for thead
                "style": "background-color: inherit; cursor: default;",   # Custom CSS styles for thead
            }
        }
        fields = [
            "jenis_kebjakan",
            "nomor",
            "tahun",
            "tanggal",
            "keterangan",
            "nama_kebijakan",
            "file",
            "last_updated",
            "updated_by",
            
        ]

class notice_lelangTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="aturan_update btn btn-sm btn-warning"><i class="fa fa-pen-to-square"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="aturan_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    last_updated = TemplateColumn(template_code='<span>{{ record.last_updated|date:"d F Y H:i:s" }}</span>')
    updated_by = TemplateColumn(template_code='<span>{{ record.updated_by.username }}</span>')
    class Meta:
        model = models.aturan_lelang
        template_name = "django_tables2/bootstrap5.html"
        attrs = {
            "class": "table table-striped table-dark",
            "thead": {
                "class": "thead-custom",    # Custom class for thead
                "style": "background-color: inherit; cursor: default;",   # Custom CSS styles for thead
            }
        }
        fields = [
            "tanggal",
            "nama_notice",
            "last_updated",
            "updated_by",
            
        ]


class profilTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-sm btn-warning"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"></i></button></div>')
    last_updated = TemplateColumn(template_code='<span>{{ record.last_updated|date:"d F Y H:i:s" }}</span>')
    # updated_by = TemplateColumn(template_code='<span>{{ record.updated_by.username }}</span>')
    class Meta:
        model = models.profil
        template_name = "tables/table_kebawah.html"
        attrs = {
            "class": "table table-striped table-dark",
            "thead": {
                "class": "thead-custom",    # Custom class for thead
                "style": "background-color: inherit; cursor: default;",   # Custom CSS styles for thead
            }
        }
        fields = [
            "latar_belakang",
            "sejarah_seleksi",
            "visi",
            "misi",
            "tugas_dir",
            "last_updated",
            # "updated_by",
        ]