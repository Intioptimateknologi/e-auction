from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
#from ckeditor.fields import RichTextField
from prose.fields import RichTextField

from userman.models import Users

class banner(models.Model):
    JENIS_TAG= [
        ("front", "Aktif"),
        ("back", "Non Aktif"),
    ]
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Diubah Terakhir")
    nama_banner = models.CharField()
    image = models.ImageField(upload_to="upload/images/")
    tag = models.CharField(max_length=120, choices=JENIS_TAG)
    caption = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name="Diubah Oleh", related_name="diubah_oleh_banner")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_banner")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("portal_banner_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("portal_banner_update", args=(self.pk,))

class aturan_lelang(models.Model):
    JENIS_KEBIJAKAN_CHOICES= [
        ("Undang - Undang", "Undang - Undang"),
        ("Peraturan Pemerintah", "Peraturan Pemerintah"),
        ("Peraturan Presiden", "Peraturan Presiden"),
        ("Keputusan Presiden", "Keputusan Presiden"),
        ("Instruksi Presiden", "Instruksi Presiden"),
        ("Peraturan Menteri Komunikasi dan Informatika", "Peraturan Menteri Komunikasi dan Informatika"),
        ("Keputusan Menteri Komunikasi dan Informatika", "Keputusan Menteri Komunikasi dan Informatika"),
        ("Pedoman Menteri Komunikasi dan Informatika", "Pedoman Menteri Komunikasi dan Informatika"),
        ("Lain-Lain", "Lain-Lain"),
    ]

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Diubah Terakhir")
    jenis_kebjakan = models.CharField(max_length=120, choices=JENIS_KEBIJAKAN_CHOICES)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    nomor = models.CharField(max_length=100)
    #file = models.FileField(upload_to="upload/files/")
    file = models.FileField(upload_to="upload/aturan_lelang/")
    nama_kebijakan = models.CharField(blank=True, null=True)
    tahun = models.DateField(blank=True, null=True)
    tanggal = models.DateField(blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name="Diubah Oleh", related_name="diubah_oleh_aturan_lelang")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_aturan_lelang")
    
    
    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("portal_aturan_lelang_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("portal_aturan_lelang_update", args=(self.pk,))

class notice_lelang(models.Model):
    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Diubah Terakhir")
    nama_notice = models.CharField(blank=True, null=True)
    tanggal = models.DateField(blank=True, null=True)
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name="Diubah Oleh", related_name="diubah_oleh_notice_lelang")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_notice_lelang")
    
    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("portal_notice_lelang_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("portal_notice_lelang_update", args=(self.pk,))


class history_lelang(models.Model):

    # Fields
    image = models.ImageField(upload_to="upload/images/")
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Diubah Terakhir")
    hasil = models.CharField(blank=True, null=True)
    penyelenggaraan = models.CharField(blank=True, null=True)
    nama_lelang = models.CharField(blank=True, null=True)
    pemenang = models.TextField(blank=True, null=True)
    tahun = models.CharField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    keterangan = models.TextField(blank=True, null=True)
    pita = models.CharField(blank=True, null=True)
    bandwidth = models.CharField(blank=True, null=True)
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name="Diubah Oleh", related_name="diubah_oleh_histori_lelang")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_histori_lelang")
   

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("portal_history_lelang_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("portal_history_lelang_update", args=(self.pk,))
    
    
class portal_block(models.Model):

    # Fields
    image_header = models.ImageField(upload_to="upload/images/")
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Diubah Terakhir")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    tag = models.TextField(max_length=25)
    judul = models.CharField(max_length=100, verbose_name="Isi konten")
    content = RichTextField(verbose_name="Konten")
    order = models.IntegerField(null=True)
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name="Diubah Oleh", related_name="diubah_oleh_portal_blok")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("portal_portal_block_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("portal_portal_block_update", args=(self.pk,))

class lelang_mancanegara(models.Model):

    # Fields
    #image = models.ImageField(upload_to="upload/images/")
    image = models.ImageField(upload_to="upload/images/")
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Diubah Terakhir")
    keterangan = RichTextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    tahun = models.CharField(max_length=4)
    pita = models.TextField(max_length=100)
    negara = CountryField()
    nama_negara = models.CharField(max_length=100, blank=True, null=True)
    bandwidth = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name="Diubah Oleh", related_name="diubah_oleh_lelang_mancanegara")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_lelang_mancanegara")
    

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("portal_lelang_mancanegara_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("portal_lelang_mancanegara_update", args=(self.pk,))

class istilah_lelang(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    nama_istilah = models.TextField()
    penjelasan = RichTextField()
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name="Diubah Oleh", related_name="diubah_oleh_istilah_lelang")
    dibuat_oleh = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True, related_name="dibuat_oleh_istilah_lelang")
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("portal_istilah_lelang_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("portal_istilah_lelang_update", args=(self.pk,))
    
class profil(models.Model):

    # Fields
    latar_belakang = models.TextField(blank=True, null=True, verbose_name="Latar Belakang")
    visi = models.TextField(blank=True, null=True, verbose_name="Visi")
    misi = models.TextField(blank=True, null=True, verbose_name="Misi")
    status = models.BooleanField(default=True)
    sejarah_seleksi = models.TextField(blank=True, null=True, verbose_name="Sejarah Seleksi Pita Frekuensi Radio")
    tugas_dir = models.TextField(blank=True, null=True, verbose_name="Tugas Direktorat Penataan")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, verbose_name="Diubah Oleh", related_name="diubah_oleh_profil")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
