import django_tables2 as tables
from . import models
from django_tables2 import TemplateColumn

class round_scheduleTable(tables.Table):
    actions = TemplateColumn(template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    mulai = tables.TimeColumn(format ='h:i A')
    selesai = tables.TimeColumn(format ='h:i A')
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Dibuat")
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Diubah")

    class Meta:
        empty_text = "Tidak ada data"
        orderable = False
        model = models.round_schedule_smra
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("hari", "mulai", "selesai", "created", "last_updated", "diubah_oleh", "dibuat_oleh")

class round_scheduleTable2(tables.Table):
    mulai = tables.TimeColumn(localize=True, format ='h:i A')
    selesai = tables.TimeColumn(localize=True, format ='h:i A')
    #created = tables.DateTimeColumn(verbose_name="Dibuat Pertama",format ='d F Y H:i:s')
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s')
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    class Meta:
        empty_text = "Tidak ada data"
        orderable = False
        model = models.round_schedule_smra
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("hari", "mulai", "selesai", 
        #"created", 
        "last_updated",) #"diubah_oleh", "dibuat_oleh")

# tabels undangan
class smra_cca_Tabel(tables.Table):
    actions = TemplateColumn(template_code='<div style="display: flex; "><button id="{{ record.id }}" class="undangan_send btn badge mr-1"><i class="icon fa fa-envelope"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="undangan_update btn btn-sm btn-warning"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="undangan_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    class Meta:
        model = models.undangan_smra_cca
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","tempat","agenda","link_teleconference","keterangan","bidder","auctioneer","link_file")
        

class smra_cca_Tabel2(tables.Table):
    class Meta:
        model = models.undangan_smra_cca
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","tempat","agenda","link_teleconference","keterangan","link_file")

class bertia_acara(tables.Table):
    class Meta:
        model = models.berita_acara_lelang
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","keterangan", "bidder",  "auctioneer", "link_file",)  
