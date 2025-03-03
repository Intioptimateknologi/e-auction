import django_tables2 as tables
from . import models
#from smra.models import berita_acara_lelang
from django_tables2 import TemplateColumn

class penentuan_parameterTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex;"><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    bobot2 = tables.Column(verbose_name="Bobot SMRA")
    bobot = tables.Column(verbose_name="Bobot BC")
    class Meta:
        model = models.penentuan_parameter
        empty_text = "Tidak ada data"
        orderable = False
        #attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("obyek_bc","bobot", "obyek_smra","bobot2")
        
class ba_gabungan(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex;"><button id="{{ record.id }}" class="b_gabungan_update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="b_gabungan_delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    dokumen_ba = TemplateColumn(template_code='<div style="display:flex;"><a href="/media/{{record.dokumen_ba}}"><i class="fa-solid fa-eye"></i></a></div>')
    class Meta:
        model = models.ba_gabungan
        empty_text = "Tidak ada data"
        orderable = False
        
        # attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("dokumen_ba",)
        
class nilai_gabungan(tables.Table):
    #Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="nilai_gabungan_update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="nilai_gabungan_delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    penilaian = TemplateColumn(attrs={"td": {"align": "left"}},template_code='{{ record.penilaian|floatformat:"5g" }}')
    item = tables.Column(verbose_name="Objek Seleksi")
    bidder = tables.Column(verbose_name="Nama Perusahaan")
    class Meta:
        model = models.penilaian_gabungan
        empty_text = "Tidak ada data"
        orderable = False
        # attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("bidder","item", "parameter", "bobot","penilaian")

class hasil_gabungan(tables.Table):
    #Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="nilai_gabungan_update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="nilai_gabungan_delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    total = TemplateColumn(attrs={"td": {"align": "left"}},template_code='{{ record.total|floatformat:"5g" }}')
    harga = TemplateColumn(attrs={"td": {"align": "right"}},template_code='{{ record.harga|floatformat:"2g" }}')
    item = tables.Column(verbose_name="Objek Seleksi")
    bidder = tables.Column(verbose_name="Nama Perusahaan")
    class Meta:
        model = models.hasil_gabungan
        empty_text = "Tidak ada data"
        orderable = False
        # attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("bidder","item", "ranking", "harga","total", )

#class sum_gabungan_Table2(tables.Table):
#    sum = TemplateColumn(attrs={"td": {"align": "left"}},template_code='{{ record.sum|floatformat:"5g" }}')
#    class Meta:
#        model = models.sum_gabungan
#        attrs = {"class": "table table-sm table-striped"}
#        template_name = "django_tables2/bootstrap.html"
#        fields = ("bidder","sum",)

"""class berita_acara1(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex;"><button id="{{ record.id }}" class="b_gabungan_update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="b_gabungan_delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    class Meta:
        model = berita_acara_lelang
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("nomor","judul","tanggal","keterangan","file",)  

class berita_acara2(tables.Table):
    class Meta:
        model = berita_acara_lelang
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("nomor","judul","tanggal","keterangan","file",)  
"""