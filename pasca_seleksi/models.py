from django.db import models
from adm_lelang.models import item_lelang
from adm_lelang.models import detail_itemlelang
from userman.models import bidder, tim_lelang, bidder_perwakilan, bidder_user, Users
from userman.models import Users
from django.utils import timezone

# Create your models here.
# undangan pemilihan blok
class blok(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    users = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)

    # Fields
    nomor = models.CharField()
    judul = models.CharField(max_length=100)
    tanggal = models.DateTimeField()
    tempat = models.CharField(max_length=100)
    agenda = models.TextField()
    link_teleconference = models.TextField()
    keterangan = models.TextField()
    link_file = models.FileField(upload_to="upload/files/pasca_seleksi/blok/")

    # default
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

# pemilihan blok
class blok_pasca_seleksi(models.Model):
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, null=True)
    nama_block = models.CharField(verbose_name="Nama Blok", max_length=100)
    class Meta:
        pass
    def __str__(self):
        return str(self.nama_block)

class pemilihan_blok_pasca_seleksi(models.Model):

    # foreign key
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, null=True)
    item_lelang = models.IntegerField(null=True)
    bidder = models.ForeignKey(bidder_user, verbose_name="Nama Perusahaan", on_delete=models.CASCADE, null=True)
    ranking = models.IntegerField(null=True, blank=True)
    blok = models.ForeignKey(blok_pasca_seleksi, on_delete=models.CASCADE, null=True)
    # Fields
    pilih_blok = models.BooleanField(verbose_name="Pilih Blok", default=False)
    penawaran = models.FloatField(verbose_name="Penawaran", null=True)
    persetujuan = models.BooleanField(verbose_name="Persetujuan", default=False)
    sudah_pilih = models.BooleanField(verbose_name="Sudah Memilih", default=False)
    keterangan = models.TextField(blank=True, null=True)
    # default
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class hasil_blok_pasca_seleksi(models.Model):
    pilih_block = models.ForeignKey(pemilihan_blok_pasca_seleksi, on_delete=models.CASCADE, null=True)
    block = models.ForeignKey(blok_pasca_seleksi, on_delete=models.CASCADE, null=True)
    dipilih = models.BooleanField(False)

# hasil seleksi akhir

# hasil seleksi
class seleksi(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)

    # Fields
    nomor = models.IntegerField()
    judul = models.CharField(max_length=100)
    tanggal = models.DateField()
    keterangan = models.TextField()
    file_link = models.FileField(upload_to="upload/files/pasca_seleksi/seleksi/")

    # default
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)   

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

# kirim sanggahan
class sanggahan(models.Model):
    HASIL_PEMERIKSAAN_CHOICES = (
        ('Ada', 'Sanggah'),
        ('Tidak Ada', 'Tidak Sanggah'),
       
    )

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
   
    # Fields
    status_sanggahan = models.CharField(max_length=10,null=True, blank=True, choices=HASIL_PEMERIKSAAN_CHOICES, default='na')
    file_link = models.FileField(upload_to="upload/files/pasca_seleksi/sanggahan/")
    waktu_sanggahan = models.DateTimeField(default=timezone.now)
    keterangan = models.TextField(blank=True, null=True)
    bidder = models.ForeignKey(bidder_perwakilan, on_delete=models.CASCADE, null=True)

    # default
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)   
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_paska_sanggahan")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_paska_sanggahan")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
    
# sanggahan dan jawaban
class sanggahan_jawaban(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)

    # Fields
    nomor = models.IntegerField()
    judul = models.CharField(max_length=100)
    tanggal = models.DateField()
    tempat = models.CharField(max_length=100)
    waktu = models.DateTimeField()
    agenda = models.TextField()
    link_teleconference = models.TextField()
    keterangan = models.TextField()
    link_file = models.FileField(upload_to="upload/files/pasca_seleksi/sanggahan_jawaban/")

    # default
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

# jawaban atas sanggahan
class jawaban_atas_sanggahan(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    nama_perusahaan = models.ForeignKey(bidder, on_delete=models.CASCADE, null=True)

    # Fields
    sampul1 = models.CharField(max_length=100)
    bidbond = models.CharField(max_length=100)
    hasil_sanggahan = models.CharField(max_length=100)

    # default
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

# penetapan pemenang
class pemenang(models.Model):
    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ManyToManyField('userman.bidder_user', blank=True)
    auctioneer = models.ManyToManyField('userman.tim_lelang', blank=True)
    viewer = models.ManyToManyField('userman.viewers', blank=True)

    # Fields
    nomor = models.CharField(max_length=100, blank=True, null=True)
    judul = models.CharField(max_length=100, blank=True, null=True)
    tanggal = models.DateField(blank=True, null=True, verbose_name="Tanggal Penetapan")
    keterangan = models.TextField()
    file_link = models.FileField(upload_to="upload/files/pasca_seleksi/pemenang/", max_length=255)

    # default
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)   

    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_pemenang")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_pemenang")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

# pengumuman penetapan pemenang
class pengumuman_pemenang(models.Model):
    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)

    # Fields
    nomor = models.IntegerField()
    judul = models.CharField(max_length=100)
    tanggal = models.DateField()
    keterangan = models.TextField()
    file_link = models.FileField(upload_to="upload/files/pasca_seleksi/pemenang/")

    # default
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)   

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
    
# semua berita acara
# berita acara
class berita_acara_pasca_seleksi(models.Model):
    OWNER_CHOICES = (
        ("PEMILIHAN", "Pemilihan"),
        ("HASIL", "Hasil"),
        ("SANGGAHAN", "Sanggahan"),
        ("PENETAPAN", "Penetapan"),
    )
    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)

    # Fields
    nomor = models.CharField()
    judul = models.CharField(max_length=100)
    tanggal = models.DateField()
    keterangan = models.TextField(max_length=100, null=True, blank=True)
    link_file = models.FileField(upload_to="upload/files/pasca_seleksi/ba/")
    owner = models.TextField(max_length=100, null=True, blank=True, choices=OWNER_CHOICES, default="UNKNOWN")
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

#form sanggahan
#ps for pasca seleksi
class form_ps_sanggahan(models.Model):
    HASIL_PEMERIKSAAN_CHOICES = (
        ('Ada', 'Sanggah'),
        ('Tidak Ada', 'Tidak Sanggah'),
       
    )
    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, null=True)

    # Fields
    status_sanggah = models.CharField(max_length=10,null=True, blank=True, choices=HASIL_PEMERIKSAAN_CHOICES, default='na')
    # status_sanggah = models.BooleanField(default=False)
    file = models.FileField(upload_to="upload/files/")
    keterangan = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    waktu_sanggahan = models.DateTimeField(default=timezone.now)
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_form_ps_sanggahan")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_form_ps_sanggahan")
    class Meta:
        pass

    def __str__(self):
        return str(self.pk) 
    
#kirim undnagan sanggah pasca seleksi
    
class undangan_ps_sanggahan(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder, on_delete=models.CASCADE, null=True)
    auctioneer = models.ForeignKey(tim_lelang, on_delete=models.CASCADE, blank=True, null=True)

    # Fields
    nomor = models.CharField( null=True, blank=True)
    judul = models.CharField( null=True, blank=True)
    tanggal = models.DateTimeField(default=timezone.now, null=True, blank=True)
    tempat = models.TextField( null=True, blank=True)
    agenda = models.TextField( null=True, blank=True)
    keterangan = models.TextField( null=True, blank=True)
    link_teleconference = models.TextField( null=True, blank=True)
    file = models.FileField(upload_to="upload/files/")
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
    
    
#Jawaban sanggahan pasca seleksi

class jawaban_ps_sanggahan(models.Model):
    HASIL_PEMERIKSAAN_CHOICES = (
        ('Diterima', 'Diterima'),
        ('Ditolak', 'Ditolak'),
    )
    
    TINDAK_LANJUT_CHOICES = (
        ('Berhenti', 'Berhenti'),
        ('Lanjut', 'Lanjut'),
        ('Berhenti Sementara', 'Berhenti Sementara'),
    )
    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, null=True)

    # Fields
    jawaban_sanggah = models.CharField(max_length=10,null=True, blank=True, choices=HASIL_PEMERIKSAAN_CHOICES, default='na')
    keterangan = models.TextField(blank=True, null=True)
    tindak_lanjut_seleksi = models.CharField(max_length=20,null=True, blank=True, choices=TINDAK_LANJUT_CHOICES, default='Lanjut')
    file = models.FileField(upload_to="upload/files/", max_length=255)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_jawaban_ps_sanggahan")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="diubah_oleh_jawaban_ps_sanggahan")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
    
    
