from django.db import models
from django.urls import reverse
from userman.models import bidder_user, tim_lelang, tim_lelang, viewers, Users
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey

class jabatan(models.TextChoices):
    Pengarah = "pengarah", "Pengarah"
    Pembina = "pembina", "Pembina"
    Ketua = "ketua", "Ketua"
    Sekretaris = "sekretaris", "Sekretaris"
    Anggota = "anggota", "Anggota"

class bidder_lelang(models.Model):
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, null=True)
    item_lelang = models.ForeignKey("adm_lelang.item_lelang", on_delete=models.CASCADE, null=True)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    eligibility = models.IntegerField(default=0)
    ip_address = models.GenericIPAddressField(null=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="bidder_lelang_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="bidder_lelang_diubah_oleh")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class auctioner_lelang(models.Model):
    auctioner = models.ForeignKey(tim_lelang, on_delete=models.CASCADE, null=True, verbose_name="Auctioneer")
    item_lelang = models.ForeignKey("adm_lelang.item_lelang", on_delete=models.CASCADE, null=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="auctioner_lelang_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="auctioner_lelang_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class viewers_lelang(models.Model):
    viewer = models.ForeignKey(viewers, on_delete=models.CASCADE, null=True)
    item_lelang = models.ForeignKey("adm_lelang.item_lelang", on_delete=models.CASCADE, null=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="viewers_lelang_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="viewers_lelang_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class detail_itemlelang(models.Model):

    STATUS_CHOICES = (
        ('smra', 'smra'),
        ('cca', 'cca'),
    )

    # Relationships
    item_lelang = models.ForeignKey("adm_lelang.item_lelang", on_delete=models.CASCADE)

    # Fields
    urutan = models.IntegerField(null=True, blank=True, default=1)
    teknologi = models.CharField(max_length=100, blank=True)
    band = models.CharField(max_length=10, verbose_name='Pita (MHz)')
    rentang_frekuensi = models.CharField(max_length=100, verbose_name='Rentang (Dari MHz s/d MHz)',blank=True)
    harga_minimal = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    eligibility_point_per_block = models.IntegerField(default=0)
    max_block = models.IntegerField(default=0)
    spectrum_cap = models.IntegerField(default=0)
    emd_price_per_block = models.IntegerField(default=0)
    disabled = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name='Tanggal Diubah')
    # penambahan kolom uat 
    penyelenggaraan = models.CharField(max_length=100, blank=True)
    bandwidth = models.CharField(max_length=100, verbose_name='Lebar Pita (MHz)', blank=True)
    cakupan = models.CharField(max_length=100, verbose_name='Cakupan', blank=True)
    keterangan = models.TextField(max_length=255, blank=True)
    # 
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="detail_itemlelang_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="detail_itemlelang_diubah_oleh")

    class Meta:
        pass

    def __str__(self):
      #  return "Pita {}, rentang {}, cakupan {}, peruntukan {}".format(self.band, self.rentang_frekuensi, self.cakupan, self.penyelenggaraan)
        return "Pita {}-Cakupan {}".format(self.band, self.cakupan)

    def get_absolute_url(self):
        return reverse("adm_lelang_detail_itemlelang_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("adm_lelang_detail_itemlelang_update", args=(self.pk,))



class item_lelang(models.Model):
    # Fields
    tayang = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    nama_lelang = models.TextField(max_length=1000)
    keterangan = models.TextField(max_length=1000)
    tahun= models.CharField(max_length=4, null=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="item_lelang_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="item_lelang_diubah_oleh")

    class Meta:
        pass

    def __str__(self):
        return str(self.nama_lelang)

    def get_absolute_url(self):
        return reverse("adm_lelang_item_lelang_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("adm_lelang_item_lelang_update", args=(self.pk,))

class jadwal_seleksi(models.Model):
    tanggal_awal = models.DateTimeField()
    tanggal_akhir = models.DateTimeField()
    tahap = TreeForeignKey("adm_lelang.tahapan_lelang2", on_delete=models.CASCADE, null=True,related_name='jadwal_seleksi_children')
    perubahan = models.CharField(max_length=100)
    item_lelang = models.ForeignKey("adm_lelang.item_lelang", on_delete=models.CASCADE, null=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="jadwal_seleksi_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="jadwal_seleksi_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, verbose_name="Tanggal Dibuat")
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")
    
    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("adm_lelang_jadwal_seleksi_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("adm_lelang_jadwal_seleksi_update", args=(self.pk,))


class dasar_hukum(models.Model):
    item_lelang = models.ForeignKey("adm_lelang.item_lelang", on_delete=models.CASCADE, null=True)
    
    nomor= models.CharField(max_length=255, null=True)
    judul= models.CharField(max_length=255, verbose_name="Judul Peraturan")
    keterangan= models.CharField(max_length=255, null=True)
    tanggal = models.DateField(blank=True, null=True)
    attachment = models.FileField(upload_to="upload/dasar_hukum/", blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="dasar_hukum_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="dasar_hukum_diubah_oleh")

    def __str__(self):
        return str(self.pk)
    
class persyaratan_lelang(models.Model):
    item_lelang = models.ForeignKey("adm_lelang.item_lelang", on_delete=models.CASCADE, null=True)

    no_urut = models.CharField(max_length=255, null=True, verbose_name="Nomor Urut")
    persyaratan = models.CharField(max_length=255, null=True)
    keterangan = models.CharField(max_length=255, null=True)
    dokumen = models.FileField(upload_to="upload/adm_lelang/", null=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="persyaratan_lelang_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="persyaratan_lelang_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")

    def __str__(self):
        return str(self.pk)

class tahapan_lelang(models.Model):
    tahapan_utama = models.CharField(max_length=255, null=True)
    tahapan = models.CharField(max_length=255, null=True)
    code_tahapan = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.tahapan)

class tahapan_lelang2(MPTTModel):
    name = models.CharField(max_length=255, verbose_name='Tahapan')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    judul = models.CharField(max_length=255, null=True)
    attribute = models.JSONField(null=True)
    orderby = models.IntegerField()
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="tahapan_lelang2_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="tahapan_lelang2_diubah_oleh")

    class MPTTMeta:
        order_insertion_by = ['orderby']

    class Meta:
        ordering = ('lft',)
    def __str__(self):
        return str(self.name)

# ditambahkan baru untuk modul pengumuman pemenang
class pengumuman(models.Model):
    OWNER_CHOICES = (
        ("PEMBUKAAN", "Pembukaan"),
        ("HASIL EVALUASI", "Evaluasi"),
        ("HASIL SELEKSI", "Seleksi"),
        ("PENETAPAN PEMENANG", "Penetepan"),
        ("UNKNOWN", "Unknown"),
    )
    # bidder = models.ForeignKey(bidder, on_delete=models.CASCADE, null=True)
    tahapan = models.ForeignKey(tahapan_lelang2, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="upload/images/")
    nomor= models.CharField(max_length=255, null=True)
    judul= models.CharField(max_length=255, null=True)
    pengumuman= models.TextField(null=True, verbose_name="Keterangan")
    item_lelang = models.ForeignKey("adm_lelang.item_lelang", on_delete=models.CASCADE, null=True)
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    tgl_release = models.DateTimeField(null=True, editable=True, verbose_name="Tanggal Penetapan")
    dokumen = models.FileField(upload_to="upload/adm_lelang/", null=True, verbose_name="File Pengumuman", max_length=255)
    owner = models.TextField(max_length=100, null=True, blank=True, choices=OWNER_CHOICES, default="UNKNOWN")
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, verbose_name="Tanggal Dibuat")
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="pengumuman_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="pengumuman_diubah_oleh")

    def __str__(self):
        return str(self.pk)


class alamat_panitia(models.Model):
    item_lelang = models.ForeignKey("adm_lelang.item_lelang", on_delete=models.CASCADE, null=True)
    alamat = models.CharField(max_length=255, null=True)
    kota = models.CharField(max_length=100, null=True, verbose_name="Kota/Kab")
    provinsi = models.CharField(max_length=100, null=True, verbose_name="Provinsi")
    status = models.BooleanField(default=True)
    keterangan = models.CharField(null=True,)
    kodepos = models.CharField(max_length=5, null=True)
    telp = models.CharField(max_length=25, null=True)
    email = models.CharField(max_length=100, null=True)
    cq = models.CharField(max_length=255, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, blank="true", null="true")
    created = models.DateTimeField(auto_now_add=True, editable=False, blank="true", null="true")
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="alamat_panitia_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="alamat_panitia_diubah_oleh")

    def __str__(self):
        return str(self.tahapan)

class undangan(models.Model):

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder_user = models.ManyToManyField('userman.bidder_user', blank=True)
    auctioneer = models.ManyToManyField('userman.tim_lelang', blank=True)
    viewer = models.ManyToManyField('userman.viewers', blank=True)
    tahapan = models.ForeignKey(tahapan_lelang2, on_delete=models.CASCADE, blank=True, null=True)

    # Fields
    nomor = models.CharField(verbose_name="Nomor", null=True, blank=True)
    judul = models.CharField(verbose_name="Judul",  null=True, blank=True)
    tanggal = models.DateTimeField(verbose_name="Tanggal dibuat", null=True, blank=True)
    waktu_awal = models.DateTimeField(null=True, blank=True) 
    waktu_akhir = models.DateTimeField(null=True, blank=True) 
    tempat = models.TextField(verbose_name="Tempat", null=True, blank=True)
    agenda = models.CharField(verbose_name="Agenda", null=True, blank=True)
    keterangan = models.TextField(verbose_name="Keterangan", null=True, blank=True)
    link_teleconference = models.TextField(verbose_name="Link Telekonferensi", null=True, blank=True)
    file = models.FileField(verbose_name="Berkas", upload_to="upload/files/", max_length=255)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="undangan_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="undangan_diubah_oleh")


    #class Meta:
    #    unique_together = ('item_lelang', 'tahapan',)

    def __str__(self):
        return str(self.pk)

class berita_acara(models.Model):
    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder_user = models.ManyToManyField('userman.bidder_user', blank=True)
    auctioneer = models.ManyToManyField('userman.tim_lelang', blank=True)
    viewer = models.ManyToManyField('userman.viewers', blank=True)
    tahapan = models.ForeignKey(tahapan_lelang2, on_delete=models.CASCADE, blank=True, null=True)

    # Fields
    nomor = models.CharField(null=True, blank=True)
    judul = models.CharField( null=True, blank=True)
    tanggal = models.DateTimeField( null=True, blank=True)
    keterangan = models.TextField( null=True, blank=True)
    file = models.FileField(upload_to="upload/files/", blank=True, default="upload/files/kosong.pdf", max_length=255)
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True,related_name="ba_dibuat_oleh")
    diubah_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True,related_name="ba_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class pengambilan_undangan(models.Model):
    undangan = models.ForeignKey(undangan, on_delete=models.CASCADE, null=True)
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    tgl_download = models.DateTimeField( auto_now_add=True, editable=False)


class pengambilan_ba(models.Model):
    ba = models.ForeignKey(berita_acara, on_delete=models.CASCADE, null=True)
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    tgl_download = models.DateTimeField( auto_now_add=True, editable=False)

class template_berita_acara(models.Model):
    code_menu = [
        ("persiapan", "Persiapan"),
        ("administrasi", "Administrasi"),
        ("beauty_contest", "Beauty Contest"),
        ("gabungan", "Gabungan"),
        ("negosiasi", "Negosiasi"),
        ("pasca_seleksi", "Pasca Seleksi"),
        ("unknown", "Unknown"),
    ]

    code_sub_menu = [
        # persiapan
        ("1_dokumen_seleksi", "Dokumen Seleksi"),
        ("1_pertanyaan", "Pertanyaan"),
        ("1_aanwizing", "Aanwizing"),
        ("1_simulasi", "Simulasi"),
        ("1_pengambilan_addendum_doksel", "Pengambilan Addendum Dokumen Seleksi"),
        # persiapan
        # administrasi
        ("2_permohonan_keikutsertaan", "Permohonan Keikutsertaan"),
        ("2_pemeriksaan_kelengkapan", "Pemeriksaan Kelengkapan"),
        ("2_verifikasi", "Verifikasi"),
        ("2_hasil_evaluasi", "Hasil Evaluasi"),
        ("2_sanggahan1", "Sanggahan Adm"),
        # administrasi
        # beauty contet
        ("3_beauty_contest", "Beauty Contest"),
        # beauty contet
        # gabungan
        ("4_gabungan", "Gabungan"),
        # gabungan
        # negosiasi
        ("5_sampul2", "Sampul 2"),
        ("5_evaluasi_sampul_2", "Evaluasi Sampul 2"),
        ("5_revisi_evaluasi_sampul_2", "Revisi Sampul 2"),
        ("5_evaluasi_revisi_evaluasi_sampul_2", "Evaluasi Revisi Sampul 2"),
        # negosiasi
        # pasca seleksi
        ("6_pemilihan_blok", "Pemilihan Blok"),
        ("6_sanggahan2", "Sanggahan Pasca"),
        # pasca seleksi
        ("unknown", "Unknown"),
    ]
    item_lelang = models.ForeignKey("adm_lelang.item_lelang", on_delete=models.CASCADE, null=True)
    nama_template = models.CharField(max_length=255, null=True, blank=True)
    keterangan_template = models.CharField(max_length=255, null=True, blank=True)
    template_code_menu = models.CharField(verbose_name="Template Menu", max_length=255, null=True, blank=True, choices=code_menu, default="Unknown")
    template_code_sub = models.CharField(verbose_name="Template Submenu", max_length=255, null=True, blank=True, choices=code_sub_menu, default="Unknown")
    dokumen = models.FileField(upload_to="upload/adm_lelang/", null=True)

class penangung_jawab_seleksi(models.Model):
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    nama = models.CharField(null=True, blank=True)
    nip = models.CharField(null=True, blank=True, verbose_name="NIP")
    tanggung_jawab = models.CharField(null=True, blank=True, choices=jabatan.choices,)
    tgl_mulai = models.DateField(null=True, blank=True, verbose_name="Tanggal Mulai")
    tgl_akhir = models.DateField(null=True, blank=True, verbose_name="Tanggal Akhir")
    status = models.BooleanField(default=True)
    keterangan = models.CharField(null=True, blank=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="penangung_jawab_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="penangung_jawab_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")

class template_jadwal_seleksi(models.Model):
    tanggal_awal = models.DateTimeField()
    tanggal_akhir = models.DateTimeField()
    tahap = TreeForeignKey("adm_lelang.tahapan_lelang2", on_delete=models.CASCADE, null=True,related_name='jadwal_seleksi_children2')
    perubahan = models.CharField(max_length=100)
    item_lelang = models.ForeignKey("adm_lelang.item_lelang", on_delete=models.CASCADE, null=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="jadwal_seleksi_dibuat_oleh2")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="jadwal_seleksi_diubah_oleh2")
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True, verbose_name="Tanggal Dibuat2")
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah2")
    
    class Meta:
        managed= False

    def __str__(self):
        return "{}".format(self.pk)

