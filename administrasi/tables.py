import django_tables2 as tables
from . import models
from django_tables2 import TemplateColumn
from adm_lelang.models import pengumuman
from django.utils.html import format_html
from adm_lelang import utils
        
class berita_acaraTable(tables.Table):
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" style="display:flex; align-items: center; justify-content: center; font-size: 20px;"><img data_1="{{record.file.url}}" class="fa fa-file-pdf" ></a>')
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="ba_pemeriksaan_update btn btn-sm btn-warning"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="ba_pemeriksaan_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    class Meta:
        model = models.berita_acara_administrasi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","bidder","auctioneer","keterangan","file",)
        
class berita_acara2Table(tables.Table):
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" style="display:flex; align-items: center; justify-content: center; font-size: 20px;"><img data_1="{{record.file.url}}" class="fa fa-file-pdf" ></a>')
    class Meta:
        model = models.berita_acara_administrasi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","keterangan","file",)

class p_keikutsertaanTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="delete btn btn-sm btn-danger"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    # file2 = TemplateColumn(template_code='<a target="_blank" href="{{record.file2.url}}" ><img class="fa fa-file-pdf" src="/static/img/dollar_icon.png" style="height: 20px; width: 20px"></a>', verbose_name="File Bidbond")
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Permohonan (WIB)")
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    file = TemplateColumn(template_code='{% if record.file %}<a target="_blank" href="{{record.file.url}}"  class="btn btn-sm btn-info"><i data_1="{{record.file.url}}" class="fa fa-file-zipper" ></i>&nbsp;&nbsp;Unduh File Formulir Keikutsertaan Seleksi</a>{% else %}<p>-</p>{% endif %}', verbose_name="Formulir Permohonan Keikutsertaan Seleksi")
    file2 = TemplateColumn(template_code='{% if record.file2 %}<a target="_blank" href="{{record.file2.url}}" class="btn btn-sm btn-info"><i class="fa fa-file-zipper"  data_1="{{record.file2.url}}" ></i>&nbsp;&nbsp;Unduh File Jaminan Keikutsertaan Seleksi</a>{% else %}<p>-</p>{% endif %}', verbose_name="Jaminan Keikutsertaan Seleksi (Bid Bond)")
    file3= TemplateColumn(template_code='Disampaikan secara luring dan Dalam Sampul tertutup sesuai waktu yang ditentukan pada Dokumen Seleksi ', verbose_name="Dokumen Penawaran Harga")
    pernyataan = TemplateColumn(template_code='{% if record.pernyataan == "MENGIKUTI"%}<span class="rounded-pill bg-success" style="padding:5px">Mengikuti Seleksi</span>{% else %}<span class="rounded-pill bg-danger" style="padding:5px">Tidak Mengikuti Seleksi</span>{% endif %}', verbose_name = "Status")
    nama_perwakilan = TemplateColumn(template_code='<b>{{record.perwakilan.nama_lengkap}}</b>', verbose_name="Perwakilan")
    bidder_perwakilan = TemplateColumn(template_code='<b>{{record.bidder.bidder.nama_perusahaan}}</b>', verbose_name="Perusahaan")
    # bidder_perwakilan = TemplateColumn(template_code='<b>{{record.bidder.bidder.nama_perusahaan }}</b>', verbose_name="Perusahaan")
    class Meta:
        model = models.permohonan_keikutsertaan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("bidder_perwakilan","nama_perwakilan","pernyataan","file","file2","file3","created",)
        
class p_keikutsertaan2Table(tables.Table):
    # file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" ><i class="fa fa-download"></i></a>', verbose_name="File Permohonan")
    #created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Dibuat pada")
    file = TemplateColumn(template_code='{% if record.file %}<a target="_blank" href="{{record.file.url}}"  class="btn btn-sm btn-info"><i data_1="{{record.file.url}}" class="fa fa-file-zipper" ></i>&nbsp;&nbsp;Unduh File Formulir Keikutsertaan Seleksi</a>{% else %}<p>-</p>{% endif %}', verbose_name="Formulir Permohonan Keikutsertaan Seleksi")
    file2 = TemplateColumn(template_code='{% if record.file2 %}<a target="_blank" href="{{record.file2.url}}" class="btn btn-sm btn-info"><i class="fa fa-file-zipper"  data_1="{{record.file2.url}}" ></i>&nbsp;&nbsp;Unduh File Jaminan Keikutsertaan Seleksi</a>{% else %}<p>-</p>{% endif %}', verbose_name="Jaminan Keikutsertaan Seleksi (Bid Bond)")
    file3= TemplateColumn(template_code='Disampaikan secara luring dan Dalam Sampul tertutup sesuai waktu yang ditentukan pada Dokumen Seleksi ', verbose_name="Dokumen Penawaran Harga")
   
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Permohonan (WIB)")
    pernyataan = TemplateColumn(template_code='{% if record.pernyataan == "MENGIKUTI"%}<span class="rounded-pill bg-success" style="padding:5px" >Mengikuti Seleksi</span>{% else %}<span class="rounded-pill bg-danger"  style="padding:5px" >Tidak Mengikuti Seleksi</span>{% endif %}', verbose_name = "Status")
    nama_perwakilan = TemplateColumn(template_code='<b>{{record.perwakilan.nama_lengkap}}</b>', verbose_name="Perwakilan")
    bidder_perwakilan = TemplateColumn(template_code='<b>{{record.bidder.bidder.nama_perusahaan }}</b>', verbose_name="Perusahaan")
    class Meta:
        model = models.permohonan_keikutsertaan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah_pecah2.html"
        fields = ("bidder_perwakilan","nama_perwakilan","pernyataan","file","file2","file3","created",)
        
class p_keikutsertaan3Table(tables.Table):
    # file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" ><i class="fa fa-download"></i></a>')
   # last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Permohonan (WIB)")
  #  nama_perwakilan = TemplateColumn(template_code='{{record.bidder.nama_lengkap}}',  verbose_name="Nama Perwakilan")
    file = TemplateColumn(verbose_name="Tanda Terima Bukti Permohonan", template_code='<a target="_blank" href="/administrasi/administrasi/pengambilan_keikutsertaan/{{record.id}}/" class="btn btn-sm btn-info"><i class="fa fa-file-pdf" ></i>&nbsp;&nbsp;Unduh Tanda Terima&nbsp;&nbsp;</a>')
    pernyataan = TemplateColumn(template_code='{% if record.pernyataan == "MENGIKUTI"%}<span class="rounded-pill bg-success" style="padding:5px;">Mengikuti Seleksi</span>{% else %}<span class="rounded-pill bg-danger" style="padding:5px;">Tidak Mengikuti Seleksi</span>{% endif %}', verbose_name = "Status")
    nama_perwakilan = TemplateColumn(template_code='<b>{{record.perwakilan.nama_lengkap}}</b>', verbose_name="Perwakilan")
    bidder_perwakilan = TemplateColumn(template_code='<b>{{record.bidder.bidder.nama_perusahaan }}</b>', verbose_name="Perusahaan")
    class Meta:
        model = models.permohonan_keikutsertaan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah_pecah2.html"
        fields = ("bidder_perwakilan","nama_perwakilan", "pernyataan","created","file")

class evaluasi_hasilTable(tables.Table):
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" ><img data_1="{{record.file.url}}" class="fa fa-file-pdf" src="/static/img/pdf.png"style="height: 20px; width: 20px"></a>')
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    tgl_release = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Terbit", )
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Dibuat")
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    class Meta:
        model = pengumuman
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tgl_release","pengumuman","file","dibuat_oleh","diubah_oleh", "created","last_updated",)
        
class evaluasi_hasilTable2(tables.Table):
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" style="display:flex; align-items: center; justify-content: center; font-size: 20px;"><img data_1="{{record.file.url}}" class="fa fa-file-pdf" src="/static/img/pdf.png"style="height: 20px; width: 20px"></a>')
    tgl_release = tables.DateTimeColumn(verbose_name="Tanggal Terbit", format ='d F Y H:i:s')
    class Meta:
        model = pengumuman
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tgl_release","pengumuman","file",)
        

        
#form

class form_pemeriksaanTable(tables.Table):
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" class="btn btn-info btn-sm"><i data_1="{{record.file.url}}" class="fa fa-file-pdf" ></i>&nbsp;&nbsp;Unduh File</a>',verbose_name="File Hasil Pemeriksaan Kelengkapan Dokumen Permohonan")
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    sampul1 = TemplateColumn(template_code='<span {% if record.sampul1 == "Tidak Ada" %}class="rounded-pill bg-danger"{% else %}class="rounded-pill bg-success"{% endif %} style="padding:5px;">&nbsp;&nbsp;&nbsp;&nbsp;{% if record.sampul1 == "Ada" %} Lengkap {% else %} Tidak lengkap {% endif %} &nbsp;&nbsp;&nbsp;&nbsp;</span>', verbose_name="Kelengkapan Formulir Permohonan Keikutsertaan Seleksi ")
    sampul2 = TemplateColumn(template_code='<span {% if record.sampul2 == "Tidak Ada" %}class="rounded-pill bg-danger"{% else %}class="rounded-pill bg-success"{% endif %} style="padding:5px;">&nbsp;&nbsp;&nbsp;&nbsp;{% if record.sampul2 == "Ada" %} Lengkap {% else %} Tidak lengkap {% endif %}&nbsp;&nbsp;&nbsp;&nbsp;</span>', verbose_name="Kelengkapan Dokumen Penawaran Harga")
    bidbond = TemplateColumn(template_code='<span {% if record.bidbond == "Tidak Ada" %}class="rounded-pill bg-danger"{% else %}class="rounded-pill bg-success"{% endif %} style="padding:5px;">&nbsp;&nbsp;&nbsp;&nbsp;{% if record.bidbond == "Ada" %} Lengkap {% else %} Tidak lengkap {% endif %}&nbsp;&nbsp;&nbsp;&nbsp;</span>', verbose_name="Kelengkapan Jaminan Keikutsertaan Seleksi (Bid Bond)")
    kesimpulan = TemplateColumn(template_code='{% if record.kesimpulan %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;&nbsp;&nbsp;&nbsp;Lengkap&nbsp;&nbsp;&nbsp;&nbsp;</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;">&nbsp;&nbsp;&nbsp;&nbsp;Tidak Lengkap&nbsp;&nbsp;&nbsp;&nbsp;</span>{%endif%}')
    created = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Dibuat")
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Terakhir Diubah")
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    # bidder = TemplateColumn(template_code='<b>{{record.bidder }}</b>', verbose_name="Perusahaan")
    # bidder = TemplateColumn(template_code='<b>{{record.bidder.bidder.nama_perusahaan }} - {{record.bidder }}</b>', verbose_name="Perusahaan")
 
    class Meta:
        model = models.form_pemeriksaan
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "tables/table_verifikasi.html"
        fields = ("bidder","sampul1","bidbond","sampul2","kesimpulan", "file", "keterangan", "created", "dibuat_oleh", "last_updated", "diubah_oleh", )
        
    def render_bidder(self, value):
        perwakilan1 = value.bidder_perwakilan_bidder.all().first()
        return format_html(f"<b>{value} ({perwakilan1.nama_lengkap})</b>")
        
class form_pemeriksaan2Table(tables.Table):
    sampul1 = TemplateColumn(template_code='<span {% if record.sampul1 == "Tidak Ada" %}class="rounded-pill bg-danger"{% else %}class="rounded-pill bg-success"{% endif %}  style="padding:5px;">&nbsp;&nbsp;&nbsp;&nbsp;{{record.sampul1}}&nbsp;&nbsp;&nbsp;&nbsp;</span>', verbose_name="Kelengkapan Formulir Permohonan Keikutsertaan Seleksi")
    sampul2 = TemplateColumn(template_code='<span {% if record.sampul2 == "Tidak Ada" %}class="rounded-pill bg-danger"{% else %}class="rounded-pill bg-success"{% endif %}  style="padding:5px;">&nbsp;&nbsp;&nbsp;&nbsp;{{record.sampul2}}&nbsp;&nbsp;&nbsp;&nbsp;</span>', verbose_name="Kelengkapan Dokumen Penawaran Harga")
    bidbond = TemplateColumn(template_code='<span {% if record.bidbond == "Tidak Ada" %}class="rounded-pill bg-danger"{% else %}class="rounded-pill bg-success"{% endif %}  style="padding:5px;">&nbsp;&nbsp;&nbsp;&nbsp;{{record.bidbond}}&nbsp;&nbsp;&nbsp;&nbsp;</span>', verbose_name="Kelengkapan Jaminan Keikutsertaan Seleksi (Bid Bond)")
    kesimpulan = TemplateColumn(template_code='{% if record.kesimpulan %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;Lengkap&nbsp;</span>{%else%}<span class="text-danger">&nbsp;Tidak Lengkap&nbsp;</span>{%endif%}')
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" class="btn btn-info btn-sm"><i data_1="{{record.file.url}}" class="fa fa-file-pdf" ></i>&nbsp;&nbsp;Unduh File</a>',verbose_name="File Hasil Pemeriksaan Kelengkapan Dokumen Permohonan")
    #nama_perwakilan = TemplateColumn(template_code='<b>{{record.bidder.bidder.perwakilan.nama_lengkap}}</b>', verbose_name="Perwakilan x")
    # bidder = TemplateColumn(template_code='<b>{{record.bidder.bidder.nama_perusahaan }}</b>', verbose_name="Perusahaan")
 
    class Meta:
        model = models.form_pemeriksaan
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "tables/table_verifikasi.html"
        fields = ("bidder","sampul1","bidbond","sampul2","kesimpulan","keterangan","file")
        
    def render_bidder(self, value):
        perwakilan1 = value.bidder_perwakilan_bidder.all().first()
        return format_html(f"<b>{value} ({perwakilan1.nama_lengkap})</b>")
    
        
class form_verifikasiTable(tables.Table):
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" class="btn btn-info btn-sm"><i data_1="{{record.file.url}}" class="fa fa-file-pdf" ></i>&nbsp;&nbsp;Unduh File</a>',verbose_name="File Hasil Verifikasi Dokumen Permohonan")
    # bidder = TemplateColumn(template_code='<b>{{record.bidder.bidder.nama_perusahaan }}</b>', verbose_name="Perusahaan")
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-sm btn-danger"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    kesimpulan = TemplateColumn(template_code='{% if record.kesimpulan %}<span <span class="rounded-pill bg-success" style="padding:5px;">&nbsp;Lengkap&nbsp;</span>{%else%}<span class="text-danger">&nbsp;Tidak Lengkap&nbsp;</span>{%endif%}')
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Dibuat")
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    sampul1 = TemplateColumn(template_code='{% if record.sampul1 == "Ada"  %} <span  <span class="rounded-pill bg-success" style="padding:5px;">&nbsp;Sesuai&nbsp;</span>{% else %}<span class="text-danger">&nbsp;Tidak Sesuai&nbsp;</span>{%endif%}', verbose_name="Verifikasi Formulir Permohonan Keikutsertaan Seleksi")
    bidbond = TemplateColumn(template_code='{% if record.bidbond == "Ada" %}<span <span class="rounded-pill bg-success" style="padding:5px;">&nbsp;Sesuai&nbsp;</span>{%else%}<span class="text-danger">&nbsp;Tidak Sesuai&nbsp;</span>{%endif%}', verbose_name="Verifikasi Jaminan Penawaran Harga")
    class Meta:
        model = models.form_verifikasi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_verifikasi.html"
        fields = ("bidder","sampul1","bidbond","kesimpulan","keterangan","file", "created", "dibuat_oleh", "last_updated", "diubah_oleh",)
    
    def render_bidder(self, value):
        perwakilan1 = value.bidder_perwakilan_bidder.all().first()
        return format_html(f"<b>{value} ({perwakilan1.nama_lengkap})</b>")
        
class form_verifikasi2Table(tables.Table):
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" class="btn btn-info btn-sm"><i data_1="{{record.file.url}}" class="fa fa-file-pdf" ></i>&nbsp;&nbsp;Unduh File</a>',verbose_name="File Hasil Verifikasi Dokumen Permohonan")
    # bidder_perwakilan = TemplateColumn(template_code='<b>{{record.bidder.bidder.nama_perusahaan }}</b>', verbose_name="Perusahaan")
    kesimpulan = TemplateColumn(template_code='{% if record.kesimpulan %}<span <span class="rounded-pill bg-success" style="padding:5px;">&nbsp;Lengkap&nbsp;</span>{%else%}<span class="text-danger">&nbsp;Tidak Lengkap&nbsp;</span>{%endif%}', verbose_name="Hasil Verifikasi Permohonan")
    sampul1 = TemplateColumn(template_code='{% if record.sampul1 == "Ada"  %} <span  <span class="rounded-pill bg-success" style="padding:5px;">&nbsp;Sesuai&nbsp;</span>{% else %}<span class="text-danger">&nbsp;Tidak Sesuai&nbsp;</span>{%endif%}', verbose_name="Kelengkapan Formulir Permohonan Keikutsertaan Seleksi")
    bidbond = TemplateColumn(template_code='{% if record.bidbond == "Ada" %}<span <span class="rounded-pill bg-success" style="padding:5px;">&nbsp;Sesuai&nbsp;</span>{%else%}<span class="text-danger">&nbsp;Tidak Sesuai&nbsp;</span>{%endif%}', verbose_name="Kelengkapan Jaminan Penawaran Harga")
    class Meta:
        model = models.form_verifikasi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_verifikasi.html"
        fields = ("bidder","sampul1","bidbond","kesimpulan","keterangan","file",)
        
    def render_bidder(self, value):
        perwakilan1 = value.bidder_perwakilan_bidder.all().first()
        return format_html(f"<b>{value} ({perwakilan1.nama_lengkap})</b>")
        
class form_evaluasiTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    class Meta:
        model = models.form_evaluasi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_verifikasi.html"
        fields = ("nama_perusahaan","hasil_pemeriksaan",)
        
class form_evaluasi2Table(tables.Table):
    class Meta:
        model = models.form_evaluasi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah_pecah2.html"
        fields = ("nama_perusahaan","hasil_pemeriksaan",)
        
class form_sanggahanTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div  style="display: flex; "><button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    file = TemplateColumn(template_code='{% if record.file %}<a class="btn btn-sm btn-info" target="_blank" href="{{record.file.url}}" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh Bukti Penyampaian Sanggahan</a>{% else %}<p>-</p>{% endif %}', verbose_name="Bukti Penyampaian Sanggahan")
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Pengiriman Sanggahan (WIB)")
    status_sanggah = TemplateColumn(template_code='{% if record.status_sanggah == "Ada" %} <span class="rounded-pill btn-success" style="padding:5px;">&nbsp;Ada Sanggahan&nbsp;</span>{% else %}<span class="rounded-pill bg-danger" style="padding:5px;">&nbsp;Tidak Ada Sanggahan&nbsp;</span>{% endif %}', verbose_name="Status Sanggahan")
    #nama_perwakilan = TemplateColumn(template_code='<b>{{record.bidder.nama_lengkap}}</b>', verbose_name="Perwakilan")
    nama_perusahaan = TemplateColumn(template_code='<b>{{record.bidder.bidder.nama_perusahaan }}</b>', verbose_name="Perusahaan")
 
    class Meta:
        model = models.form_sanggahan
        empty_text = "Tidak ada data"
        orderable = False
        # attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_sanggahan.html"
        fields = ("nama_perusahaan","status_sanggah","keterangan","file","created",)
        
class form_sanggahan2Table(tables.Table):
    file = TemplateColumn(template_code='{% if record.file %}<a class="btn btn-sm btn-info" target="_blank" href="/media/{{ record.file }}"><i data_1="{{record.file.url}}" class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh Bukti Penyampaian Sanggahan</a>{% else %}<p>-</p>{% endif %}')
    status_sanggah = TemplateColumn(template_code='{% if record.status_sanggah == "Ada" %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;&nbsp;Ada Sanggahan</span>{%else%}<span <span class="rounded-pill bg-danger" style="padding:5px;">&nbsp;Tidak Ada Sanggahan{%endif%}')
    #nama_perwakilan = TemplateColumn(template_code='<b>{{record.bidder.nama_lengkap}}</b>', verbose_name="Perwakilan")
    nama_perusahaan = TemplateColumn(template_code='<b>{{record.bidder.bidder.nama_perusahaan }}</b>', verbose_name="Perusahaan")
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Sanggahan Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Penyampaian Sanggahan (WIB)")
    class Meta:
        model = models.form_sanggahan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_dfsanggahan.html"
        fields = ("nama_perusahaan","status_sanggah","keterangan","file","created", )

class jawaban_sanggahanTable(tables.Table):
    file = TemplateColumn(template_code='<a class="btn btn-sm btn-info" target="_blank" href="{{record.file.url}}" ><i data_1="{{record.file.url}}" class="fa fa-file-pdf" ></i>&nbsp;&nbsp;Unduh Jawaban Sanggahan</a>')
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Penyampaian Sanggahan (WIB)")
    jawaban_sanggah = TemplateColumn(template_code='{% if record.jawaban_sanggah == "Ada"  %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;&nbsp;Diterima</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;">Ditolak</span>{%endif%}')
    tindak_lanjut_seleksi = TemplateColumn(template_code='{% if record.tindak_lanjut_seleksi == "Lanjut"  %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;&nbsp;Lanjut</span>{% elif record.tindak_lanjut_seleksi == "Tunda" %}<span class="btn bg-warning">Berhenti Sementara</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;">Berhenti</span>{%endif%}')
    nama_perwakilan = TemplateColumn(template_code='<b>{{record.bidder}}</b>', verbose_name="Perusahaan")
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}}')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}}')
    
    class Meta:
        model = models.jawaban_sanggahan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_jwbsanggahan.html"
        fields = ("nama_perwakilan","jawaban_sanggah","keterangan","file","tindak_lanjut_seleksi", "created", )

class jawaban_sanggahan2Table(tables.Table):
    file = TemplateColumn(template_code='<a class="btn btn-sm btn-info" target="_blank" href="{{record.file.url}}" ><i data_1="{{record.file.url}}" class="fa fa-file-pdf" ></i>&nbsp;&nbsp;Unduh Jawaban Sanggahan</a>')
    jawaban_sanggah = TemplateColumn(template_code='{% if record.jawaban_sanggah == "Ada"  %}<span <span class="rounded-pill bg-success" style="padding:5px;">&nbsp;&nbsp;Diterima</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;">&nbsp;Ditolak</span>{%endif%}')
    tindak_lanjut_seleksi = TemplateColumn(template_code='{% if record.tindak_lanjut_seleksi == "Lanjut"  %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;&nbsp;Lanjut</span>{% elif record.tindak_lanjut_seleksi == "Tunda" %}<span class="btn bg-warning">Berhenti Sementara</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;">Berhenti</span>{%endif%}')
    nama_perwakilan = TemplateColumn(template_code='<b>{{record.bidder}}</b>', verbose_name="Perwakilan")
    
    class Meta:
        model = models.jawaban_sanggahan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_dfjwbsanggahan.html"
        fields = ("nama_perwakilan","jawaban_sanggah","keterangan","file","tindak_lanjut_seleksi", )

class hasil_kesimpulanTable(tables.Table):
    kesimpulan1 = TemplateColumn(verbose_name="Hasil Pemeriksaan Kelengkapan Dokumen Administrasi", template_code='{% if record.kesimpulan1 %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;Lengkap&nbsp;</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;">&nbsp;Tidak Lengkap&nbsp;</span>{%endif%}')
    kesimpulan2 = TemplateColumn(verbose_name="Hasil Verifikasi Dokumen Administrasi", template_code='{% if record.kesimpulan2 %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;Sesuai&nbsp;</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;">&nbsp;Tidak Sesuai&nbsp;</span>{%endif%}')
    kesimpulan3 = TemplateColumn(verbose_name="Hasil Evaluasi Dokumen Administrasi", template_code='{% if record.kesimpulan3 %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;&nbsp;Lulus&nbsp;&nbsp;</span>{%else%}<span class="rounded-pill bg-danger">&nbsp;&nbsp;Tidak Lulus&nbsp;&nbsp;</span>{%endif%}')
    hasil_pemeriksaan = TemplateColumn(verbose_name="Penetapan Hasil Evaluasi", template_code='{% if record.hasil_pemeriksaan %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;&nbsp;Sudah ditetapkan&nbsp;&nbsp;</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;">&nbsp;&nbsp;Belum ditetapkan&nbsp;&nbsp;</span>{%endif%}')
    #Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/edit-3.svg"> </i></button><button id="{{ record.id }}" class="delete btn badge mr-1" style="color:red;"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    Aksi = TemplateColumn(template_code='<span style="font-size:8px; color:red;">Tekan Tombol Buat Form Lebih Dulu Untuk Mengaktifkan Form</span><div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i id="evalusi" class="fa fa-edit"></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    #file = TemplateColumn(template_code='{% if record.file %}<a target="_blank" href="/media/{{record.file}}" ><img data_1="/media/{{record.file}}" class="fa fa-file-pdf" ></a>{% endif %}')
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Dibuat")
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    bidder = TemplateColumn(template_code='<span class="text-bold">{{record.bidder.bidder.nama_perusahaan}}</span>')
    class Meta:
        model = models.hasil_kesimpulan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kesimpulan.html"
        fields = ("bidder",
            "kesimpulan1",
            "kesimpulan2",
            "kesimpulan3",
            "hasil_pemeriksaan",
            "keterangan",
           
            "created",
            "dibuat_oleh",
            "last_updated",
            "diubah_oleh",
           
            
            )

class hasil_kesimpulanTable2(tables.Table):
    kesimpulan1 = TemplateColumn(verbose_name="Hasil Pemeriksaan Kelengkapan Dokumen Administrasi", template_code='{% if record.kesimpulan1 %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;&nbsp;Lengkap&nbsp;&nbsp;</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;">&nbsp;&nbsp;Tidak Lengkap&nbsp;&nbsp;</span>{%endif%}')
    kesimpulan2 = TemplateColumn(verbose_name="Hasil Verifikasi Dokumen Administrasi", template_code='{% if record.kesimpulan2 %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;&nbsp;Sesuai&nbsp;&nbsp;</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;">&nbsp;&nbsp;Tidak Sesuai&nbsp;&nbsp;</span>{%endif%}')
    kesimpulan3 = TemplateColumn(verbose_name="Hasil Evaluasi Dokumen Administrasi", template_code='{% if record.kesimpulan3 %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;&nbsp;Lulus&nbsp;&nbsp;</span>{%else%}<span class="rounded-pill bg-danger">&nbsp;&nbsp;Tidak Lulus&nbsp;&nbsp;</span>{%endif%}')
    bidder = TemplateColumn(template_code='<span class="text-bold">{{record.bidder.bidder.nama_perusahaan}}</span>')
    class Meta:
        model = models.hasil_sementara
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kesimpulan.html"
        fields = ("bidder",
            "kesimpulan1",
            "kesimpulan2",
            "kesimpulan3",)

class hasil_kesimpulanTable3(tables.Table):
    kesimpulan1 = TemplateColumn(verbose_name="Hasil Pemeriksaan Kelengkapan Dokumen Administrasi", template_code='{% if record.kesimpulan1 %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;Lengkap&nbsp;</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;">&nbsp;Tidak Lengkap&nbsp;</span>{%endif%}')
    kesimpulan2 = TemplateColumn(verbose_name="Hasil Verifikasi Dokumen Administrasi", template_code='{% if record.kesimpulan2 %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;Sesuai&nbsp;</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;">&nbsp;Tidak Sesuai&nbsp;</span>{%endif%}')
    kesimpulan3 = TemplateColumn(verbose_name="Hasil Evaluasi Dokumen Administrasi", template_code='{% if record.kesimpulan3 %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;Lulus&nbsp;</span>{%else%}<span class="rounded-pill bg-danger">&nbsp;Tidak Lulus&nbsp;</span>{%endif%}')
    hasil_pemeriksaan = TemplateColumn(verbose_name="Penetapan Hasil Evaluasi", template_code='{% if record.hasil_pemeriksaan %}<span class="rounded-pill bg-success" style="padding:5px;">&nbsp;&nbsp;Sudah ditetapkan&nbsp;&nbsp;</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;">&nbsp;&nbsp;Belum ditetapkan&nbsp;</span>{%endif%}')
    #file = TemplateColumn(verbose_name="File Hasil ",template_code='{% if record.file %}<a target="_blank" href="/media/{{record.file}}" class="btn btn-sm btn-info"><i class="fa fa-file-pdf" ></i>&nbsp;&nbsp;Unduh File</a>{% endif %}')
    # file = TemplateColumn(template_code='{% if record.file %}<a target="_blank" href="/media/{{record.file}}" ><img data_1="/media/{{record.file}}" class="fa fa-file-pdf" ></a>{% endif %}')
    bidder = TemplateColumn(template_code='<span class="text-bold">{{record.bidder.bidder.nama_perusahaan}}</span>')
    class Meta:
        model = models.hasil_kesimpulan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kesimpulan.html"
        fields = ("bidder",
            "kesimpulan1",
            "kesimpulan2",
            "kesimpulan3",
            "hasil_pemeriksaan",
            "keterangan",
            
            )