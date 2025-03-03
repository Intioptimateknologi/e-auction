import django_tables2 as tables
from . import models
from django_tables2 import TemplateColumn


class obyek_seleksiTable(tables.Table):
    actions = TemplateColumn(template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    dibuat_oleh = TemplateColumn(template_code='{% if record.dibuat_oleh %}{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}}){% else %}<p>-</p>{% endif %}')
    #diubah_oleh = TemplateColumn(template_code='{% if record.diubah_oleh %}{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}}){% else %}<p>-</p>{% endif %}')
    created = tables.DateTimeColumn(verbose_name="Tanggal Dibuat", format ='d M Y H:i:s')
    last_updated = tables.DateTimeColumn(verbose_name="Tanggal Diubah", format ='d M Y H:i:s')
    bidder_user = tables.Column(verbose_name="Nama Perusahaan")
    block = tables.Column(verbose_name="Jumlah Blok")
    class Meta:
        model = models.obyek_seleksi_nego
        template_name = "django_tables2/bootstrap.html"
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "item",
            "bidder_user",
            "block",
            "created", 
            "last_updated", "diubah_oleh", 
            #"dibuat_oleh",
            "actions"
        )
class obyek_seleksi2Table(tables.Table):
    #dibuat_oleh = TemplateColumn(template_code='{% if record.dibuat_oleh %}{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}}){% else %}<p>-</p>{% endif %}')
    #diubah_oleh = TemplateColumn(template_code='{% if record.diubah_oleh %}{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}}){% else %}<p>-</p>{% endif %}')
    #created = tables.DateTimeColumn(verbose_name="Dibuat Pertama", format ='d M Y H:i:s')
    last_updated = tables.DateTimeColumn(verbose_name="Tanggal Diubah", format ='d M Y H:i:s')
    item = tables.Column(verbose_name="Obyek Seleksi")
    class Meta:
        model = models.obyek_seleksi_nego
        template_name = "django_tables2/bootstrap.html"
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "item",
            "last_updated")#, "diubah_oleh", "dibuat_oleh",)

class penawaranTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button> </div>')
    harga = TemplateColumn(attrs={"td": {"align": "right"}},template_code='{{ record.harga|floatformat:"2g" }}')
    dokumen_penawaran = TemplateColumn(verbose_name="Penawaran",template_code='<a target="_blank" href="{{ record.dokumen_penawaran.url }}"><i class="fa fa-download"></i></a>')
    verified_by = TemplateColumn(verbose_name="Diverifikasi Oleh", template_code='{% if record.verified_by %}<span>{{record.verified_by.nama_lengkap}} ({{record.verified_by.username}})</span>{% else %}<p>-</p> {% endif %}')
    item = tables.Column(verbose_name="Obyek Seleksi")
    bidder = tables.Column(verbose_name="Nama Perusahaan")
    perwakilan = TemplateColumn(verbose_name="Nama Perwakilan",template_code="<div>{{record.perwakilan.nama_lengkap}}</div>")
    class Meta:
        model = models.penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/bootstrap.html"
        fields = ("bidder", "perwakilan", "item","harga","blok", "dokumen_penawaran","verified", "verified_by")
        
class penawaran2Table(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    dokumen_penawaran = TemplateColumn(template_code='<a target="_blank" href="{{ record.dokumen_penawaran.url }}"><img class="pdf_icon" data_1="{{record.dokumen_penawaran.url}}" src="/static/img/pdf.png" style="height: 20px; width: 20px"></a>')
    harga = TemplateColumn(template_code='{{ record.harga|floatformat:"2g" }}')
    item = tables.Column(verbose_name="Obyek Seleksi")
    class Meta:
        model = models.penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/bootstrap.html"
        fields = ("item","harga","blok", "dokumen_penawaran",)

class hasil_penawaranTable(tables.Table):
    #actions = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    verified_by = TemplateColumn(verbose_name="Diverifikasi Oleh", template_code='{% if record.verified_by %}<span>{{record.verified_by.nama_lengkap}} ({{record.verified_by.username}})</span>{% else %}<p>-</p> {% endif %}')
    last_updated = TemplateColumn(verbose_name="Waktu Diverifikasi",template_code='<span>{{record.last_updated}}</span>')
    item = tables.Column(verbose_name="Obyek Seleksi")
    bidder = tables.Column(verbose_name="Nama Perusahaan")
    perwakilan = TemplateColumn(verbose_name="Nama Perwakilan",template_code="<div>{{record.perwakilan.nama_lengkap}}</div>")
    class Meta:
        model = models.penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/bootstrap.html"
        fields = ("bidder", "perwakilan","item","verified", "last_updated", "verified_by")
class hasil_penawaran2Table(tables.Table):
    #actions = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    verified_by = TemplateColumn(verbose_name="Diverifikasi Oleh", template_code='{% if record.verified_by %}<span>{{record.verified_by.nama_lengkap}} ({{record.verified_by.username}})</span>{% else %}<p>-</p> {% endif %}')
    last_updated = TemplateColumn(verbose_name="Waktu Diverifikasi",template_code='<span>{{record.last_updated}}</span>')
    item = tables.Column(verbose_name="Obyek Seleksi")
    class Meta:
        model = models.penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/bootstrap.html"
        fields = ("item","verified", "last_updated", "verified_by")

class revisi_penawaranTable(tables.Table):
    harga = TemplateColumn(attrs={"td": {"align": "right"}},template_code='{{ record.harga|floatformat:"2g" }}')
    dokumen_penawaran = TemplateColumn(verbose_name="Revisi Penawaran",template_code='<a target="_blank" href="{{ record.dokumen_penawaran.url }}"><i class="fa fa-download"></i></a>')
    actions = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button></div>')
    verified_by = TemplateColumn(verbose_name="Diverifikasi Oleh", template_code='{% if record.verified_by %}<span>{{record.verified_by.nama_lengkap}} ({{record.verified_by.username}})</span>{% else %}<p>-</p> {% endif %}')
    item = tables.Column(verbose_name="Obyek Seleksi")
    bidder = tables.Column(verbose_name="Nama Perusahaan")
    perwakilan = TemplateColumn(verbose_name="Nama Perwakilan",template_code="<div>{{record.perwakilan.nama_lengkap}}</div>")
    class Meta:
        model = models.revisi_penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/bootstrap.html"
        fields = ("bidder","perwakilan","item","harga","blok", "keterangan", "dokumen_penawaran","verified", "verified_by",)

class revisi_penawaran2Table(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    harga = TemplateColumn(attrs={"td": {"align": "right"}},template_code='{{ record.harga|floatformat:"2g" }}')
    dokumen_penawaran = TemplateColumn(verbose_name="Revisi Penawaran",template_code='<a target="_blank" href="{{ record.dokumen_penawaran.url }}"><i class="fa fa-download"></i></a>')
    item =tables.Column(verbose_name="Obyek Seleksi")
    dibuat_oleh = TemplateColumn(template_code='{% if record.dibuat_oleh %}{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}}){% else %}<p>-</p>{% endif %}')
    diubah_oleh = TemplateColumn(template_code='{% if record.diubah_oleh %}{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}}){% else %}<p>-</p>{% endif %}')
    class Meta:
        model = models.revisi_penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/bootstrap.html"
        fields = ("item","harga","blok","keterangan", "dokumen_penawaran","dibuat_oleh","diubah_oleh")

class hasil_revisipenawaranTable(tables.Table):
    #actions = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    verified_by = TemplateColumn(verbose_name="Diverifikasi Oleh", template_code='{% if record.verified_by %}<span>{{record.verified_by.nama_lengkap}} ({{record.verified_by.username}})</span>{% else %}<p>-</p> {% endif %}')
    last_updated = TemplateColumn(verbose_name="Waktu Diverifikasi",template_code='<span>{{record.last_updated}}</span>')
    bidder = tables.Column(verbose_name="Nama Perusahaan")
    item = tables.Column(verbose_name="Obyek Seleksi")
    perwakilan = TemplateColumn(verbose_name="Nama Perwakilan",template_code="<div>{{record.perwakilan.nama_lengkap}}</div>")
    class Meta:
        model = models.revisi_penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/bootstrap.html"
        fields = ("bidder","perwakilan","item", "verified", "keterangan","last_updated", "verified_by",)

class hasil_revisipenawaran2Table(tables.Table):
    #actions = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    last_updated = TemplateColumn(verbose_name="Waktu Diverifikasi",template_code='<span>{{record.last_updated}}</span>')
    verified_by = TemplateColumn(verbose_name="Diverifikasi Oleh", template_code='{% if record.verified_by %}<span>{{record.verified_by.nama_lengkap}} ({{record.verified_by.username}})</span>{% else %}<p>-</p> {% endif %}')
    item = tables.Column(verbose_name="Obyek Seleksi")
    class Meta:
        model = models.revisi_penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/bootstrap.html"
        fields = ("item","verified", "keterangan","last_updated", "verified_by",)

class evaluasi_penawaranTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    dokumen = TemplateColumn(template_code='<a target="_blank" href="{{record.dokumen.url}}"><img data_1="{{record.dokumen.url}}" class="pdf_icon" src="/static/img/pdf.png" style="height: 20px; width: 20px"></a>')
    diubah_oleh = TemplateColumn(verbose_name="Diubah Oleh", template_code='{% if record.diubah_oleh %}<span>{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}})</span>{% else %}<p>-</p> {% endif %}')
    dibuat_oleh = TemplateColumn(verbose_name="Dibuat Oleh", template_code='{% if record.dibuat_oleh %}<span>{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}})</span>{% else %}<p>-</p> {% endif %}')
    last_updated= TemplateColumn(verbose_name="Tanggal Diubah", template_code="{{record.last_updated}}")
    blok = TemplateColumn(template_code='<span>{{record.penawaran.blok}}</span>')
    harga = TemplateColumn(verbose_name="Nilai Penawaran",template_code='<span>{{record.penawaran.harga|floatformat:"2g"}}</span>')
    catatan = tables.Column(verbose_name="Keterangan")
    penawaran = tables.Column(verbose_name="Perusahaan")
    class Meta:
        model = models.evaluasi_penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/bootstrap.html"
        fields = ("penawaran", "blok", "harga","hasil","catatan", "dokumen", "dibuat_oleh","diubah_oleh",  "last_updated",)

class evaluasi_penawaran2Table(tables.Table):
    dokumen = TemplateColumn(template_code='<a target="_blank" href="{{record.dokumen.url}}"><img data_1="{{record.dokumen.url}}" "class="pdf_icon" src="/static/img/pdf.png" style="height: 20px; width: 20px"></a>')
    blok = TemplateColumn(template_code='<span>{{record.penawaran.blok}}</span>')
    harga = TemplateColumn(verbose_name="Nilai Penawaran",template_code='<span>{{record.penawaran.harga|floatformat:"2g"}}</span>')
    catatan = tables.Column(verbose_name="Keterangan")
    class Meta:
        model = models.evaluasi_penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/bootstrap.html"
        fields = ("penawaran", "blok", "harga","hasil","catatan","dokumen", )
        
class evaluasi_revisi_penawaranTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    dokumen = TemplateColumn(template_code='<a target="_blank" href="{{record.dokumen.url}}"><img class="pdf_icon" data_1="{{record.dokumen.url}}" src="/static/img/pdf.png" style="height: 20px; width: 20px"></a>')
    # add new code
    blok = TemplateColumn(template_code='<span>{{record.revisi_penawaran.blok}}</span>')
    harga = TemplateColumn(verbose_name="Nilai Penawaran",template_code='<span>{{record.revisi_penawaran.harga|floatformat:"2g"}}</span>')
    #end new code
    last_updated= TemplateColumn(verbose_name="Tanggal Diubah", template_code="{{record.last_updated}}")
    created= TemplateColumn(verbose_name="Tanggal Dibuat", template_code="{{record.created}}")
    catatan = tables.Column(verbose_name="Keterangan")
    class Meta:
        model = models.evaluasi_revisi_penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/bootstrap.html"
        fields = ("revisi_penawaran", "blok","harga","hasil","catatan","dokumen", "created","last_updated", "dibuat_oleh", "diubah_oleh", )

class evaluasi_revisi_penawaran2Table(tables.Table):
    #actions = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="penawaran_update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="penawaran_delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    dokumen = TemplateColumn(template_code='<a target="_blank" href="{{record.dokumen.url}}"><img data_1="{{record.dokumen.url}}" class="pdf_icon" src="/static/img/pdf.png" style="height: 20px; width: 20px"></a>')
    blok = TemplateColumn(template_code='<span>{{record.revisi_penawaran.blok}}</span>')
    harga = TemplateColumn(verbose_name="Nilai Penawaran",template_code='<span>{{record.revisi_penawaran.harga|floatformat:"2g"}}</span>')
    
    class Meta:
        model = models.evaluasi_revisi_penawaran
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/bootstrap.html"
        fields = ("revisi_penawaran", "blok", "harga","hasil","catatan","dokumen", )
        
class hasil_negosiasiTable(tables.Table):
    harga = TemplateColumn(template_code='<span>{{record.harga|floatformat:"2g"}}</span>')
    item = tables.Column(verbose_name="Obyek Seleksi")

    class Meta:
        model = models.hasil_negosiasi
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/bootstrap.html"
        fields = ("bidder", "item", "harga","ranking", )