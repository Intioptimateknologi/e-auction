import django_tables2 as tables
from . import models
from adm_lelang.models import detail_itemlelang
from django_tables2 import TemplateColumn


class obyek_seleksiTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    diubah_oleh = TemplateColumn(template_code='{% if record.diubah_oleh %}{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}}){% else %}<p>-</p>{% endif %}')
    #dibuat_oleh = TemplateColumn(template_code='{% if record.dibuat_oleh %}{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}}){% else %}<p>-</p>{% endif %}')
    created = tables.DateTimeColumn(verbose_name="Tanggal Dibuat", format ='d M Y H:i:s')
    last_updated = tables.DateTimeColumn(verbose_name="Tanggal Diubah",format ='d M Y H:i:s')
    class Meta:
        model = models.obyek_seleksi_cca
        template_name = "django_tables2/bootstrap.html"
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "item",
            "bidder_user",
            "eli_awal",
            "ipaddress",
            "created", 
            "last_updated", "diubah_oleh", 
            #"dibuat_oleh",
            "actions"
        )

class item_lelang_detailTable(tables.Table):
    aksi = TemplateColumn(template_code='<div class="" style="display: flex; justify-content: center;"><button data-toggle="tooltip" data-placement="right" title="Sunting" id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button data-toggle="tooltip" data-placement="right" title="Hapus" id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    harga_minimal = TemplateColumn(verbose_name="Harga Dasar Penawaran",attrs={"td": {"align": "right"}},template_code='{{ record.harga_minimal|floatformat:"2g" }}')
    spectrum_cap = tables.Column(attrs={"td": {"align": "center"}})
    band = tables.Column(verbose_name="Obyek Seleksi")
    max_block = tables.Column(verbose_name="Jumlah Blok Tersedia")
    bandwidth = tables.Column(verbose_name="Lebar Pita Per Blok", attrs={"td": {"align": "left"}})
    diubah_oleh = TemplateColumn(template_code='{% if record.diubah_oleh %}{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}}){% else %}<p>-</p>{% endif %}')
    dibuat_oleh = TemplateColumn(template_code='{% if record.dibuat_oleh %}{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}}){% else %}<p>-</p>{% endif %}')
    created = tables.DateTimeColumn(verbose_name="Tanggal Dibuat", format ='d M Y H:i:s')
    last_updated = tables.DateTimeColumn(format ='d M Y H:i:s')
    class Meta:
        model = detail_itemlelang
        empty_text = "Tidak ada data"
        orderable = False
#        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = ("band","max_block", "bandwidth","spectrum_cap", "harga_minimal", "eligibility_point_per_block","disabled", "created", "last_updated", "diubah_oleh", "dibuat_oleh","aksi"
)

class obyek_seleksi2Table(tables.Table):
    #diubah_oleh = TemplateColumn(template_code='{% if record.diubah_oleh %}{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}}){% else %}<p>-</p>{% endif %}')
    #dibuat_oleh = TemplateColumn(template_code='{% if record.dibuat_oleh %}{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}}){% else %}<p>-</p>{% endif %}')
    #created = tables.DateTimeColumn(verbose_name="Dibuat Pertama", format ='d M Y H:i:s')
    last_updated = tables.DateTimeColumn(format ='d M Y H:i:s',verbose_name="Tanggal Diubah")
    class Meta:
        model = models.obyek_seleksi_cca
        template_name = "django_tables2/bootstrap.html"
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "item",
            "eli_awal",
            #"created", 
            "last_updated"#, "diubah_oleh", "dibuat_oleh",
        )

class round_ccaTable(tables.Table):
    min_price = TemplateColumn(verbose_name="Harga Minimal", attrs={"td": {"align": "right"}},template_code='{{ record.min_price|floatformat:"2g" }}')
    price = TemplateColumn(verbose_name="Harga", attrs={"td": {"align": "right"}},template_code='{{ record.price|floatformat:"2g" }}')
    eli_point = TemplateColumn(verbose_name="Eligibility", attrs={"td": {"align": "right"}},template_code='{{ record.eli_point|floatformat }}')
    item = TemplateColumn(verbose_name="Obyek Seleksi", attrs={"td": {"class": "text-bold"}},template_code='{{ record.item }}')
    class Meta:
        model = models.round_cca
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-striped"}
        fields = (
            "item",
            "max_block",
            "spectrum_cap",
            "eli_point",
            "activity",
            "prev_block",
            "min_price",
            "block",
            "price",
        )

class round_detail_ccaTable(tables.Table):
    prev_price = TemplateColumn(verbose_name="Harga Sebelumnya",attrs={"td": {"align": "right"}},template_code='{{ record.prev_price|floatformat:"2g" }}')
    prev_blocl = TemplateColumn(verbose_name="Blok Sebelumnya",attrs={"td": {"align": "right"}},template_code='{{ record.prev_block|floatformat:"2g" }}')
    harga_minimal = TemplateColumn(attrs={"td": {"align": "right"}},template_code='{{ record.harga_minimal|floatformat:"2g" }}')
    eli_per_block = TemplateColumn(verbose_name="Eligibility per Blok",attrs={"td": {"align": "right"}},template_code='{{ record.eli_per_block|floatformat }}')
    band = TemplateColumn(attrs={"td": {"class": "text-bold"}},template_code='{{ record.item }}')
    max_block = TemplateColumn(verbose_name="Maksimum Blok", attrs={"td": {"class": "text-bold"}},template_code='{{ record.item.max_block }}')
    spectrum_cap = TemplateColumn(verbose_name="Kapasitas Spektrum", attrs={"td": {"class": "text-bold"}},template_code='{{ record.item.spectrum_cap }}')
    class Meta:
        model = models.round_detail_cca
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-striped"}
        fields = (
            "band",
            "max_block",
            "spectrum_cap",
            "eli_per_block",
            "harga_minimal",
        )

class hasil_ccaTable(tables.Table):
    parent__submit = tables.DateTimeColumn(verbose_name="Tanggal Kirim", format ='M d Y, h:i:s.u A')
    item = tables.Column(verbose_name="Obyek Seleksi")
    price = TemplateColumn(verbose_name="Harga Penawaran", attrs={"td": {"align": "right"}},template_code='{{ record.price|floatformat:"2g" }}')
    parent__berita_acara = TemplateColumn(verbose_name="BA tanpa Ttd", template_code='{% if record.parent.berita_acara %}<a target="blank" href="{{ record.parent.berita_acara.url }}">Unduh</a>{% else %} - {% endif %}')
    parent__berita_acara_unsigned = TemplateColumn(verbose_name="BA dengan Ttd", template_code='{% if record.parent.berita_acara_unsigned %}<a target="blank" href="{{ record.parent.berita_acara_unsigned.url }}">Unduh</a>{% else %} - {% endif %}')
    class Meta:
        model = models.hasil_cca
        attrs = {"class": "table table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "item",
            #parent__round",
            "price",
            "parent__submit",
            "parent__berita_acara",
            "parent__berita_acara_unsigned",
            "ranking_putaran"
        )


class auctioner_hasilTable(tables.Table):
    item = tables.Column(verbose_name="Obyek Seleksi")
    parent__submit = tables.DateTimeColumn(verbose_name="Tanggal Kirim", format ='M d Y, h:i A')
    price = TemplateColumn(verbose_name="Harga Penawaran", attrs={"td": {"align": "right"}},template_code='{{ record.price|floatformat:"2g" }}')
    parent__berita_acara = TemplateColumn(verbose_name="BA tanpa Ttd", template_code='{% if record.parent.berita_acara %}<a target="blank" href="{{ record.parent.berita_acara.url }}">Unduh</a>{% else %} - {% endif %}')
    parent__berita_acara_unsigned = TemplateColumn(verbose_name="BA dengan Ttd", template_code='{% if record.parent.berita_acara_unsigned %}<a target="blank" href="{{ record.parent.berita_acara_unsigned.url }}">Unduh</a>{% else %} - {% endif %}')
    class Meta:
        model = models.hasil_cca
        attrs = {"class": "table table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "item",
            "parent__bidder",
            "parent__round",
            "price",
            "parent__submit",
            "parent__berita_acara",
            "parent__berita_acara_unsigned",
            "ranking_putaran",
        )

class matrix_hasil_crTable(tables.Table):
    total = TemplateColumn(attrs={"td": {"align": "right"}},template_code='{{ record.total|floatformat:"2g" }}')
    json_agg = TemplateColumn(verbose_name="Kombinasi",template_code='<table class="w-100"><tr><th>Pita</th><th>Blok</th><th>Penawaran</th></tr>{% for key in record.json_agg %}<tr><td>{{ key.item }}</td><td>{{key.block}}</td><td>{{key.price|floatformat:"2g"}}</td></tr>{% endfor %}</table>')
    actions = TemplateColumn(verbose_name="Koreksi", template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.parent.round }}" class="koreksi btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button></div>')

    class Meta:
        model = models.matrix_hasil_cr
        attrs = {"class": "table table-striped"}
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "json_agg",
            "total",
            "actions"
        )

class price_increaseTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    rentang_max = TemplateColumn(verbose_name="Batas Atas", attrs={"td": {"align": "right"}},template_code='{{ record.rentang_max|floatformat:"2g" }}')
    rentang_min = TemplateColumn(verbose_name="Batas Bawah", attrs={"td": {"align": "right"}},template_code='{{ record.rentang_min|floatformat:"2g" }}')
    kenaikan = tables.Column(attrs={"td": {"align": "right"}})
    diubah_oleh = TemplateColumn(template_code='{% if record.diubah_oleh %}{{record.diubah_oleh.nama_lengkap}} ({{record.diubah_oleh.username}}){% else %}<p>-</p>{% endif %}')
    #dibuat_oleh = TemplateColumn(template_code='{% if record.dibuat_oleh %}{{record.dibuat_oleh.nama_lengkap}} ({{record.dibuat_oleh.username}}){% else %}<p>-</p>{% endif %}')
    created = tables.DateTimeColumn(verbose_name="Tanggal Dibuat", format ='d M Y H:i:s')
    #last_updated = tables.DateTimeColumn(format ='d M Y H:i:s')
    detail_item=tables.Column(verbose_name="Obyek Seleksi")
    class Meta:
        model = models.cca_price_increase
        template_name = "django_tables2/bootstrap.html"
        empty_text = "Tidak ada data"
        orderable = False
        fields = (
            "detail_item",
            "rentang_min",
            "rentang_max",
            "kenaikan",
            "created", 
            #"last_updated", 
            "diubah_oleh", 
            #"dibuat_oleh",
            "actions",
        )
