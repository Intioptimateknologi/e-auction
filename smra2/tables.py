import django_tables2 as tables
from . import models
from django_tables2 import TemplateColumn
from adm_lelang.models import detail_itemlelang
import itertools
from background_task.models import Task as BTask

class hasil_smra2Table(tables.Table):
    submit = tables.DateTimeColumn(verbose_name="Waktu Penawaran",format ='M d Y, h:i:s.u A')
    class Meta:
        model = models.hasil_smra2
        template_name = "django_tables2/custom_bootstrap_tengah.html"
#        attrs = {"class": "table table-striped"}
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "item",
            "round",
            "price",
            "block",
            "submit"
        )

class item_lelang_detailTable(tables.Table):
    aksi = TemplateColumn(template_code='<div class="" style="display: flex; justify-content: center;"><button  id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    harga_minimal = TemplateColumn(verbose_name="Harga Dasar Penawaran",attrs={"td": {"align": "right"}},template_code='{{ record.harga_minimal|floatformat:"2g" }}')
    spectrum_cap = tables.Column(attrs={"td": {"align": "center"}})
    band = TemplateColumn(verbose_name="Obyek Seleksi",template_code='<b>{{ record.band}}-{{ record.cakupan}}</b>')
    max_block = tables.Column(verbose_name="Total Blok")
    bandwidth = tables.Column(verbose_name="Lebar Pita Per Blok", attrs={"td": {"align": "left"}})
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    created = tables.DateTimeColumn(verbose_name="Tanggal Dibuat", format ='d F Y H:i:s')
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s')
    disabled=TemplateColumn(verbose_name="Status",template_code='{% if record.disabled%}<span class="btn bg-danger">Tidak Digunakan</span>{% else %}<span class="btn bg-success">Digunakan</span>{% endif%}')
    class Meta:
        model = detail_itemlelang
        empty_text = "Tidak ada data"
        orderable = False
#        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("band", "bandwidth","max_block","spectrum_cap", "harga_minimal", "disabled", "created", "last_updated", "diubah_oleh", "dibuat_oleh","aksi"
)

class obyek_seleksi_groupTable(tables.Table):
    class Meta:
        model = models.obyek_seleksi_smra
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "item",
        )

class price_increaseTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    rentang_max = TemplateColumn(verbose_name="Batas Atas", attrs={"td": {"align": "right"}},template_code='Rp{{ record.rentang_max|floatformat:"2g" }}')
    rentang_min = TemplateColumn(verbose_name="Batas Bawah",attrs={"td": {"align": "right"}},template_code='Rp{{ record.rentang_min|floatformat:"2g" }}')
    kenaikan = tables.Column(attrs={"td": {"align": "right"}})
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    created = tables.DateTimeColumn(verbose_name="Tanggal Dibuat", format ='d F Y H:i:s')
    last_updated = tables.DateTimeColumn(verbose_name="Tanggal Diubah", format ='d F Y H:i:s')
    detail_item=tables.Column(verbose_name="Obyek Seleksi")
    class Meta:
        model = models.price_increase
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        empty_text = "Tidak ada data"
        orderable = True
        fields = (
            "detail_item",
            "rentang_min",
            "rentang_max",
            "kenaikan",
            "created", 
            "last_updated", 
            "diubah_oleh", 
            "dibuat_oleh",
            "actions",
        )
        
class obyek_seleksiTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    created = tables.DateTimeColumn(verbose_name="Tanggal Dibuat", format ='d F Y H:i:s')
    last_updated = tables.DateTimeColumn(verbose_name="Tanggal Diubah", format ='d F Y H:i:s')
    bidder_user = tables.Column(verbose_name="Nama Penawaran")
    class Meta:
        model = models.obyek_seleksi_smra
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "item",
            "bidder_user",
            "blok_awal",
            "ipaddress",
            "created", 
            "last_updated", 
            "diubah_oleh", 
            "dibuat_oleh",
            "actions"
        )
class obyek_seleksi2Table(tables.Table):
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    #created = tables.DateTimeColumn(verbose_name="Dibuat Pertama", format ='d F Y H:i:s')
    last_updated = tables.DateTimeColumn(verbose_name="Tanggal Diubah", format ='d F Y H:i:s')
    class Meta:
        model = models.obyek_seleksi_smra
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "item",
            "blok_awal",
            #"created", 
            "last_updated"#, "diubah_oleh", "dibuat_oleh",
        )

class hasil_smra2Table(tables.Table):
    submit = tables.DateTimeColumn(verbose_name="Waktu Penawaran", format ='M d Y, h:i:s.u A')
    price = TemplateColumn(verbose_name="Harga Penawaran Per Blok", attrs={"td": {"align": "right"}},template_code='{{ record.price|floatformat:"2g" }}')
    berita_acara_unsigned = TemplateColumn(verbose_name="Formulir Penawaran Harga",template_code='<a class="btn btn-info" target="_blank" href="{{ record.berita_acara.url }}"><i class="fa fa-download"></i> Unduh</a>')
    item = tables.Column(verbose_name="Obyek Seleksi")
    round = tables.Column(verbose_name="Putaran")
    block = tables.Column(verbose_name="Jumlah Blok")
    class Meta:
        model = models.hasil_smra2
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "django_tables2/custom_bootstrap_tengah.html"
#        attrs = {"class": "table table-striped"}
        fields = (
            "round",
            "item",
            "block",
            "price",
            
            "submit",
            "berita_acara_unsigned",
            #"berita_acara"
        )

class hasilvalid_smra2Table(tables.Table):
    last_updated = tables.DateTimeColumn(verbose_name="Waktu Penawaran", format ='M d Y, h:i:s.u A')
    price = TemplateColumn(verbose_name="Harga Penawaran Per Blok", attrs={"td": {"align": "right"}},template_code='{{ record.price|floatformat:"2g" }}')
    berita_acara = TemplateColumn(verbose_name="Formulir Penawaran Harga",template_code='<a class="btn btn-info" target="_blank" href="{% if record.berita_acara %}{{ record.berita_acara.url }}{% endif %}"><i class="fa fa-download"></i> Unduh</a>')
    item = tables.Column(verbose_name="Obyek Seleksi")
    round = tables.Column(verbose_name="Putaran")
    block = tables.Column(verbose_name="Jumlah Blok")
    class Meta:
        model = models.hasil_smra2
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "django_tables2/custom_bootstrap_tengah.html"
#        attrs = {"class": "table table-striped"}
        fields = (
            "round",
            "item",
            "block",
            "price",
            "last_updated",
            "berita_acara"
        )

class hasil2_smra2Table(tables.Table):
    #counter = tables.Column(empty_values=(), orderable=False)
    submit = tables.DateTimeColumn(verbose_name="Waktu Penawaran", format ='M d Y, h:i:s.u A')
    price = TemplateColumn(verbose_name="Harga Penawaran", attrs={"td": {"align": "right"}},template_code='<b>{{ record.price|floatformat:"2g" }}</b>')
    item = tables.Column(verbose_name="Obyek Seleksi")
    round = TemplateColumn(verbose_name="Putaran", template_code='{%if record.jenis == "KHUSUS" %} <span class="btn bg-primary text-bold">{{ record.round }} [Khusus]</span> {% else %} <span class="btn bg-primary text-bold">{{ record.round }}</span> {% endif %}')
    ranking_putaran = TemplateColumn(verbose_name="Rangking", template_code='<span class="btn bg-danger">{{ record.ranking_putaran }}</span>')
    class Meta:
        model = models.hasil2_smra
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "django_tables2/custom_bootstrap_tengah.html"
#        attrs = {"class": "table table-striped"}
        fields = (
            "round",
            "item",
            "price",
            "submit",
            "ranking_putaran",
        )
    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count())
        return next(self.row_counter)

class hasil5_smra2Table(tables.Table):
    #counter = tables.Column(empty_values=(), orderable=False)
    submit = tables.DateTimeColumn(verbose_name="Waktu Penawaran", format ='M d Y, h:i:s.u A')
    price = TemplateColumn(verbose_name="Harga Penawaran", attrs={"td": {"align": "right"}},template_code='<b>{{ record.price|floatformat:"2g" }}</b>')
    item = tables.Column(verbose_name="Obyek Seleksi")
    round = TemplateColumn(verbose_name="Putaran", template_code='{%if record.jenis == "KHUSUS" %} <span class="btn bg-primary text-bold">{{ record.round }} [Khusus]</span> {% else %} <span class="btn bg-primary text-bold">{{ record.round }}</span> {% endif %}')
    ranking = TemplateColumn(verbose_name="Rangking", template_code='<span class="btn bg-danger">{{ record.ranking }}</span>')
    class Meta:
        model = models.hasil2_smra
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "django_tables2/custom_bootstrap_tengah.html"
#        attrs = {"class": "table table-striped"}
        fields = (
            "round",
            "item",
            "bidder",
            "price",
            "submit",
            "ranking",
        )
    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count())
        return next(self.row_counter)

class hasil2_smra2Table2(tables.Table):
    submit = tables.DateTimeColumn(verbose_name="Waktu Penawaran", format ='M d Y, h:i:s.u A')
    price = TemplateColumn(verbose_name="Harga Penawaran", attrs={"td": {"align": "right"}},template_code='<b>{{ record.price|floatformat:"2g" }}</b>')
    item = tables.Column(verbose_name="Obyek Seleksi")
    round = TemplateColumn(verbose_name="Putaran", template_code='{%if record.jenis == "KHUSUS" %} <span class="btn bg-primary text-bold">{{ record.round }} [Khusus]</span> {% else %} <span class="btn bg-primary text-bold">{{ record.round }}</span> {% endif %}')
    ranking_putaran = TemplateColumn(verbose_name="Rangking", template_code='<span class="btn bg-danger">{{ record.ranking_putaran }}</span>')
    class Meta:
        model = models.hasil2_smra
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "django_tables2/custom_bootstrap_tengah.html"
#        attrs = {"class": "table table-striped"}
        fields = (
            "round",
            "bidder",
            "price",
            "submit",
            "ranking_putaran",
        )

class hasil2_smra2_auctioneerTable2(tables.Table):
    submit = tables.DateTimeColumn(verbose_name="Waktu Penawaran", format ='M d Y, h:i:s.u A')
    price = TemplateColumn(verbose_name="Harga Penawaran", attrs={"td": {"align": "right"}},template_code='<b>{% if record.ranking_putaran %}{{ record.price|floatformat:"2g" }}{% endif %}</b>')
    item = tables.Column(verbose_name="Obyek Seleksi")
    round = TemplateColumn(verbose_name="Putaran", template_code='{%if record.jenis == "KHUSUS" %} <span class="btn bg-primary text-bold">{{ record.round }} [Khusus]</span> {% else %} <span class="btn bg-primary text-bold">{{ record.round }}</span> {% endif %}')
    ranking_putaran = TemplateColumn(verbose_name="Rangking", template_code='<span class="btn bg-danger">{{ record.ranking_putaran }}</span>')
    class Meta:
        model = models.hasil2_smra
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "django_tables2/custom_bootstrap_tengah.html"
#        attrs = {"class": "table table-striped"}
        fields = (
            "round",
            "bidder",
            "price",
            "submit",
            "ranking_putaran",
        )

class hasil_smra2_auctionerTable(tables.Table):
    submit = tables.DateTimeColumn(verbose_name="Waktu Penawaran", format ='M d Y, h:i:s.u A')
    price = TemplateColumn(verbose_name="Harga Penawaran", attrs={"td": {"align": "right"}},template_code='{{ record.price|floatformat:"2g" }}')
    berita_acara_unsigned = TemplateColumn(verbose_name="BA tanpa Ttd",template_code='<a target="_blank" href="{{ record.berita_acara_unsigned.url }}"><i class="fa fa-download"></i></a>')
    item = tables.Column(verbose_name="Obyek Seleksi")
    row_number = TemplateColumn(verbose_name="Urutan",template_code='{{ record.row_number|add:"1" }}')
    round = tables.Column(verbose_name="Putaran")
    bidder = tables.Column(verbose_name="Nama Penawaran")
    class Meta:
        model = models.hasil_smra2
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "django_tables2/custom_bootstrap_tengah.html"
#        attrs = {"class": "table table-striped"}
        fields = (
            "row_number",
            "round",
            "bidder",
            "item",
            "price",
            "submit",
            "berita_acara_unsigned",
            #"berita_acara"
        )

class hasil_valid_smra2Table(tables.Table):
    last_updated = tables.DateTimeColumn(verbose_name="Waktu Penawaran", format ='M d Y, h:i:s A')
    price = TemplateColumn(verbose_name="Harga Penawaran", attrs={"td": {"align": "right"}},template_code='{{ record.price|floatformat:"2g" }}')
    berita_acara_unsigned = TemplateColumn(verbose_name="Formulir Penawaran Harga",template_code='<a target="_blank" href="{% if record.berita_acara_unsigned %}{{ record.berita_acara_unsigned.url }}{% endif %}"><i class="fa fa-download"></i></a>')
    berita_acara = TemplateColumn(verbose_name="Formulir Penawaran Harga Valid",template_code='<a target="_blank" href="{% if record.berita_acara %}{{ record.berita_acara.url }}{% endif %}"><i class="fa fa-download"></i></a>')
    item = tables.Column(verbose_name="Obyek Seleksi")
    round = tables.Column(verbose_name="Putaran")
    class Meta:
        model = models.hasil_smra2
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "django_tables2/custom_bootstrap_tengah.html"
#        attrs = {"class": "table table-striped"}
        fields = (
            "round",
            "ranking_putaran",
            "item",
            "price",
            "last_updated",
            "berita_acara_unsigned",
            "berita_acara"
        )

class auctioner_hasilTable(tables.Table):
    harga = TemplateColumn(attrs={"td": {"align": "right"}},template_code='{{ record.harga|floatformat:"2g" }}')
    increase = TemplateColumn(verbose_name= 'Kenaikan Harga (%)', attrs={"td": {"align": "right"}},template_code='{{ record.increase|floatformat:"2g" }}%')
    class Meta:
        model = models.auctioner_hasil
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = (
            "round",
            "harga",
            "block",
            "increase"
        )

class auctioner_hasil_maxminTable(tables.Table):
    harga_max = TemplateColumn(attrs={"td": {"align": "right"}},template_code='{{ record.harga_max|floatformat:"2g" }}')
    harga_minimal = TemplateColumn(attrs={"td": {"align": "right"}},template_code='{{ record.harga_minimal|floatformat:"2g" }}')
    persen1 = TemplateColumn(verbose_name="Kenaikan terhadap harga minimal (%)", attrs={"td": {"align": "right"}},template_code='{{ record.persen1|floatformat:"2g" }}')
    class Meta:
        model = models.hasil_auctioner_maxmin
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = (
            "round",
            "harga_max",
#            "harga_min",
            "harga_minimal",
            "persen1"
#            "block_max",
#            "block_min"
        )

class auctioner_highestTable(tables.Table):
    price = TemplateColumn(attrs={"td": {"align": "right"}},template_code='{{ record.price|floatformat:"2g" }}')
    item = tables.Column(verbose_name="Obyek Seleksi")
    submit = TemplateColumn(verbose_name="Waktu Penawaran", template_code='{{record.submit|date:"d F Y H:i:s.u"}}')
    #bidder = tables.Column(accessor = 'bidder.nama_perusahaan}')
    bidder = tables.Column(verbose_name="Nama Penawaran")

    class Meta:
        model = models.hasil_highest
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = (
            "bidder",
            "item",
            "round",
            "price",
            "block",
            "submit"
        )


class hasil_smra2PivotTable(tables.Table):
    static_column = tables.Column()


class scheduler_smra2Table(tables.Table):
    run_at = tables.DateTimeColumn(verbose_name="Jadwal",format ='M d Y, h:i:s A')
    verbose_name = tables.Column(verbose_name="Tipe Penjadwalan")
    class Meta:
        model = BTask
        template_name = "django_tables2/custom_bootstrap_tengah.html"
#        attrs = {"class": "table table-striped"}
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "hari",
            "verbose_name",
            'seleksi',
            "run_at",
        )

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
        model = models.round_schedule_smra2
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
        model = models.round_schedule_smra2
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("hari", "mulai", "selesai", 
        #"created", 
        "last_updated",) #"diubah_oleh", "dibuat_oleh")