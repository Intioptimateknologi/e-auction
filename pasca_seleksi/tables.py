import django_tables2 as tables
from . import models
from django_tables2 import TemplateColumn

#tabel undangan pemilihan blok
class bloknyaTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="penawaran_update btn btn-sm btn-warning"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="penawaran_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    class Meta:
        model = models.blok
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("users","nomor","judul","tanggal","tempat","agenda","link_teleconference","keterangan","link_file")
        
class bloknya2Table(tables.Table):
    class Meta:
        model = models.blok
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","tempat","agenda","link_teleconference","keterangan","link_file")
        
#pemilihan blok

class blok_pasca_seleksiTable(tables.Table):
    #persetujuan = TemplateColumn(attrs={"td": {"style": "display: flex; align-items: center;"}},template_code='<label>Abaikan</label><label class="switch "><input {% if record.sudah_pilih %} disabled {% endif %} class="success" type="checkbox" id="{{ record.id }}" {% if record.sudah_pilih %} checked {% endif %}><span class="slider round"></span></label><label>Pilih Blok</label>')
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    class Meta:
        model = models.blok_pasca_seleksi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = (
            "item", "nama_block",
            )

class pemilihan_bloknyaTable(tables.Table):
    item = tables.Column(verbose_name="Obyek Seleksi")
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex;"><button id="{{ record.id }}_{{record.item.id}}_{{record.jatah_block}}" class="penawaran_update btn btn-sm btn-warning"><i class="fa fa-edit "></i></button></div>')
    penawaran = TemplateColumn(verbose_name="Penawaran",template_code='{{ record.penawaran|floatformat:"2g"}}')
    class Meta:
        model = models.pemilihan_blok_pasca_seleksi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = (
            "item","rangking",
        )

class pemilihan_bloknya2Table(tables.Table):
    item = tables.Column(verbose_name="Obyek Seleksi")
  #  persetujuan = TemplateColumn(attrs={"td": {"align": "center"}},template_code='{% if record.persetujuan == False %}<i class="fa fa-circle-xmark fa-lg text-danger"></i>{% else %}<i class="fa fa-circle-check fa-lg text-green"></i>{% endif %}')
    blok = TemplateColumn(attrs={"td": {"align": "center"}},template_code='{% if record.persetujuan == False %}---{% else %}<b>{{record.blok}}</b>{% endif %}')
    penawaran = TemplateColumn(template_code='{{record.penawaran|floatformat:"2g"}}',verbose_name='Harga Penawaran')
   
    class Meta:
        model = models.pemilihan_blok_pasca_seleksi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = (
            "bidder","item", "ranking", "penawaran","keterangan","blok",
            )

class pemilihan_bloknya3Table(tables.Table):
    buka_pilihan = TemplateColumn(verbose_name="Aksi Buka Pilihan",attrs={"td": {"align": "center"}},template_code='{% if record.pilih_blok == False %}<button  id="{{ record.id }}" class="buka_pilihan btn btn-success btn-sm b mr-1"><i class="fa fa-lock-open"></i>&nbsp;&nbsp;Buka Kembali Pilihan</button>{% else %}<button  id="{{ record.id }}" class="buka_pilihan btn btn-danger btn-sm b mr-1"><i class="fa fa-lock"></i>&nbsp;&nbsp;Tutup Pilihan</button>{% endif %}')
    beri_persetujuan = TemplateColumn(verbose_name="Aksi Beri Persetujuan",attrs={"td": {"align": "center"}},template_code='{% if record.persetujuan == False %}<button  id="{{ record.id }}" class="persetujuan btn btn-success btn-sm b mr-1"><i class="fa fa-circle-check"></i>&nbsp;&nbsp;Buat Persetujuan</button>{% else %}<button  id="{{ record.id }}" class="persetujuan btn btn-warning btn-sm b mr-1"><i class="fa fa-circle-xmark"></i>&nbsp;&nbsp;Ubah Persetujuan</button>{% endif %}')
    item = tables.Column(verbose_name="Obyek Seleksi")
    pilih_blok = TemplateColumn(verbose_name="Buka / Tutup", attrs={"td": {"align": "center"}},template_code='{% if record.pilih_blok == False %}<i class="fa fa-lock fa-lg text-danger"></i>{% else %}<i class="fa fa-lock-open fa-lg text-green"></i>{% endif %}')
    persetujuan = TemplateColumn(attrs={"td": {"align": "center"}},template_code='{% if record.persetujuan == False %}<i class="fa fa-circle-xmark fa-lg text-danger"></i>{% else %}<i class="fa fa-circle-check text-green fa-lg"></i>{% endif %}')
    penawaran = TemplateColumn(attrs={"td": {"align": "right"}}, template_code='{{record.penawaran|floatformat:"2g"}}',verbose_name='Harga Penawaran')
    class Meta:
        model = models.pemilihan_blok_pasca_seleksi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = (
            "bidder","item", "ranking","penawaran","keterangan", 
            "blok",
            "pilih_blok",
            
            "persetujuan",
            
            "buka_pilihan",
            "beri_persetujuan",
            
            )

class pemilihan_bloknya4Table(tables.Table):
    item = tables.Column(verbose_name="Obyek Seleksi")
    blok = tables.Column(verbose_name="Blok Yang Dipilih")
    pilihan = TemplateColumn(verbose_name="Pilih Blok", attrs={"td": {"align": "center"}},template_code='{% if record.persetujuan == False %}<button id="{{ record.id }}" class="buka_pilihan btn btn-warning"><i class="fa fa-edit "></i>&nbsp;&nbsp;Pilih Blok</button>{% endif %}')
    penawaran = TemplateColumn(template_code='{{record.penawaran|floatformat:"2g"}}',verbose_name='Harga Penawaran')
    class Meta:
        model = models.pemilihan_blok_pasca_seleksi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = (
            "bidder","item", "ranking","penawaran","keterangan",
            "blok",
            "pilihan",
            #"aksi"
            )
        

        
#hasil seleksi

class hasilseleksinyaTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex;"><button id="{{ record.id }}" class="penawaran_update btn btn-sm btn-warning"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="penawaran_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    class Meta:
        model = models.seleksi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","keterangan","file_link")
        
class hasilseleksinya2Table(tables.Table):
    class Meta:
        model = models.seleksi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","keterangan","file_link")
        
#sanggahan

class sanggahannyaTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="penawaran_update btn btn-sm btn-warning"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="penawaran_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    class Meta:
        model = models.sanggahan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_sanggahan.html"
        fields = ("status_sanggahan","file_link",)
        
class sanggahannya2Table(tables.Table):
    class Meta:
        model = models.sanggahan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_sanggahan.html"
        fields = ("status_sanggahan","file_link",)
        
        
#sanggahan dan jawaban
#s untuk sanggah

class s_jawabanTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="penawaran_update btn btn-sm btn-warning"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="penawaran_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    class Meta:
        model = models.sanggahan_jawaban
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_sanggahan.html"
        fields = ("nomor","judul","tanggal","tempat","waktu","agenda","link_teleconference","keterangan","link_file")
        
class s_jawaban2Table(tables.Table):
    class Meta:
        model = models.sanggahan_jawaban
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_sanggahan.html"
        fields = ("nomor","judul","tanggal","tempat","waktu","agenda","link_teleconference","keterangan","link_file")
        
#jawaban atas sanggahan

class jawaban_atas_sTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex; justify-content:center;"><button id="{{ record.id }}" class="penawaran_update btn btn-sm btn-warning"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="penawaran_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    class Meta:
        model = models.jawaban_atas_sanggahan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_sanggahan.html"
        fields = ("nama_perusahaan","sampul1","bidbond","hasil_sanggahan")   

class jawaban_atas_s2Table(tables.Table):
    class Meta:
        model = models.jawaban_atas_sanggahan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_sanggahan.html"
        fields = ("nama_perusahaan","sampul1","bidbond","hasil_sanggahan")      
        
        
#penetapan pemenang

class pemenangnyaTable(tables.Table):
    aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    file_link = TemplateColumn(template_code='<a target="_blank" class="btn btn-sm btn-info" href="{{record.file_link.url}}" ><i class="fa fa-download"></i>&nbsp;&nbsp;Unduh File Keputusan</a>', verbose_name = "File Keputusan")
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Dibuat")
    tanggal = tables.DateTimeColumn(format ='d F Y',  verbose_name="Tanggal Penetapan")
    class Meta:
        empty_text = "Tidak ada data"
        orderable = False
        model = models.pemenang
        template_name = "tables/table_kebawah.html"
        fields = ("nomor","judul","tanggal","keterangan","file_link", "bidder",  "auctioneer",  "viewer", "created","dibuat_oleh","last_updated","diubah_oleh", )
        
class pemenangnya2Table(tables.Table):
    file_link = TemplateColumn(template_code='<a target="_blank" class="btn btn-sm btn-info" href="{{record.file_link.url}}" ><i class="fa fa-download"></i>&nbsp;&nbsp;Unduh File Keputusan</a>', verbose_name = "File Keputusan")
    tanggal = tables.DateTimeColumn(format ='d F Y',  verbose_name="Tanggal Penetapan")
    class Meta:
        empty_text = "Tidak ada data"
        orderable = False
        model = models.pemenang
        template_name = "tables/table_kebawah.html"
        fields = ("nomor","judul","tanggal","keterangan","file_link",)
        

#pengumuman penetapan pemenang

class pemenang_pengumumanTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex;"><button id="{{ record.id }}" class="p_pengumuman_update btn btn-sm btn-warning"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="p_pengumuman_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    class Meta:
        model = models.pengumuman_pemenang
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","keterangan","file_link",)
        
class pemenang_pengumuman2Table(tables.Table):
    class Meta:
        model = models.pengumuman_pemenang
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","keterangan","file_link",)      
        
#beritaacara

class berita_acara_pasca_seleksiTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="ba_update btn btn-sm btn-warning"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="ba_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    class Meta:
        model = models.berita_acara_pasca_seleksi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","link_file", "keterangan",)
        
class berita_acara_pasca_seleksi2Table(tables.Table):
    class Meta:
        model = models.berita_acara_pasca_seleksi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","link_file", "keterangan",)

#form_ps_sanggahan
class form_pasca_sanggahannyaTable(tables.Table):
    Aksi = TemplateColumn(template_code='<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button>')
    file = TemplateColumn(template_code='{% if record.file %}<a class="btn btn-sm btn-info" target="_blank" href="{{record.file.url}}" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh Bukti Penyampaian Sanggahan</a>{% else %}<p>-</p>{% endif %}', verbose_name="Bukti Penyampaian Sanggahan")
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Pengiriman Sanggahan (WIB)")
    bidder = TemplateColumn(verbose_name="Nama Perusahaan",template_code='{{record.bidder.bidder.nama_perusahaan}}')
    class Meta:
        model = models.form_ps_sanggahan
        empty_text = "Tidak ada data"
        orderable = False

        template_name = "tables/table_sanggahan.html"
        fields = ("bidder","status_sanggah","keterangan","file","created","Aksi")
        
#undangan_kirim        
class undg_ps_sanggahannyaTable(tables.Table):
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="undg_sanggah_update btn btn-sm btn-warning"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="undg_sanggah_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    class Meta:
        model = models.undangan_ps_sanggahan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("bidder","nomor","judul","tanggal","tempat","agenda","keterangan","link_teleconference","file",)
        
##Jawaban sanggahan pasca seleksi
class pasca_jawaban_sanggahannyaTable(tables.Table):
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" ><img class="fa fa-file-pdf" data_1="{{record.file.url}}" ></i></a>')
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal dibuat")
    jawaban_sanggah = TemplateColumn(template_code='{% if record.jawaban_sanggah == "Ada"  %}<span class="rounded-pill btn-success" style="padding:5px;"><i class="fa fa-check-circle"></i>&nbsp;Diterima</span>{%else%}<span class="rounded-pill btn-danger" style="padding:5px;"><i class="fa fa-check-xmark"></i>&nbsp;Ditolak</span>{%endif%}')
    tindak_lanjut_seleksi = TemplateColumn(template_code='{% if record.tindak_lanjut_seleksi == "Lanjut"  %}<span class="rounded-pill btn-success" style="padding:5px;"><i class="fa fa-check-circle"></i>&nbsp;Lanjut</span>{% elif record.tindak_lanjut_seleksi == "Berhenti Sementara" %}<span class="rounded-pill btn-danger" style="padding:5px;"><i class="fa fa-check-xmark"></i>&nbsp;Berhenti Sementara</span>{%else%}<span class="rounded-pill btn-danger">Berhenti</span>{%endif%}')
    # actions = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="jawaban_sanggah_update btn btn-sm btn-warning"><i class="fa fa-edit "></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="jawaban_sanggah_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    class Meta:
        model = models.jawaban_ps_sanggahan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("bidder","jawaban_sanggah","keterangan","tindak_lanjut_seleksi","file","created", "dibuat_oleh", "last_updated","diubah_oleh", "Aksi")
        
#form_ps_sanggahan
class form_pasca_sanggahannyaTable2(tables.Table):
   #file = TemplateColumn(template_code='<a target="_blank" href="/media/{{ record.file }}" "><img class="fa fa-file-pdf" data_1="{{record.file.url}}" ></i></a>')
    file = TemplateColumn(template_code='{% if record.file %}<a class="btn btn-sm btn-info" target="_blank" href="{{record.file.url}}" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh Bukti Penyampaian Sanggahan</a>{% else %}<p>-</p>{% endif %}', verbose_name="Bukti Penyampaian Sanggahan")
    status_sanggah = TemplateColumn(template_code='{% if record.status_sanggah == "Ada" %}<span class="rounded-pill bg-green" style="padding:5px;"><i class="fa fa-check-circle"></i>&nbsp;Sanggah</span>{%else%}<span class="btn btn-sm bg-danger" style="padding:5px;"><i class="fa fa-check-xmark"></i>&nbsp;Tidak Sanggah</span>{%endif%}')
    #bidder = TemplateColumn( verbose_name="Nama Perwakilan",template_code='{{record.bidder.nama_lengkap}}')
    bidder = TemplateColumn(verbose_name="Nama Perusahaan",template_code='{{record.bidder.bidder.nama_perusahaan}}')
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Pengiriman Sanggahan (WIB)")
   
    #last_updated = tables.Column(verbose_name="Waktu Diubah")
    class Meta:
        model = models.form_ps_sanggahan
        template_name = "tables/table_kebawah_pecah2.html"
        fields = ("bidder","status_sanggah","keterangan","file","created",)
        
#undangan_kirim        
class undg_ps_sanggahannyaTable2(tables.Table):
    class Meta:
        model = models.undangan_ps_sanggahan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("bidder","nomor","judul","tanggal","tempat","agenda","keterangan","link_teleconference","file",)
        
##Jawaban sanggahan pasca seleksi
class pasca_jawaban_sanggahannyaTable2(tables.Table):
    file = TemplateColumn(template_code='{% if record.file %}<a class="btn btn-sm btn-info" target="_blank" href="{{record.file.url}}" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh Justifikasi Jawaban</a>{% else %}<p>-</p>{% endif %}', verbose_name="Justifikasi Jawaban Sanggahan")
    jawaban_sanggah = TemplateColumn(template_code='{% if record.jawaban_sanggah == "Ada"  %}<span class="rounded-pill btn-success" style="padding:5px;"><i class="fa fa-check-circle"></i>&nbsp;Diterima</span>{%else%}<span class="rounded-pill bg-danger" style="padding:5px;"><i class="fa fa-check-xmark"></i>&nbsp;Ditolak</span>{%endif%}')
    tindak_lanjut_seleksi = TemplateColumn(template_code='{% if record.tindak_lanjut_seleksi == "Lanjut"  %}<span class="rounded-pill btn-success" style="padding:5px;"><i class="fa fa-check-circle"></i>&nbsp;Lanjut</span>{% elif record.tindak_lanjut_seleksi == "Berhenti Sementara" %}<span class="rounded-pill btn-danger" style="padding:5px;"><i class="fa fa-check-xmark"></i>&nbsp;Berhenti Sementara</span>{%else%}<span class="rounded-pill btn-danger">Berhenti</span>{%endif%}')
    #Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    
    class Meta:
        model = models.jawaban_ps_sanggahan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("bidder","jawaban_sanggah","keterangan","tindak_lanjut_seleksi","file",)
        
#pemenang seleksi
class pemenang_bloknyaTable(tables.Table):
    item = tables.Column(verbose_name="Obyek Seleksi")
    #penawaran = TemplateColumn(verbose_name="Harga Penawaran",template_code='Rp. {% record.penawaran %}')
    penawaran = TemplateColumn(template_code='{{record.penawaran}}',verbose_name='Harga Penawaran')
    actions = TemplateColumn(verbose_name="Aksi",template_code='<div><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit "></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    class Meta:
        model = models.pemilihan_blok_pasca_seleksi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = (
            "item","bidder","ranking","penawaran","keterangan"
        )