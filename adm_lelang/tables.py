from django.utils.safestring import mark_safe
import django_tables2 as tables
from . import models
from persiapan.models import p_dokumen
from django_tables2 import TemplateColumn

from userman.models import Notifikasi

class item_lelangTable(tables.Table):
    class Meta:
        model = models.item_lelang
        template_name = "tables/table_kebawah.html"
        fields = ("nama_lelang", "keterangan", "tahun")

class item_lelang_detailTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; justify-content: center;"><button data-toggle="tooltip" data-placement="right" title="Sunting" id="{{ record.id }}" class="objek_seleksi_update btn btn-sm btn-warning"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;<button data-toggle="tooltip" data-placement="right" title="Hapus" id="{{ record.id }}" class="objek_seleksi_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    #created = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Dibuat pada")
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Diubah pada")
    band = TemplateColumn(template_code='<span style="font-weight:700;">{{record.band}}</span>')
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}}')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}}')
    class Meta:
        model = models.detail_itemlelang
        empty_text = "Tidak ada data"
        orderable = False
#        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("band","bandwidth","rentang_frekuensi","cakupan","penyelenggaraan","teknologi", "keterangan", )

class item_lelang_detail2Table(tables.Table):
    harga_minimal = TemplateColumn(attrs={"td": {"align": "left"}},template_code='{{ record.harga_minimal|floatformat:"2g" }}')
    spectrum_cap = tables.Column(attrs={"td": {"align": "center"}})
    max_block = tables.Column(verbose_name="Maksimum Blok", attrs={"td": {"align": "center"}})
    eligibility_point_per_block = tables.Column(attrs={"td": {"align": "center"}})
    class Meta:
        empty_text = "Tidak ada data"
        orderable = False
        model = models.detail_itemlelang
#        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap.html"
        fields = ("penyelenggaraan","teknologi","band","bandwidth","rentang_frekuensi","cakupan", "spectrum_cap","max_block", "eligibility_point_per_block","harga_minimal",)

# detail itemlelang yang hanya menampilkan, pita teknologi spectrum cap max block eligility point harga minimal
class nilai_item_lelang_detailTable(tables.Table):
    max_block = tables.Column(verbose_name="Maksimum Blok", attrs={"td": {"align": "center"}})
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; justify-content: center;"><button data-toggle="tooltip" data-placement="right" title="Sunting" id="{{ record.id }}" class="objek_seleksi_update btn btn-sm btn-warning"><i class="fa fa-edit"></i></button></div>')
    harga_minimal = TemplateColumn(attrs={"td": {"align": "left"}},template_code='{{ record.harga_minimal|floatformat:"2g" }}')
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Diubah pada")
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}}')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}}')
    class Meta:
        empty_text = "Tidak ada data"
        orderable = False
        model = models.detail_itemlelang
#        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap.html"
        fields = ("band","spectrum_cap","max_block", "eligibility_point_per_block", "harga_minimal", "keterangan", "last_updated", "dibuat_oleh", "diubah_oleh",)

class pengumuman_Table(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div><button id="{{ record.id }}" class="update btn btn-sm btn-warning"><i class="fa fa-edit"></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-sm btn-danger"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    dokumen = TemplateColumn(template_code='<div><a class="btn btn-info btn-sm" target="_blank" href="{{record.dokumen.url}}"><i class="fa fa-download"></i>&nbsp;&nbsp;Unduh Pengumuman</a></div>')
    tgl_release = tables.DateTimeColumn(format ='d F Y', verbose_name="Tanggal Penetapan")
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(verbose_name="Tanggal Dibuat", format ='d F Y H:i:s')
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    image = tables.TemplateColumn(
        '<a href="{{ record.image.url }}" target="_blank"><img src="{{ record.image.url }}" class="thumbnail" width="100" height="100"></a>',
        verbose_name=u'Image',
    )
    class Meta:
        model = models.pengumuman
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "tables/table_crud_pengumuman.html"
        fields = ("nomor", "judul","tgl_release","pengumuman", "dokumen", "created","dibuat_oleh","last_updated","diubah_oleh","image","actions")
        
class pengumuman2_Table(tables.Table):
    dokumen = TemplateColumn(template_code='<div><a class="btn btn-info btn-sm" target="_blank" href="{{record.dokumen.url}}"><i class="fa fa-download"></i>&nbsp;&nbsp;Unduh Pengumuman</a></div>')
    tgl_release = tables.DateTimeColumn(format ='d F Y ', verbose_name="Tanggal Penetapan")
    
    class Meta:
        model = models.pengumuman
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "tables/table_pengumuman.html"
        fields = ("nomor", "judul","tgl_release","pengumuman", "dokumen",)

class pengumuman3_Table(tables.Table):
    dokumen = TemplateColumn(template_code='<div><a class="btn btn-info btn-sm" target="_blank" href="{{record.dokumen.url}}"><i class="fa fa-download"></i>&nbsp;&nbsp;Unduh Pengumuman</a></div>')
    tgl_release = tables.DateTimeColumn(format ='d F Y ', verbose_name="Tanggal Penetapan")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',verbose_name="Tanggal Dibuat")
    image = tables.TemplateColumn(
        '<a href="{{ record.image.url }}" target="_blank"><img src="{{ record.image.url }}" class="thumbnail" width="300" height="300"></a>',
        verbose_name=u'Image',
    )
    class Meta:
        model = models.pengumuman
        empty_text = "Tidak ada data"
        orderable = False
#        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah4.html"
        fields = ("nomor", "judul","tgl_release","pengumuman", "dokumen","image")
        
class dasar_hukum_Table(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="dasar_hukum_update btn btn-sm btn-warning"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="dasar_hukum_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    judul= TemplateColumn(template_code='<span class="text-bold">{{record.judul}}</span>' )
    tanggal = tables.DateColumn(format ='d F Y ', verbose_name="Tanggal Penetapan")
    #created = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Dibuat")
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    attachment = TemplateColumn(verbose_name="File Peraturan",template_code='<div>{% if record.attachment %}<a class="btn btn-sm btn-info" target="_blank" href="/media/{{record.attachment}}"><i class="fa fa-file-pdf"></i></a>{% else %}- {% endif %}</div>')
    class Meta:
        model = models.dasar_hukum
        empty_text = "Tidak ada data"
        orderable = False
#        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap.html"
        fields = ( "judul", "nomor","tanggal", "attachment","keterangan", )

class dasar_hukum_Table2(tables.Table):
    class Meta:
        model = models.dasar_hukum
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap.html"
        fields = ("nomor", "judul", "tanggal", "keterangan")
        empty_text = "Tidak ada data"
        orderable = False

class bidder_lelangTable(tables.Table):
    created = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Dibuat")
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div><button id="{{ record.id }}" class="bidder_lelang_edit btn btn-sm btn-success mr-1"><i class="fa fa-edit"></i></button><button id="{{ record.id }}" class="bidder_lelang_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    bidder = TemplateColumn(template_code='{{ record.bidder.users.nama_lengkap }} ({{ record.bidder.users.username }})')
    class Meta:
        model = models.bidder_lelang
        #attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        # fields = ("bidder", )
        fields = ("bidder", "eligibility")
        empty_text = "Tidak ada data"
        orderable = False

class auctioner_lelangTable(tables.Table):
    created = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Dibuat")
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div><button id="{{ record.id }}" class="auctioner_lelang_edit btn btn-sm btn-success mr-1"><i class="fa fa-edit"></i></button><button id="{{ record.id }}" class="auctioner_lelang_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    auctioner = TemplateColumn(template_code='{{ record.auctioner.users.nama_lengkap }} ({{ record.auctioner.users.username }})')
    class Meta:
        model = models.auctioner_lelang
       # attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("auctioner",)
        empty_text = "Tidak ada data"
        orderable = False

class viewer_lelangTable(tables.Table):
    created = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Dibuat")
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div><button id="{{ record.id }}" class="viewer_lelang_edit btn btn-sm btn-success mr-1"><i class="fa fa-edit"></i></button><button id="{{ record.id }}" class="viewer_lelang_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    viewer = TemplateColumn(template_code='{{ record.viewer.users.nama_lengkap }} ({{ record.viewer.users.username }})')
    class Meta:
        model = models.viewers_lelang
        #attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("viewer",)
        empty_text = "Tidak ada data"
        orderable = False

class persyaratan_lelang_Table(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class=""><button id="{{ record.id }}" class="persyaratan_lelang_update btn btn-sm btn-warning"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="persyaratan_lelang_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    # dokumen = TemplateColumn(template_code='<div class="" style="display: flex; justify-content: center;"><a target="_blank" href="{{ record.dokumen }}" class="btn btn-outline mr-1"><i class="icon"><img style="height:18px;" src="/static/img/attach.svg"> </i></button></div>', verbose_name="Dokumen Persyaratan")
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    no_urut = TemplateColumn(template_code='<span class="text-bold">{{record.no_urut}}</span>')
    #dokumen = TemplateColumn(template_code='<a class="btn btn-sm btn-info" target="_blank" href="{{record.dokumen}}" ><i class="fa fa-download"></i></a>')
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal diubah")
    #created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal dibuat")
    class Meta:
        model = models.persyaratan_lelang

        template_name = "django_tables2/custom_bootstrap.html"
        fields = ("no_urut","persyaratan","keterangan",)
        empty_text = "Tidak ada data"
        orderable = False

class jadwal_seleksi_Table(tables.Table):
    #tanggal_awal = tables.DateTimeColumn(verbose_name="Mulai",format ='d F Y H:i:s')
    #tanggal_akhir = tables.DateTimeColumn(verbose_name="Berakhir",format ='d F Y H:i:s')
    #created = tables.DateTimeColumn(format ='d F Y H:i:s')
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s')
    tahap = TemplateColumn(template_code="{% if record.tahap.level > 0%}<i class='fa fa-circle-dot'></i>&nbsp;&nbsp;{% if record.tanggal_awal %} <span style='font-weight:700'> {% else %} <span style='font-weight:300'> {% endif %}{{record.tahap}}</span>{% else %}<span style='font-weight:700; font-size:20px;' class='text-primary'>{{record.tahap}}</span>{% endif %}")
    tanggal_akhir = TemplateColumn(template_code="{% if record.tahap.level > 0%}{% if record.tanggal_awal %} <span style='font-weight:700'> {% else %} <span style='font-weight:300'> {% endif %}{{record.tanggal_akhir}}</span>{% else %}<span style='font-weight:700; font-size:14px;' class='text-primary'>{{record.tanggal_akhir}}</span>{% endif %}")
    tanggal_awal = TemplateColumn(template_code="{% if record.tahap.level > 0%}{% if record.tanggal_awal %} <span style='font-weight:700'> {% else %} <span style='font-weight:300'> {% endif %}{{record.tanggal_awal}}</span>{% else %}<span style='font-weight:700; font-size:14px;' class='text-primary'>{{record.tanggal_awal}}</span>{% endif %}")

    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit"></i></button>&nbsp;<button id="{{ record.id }}" class="duplicate btn btn-success btn-sm mr-1"><i class="fa fa-copy"></i></button>&nbsp;<button id="{{ record.id }}" class="delete btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    
    class Meta:
        empty_text = "Tidak ada data"
        orderable = False
        model = models.jadwal_seleksi
#        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_jadwal.html"
        fields = ("tree_id","lft","tahap", "tanggal_awal", "tanggal_akhir","perubahan",)

class jadwal_seleksi2_Table(tables.Table):
    tanggal_awal = tables.DateTimeColumn(verbose_name="Mulai", format ='d F Y H:i:s')
    tanggal_akhir = tables.DateTimeColumn(verbose_name="Berakhir", format ='d F Y H:i:s')
    class Meta:
        empty_text = "Tidak ada data"
        orderable = False
        model = models.jadwal_seleksi
        #attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap.html"
        fields = ("tahap", "tanggal_awal", "tanggal_akhir","perubahan")

class alamat_panitia_Table(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="alamat_panitia_update btn btn-sm btn-warning"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="alamat_panitia_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    alamat = TemplateColumn(template_code='<span class="text-bold">{{record.alamat}}</span>')
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal diubah")
    #created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal dibuat")
    status=TemplateColumn(template_code='{% if record.status %} <i class="fa fa-solid  fa-circle-check" style="color:#28a745; font-size:24px;"></i> {% else %} <i class="fa fa-solid fa-circe-xmark" style="color:red; font-size:24px;"></i> {% endif %}');
    class Meta:
        empty_text = "Tidak ada data"
        orderable = False
        model = models.alamat_panitia
#        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("alamat", "provinsi", "kota", "kodepos","telp","email","status",)

class undangan_auctionerTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="send btn btn-success btn-sm"><i class="icon fa fa-envelope"></i>&nbsp;&nbsp;Kirim Lewat Email</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit"></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    file = TemplateColumn(verbose_name="File Undangan", template_code='<a class="btn btn-info btn-sm" target="_blank" href="{{record.file.url}}" ><i class="fa fa-download"></i>&nbsp;&nbsp;Unduh File Undangan</a>')
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    tanggal = tables.DateTimeColumn(format ='d F Y', verbose_name="Tanggal Penetapan")
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal dibuat")
    waktu_awal = tables.DateTimeColumn(format ='d F Y H.i', verbose_name="Tanggal Mulai Kegiatan (WIB)")
    waktu_akhir = tables.DateTimeColumn(format ='d F Y H.i', verbose_name="Tanggal Berakhir Kegiatan (WIB)")
    #bidder_user = tables.Column(verbose_name="Daftar Bidder")
    #auctioneer = tables.Column(verbose_name="Daftar Auctioneer")
    #viewer = tables.Column(verbose_name="Daftar Viewer")
    class Meta:
        empty_text = "Tidak ada data"
        orderable = False
        model = models.undangan
#        attrs = {"class": "table table-sm table-striped undangan_auctioner"}
        template_name = "tables/table_crud_undangan.html"
        fields = ("nomor","judul","tanggal","tempat","waktu_awal", "waktu_akhir",  "agenda","keterangan", "link_teleconference", "bidder_user","auctioneer",  "viewer", "file", "created","dibuat_oleh","last_updated","diubah_oleh",)
# hanya List Data 
class undangan_bidderTable(tables.Table):
    file = TemplateColumn(verbose_name="File Undangan", template_code='<button class="download btn btn-sm btn-info" id="{{record.id}}" ><i class="fa fa-download"></i>&nbsp;&nbsp;Unduh File Undangan</button>')
    tanggal = tables.DateTimeColumn(format ='d F Y', verbose_name="Tanggal Penetapan")
    waktu_awal = tables.DateTimeColumn(format ='d F Y H.i', verbose_name="Tanggal Mulai Kegiatan (WIB)")
    waktu_akhir = tables.DateTimeColumn(format ='d F Y H.i', verbose_name="Tanggal Berakhir Kegiatan (WIB)")
  
    class Meta:
        model = models.undangan
        empty_text = "Tidak ada data"
        orderable = False
#        attrs = {"class": "table table-sm table-striped  undangan_auctioner"}
        template_name = "tables/table_undangan.html"
        fields = ("nomor","judul","tanggal","tempat", "waktu_awal", "waktu_akhir", "agenda","keterangan", "link_teleconference", "file", )
        
class berita_acaraTable(tables.Table):
    # Draft = TemplateColumn(template_code='<div class="" style="display: flex; "><a class="btn btn-sm btn-secondary" href="/adm_lelang/adm_lelang/download_ba/{{ record.id }}/"><i class="fa fa-file-word"></i>&nbsp;&nbsp;Unduh Draft Berita Acara</a></div>', verbose_name="File Draft Berita Acara (Doc)")
    Draft = TemplateColumn(template_code='<div class="" style="display: flex; "><a class="btn btn-sm btn-secondary download-draft" id="{{ record.id }}"><i class="fa fa-file-word"></i>&nbsp;&nbsp;Unduh Draft Berita Acara</a></div>', verbose_name="File Draft Berita Acara (Doc)")
    Aksi = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="send btn btn-success btn-sm"><i class="fa fa-envelope"></i>&nbsp;&nbsp;Kirim Lewat Email</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit"></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    file = TemplateColumn(template_code='<a target="_blank" class="btn btn-sm btn-info" href="{{record.file.url}}" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh Berita Acara</a>', verbose_name="File Berita Acara (Pdf)")
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    tanggal = tables.DateTimeColumn(format ='d F Y', verbose_name="Tanggal Penetapan")
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal dibuat")
    class Meta:
        model = models.berita_acara
        empty_text = "Tidak ada data"
        orderable = False
#        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_crud_ba.html"
        fields = ("nomor","judul","tanggal","keterangan", "bidder_user",  "auctioneer", "viewer", "Draft", "file","created","dibuat_oleh", "last_updated","diubah_oleh", )  
# hanya List Data        
class berita_acara_bidderTable(tables.Table):
    file = TemplateColumn(verbose_name="File Berita Acara", template_code='<button class="download btn btn-sm btn-info" id="{{record.id}}" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh Berita Acara</button>')
    tanggal = tables.DateTimeColumn(format ='d F Y', verbose_name="Tanggal Penetapan")

    class Meta:
        empty_text = "Tidak ada data"
        orderable = False
        model = models.berita_acara
#        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_ba.html"
        # fields = ("nomor","judul","tanggal","keterangan", "file",)  
        fields = ("nomor","judul","tanggal","keterangan", "file",) 

# TEMPLATE BERITA ACARA
class template_berita_acara_Table(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="ba_update btn btn-sm btn-warning"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="ba_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    class Meta:
        model = models.template_berita_acara
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_crud_ba.html"
        fields = ("nama_template","keterangan_template","template_code_menu","template_code_sub","dokumen",)

class pengambilan_berita_acara_Table(tables.Table):
    # actions = TemplateColumn(template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="ba_update btn btn-sm btn-warning"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="ba_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    class Meta:
        model = models.pengambilan_ba
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_crud_ba.html"
        fields = ("user","tgl_download",)

class pengambilan_undangan_Table(tables.Table):
    # actions = TemplateColumn(template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="ba_update btn btn-sm btn-warning"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="ba_delete btn btn-sm btn-danger"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    class Meta:
        model = models.pengambilan_undangan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("undangan__judul", "user","tgl_download",)

# penanggung jawab
class penanggung_jawab_Table(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi", template_code='<div class="" style="display: flex; justify-content: center;"><button id="{{ record.id }}" class="updatepenanggung btn btn-sm btn-warning"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="deletepenanggung btn btn-sm btn-danger"><i class="fa fa-trash"></i></button></div>')
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    nama= TemplateColumn(template_code='<span class="text-bold">{{record.nama}}</span>')
    tanggung_jawab= TemplateColumn(template_code='<span class="text-bold">{{record.tanggung_jawab}}</span>')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    tgl_mulai = tables.DateTimeColumn(format ='d F Y', verbose_name="Tanggal Mulai")
    tgl_akhir = tables.DateTimeColumn(format ='d F Y',  verbose_name="Tanggal Berakhir")
    status=TemplateColumn(template_code='{% if record.status %} <i class="fa fa-solid  fa-circle-check" style="color:#28a745; font-size:24px;"></i> {% else %} <i class="fa fa-solid fa-circe-xmark" style="color:red; font-size:24px;"></i> {% endif %}');
 
    class Meta:
        empty_text = "Tidak ada data"
        orderable = False
        model = models.penangung_jawab_seleksi
#        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap.html"
        fields = (
            "nama",
            "nip",
            "tanggung_jawab",
            "tgl_mulai",
            "tgl_akhir",
            "status",
            "keterangan",
            )

# table undangan rekapitulasi
class undangan_rekapitulasiTable(tables.Table):
    file = TemplateColumn(template_code='<a href="{{record.file.url}}" download><button class="download" id="{{record.id}}" ><i data_1="{{record.file.url}}" class="fa fa-file-pdf" ></i></btn>')
    tanggal = tables.DateTimeColumn(format ='d F Y')

    class Meta:
        model = models.undangan
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "tables/table_tambah_search_rekap.html"
        fields = ("nomor","judul","tanggal","file", )
        
        
# table pengumuman rekapitulasi

class pengumuman_rekapitulasiTable(tables.Table):
    dokumen = TemplateColumn(template_code='<a href="{{record.dokumen.url}}" download><button class="download" id="{{record.id}}" ><i data_1="{{record.dokumen.url}}" class="fa fa-file-pdf" ></i></btn>')
    tgl_release = tables.DateTimeColumn(format ='d F Y')

    class Meta:
        model = models.pengumuman
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "tables/table_tambah_search.html"
        fields = ("nomor","judul","tgl_release","dokumen", )
        
# table berita acara rekapitulasi


class berita_acara_rekapitulasiTable(tables.Table):
    file = TemplateColumn(template_code='<a href="{{record.file.url}}" download><button class="download" id="{{record.id}}" ><i data_1="{{record.file.url}}" class="fa fa-file-pdf" ></i></btn>')
    tanggal = tables.DateTimeColumn(format ='d F Y')

    class Meta:
        model = models.berita_acara
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "tables/table_tambah_search_rekap2.html"
        fields = ("nomor","judul","tanggal","file", )
        
        
# table doksel
class doksel_rekapitulasiTable(tables.Table):
    file = TemplateColumn(template_code='<a href="{{record.file.url}}" download><button class="download" id="{{record.id}}" ><i data_1="{{record.file.url}}" class="fa fa-file-pdf" ></i></btn>')
    tanggal = tables.DateTimeColumn(format ='d F Y')

    class Meta:
        model = p_dokumen
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "tables/table_tambah_search_rekap3.html"
        fields = ("nomor","judul","tanggal","keterangan","file", )

# table email
class email_rekapitulasiTable(tables.Table):
    nomor = tables.Column(empty_values=(), verbose_name="No", attrs={"td": {"class": "text-center"}})
    notifikasi = tables.TemplateColumn('{{ record.notifikasi|safe }}', verbose_name="Notifikasi")
    email = tables.Column(attrs={"td": {"class": "text-center"}})
    notification_type = tables.Column(verbose_name="Tipe Notifikasi")
    read = tables.Column(attrs={"td": {"class": "text-center"}}, verbose_name="Status Baca")
    email_status = tables.Column(attrs={"td": {"class": "text-center text-capitalize"}})
    created = tables.Column(attrs={"td": {"class": "text-center"}}, verbose_name="Waktu Kirim")
    expire_date = tables.Column(attrs={"td": {"class": "text-center"}}, verbose_name="Waktu Kadaluarsa")
    
    class Meta:
        model = Notifikasi
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "tables/table_tambah_search_email.html"
        #fields = ("email", "id_undangan", "id_ba", "subyek", "notifikasi", "created", "read", "email_status", "expire_date", "notification_type")
        fields = ("nomor", "notification_type", "email", "subyek", "notifikasi", "read", "email_status", "created", "expire_date")
    
    def render_nomor(self, record, table):
        """ Menghasilkan nomor urut berdasarkan index data di tabel """
        return table.page.start_index() + list(table.data).index(record)
    
    def render_notification_type(self, value):
        """ Mengubah 'BA' menjadi 'Berita Acara' """
        return "Berita Acara" if value == "BA" else value
    
    def render_read(self, value):
        if value:
            return "Sudah dibaca"
        else:
            return "Belum dibaca"
        
    def render_email_status(self, value):
        """ Menampilkan teks + ikon dengan padding kiri """
        icon_mapping = {
            "delivered": ('Delivered', '<i class="fas fa-check text-success pl-1"></i>'),
            "blocked": ('Blocked', '<i class="fas fa-xmark text-danger pl-1"></i>'),
            "request": ('Request', '<i class="fas fa-clock text-primary pl-1"></i>'),
        }
        text, icon = icon_mapping.get(value, (value, ''))
        return mark_safe(f"{text} {icon}")