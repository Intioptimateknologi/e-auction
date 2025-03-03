import django_tables2 as tables
from . import models
from django_tables2 import TemplateColumn
#from smra.models import undangan_smra_cca


class kriteria_evaluasi_Table(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    last_updated = tables.DateTimeColumn(format ='d M Y H:i:s', verbose_name="Tanggal Diubah")
    bobot = tables.Column(verbose_name="Bobot (%)")
    item = tables.Column(verbose_name="Objek Seleksi")
    class Meta:
        model = models.parameter_evaluasi
        empty_text = "Tidak ada data"
        orderable = False
       # attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("item","parameter","bobot", "last_updated",)
# curd
class dokumen_beauty_content_Table(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    dokumen_bc = TemplateColumn(verbose_name="Dokumen Penawaran Beauty Contest",template_code='<div style="display:flex;"><a href="/media/{{record.dokumen_bc}}"><img class="pdf_icon" src="/static/img/zip_icon.png" style="height: 20px; width: 20px"></a></div>')
    last_updated = tables.DateTimeColumn(format ='d M Y H:i:s', verbose_name="Tanggal Diubah")
    diubah_oleh = TemplateColumn(verbose_name="Diubah Oleh", template_code='{% if record.diubah_oleh %}{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}}){% else %}<p>-</p>{% endif %}')
    #dibuat_oleh = TemplateColumn(template_code='{% if record.dibuat_oleh %}{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}}){% else %}<p>-</p>{% endif %}')
    item = tables.Column(verbose_name="Objek Seleksi")
    created = tables.DateTimeColumn(format ='d M Y H:i:s', verbose_name="Tanggal Dibuat")
    perwakilan = tables.Column(verbose_name="Perwakilan Perusahaan")
    nama_dok = tables.Column(verbose_name="Nama Dokumen")
    class Meta:
        model = models.dokumen_bc
        empty_text = "Tidak ada data"
        orderable = False
        
       # attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("item", "perwakilan", "nama_dok","dokumen_bc", "dibuat_oleh", "diubah_oleh", "created", "last_updated",  )

# view only
class dokumen_beauty_content_Table2(tables.Table):
    item = tables.Column(verbose_name="Objek Seleksi")
    bidder = TemplateColumn(verbose_name="Nama Perusahaan", template_code="{{record.bidder.users.username}} ({{record.bidder.bidder.nama_perusahaan}})")
    dokumen_bc = TemplateColumn(verbose_name="Dokumen Penawaran Beauty Contest",template_code='<div style="display:flex;"><a href="/media/{{record.dokumen_bc}}"><img class="pdf_icon" src="/static/img/zip_icon.png" style="height: 20px; width: 20px"></a></div>')
    perwakilan = tables.Column(verbose_name="Perwakilan Perusahaan")
    nama_dok = tables.Column(verbose_name="Nama Dokumen")
    class Meta:
        model = models.dokumen_bc
        empty_text = "Tidak ada data"
        orderable = False
        
        #attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("item", "bidder", "perwakilan", "nama_dok","dokumen_bc", )
        
# curd
class dokumen_persyaratan_Table(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    tgl_penetapan = tables.DateTimeColumn(format ='d M Y H:i:s')
  #  dokumen_bc = TemplateColumn(template_code='<div style="display:flex;"><a href="/media/{{record.dokumen_bc}}"><i class="fa-solid fa-eye"></i></a></div>')
    last_updated = tables.DateTimeColumn(format ='d M Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d M Y H:i:s',  verbose_name="Tanggal Dibuat")
    diubah_oleh = TemplateColumn(template_code='{% if record.diubah_oleh %}{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}}){% else %}<p>-</p>{% endif %}')
    dibuat_oleh = TemplateColumn(template_code='{% if record.dibuat_oleh %}{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}}){% else %}<p>-</p>{% endif %}')
    fotmat_doc = TemplateColumn(template_code='<a target="_blank" href="/media/{{record.fotmat_doc}}" style="display:flex; align-items: center; justify-content: left; font-size: 20px;"><img class="pdf_icon" src="/static/img/word_icon.png" style="height: 20px; width: 20px"></a>', verbose_name="File Penawaran Word")
    format_xls = TemplateColumn(template_code='<a target="_blank" href="/media/{{record.format_xls}}" style="display:flex; align-items: center; justify-content: left; font-size: 20px;"><img class="pdf_icon" src="/static/img/xls_icon.png" style="height: 20px; width: 20px"></a>', verbose_name="File Penawaran Excel")
    item = tables.Column(verbose_name="Objek Seleksi")
    class Meta:
        model = models.format_dokumen_bc
        empty_text = "Tidak ada data"
        orderable = False
       
       # attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("item","judul","nomor", "tgl_penetapan","keterangan",  "fotmat_doc", "format_xls",  "dibuat_oleh",  "diubah_oleh", "created", "last_updated",  )

# view only
class dokumen_persyaratan2_Table(tables.Table):
    item = tables.Column(verbose_name="Objek Seleksi")
    tgl_penetapan = tables.DateTimeColumn(format ='d M Y H:i:s')
    # last_updated = tables.DateTimeColumn(format ='d M Y H:i:s')
    #dokumen_bc = TemplateColumn(template_code='<div style="display:flex;"><a href="/media/{{record.dokumen_bc}}"><i class="fa-solid fa-eye"></i></a></div>')
    fotmat_doc = TemplateColumn(template_code='<a target="_blank" href="/media/{{record.fotmat_doc}}" style="display:flex; align-items: center; justify-content: left; font-size: 20px;"><img class="pdf_icon" src="/static/img/word_icon.png" style="height: 20px; width: 20px"></a>', verbose_name="File Penawaran Word")
    format_xls = TemplateColumn(template_code='<a target="_blank" href="/media/{{record.format_xls}}" style="display:flex; align-items: center; justify-content: left; font-size: 20px;"><img class="pdf_icon" src="/static/img/xls_icon.png" style="height: 20px; width: 20px"></a>', verbose_name="File Penawaran Excel")
    
    class Meta:
        model = models.format_dokumen_bc
        empty_text = "Tidak ada data"
        orderable = False
        
        #attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("item","judul", "nomor", "tgl_penetapan", "keterangan", "fotmat_doc", "format_xls")
        
class dokumen_persyaratan3_Table(tables.Table):
    item = tables.Column(verbose_name="Objek Seleksi")
    last_updated = tables.DateTimeColumn(format ='d M Y H:i:s',  verbose_name="Tanggal Pemasukkan")
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}})', verbose_name="Nama Perwakilan")
    bidder = tables.TemplateColumn(template_code='{{record.bidder.bidder.nama_perusahaan}}', verbose_name="Nama Perusahaan")
    class Meta:
        model = models.dokumen_bc
        empty_text = "Tidak ada data"
        orderable = False
        
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("item", "bidder","dibuat_oleh", "last_updated",)
        

class input_penilaian_Table(tables.Table):
    #Aksi = TemplateColumn(template_code='<div class="" style="display: flex;"><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    # dibawah ini pada aksi, tombol delete dihilangkan sedangkan tombol delete tetap masih ada di atas
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex;"><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button></div>')
    bobot = TemplateColumn(verbose_name="Bobot Penilaian",attrs={"td": {"align": "right"}}, template_code='{{record.parameter.bobot}}')
    item = tables.Column(verbose_name="Objek Seleksi")
    penilaian = tables.Column(verbose_name="Nilai Total",attrs={"td": {"align": "right"}})
    last_updated = tables.DateTimeColumn(format ='d M Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d M Y H:i:s',  verbose_name="Tanggal Dibuat")
    diubah_oleh = TemplateColumn(template_code='{% if record.diubah_oleh %}{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}}){% else %}<p>-</p>{% endif %}')
    dibuat_oleh = TemplateColumn(template_code='{% if record.dibuat_oleh %}{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}}){% else %}<p>-</p>{% endif %}')
    class Meta:
        model = models.penilaian_bc
        empty_text = "Tidak ada data"
        orderable = False
       # attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("item", "parameter","bobot", "penilaian","hasil_evaluasi","keterangan", "dibuat_oleh", "diubah_oleh", "created", "last_updated", )

class input_penilaian_Table2(tables.Table):
    bidder=tables.Column(verbose_name="Nama Perusahaan")
    class Meta:
        model = models.penilaian_bc
        empty_text = "Tidak ada data"
        orderable = False
        #attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("bidder","parameter","penilaian","hasil_evaluasi","keterangan")

class sum_penilaian_Table2(tables.Table):
    bidder=tables.Column(verbose_name="Nama Perusahaan")
    item = tables.Column(verbose_name="Objek Seleksi")
    sum = TemplateColumn(verbose_name="Total Nilai", attrs={"td": {"align": ""}},template_code='{{ record.sum|floatformat:"2g" }}')
    class Meta:
        model = models.sum_penilaian
        empty_text = "Tidak ada data"
        orderable = False
        # attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("bidder","item","sum",)


class hasil_Table2(tables.Table):
    bidder=tables.Column(verbose_name="Nama Perusahaan")
    penilaian = TemplateColumn(verbose_name="Total Nilai", attrs={"td": {"align": ""}},template_code='{{ record.penilaian|floatformat:"2g" }}')
    item = tables.Column(verbose_name="Objek Seleksi")
    ranking = tables.Column(verbose_name="Peringkat")
    class Meta:
        model = models.hasil_beauty_contest
        empty_text = "Tidak ada data"
        orderable = False
        # attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/cards.html"
        fields = ("bidder","item","penilaian","ranking")

class obyek_seleksi_groupTable(tables.Table):
    item = tables.Column(verbose_name="Objek Seleksi")
    class Meta:
        model = models.obyek_seleksi_bc
        template_name = "django_tables2/bootstrap.html"
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "item",
        )

class obyek_seleksiTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    diubah_oleh = TemplateColumn(template_code='{% if record.diubah_oleh %}{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}}){% else %}<p>-</p>{% endif %}')
    #dibuat_oleh = TemplateColumn(template_code='{% if record.dibuat_oleh %}{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}}){% else %}<p>-</p>{% endif %}')
    created = tables.DateTimeColumn(verbose_name="Tanggal Dibuat", format ='d M Y H:i:s')
    last_updated = tables.DateTimeColumn(format ='d M Y H:i:s', verbose_name="Tanggal Diubah")
    item = tables.Column(verbose_name="Objek Seleksi")
    bidder_user = tables.Column(verbose_name="Nama Perusahaan")
    block = tables.Column(verbose_name="Jumlah Blok")
    class Meta:
        model = models.obyek_seleksi_bc
        template_name = "django_tables2/bootstrap.html"
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "item",
            "bidder_user",
            "block",
            "created", 
            "last_updated", 
            "diubah_oleh", 
            #"dibuat_oleh",
            "actions"
        )
class obyek_seleksi2Table(tables.Table):
    #diubah_oleh = TemplateColumn(template_code='{% if record.diubah_oleh %}{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}}){% else %}<p>-</p>{% endif %}')
    #dibuat_oleh = TemplateColumn(template_code='{% if record.dibuat_oleh %}{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}}){% else %}<p>-</p>{% endif %}')
    #created = tables.DateTimeColumn(verbose_name="Dibuat Pertama", format ='d M Y H:i:s')
    last_updated = tables.DateTimeColumn(format ='d M Y H:i:s', verbose_name="Tanggal Diubah")
    item = tables.Column(verbose_name="Objek Seleksi")
    block = tables.Column(verbose_name="Jumlah Blok")
    class Meta:
        model = models.obyek_seleksi_bc
        template_name = "django_tables2/bootstrap.html"
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "item","block",
            #"created", 
            "last_updated"#, "diubah_oleh", "dibuat_oleh",
        )        
