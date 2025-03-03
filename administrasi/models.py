from re import T
from django.db import models
from adm_lelang.models import item_lelang
from userman.models import bidder, tim_lelang, bidder_perwakilan, bidder_user, Users
from .validators import validate_pdf
from django.utils import timezone



class jawaban_sanggahan(models.Model):
    HASIL_PEMERIKSAAN_CHOICES = (
        ('Ada', 'Sanggahan Diterima'),
        ('Tidak Ada', 'Sanggahan Ditolak'),
        
    )
    TINDAK_LANJUT_CHOICES = (
        ('Henti', 'Tahapan Seleksi Dihentikan'),
        ('Lanjut', 'Tahapan Seleksi Dilanjutkan'),
        ('Tunda', 'Tahapan Seleksi Ditunda'),
    )
    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, null=True)

    # Fields
    jawaban_sanggah = models.CharField(max_length=10,null=True, blank=True, choices=HASIL_PEMERIKSAAN_CHOICES, default='na')
    keterangan = models.TextField(blank=True, null=True)
    tindak_lanjut_seleksi = models.CharField(max_length=10,null=True, blank=True, choices=TINDAK_LANJUT_CHOICES, default='Tunda')
    file = models.FileField(upload_to="upload/files/")
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_jawaban_sanggahan")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_jawaban_sanggahan")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

# form pemeriksaan kelengkapan
class form_pemeriksaan(models.Model):
    HASIL_PEMERIKSAAN_CHOICES = (
        ('Ada', 'Ada'),
        ('Tidak Ada', 'Tidak Ada'),
        ('na', 'N/A'),
    )
    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    #bidder = models.ForeignKey(bidder, on_delete=models.CASCADE, null=True, blank=True)
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, null=True, verbose_name='Perusahaan')
    # Fields
    sampul1 = models.CharField(max_length=10,null=False, blank=True, choices=HASIL_PEMERIKSAAN_CHOICES, default='na')
    bidbond = models.CharField(max_length=10, blank=False, null=True, choices=HASIL_PEMERIKSAAN_CHOICES, default='na')
    sampul2 = models.CharField(max_length=10, blank=False, null=True, choices=HASIL_PEMERIKSAAN_CHOICES, default='na')
    keterangan = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="upload/files/")
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_form_pemeriksaan")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_form_pemeriksaan")

    class Meta:
        pass

    def __str__(self):
        return str(self.bidder.nama_perusahaan)
    @property
    def kesimpulan(self):
        return self.sampul1=="Ada" and self.sampul2 == "Ada" and self.bidbond == 'Ada'

class form_verifikasi(models.Model):
    HASIL_PEMERIKSAAN_CHOICES = (
        ('Ada', 'Sesuai'),
        ('Tidak Ada', 'Tidak Sesuai'),
        ('na', 'N/A'),
    )
    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, null=True)

    # Fields
    sampul1 = models.CharField(max_length=10,null=True, blank=True, choices=HASIL_PEMERIKSAAN_CHOICES, default='na')
    bidbond = models.CharField(max_length=10, blank=True, null=True, choices=HASIL_PEMERIKSAAN_CHOICES, default='na')
    keterangan = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="upload/files/")
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_form_verifikasi")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_form_verifikasi")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)    
    @property
    def kesimpulan(self):
        return self.sampul1=="Ada" and self.bidbond == 'Ada'

    
class form_evaluasi(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, null=True)

    # Fields
    hasil_pemeriksaan = models.BooleanField(default=False)
    keterangan = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="upload/files/", blank=True)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_form_evaluasi")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_form_evaluasi")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk) 

class form_sanggahan(models.Model):
    HASIL_PEMERIKSAAN_CHOICES = (
        ('Ada', 'Melakukan Sanggahan'),
        ('Tidak Ada', 'Tidak Melakukan Sanggah'),
        
    )
    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    #perwakilan = models.ForeignKey(bidder_perwakilan, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, null=True)

    # Fields
    status_sanggah = models.CharField(max_length=10,null=True, blank=True, choices=HASIL_PEMERIKSAAN_CHOICES, default='na')
    # status_sanggah = models.BooleanField(default=False)
    file = models.FileField(upload_to="upload/files/", blank=True, null=True)
    waktu_sanggahan = models.DateTimeField(default=timezone.now)
    keterangan = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_form_sanggahan")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_form_sanggahan")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk) 

class permohonan_keikutsertaan(models.Model):
    PERNYATAAN_CHOICES = (
        ("MENGIKUTI", "Mengikuti Seleksi Pengguna Izin Pita Frekuensi Radio"),
        ("TIDAK_MENGIKUTI", "Tidak Mengikuti Seleksi Pengguna Izin Pita Frekuensi Radio"),
        ("UNKNOWN", "Unknown"),
    )

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, null=True, blank=True)
    perwakilan = models.ForeignKey(bidder_perwakilan,on_delete=models.CASCADE, null=True, blank=True)
    

    # Fields
    pernyataan = models.TextField(max_length=100, null=True, blank=True, choices=PERNYATAAN_CHOICES, default="UNKNOWN")
    file = models.FileField(upload_to="upload/files/",blank=True,null=True)
    file2 = models.FileField(upload_to="upload/files/",blank=True,null=True)
    status = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_permohonan_keikutsertaan")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_permohonan_keikutsertaan")


    class Meta:
        #unique_together = ('item_lelang', 'bidder',)
        pass

    def __str__(self):
        return str(self.pk)

# 
class hasil_evaluasi(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)

    # Fields
    nomor = models.CharField( null=True, blank=True)
    judul = models.CharField( null=True, blank=True)
    tanggal = models.DateTimeField(default=timezone.now, null=True, blank=True)
    pengumuman = models.TextField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to="upload/files/")
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_hasil_evaluasi")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_hasil_evaluasi")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
# 

# berita acara/ ini abaikan
class berita_acara_administrasi(models.Model):
    OWNER_CHOICES = (
        ("PERMOHONAN", "Permohonan"),
        ("PEMERIKSAAN", "Pemeriksaan"),
        ("VERIFIKASI", "Verifikasi"),
        ("HASIL", "Hasil"),
        ("SANGGAHAN", "Sanggahan"),
        ("EVALUASI", "Evaluasi"),
        ("AKUN", "Akun"),
        ("UNKNOWN", "Unknown"),
    )

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder, on_delete=models.CASCADE, blank=True, null=True)
    auctioneer = models.ForeignKey(tim_lelang, on_delete=models.CASCADE, blank=True, null=True)
    
    # Fields
    nomor = models.CharField( null=True, blank=True)
    judul = models.CharField( null=True, blank=True)
    file = models.FileField(upload_to="upload/files/")
    tanggal = models.DateTimeField( null=True, blank=True)
    keterangan = models.TextField( null=True, blank=True)
    owner = models.TextField(max_length=100, null=True, blank=True, choices=OWNER_CHOICES, default="UNKNOWN")
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
# ini abaikan

class hasil_kesimpulan(models.Model):
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, blank=True, null=True)
    kesimpulan1 = models.BooleanField(verbose_name="Hasil Pemeriksaan Kelengkapan")
    kesimpulan2 = models.BooleanField(verbose_name="Hasil Verifikasi")
    kesimpulan3 = models.BooleanField(verbose_name="Hasil Evaluasi")
    keterangan = models.TextField(verbose_name="Keterangan")
    created = models.DateTimeField()
    hasil_pemeriksaan = models.BooleanField()
    file = models.CharField(max_length=255, null=True, blank=True)
    last_updated = models.DateTimeField()
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_hasil_kesimpulan")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_hasil_kesimpulan")
#    kelengkapan_sampul1 = models.CharField( max_length=10, null=True, blank=True)
#    kelengkapan_bidbond = models.CharField( max_length=10, null=True, blank=True)
#    kelengkapan_sampul2 = models.CharField( max_length=10, null=True, blank=True)
#    verifikasi_sampul1 = models.CharField( max_length=10, null=True, blank=True)
#    verifikasi_bidbond = models.CharField( max_length=10, null=True, blank=True)

    class Meta:
        managed=False

class hasil_sementara(models.Model):
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    # bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, blank=True, null=True)
    bidder = models.ForeignKey(bidder, on_delete=models.CASCADE, blank=True, null=True)
    kesimpulan1 = models.BooleanField(verbose_name="Hasil Pemeriksaan Kelengkapan")
    kesimpulan2 = models.BooleanField(verbose_name="Hasil Verifikasi")
    kesimpulan3 = models.BooleanField(verbose_name="Hasil Evaluasi")
#    kelengkapan_sampul1 = models.CharField( max_length=10, null=True, blank=True)
#    kelengkapan_bidbond = models.CharField( max_length=10, null=True, blank=True)
#    kelengkapan_sampul2 = models.CharField( max_length=10, null=True, blank=True)
#    verifikasi_sampul1 = models.CharField( max_length=10, null=True, blank=True)
#    verifikasi_bidbond = models.CharField( max_length=10, null=True, blank=True)

    class Meta:
        managed=False

