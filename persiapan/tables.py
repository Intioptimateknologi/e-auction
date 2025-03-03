import django_tables2 as tables
from . import models
from django_tables2 import TemplateColumn

# p untuk persiapan
# undangan
class p_dokumensTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="persiapan_dok_send btn badge mr-1"><i class="icon fa fa-envelope"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="persiapan_dok_update btn btn-sm btn-warning"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="persiapan_dok_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" ><i class="fa fa-download"></i></a>')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    tanggal = tables.DateTimeColumn(format ='d F Y')
    class Meta:
        model = models.p_dokumen
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("nomor","judul","tanggal","tempat","agenda","keterangan", "link_teleconference", "bidder",  "auctioneer",  "diubah_oleh", "file",)
# hanya List Data 
class p_dokumens2Table(tables.Table):
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" class="bidder_download"><img class="fa fa-file-pdf" src="/static/img/pdf.png"style="height: 20px; width: 20px"></a>')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    tanggal = tables.DateTimeColumn(format ='d F Y')

    class Meta:
        model = models.p_dokumen
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("nomor","judul","tanggal","tempat","agenda","keterangan", "link_teleconference", "file",)
        
        
# Penyusun jawab      
class penyusun_jawabTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="penyusun_jawaban_update btn btn-sm btn-warning"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="penyusun_jawaban_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" style="display:flex; align-items: center; justify-content: center; font-size: 20px;"><i class="fa fa-download"></i></a>')
    
    class Meta:
        model = models.penyusunan_jawaban
        empty_text = "Tidak ada data"
        orderable = False
        
        
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","tempat","agenda","keterangan", "link_teleconference", "bidder",  "auctioneer", "diubah_oleh", "file",)
# hanya List Data
class penyusun_jawab2Table(tables.Table):
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" style="display:flex; align-items: center; justify-content: center; font-size: 20px;"><i class="fa fa-download"></i></a>')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    class Meta:
        model = models.penyusunan_jawaban
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal","tempat","agenda","keterangan", "link_teleconference", "file", )
   
        
# Aanwizing       
class aanwizingTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="undangan_send btn badge mr-1"><i class="icon fa fa-envelope"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="persiapan_dok_update btn btn-sm btn-warning"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="persiapan_dok_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" style="display:flex; align-items: center; justify-content: center; font-size: 20px;"><img  class="fa fa-file-pdf" ></i></a>')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    class Meta:
        model = models.aanwizing
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("nomor","judul","tanggal","tempat","agenda","keterangan", "link_teleconference", "bidder",  "auctioneer", "diubah_oleh", "file",)     
# hanya List Data
class aanwizing2Table(tables.Table):
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" style="display:flex; align-items: center; justify-content: center; font-size: 20px;"><img  class="fa fa-file-pdf" ></i></a>')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    
    class Meta:
        model = models.aanwizing
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("nomor","judul","tanggal","tempat","agenda","keterangan", "link_teleconference", "file",)     


# Simulasi
class simulasiTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="undangan_send btn badge mr-1"><i class="icon fa fa-envelope"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="persiapan_dok_update btn btn-sm btn-warning"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="persiapan_dok_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button></div>')
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" style="display:flex; align-items: center; justify-content: center; font-size: 20px;"><img  class="fa fa-file-pdf" ></i></a>')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')

    class Meta:
        model = models.simulasi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("nomor","judul","tanggal","tempat","agenda","keterangan", "link_teleconference", "bidder",  "auctioneer", "diubah_oleh", "file",)   
# hanya List Data
class simulasi2Table(tables.Table):
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" style="display:flex; align-items: center; justify-content: center; font-size: 20px;"><img  class="fa fa-file-pdf" ></i></a>')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    
    class Meta:
        model = models.simulasi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("nomor","judul","tanggal","tempat","agenda","keterangan", "link_teleconference", "file",)     
        
        
# addendum        
class addendumTable(tables.Table):
    file = TemplateColumn(template_code='<a target="_blank" href="/media/{{record.file}}" ><img class="fa fa-file-pdf" src="/static/img/zip_icon.png" style="height: 20px; width: 20px"></a>')

    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit"></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    file = TemplateColumn(template_code='<button id="{{record.id}}" class="btn btn-info btn-sm bidder_download" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh Adendum Dokumen Seleksi</button>')
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Dibuat")
    tanggal = tables.DateTimeColumn(format ='d F Y')
    
    class Meta:
        model = models.p_addendum
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_ambil_dok.html"
        fields = ("nomor","judul","tanggal","keterangan","file","created","dibuat_oleh","last_updated","diubah_oleh",)
        
# hanya List Data        
class addendum2Table(tables.Table):
   # file = TemplateColumn(verbose_name="File Dokumen Seleksi",template_code='<a target="_blank" href="{{record.file.url}}" class="btn btn-info btn-sm bidder_download" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh Dokumen Seleksi</a>')
    file = TemplateColumn(template_code='<button id="{{record.id}}" class="btn btn-info btn-sm bidder_download" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh Adendum Dokumen Seleksi</button>')
   
    tanggal = tables.DateTimeColumn(format ='d F Y ')
    class Meta:
        model = models.p_addendum
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_ambil_dok.html"
        fields = ("nomor","judul","tanggal","keterangan","file",)
        
        
#dokumen

class dokumen_seleksinyaTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div><button id="{{ record.id }}" class="update btn btn-sm btn-warning"><i class="fa fa-edit"></i>&nbsp;&nbsp;Ubah</button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-sm btn-danger"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    file = TemplateColumn(verbose_name="File Dokumen Seleksi",template_code='<a target="_blank" href="{{record.file.url}}" class="btn btn-info btn-sm" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh File Dokumen Seleksi</a>')
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    tanggal = tables.DateTimeColumn(verbose_name="Tanggal Penetapan",format ='d F Y')
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Dibuat")
    class Meta:
        model = models.dokumen_seleksi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("nomor","judul","tanggal", "keterangan", "file",  "created", "dibuat_oleh", "last_updated","diubah_oleh")   
        
# untuk melihat data di ambil oleh siapa
class dokumen_seleksinya2Table(tables.Table):
    file = TemplateColumn(template_code='<button id="{{record.id}}" class="btn btn-info btn-sm bidder_download" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh Dokumen Seleksi</button>')
   # file = TemplateColumn(verbose_name="File Dokumen Seleksi",template_code='<a target="_blank" href="{{record.file.url}}" class="btn btn-info btn-sm bidder_download"><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh Dokumen Seleksi</a>')
   # file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" style="display:flex; align-items: center; justify-content: center; font-size: 20px;"><i class="fa fa-download"></i></a>')
    tanggal = tables.DateTimeColumn(verbose_name="Tanggal Penetapan",format ='d F Y')
    class Meta:
        model = models.dokumen_seleksi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_ambil_dok.html"
        fields = ("nomor","judul","tanggal", "keterangan", "file",)    

# hanya List Data
class dokumen_seleksinya3Table(tables.Table):
    file = TemplateColumn(template_code='<a id="{{ record.id }}" bidder="{{ record.bidder }}" class="link_dokumen_seleksi btn btn-info btn-sm" href="/media/{{record.file}}"><i class="fa-solid fa-eye"></i></a>')
    tanggal = tables.DateTimeColumn(verbose_name="Tanggal Penetapan",format ='d F Y')
    class Meta:
        model = models.dokumen_seleksi
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("nomor","judul","tanggal", "keterangan", "file",)    
        
class status_dokumen_seleksinyaTable(tables.Table):
    dokumen = TemplateColumn(template_code='{{record.dokumen_seleksi.judul}}')
    #nomor = TemplateColumn(template_code='{{record.dokumen_seleksi.nomor}}')
    oleh_perusahaan = TemplateColumn(template_code='{{record.bidder_perwakilan.bidder.bidder.nama_perusahaan}}', verbose_name="Perusahaan")
    oleh_perwakilan = TemplateColumn(template_code='{{record.bidder_perwakilan.nama_lengkap}}', verbose_name="Perwakilan")
   
    tgl_download = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal dan Waktu Unduh (WIB)")
    # file = TemplateColumn(verbose_name="Tanda Terima Bukti Pengambilan Dokumen", template_code='<a target="_blank" href="/persiapan/persiapan/lihat_ba_doksel/{{record.id}}/" ><i class="fa fa-download"></i></a>')
    file = TemplateColumn(verbose_name="Tanda Terima ", template_code='<a class="btn btn-info btn-sm" target="_blank" href="/persiapan/persiapan/lihat_ba_doksel/{{record.id}}/" ><i class="fa fa-download"></i></a>')

    class Meta:
        model = models.pengambilan_dokumen_seleksi
        attrs = {"class": "table table-sm table-striped"}
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("dokumen","tgl_download","oleh_perusahaan","oleh_perwakilan","file")  

class status_dokumen_seleksinya2Table(tables.Table):
    dokumen = TemplateColumn(template_code='{{record.dokumen_seleksi.judul}}')
    #nomor = TemplateColumn(template_code='{{record.dokumen_seleksi.nomor}}')
    #perwakilan = TemplateColumn(template_code='{{record.bidder_perwakilan.nama_lengkap}}')
    oleh_perusahaan = TemplateColumn(template_code='{{record.bidder_perwakilan.bidder.bidder.nama_perusahaan}}', verbose_name="Perusahaan")
    oleh_perwakilan = TemplateColumn(template_code='{{record.bidder_perwakilan.nama_lengkap}}', verbose_name="Perwakilan")
    tgl_download = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal dan Waktu Unduh (WIB)")
    # file = TemplateColumn(
    # verbose_name="Tanda Terima",
    # template_code='<a href="#" data-pdf-url="/persiapan/persiapan/pengambilan_doksel/{{record.id}}/"  data-toggle="modal" data-target="#pdfModal"><i class="fa fa-download"></i></a>'
    # )
   # file = TemplateColumn(template_code='<a class="btn btn-info" href="/persiapan/persiapan/pengambilan_doksel/{{record.id}}/"  data-toggle="modal" data-target="#pdfModal"><i class="fa fa-download"></i></a>')
    file = TemplateColumn(verbose_name="Tanda Terima ", template_code='<a class="btn btn-info btn-sm" target="_blank" href="/persiapan/persiapan/lihat_ba_doksel/{{record.id}}/" ><i class="fa fa-download"></i></a>')

    class Meta:
        model = models.pengambilan_dokumen_seleksi
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        #template_name = "tables/table_ambil_dok.html"
        fields = ("dokumen","tgl_download","oleh_perusahaan","oleh_perwakilan","file",) 
        
        

class pengambilan_addendum_dokselTable(tables.Table):
    dokumen = TemplateColumn(template_code='{{record.dokumen_addendum.judul}}')
    #nomor = TemplateColumn(template_code='{{record.dokumen_addendum.nomor}}')
    oleh_perusahaan = TemplateColumn(template_code='{{record.bidder_perwakilan.bidder.bidder.nama_perusahaan}}', verbose_name="Perusahaan")
    oleh_perwakilan = TemplateColumn(template_code='{{record.bidder_perwakilan.nama_lengkap}}', verbose_name="Perwakilan")
    tgl_download = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal dan Waktu Unduh (WIB)")
    file = TemplateColumn(verbose_name="Tanda Terima ", template_code='<a class="btn btn-info btn-sm" target="_blank" href="/persiapan/persiapan/pengambilan_addendum_pdf/{{record.id}}/" ><i class="fa fa-download"></i></a>')

    class Meta:
        model = models.pengambilan_dokumen_addendum
        empty_text = "Tidak ada data"
        orderable = False

        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("dokumen","tgl_download","oleh_perusahaan","oleh_perwakilan","file")  
        
class pengambilan_addendum_doksel2Table(tables.Table):
    dokumen = TemplateColumn(template_code='{{record.dokumen_addendum.judul}}')
    #nomor = TemplateColumn(template_code='{{record.dokumen_addendum.nomor}}')
    oleh_perusahaan = TemplateColumn(template_code='{{record.bidder_perwakilan.bidder.bidder.nama_perusahaan}}', verbose_name="Perusahaan")
    oleh_perwakilan = TemplateColumn(template_code='{{record.bidder_perwakilan.nama_lengkap}}', verbose_name="Perwakilan")
    tgl_download = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal dan Waktu Unduh (WIB)")
    file = TemplateColumn(template_code='<a target="_blank" href="/media/{{record.dokumen_addendum.file}}" ><img class="fa fa-file-pdf" src="/static/img/zip_icon.png" style="height: 20px; width: 20px"></a>')
    # file = TemplateColumn(
    # verbose_name="Tanda Terima",
    # template_code='<a href="#" data-pdf-url="/persiapan/persiapan/pengambilan_addendum_pdf/{{record.id}}/"  data-toggle="modal" data-target="#pdfModal"><i class="fa fa-download"></i></a>'
    # )
    class Meta:
        model = models.pengambilan_dokumen_addendum
        empty_text = "Tidak ada data"
        orderable = False
        template_name = "django_tables2/custom_bootstrap_tengah.html"
        fields = ("dokumen","tgl_download","oleh_perusahaan","oleh_perwakilan","file")  
#pertanyaan

class p_pertanyaanTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; ">&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    file_word = TemplateColumn(verbose_name="Pertanyaan (Doc)", template_code='<a class="btn bg-info btn-sm"  target="_blank" href="{{record.file_word.url}}" ><i class="fa fa-file-word"></i>&nbsp;&nbsp;Unduh File Doc</a>')
    file_excel = TemplateColumn(verbose_name="Pertanyaan (Xls)",template_code='<a class="btn bg-info btn-sm"  target="_blank" href="{{record.file_excel.url}}" ><i class="fa fa-file-excel"></i>&nbsp;&nbsp;Unduh File Excel</a>')
    file_pdf = TemplateColumn(verbose_name="Pertanyaan (Pdf)",template_code='<a class="btn bg-info btn-sm" target="_blank" href="{{record.file_pdf.url}}" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh File Pdf</a>')
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    nama_perwakilan = TemplateColumn(template_code='<b>{{record.perwakilan.nama_lengkap}}</b>', verbose_name="Perwakilan")
    bidder_perwakilan = TemplateColumn(template_code='<b>{{record.perwakilan.bidder.bidder.nama_perusahaan}}</b>', verbose_name="Perusahaan")
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Penyampaian (WIB)")
    class Meta:
        model = models.p_pertanyaan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("bidder_perwakilan","nama_perwakilan","file_word","file_excel","file_pdf","created",)

# hanya List Data   
class p_pertanyaan2Table(tables.Table):
#    file_word = TemplateColumn(template_code='<a target="_blank" href="{{record.file_word.url}}" ><img class="fa fa-file-pdf" s></a>')
#    file_excel = TemplateColumn(template_code='<a target="_blank" href="{{record.file_excel.url}}" ><img class="fa fa-file-pdf" src="/static/img/xls_icon.png" style="height: 20px; width: 20px"></a>')
#    file_pdf = TemplateColumn(template_code='<a target="_blank" href="{{record.file_pdf.url}}" ><i class="fa fa-download"></i></a>')
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Penyampaian (WIB)")
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    nama_perwakilan = TemplateColumn(template_code='<b>{{record.perwakilan.nama_lengkap}}</b>', verbose_name="Perwakilan")
    bidder_perwakilan = TemplateColumn(template_code='<b>{{record.perwakilan.bidder.bidder.nama_perusahaan}}</b>', verbose_name="Perusahaan")
    class Meta:
        model = models.p_pertanyaan
       # attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah_pecah3.html"
        fields = ("bidder_perwakilan","nama_perwakilan","created")
        
# hanya List Data   
class p_pertanyaan3Table(tables.Table):
    file_word = TemplateColumn(verbose_name="Pertanyaan (Doc)", template_code='<a class="btn bg-info btn-sm"  target="_blank" href="{{record.file_word.url}}" ><i class="fa fa-file-word"></i>&nbsp;&nbsp;Unduh File Doc</a>')
    file_excel = TemplateColumn(verbose_name="Pertanyaan (Xls)",template_code='<a class="btn bg-info btn-sm"  target="_blank" href="{{record.file_excel.url}}" ><i class="fa fa-file-excel"></i>&nbsp;&nbsp;Unduh File Excel</a>')
    file_pdf = TemplateColumn(verbose_name="Pertanyaan (Pdf)",template_code='<a class="btn bg-info btn-sm" target="_blank" href="{{record.file_pdf.url}}" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh File Pdf</a>')
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Penyampaian (WIB)")
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    nama_perwakilan = TemplateColumn(template_code='<b>{{record.perwakilan.nama_lengkap}}</b>', verbose_name="Perwakilan")
    bidder_perwakilan = TemplateColumn(template_code='<b>{{record.perwakilan.bidder.bidder.nama_perusahaan}}</b>', verbose_name="Perusahaan")
    class Meta:
        model = models.p_pertanyaan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah_pecah3.html"
        fields = ("bidder_perwakilan","nama_perwakilan","file_word","file_excel","file_pdf","created")      

class p_pertanyaan4Table(tables.Table):
    #Aksi = TemplateColumn(template_code='<div class="" style="display: flex; ">&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i>&nbsp;&nbsp;Hapus</button></div>')
    file_word = TemplateColumn(verbose_name="Pertanyaan (Doc)", template_code='<a class="btn bg-info btn-sm"  target="_blank" href="{{record.file_word.url}}" ><i class="fa fa-file-word"></i>&nbsp;&nbsp;Unduh File Doc</a>')
    file_excel = TemplateColumn(verbose_name="Pertanyaan (Xls)",template_code='<a class="btn bg-info btn-sm"  target="_blank" href="{{record.file_excel.url}}" ><i class="fa fa-file-excel"></i>&nbsp;&nbsp;Unduh File Excel</a>')
    file_pdf = TemplateColumn(verbose_name="Pertanyaan (Pdf)",template_code='<a class="btn bg-info btn-sm" target="_blank" href="{{record.file_pdf.url}}" ><i class="fa fa-file-pdf"></i>&nbsp;&nbsp;Unduh File Pdf</a>')
    #dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    #diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    nama_perwakilan = TemplateColumn(template_code='<b>{{record.perwakilan.nama_lengkap}}</b>', verbose_name="Perwakilan")
    bidder_perwakilan = TemplateColumn(template_code='<b>{{record.perwakilan.bidder.bidder.nama_perusahaan}}</b>', verbose_name="Perusahaan")
    #last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    created = tables.DateTimeColumn(format ='d F Y H:i:s',  verbose_name="Tanggal Penyampaian (WIB)")
    class Meta:
        model = models.p_pertanyaan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        fields = ("bidder_perwakilan","nama_perwakilan","file_word","file_excel","file_pdf","created",)

#berita acara

class berita_acara_persiapanTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="berita_acara_send btn badge mr-1"><i class="icon fa fa-envelope"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="berita_acara_update btn btn-sm btn-warning"><i class="fa fa-edit circle-icon"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="berita_acara_delete btn btn-sm btn-danger"><i class="icon"><img class="delete_icon" style="height:18px;" src="/static/img/trash-2.svg"></i></button><a href="/persiapan/persiapan/download_ba_doksel/{{ record.id }}/" class="btn badge mr-1"><i class="icon"><img style="height:18px;" src="/static/img/docx.svg"> </i></a></div>')
    file = TemplateColumn(template_code='<a target="_blank" href="{{record.file.url}}" ><i class="fa fa-file-pdf"></i></a>')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    tanggal = tables.DateTimeColumn(format ='d F Y H:i:s')
    
    class Meta:
        model = models.berita_acara_persiapan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        # fields = ("nomor","judul","tanggal","keterangan", "file",)  
        fields = ("nomor","judul","tanggal","keterangan", "bidder",  "auctioneer", "last_updated", "diubah_oleh", "file",)  
# hanya List Data        
class berita_acara_persiapan2Table(tables.Table):
    file = TemplateColumn(template_code='<a class="btn btn-info btn-sm"target="_blank" href="{{record.file.url}}" ><i class="fa fa-file-pdf">&nbsp;&nbsp;Unduh File Berita Acara</i></a>')
    tanggal = tables.DateTimeColumn(format ='d F Y')

    class Meta:
        model = models.berita_acara_persiapan
        attrs = {"class": "table table-sm table-striped"}
        template_name = "tables/table_kebawah.html"
        # fields = ("nomor","judul","tanggal","keterangan", "file",)  
        fields = ("nomor","judul","tanggal","keterangan", "file",)  

# daftar hadir
class daftar_hadirTable(tables.Table):
    Aksi = TemplateColumn(template_code='<div class="" style="display: flex; "><button id="{{ record.id }}" class="update btn btn-warning btn-sm"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;<button id="{{ record.id }}" class="delete btn btn-danger btn-sm"><i class="fa fa-trash"></i></button></div>')
    nama_perwakilan = TemplateColumn(template_code='{{record.bidder_perwakilan.nama_lengkap}}')
    bidder_perwakilan = TemplateColumn(template_code='{{record.bidder_perwakilan.bidder.bidder.nama_perusahaan}}', verbose_name="Perusahaan")
    tgl_kehadiran = tables.DateTimeColumn(format ='d F Y', verbose_name="Tanggal Kehadiran")
    created = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Dibuat")
    last_updated = tables.DateTimeColumn(format ='d F Y H:i:s', verbose_name="Tanggal Diubah")
    dibuat_oleh = TemplateColumn(template_code='{{record.dibuat_oleh.nama_lengkap}} ')
    diubah_oleh = TemplateColumn(template_code='{{record.diubah_oleh.nama_lengkap}} ')
    class Meta:
        model = models.daftar_hadir
        empty_text = "Tidak ada data"
        orderable = False
        
        template_name = "tables/table_dfhadir.html"
        fields = ("nama_perwakilan","bidder_perwakilan","tgl_kehadiran","created","dibuat_oleh","last_updated",  "diubah_oleh",)

class daftar_hadirTable2(tables.Table):
    nama_perwakilan = TemplateColumn(template_code='{{record.bidder_perwakilan.nama_lengkap}}')
    bidder_perwakilan = TemplateColumn(template_code='{{record.bidder_perwakilan.bidder.bidder.nama_perusahaan}}', verbose_name="Perusahaan")
    tgl_kehadiran = tables.DateTimeColumn(format ='d F Y', verbose_name="Tanggal Kehadiran")
    class Meta:
        model = models.daftar_hadir
        empty_text = "Tidak ada data"
        orderable = False
       
        template_name = "tables/table_dfhadir.html"
        fields = ("nama_perwakilan","bidder_perwakilan","tgl_kehadiran",)