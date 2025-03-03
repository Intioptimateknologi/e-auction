import django_tables2 as tables
from . import models
from django_tables2 import TemplateColumn


class obyek_seleksiTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit circle-icon"></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-sm btn-danger"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    created = tables.DateTimeColumn(verbose_name="Tanggal Dibuat", format ='d F Y H:i:s')
    last_updated = tables.DateTimeColumn(verbose_name="Tanggal Diubah", format ='d F Y H:i:s')
    bidder_user = tables.Column(verbose_name="Nama Perusahaan")
    block = tables.Column(verbose_name="Jumlah Blok")
    class Meta:
        model = models.obyek_seleksi_sampul2
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "item",
            "bidder_user",
            "block",
            "created", 
            "last_updated",  
            "dibuat_oleh",
            "diubah_oleh",
            "actions"
        )
class obyek_seleksi2Table(tables.Table):
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    #created = tables.DateTimeColumn(verbose_name="Dibuat Pertama", format ='d F Y H:i:s')
    last_updated = tables.DateTimeColumn(verbose_name="Tanggal Diubah", format ='d F Y H:i:s')
    item = tables.Column(verbose_name="Obyek Seleksi")
    class Meta:
        model = models.obyek_seleksi_sampul2
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "item",
            "last_updated")#, "diubah_oleh", "dibuat_oleh",)

class penawaranTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit circle-icon"></i>&nbsp;&nbsp;Ubah</button> </div>')
    harga = TemplateColumn(verbose_name="Nilai Penawaran per Blok",attrs={"td": {"align": "right"}},template_code='{{ record.harga|floatformat:"2g" }}')
    dokumen_penawaran = TemplateColumn(verbose_name="Penawaran",template_code='<a target="_blank" class="btn btn-info btn-sm" href="{{ record.dokumen_penawaran.url }}"><i class="fa fa-download"></i>&nbsp;&nbsp;Unduh Penawaran</a>')
    verified_by = TemplateColumn(verbose_name="Diverifikasi Oleh", template_code='{% if record.verified_by %}<span>{{record.verified_by.nama_lengkap}} ({{record.verified_by.username}})</span>{% else %}<p>-</p> {% endif %}')
    item = tables.Column(verbose_name="Obyek Seleksi")
    bidder = tables.Column(verbose_name="Nama Perusahaan")
    perwakilan = TemplateColumn(verbose_name="Nama Perwakilan",template_code="<div>{{record.perwakilan.nama_lengkap}}</div>")
    last_updated= TemplateColumn(verbose_name="Tanggal Diubah", template_code="{{record.last_updated}}")
    created= TemplateColumn(verbose_name="Tanggal Dibuat", template_code="{{record.created}}")
    class Meta:
        model = models.penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("bidder", "perwakilan", "item","harga","blok", "dokumen_penawaran","verified", "verified_by", "created", "last_updated",)
        
class penawaran2Table(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit circle-icon"></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    dokumen_penawaran = TemplateColumn(template_code='<a target="_blank" href="{{ record.dokumen_penawaran.url }}" class="btn btn-info btn-sm"><i class="fa fa-file-pdf" data_1="{{record.dokumen_penawaran.url}}" src="/static/img/pdf.png"></i>&nbsp;&nbsp;Unduh Penawaran</a>')
    harga = TemplateColumn(verbose_name="Nilai Penawaran per Blok", template_code='{{ record.harga|floatformat:"2g" }}')
    item = tables.Column(verbose_name="Obyek Seleksi")
    last_updated= TemplateColumn(verbose_name="Tanggal Diubah", template_code="{{record.last_updated}}")
    created= TemplateColumn(verbose_name="Tanggal Dibuat", template_code="{{record.created}}")
    class Meta:
        model = models.penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("item","harga","blok", "dokumen_penawaran","created", "last_updated",)

class hasil_penawaranTable(tables.Table):
    #actions = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit circle-icon"></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    verified_by = TemplateColumn(verbose_name="Diverifikasi Oleh", template_code='{% if record.verified_by %}<span>{{record.verified_by.nama_lengkap}} ({{record.verified_by.username}})</span>{% else %}<p>-</p> {% endif %}')
    last_updated = TemplateColumn(verbose_name="Waktu Diverifikasi",template_code='<span>{{record.last_updated}}</span>')
    item = tables.Column(verbose_name="Obyek Seleksi")
    bidder = tables.Column(verbose_name="Nama Perusahaan")
    perwakilan = TemplateColumn(verbose_name="Nama Perwakilan",template_code="<div>{{record.perwakilan.nama_lengkap}}</div>")
    verified = TemplateColumn(verbose_name="Verifikasi", template_code='{% if record.verified %}<span class="btn bg-success">Sesuai</span>{% else %}<span class="btn bg-danger">Tidak Sesuai</span> {% endif %}')
   
    class Meta:
        model = models.penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("bidder", "perwakilan","item","verified", "last_updated", "verified_by")
class hasil_penawaran2Table(tables.Table):
    #actions = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit circle-icon"></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    verified_by = TemplateColumn(verbose_name="Diverifikasi Oleh", template_code='{% if record.verified_by %}<span>{{record.verified_by.nama_lengkap}} ({{record.verified_by.username}})</span>{% else %}<p>-</p> {% endif %}')
    last_updated = TemplateColumn(verbose_name="Waktu Diverifikasi",template_code='<span>{{record.last_updated}}</span>')
    item = tables.Column(verbose_name="Obyek Seleksi")
    verified = TemplateColumn(verbose_name="Verifikasi", template_code='{% if record.verified %}<span class="btn bg-success">Sesuai</span>{% else %}<span class="btn bg-danger">Tidak Sesuai</span> {% endif %}')
   
    class Meta:
        model = models.penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("item","verified", "last_updated", "verified_by")



class evaluasi_penawaranTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit circle-icon"></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    dokumen = TemplateColumn(verbose_name="Justifikasi",template_code='<a target="_blank" class="btn btn-sm btn-info" href="{{record.dokumen.url}}"><i data_1="{{record.dokumen.url}}" class="fa fa-file-pdf" ></i>&nbsp;&nbsp;Unduh Justifikasi</a>')
    diubah_oleh = TemplateColumn(verbose_name="Diubah Oleh", template_code='<span>{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}})</span>')
    dibuat_oleh = TemplateColumn(verbose_name="Dibuat Oleh", template_code='<span>{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}})</span>')
    last_updated= TemplateColumn(verbose_name="Tanggal Diubah", template_code="{{record.last_updated}}")
    blok = TemplateColumn(template_code='<span>{{record.penawaran.blok}}</span>')
    harga = TemplateColumn(verbose_name="Nilai Penawaran",template_code='<span>{{record.penawaran.harga|floatformat:"2g"}}</span>')
    catatan = tables.Column(verbose_name="Keterangan")
    hasil= TemplateColumn(verbose_name="Hasil Evaluasi", template_code="{% if record.hasil == 'Diterima' %}<span class='btn bg-success'>Diterima</span>{% else %}span class='btn bg-danger'>Tidak Diterima</span>{% endif%}")
    
    class Meta:
        model = models.evaluasi_penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("penawaran", "blok", "harga","hasil","catatan", "dokumen", "last_updated","dibuat_oleh","diubah_oleh", )

class evaluasi_penawaran2Table(tables.Table):
    dokumen = TemplateColumn(verbose_name="Justifikasi",template_code='<a target="_blank" class="btn btn-sm btn-info" href="{{record.dokumen.url}}"><i data_1="{{record.dokumen.url}}" class="fa fa-file-pdf" ></i>&nbsp;&nbsp;Unduh Justifikasi</a>')
    blok = TemplateColumn(template_code='<span>{{record.penawaran.blok}}</span>')
    harga = TemplateColumn(verbose_name="Nilai Penawaran",template_code='<span>{{record.penawaran.harga|floatformat:"2g"}}</span>')
    catatan = tables.Column(verbose_name="Keterangan")
    hasil= TemplateColumn(verbose_name="Hasil Evaluasi", template_code="{% if record.hasil == 'Diterima' %}<span class='btn bg-success'>Diterima</span>{% else %}span class='btn bg-danger'>Tidak Diterima</span>{% endif%}")
    
    class Meta:
        model = models.evaluasi_penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("penawaran", "blok", "harga","hasil","catatan","dokumen", )
        

        
class hasil_sampul2Table(tables.Table):
    harga = TemplateColumn(template_code='<span>{{record.harga|floatformat:"2g"}}</span>')
    item = tables.Column(verbose_name="Obyek Seleksi")

    class Meta:
        model = models.hasil_sampul2
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("bidder", "item", "harga","ranking", )   