import django_tables2 as tables
from . import models
from django_tables2 import TemplateColumn

class bidder_usersTable(tables.Table):
    actions = TemplateColumn(template_code='<div class="" style="display: flex; justify-content: center;"><button data-toggle="tooltip" data-placement="right" title="Sunting" id="{{ record.id }}" class="objek_seleksi_update btn btn-sm btn-warning"><i class="fa fa-edit circle-icon"></i></button>&nbsp;&nbsp;<button data-toggle="tooltip" data-placement="right" title="Hapus" id="{{ record.id }}" class="objek_seleksi_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    nama_lengkap = TemplateColumn(attrs={"td": {"align": "left"}},template_code='{{ record.users.nama_lengkap }}')
    username = TemplateColumn(attrs={"td": {"align": "left"}},template_code='{{ record.users.username }}')
    nama_perusahaan = TemplateColumn(attrs={"td": {"align": "left"}},template_code='{{ record.bidder.nama_perusahaan }}')
    class Meta:
        model = models.bidder_user
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nama_lengkap","username","nama_perusahaan")


class bidder_perwakilanTable(tables.Table):
    actions = TemplateColumn(template_code='<div class="" style="display: flex; justify-content: center;"><button data-toggle="tooltip" data-placement="right" title="Sunting" id="{{ record.id }}" class="objek_seleksi_update btn btn-sm btn-warning"><i class="fa fa-edit circle-icon"></i></button>&nbsp;&nbsp;<button data-toggle="tooltip" data-placement="right" title="Hapus" id="{{ record.id }}" class="objek_seleksi_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    class Meta:
        model = models.bidder_perwakilan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ('nama_lengkap','nik_perwakilan','email','mobile_number','jabatan','active','sk_pengangkatan')

class bidder_perwakilan2Table(tables.Table):
    aksi = TemplateColumn(template_code='<div class="" style="display: flex; justify-content: center;"><button type="button" data-toggle="tooltip" data-placement="right" title="Sunting" id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit circle-icon"></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button type="button" data-toggle="tooltip" data-placement="right" title="Kirim" id="{{ record.id }}" class="send btn badge mr-1" style="color:green;"><i class="icon"><img style="height:18px;" src="/static/img/email.svg"></i></button></div>')
    ttd = TemplateColumn(template_code='{% if record.ttd %}<img height="50px" src="{{record.ttd.url}}">{% else %}-{% endif %}')
    bidder = tables.Column(verbose_name="Nama Perusahaan")
    class Meta:
        model = models.bidder_perwakilan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ('nama_lengkap','nik_perwakilan','email','ttd')

