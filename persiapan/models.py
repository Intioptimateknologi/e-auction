from operator import truediv
from pyexpat import model
from django.db import models
from adm_lelang.models import item_lelang, auctioner_lelang, bidder_lelang, tahapan_lelang, tahapan_lelang2
from userman.models import bidder, bidder_perwakilan, tim_lelang, Users, bidder_user
from datetime import date, datetime
from django.utils import timezone


# p untuk persiapan
# undangan
class p_dokumen(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ManyToManyField('userman.bidder', blank=True)
    auctioneer = models.ManyToManyField('userman.tim_lelang', blank=True)
    tahapan = models.ForeignKey(tahapan_lelang, on_delete=models.CASCADE, blank=True, null=True)

    # Fields
    nomor = models.CharField(null=True, blank=True)
    judul = models.CharField( null=True, blank=True)
    tanggal = models.DateTimeField(null=True, blank=True)
    tempat = models.TextField( null=True, blank=True)
    agenda = models.CharField( null=True, blank=True)
    keterangan = models.TextField( null=True, blank=True)
    link_teleconference = models.TextField( null=True, blank=True)
    file = models.FileField(upload_to="upload/files/", blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_p_dokumen")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_p_dokumen")


    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
    
class penyusunan_jawaban(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder, on_delete=models.CASCADE, blank=True, null=True)
    auctioneer = models.ForeignKey(tim_lelang, on_delete=models.CASCADE, blank=True, null=True)

    # Fields
    nomor = models.CharField(null=True, blank=True)
    judul = models.CharField( null=True, blank=True)
    tanggal = models.DateTimeField(null=True, blank=True)
    tempat = models.TextField( null=True, blank=True)
    agenda = models.CharField( null=True, blank=True)
    keterangan = models.TextField( null=True, blank=True)
    link_teleconference = models.TextField( null=True, blank=True)
    file = models.FileField(upload_to="upload/files/")
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_penyusunan_jawaban")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_penyusunan_jawaban")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
    
class aanwizing(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder, on_delete=models.CASCADE, blank=True, null=True)
    auctioneer = models.ForeignKey(tim_lelang, on_delete=models.CASCADE, blank=True, null=True)

    # Fields
    nomor = models.CharField(null=True, blank=True)
    judul = models.CharField( null=True, blank=True)
    tanggal = models.DateTimeField(null=True, blank=True)
    tempat = models.TextField( null=True, blank=True)
    agenda = models.CharField( null=True, blank=True)
    keterangan = models.TextField( null=True, blank=True)
    link_teleconference = models.TextField( null=True, blank=True)
    file = models.FileField(upload_to="upload/files/")

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_aanwizing")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_aanwizing")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class simulasi(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder, on_delete=models.CASCADE, blank=True, null=True)
    auctioneer = models.ForeignKey(tim_lelang, on_delete=models.CASCADE, blank=True, null=True)

    # Fields
    nomor = models.CharField(null=True, blank=True)
    judul = models.CharField( null=True, blank=True)
    tanggal = models.DateTimeField(null=True, blank=True)
    tempat = models.TextField( null=True, blank=True)
    agenda = models.CharField( null=True, blank=True)
    keterangan = models.TextField( null=True, blank=True)
    link_teleconference = models.TextField( null=True, blank=True)
    file = models.FileField(upload_to="upload/files/")

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_simulasi")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_simulasi")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class p_addendum(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder, on_delete=models.CASCADE, blank=True, null=True)
    auctioneer = models.ForeignKey(tim_lelang, on_delete=models.CASCADE, blank=True, null=True)

    # Fields
    nomor = models.CharField(null=True, blank=True)
    judul = models.CharField( null=True, blank=True)
    tanggal = models.DateTimeField(null=True, blank=True)
    tempat = models.TextField( null=True, blank=True)
    agenda = models.CharField( null=True, blank=True)
    keterangan = models.TextField( null=True, blank=True)
    link_teleconference = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="upload/files/")

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_paddendum")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_paddendum")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class pengambilan_dokumen_addendum(models.Model):
    dokumen_addendum = models.ForeignKey(p_addendum, on_delete=models.CASCADE, null=True)
    bidder_perwakilan = models.ForeignKey(bidder_perwakilan, on_delete=models.CASCADE, null=True)
    tgl_download = models.DateTimeField(auto_now_add=True, editable=False)

    created = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah", blank=True, null=True)

# dokumen
class dokumen_seleksi(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)

    # Fields
    nomor = models.CharField( null=True, blank=True)
    judul = models.CharField( null=True, blank=True)
    tanggal = models.DateTimeField( null=True, blank=True)
    keterangan = models.TextField( null=True, blank=True)
    file = models.FileField(verbose_name="Pengambilan Dokumen Seleksi", upload_to="upload/files/persiapan/dokumen_seleksi/")

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_dokumen_seleksi")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_dokumen_seleksi")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class pengambilan_dokumen_seleksi(models.Model):
    dokumen_seleksi = models.ForeignKey(dokumen_seleksi, on_delete=models.CASCADE, null=True)
    bidder_perwakilan = models.ForeignKey(bidder_perwakilan, on_delete=models.CASCADE, null=True)
    tgl_download = models.DateTimeField(auto_now_add=True, editable=True)

    created = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah", blank=True, null=True)

# pertanyaan
class p_pertanyaan(models.Model):
    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, null=True)

    # Fields
    file_word = models.FileField(upload_to="upload/files/")
    file_pdf = models.FileField(upload_to="upload/files/")
    file_excel = models.FileField(upload_to="upload/files/")
    pertanyaan = models.TextField(max_length=100, blank=True, null=True)
    perwakilan = models.ForeignKey(bidder_perwakilan,on_delete=models.CASCADE, null=True)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_p_pertanyaan")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_p_pertanyaan")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

# berita acara
class berita_acara_persiapan(models.Model):
    OWNER_CHOICES = (
        ("PEMBUKAAN", "Pembukaan"),
        ("DOKUMEN", "Dokumen"),
        ("PERTANYAAN", "Pertanyaan"),
        ("AANWIZING", "Aanwizing"),
        ("SIMULASI", "Simulasi"),
        ("ADDENDUM", "Addendum"),
        ("UNKNOWN", "Unknown"),
    )
    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ManyToManyField('userman.bidder')
    auctioneer = models.ManyToManyField('userman.tim_lelang')
    tahapan = models.ForeignKey(tahapan_lelang, on_delete=models.CASCADE, blank=True, null=True)

    # Fields
    nomor = models.CharField(null=True, blank=True)
    judul = models.CharField( null=True, blank=True)
    tanggal = models.DateTimeField( null=True, blank=True)
    keterangan = models.TextField( null=True, blank=True)
    file = models.FileField(upload_to="upload/files/", blank=True)
    owner = models.TextField(max_length=100, null=True, blank=True, choices=OWNER_CHOICES, default="UNKNOWN")
    # dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_ba_p")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Diubah Terakhir")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
    
class daftar_hadir(models.Model):
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder_perwakilan = models.ForeignKey(bidder_perwakilan, on_delete=models.CASCADE, null=True, verbose_name="Perwakilan Perusahaan")
    tahapan = models.ForeignKey(tahapan_lelang2, on_delete=models.CASCADE, blank=True, null=True)

    nama_perwakilan = models.CharField(null=True, blank=True)
    nama_perusahaan = models.CharField(null=True, blank=True)
    tgl_kehadiran = models.DateField()

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_daftar_hadir")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_daftar_hadir", verbose_name="Diubah Oleh")