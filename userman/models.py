from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from encrypted_model_fields.fields import EncryptedCharField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import Group
from multiselectfield import MultiSelectField

class jabatan(models.TextChoices):
        Pengarah = "pengarah", "Pengarah"
        Pembina = "pembina", "Pembina"
        Ketua = "ketua", "Ketua"
        Sekretaris = "sekretaris", "Sekretaris"
        Anggota = "anggota", "Anggota"

class tipeuser(models.TextChoices):
        ADMIN = "A", "Admin"
        VIEWER = "V", "Viewer"
        BIDDER = "B", "Bidder"
        AUCTIONER = "C", "Auctioner"

class bidder(models.Model):
    class BidderType(models.TextChoices):
        JSB = "JSB", "Jaringan Bergerak Seluler"
        JKS = "JKS", "Jaringan Tetap Lokal Packet Switched"
    # Relationships
    verified_by = models.IntegerField(blank=True, null=True)

    # Fields
    alamat_perusahaan = models.TextField(max_length=2000, verbose_name='Alamat Perusahaan')
    jenis_penyelenggara = models.CharField(max_length=3, choices=BidderType.choices, default=BidderType.JSB, verbose_name='Jenis Pengelenggara')
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(blank=True, null=True)
    telp_perusahaan = EncryptedCharField(max_length=30, verbose_name='Telp Perusahaan')
    nama_perusahaan = models.CharField(max_length=30, verbose_name='Nama Perusahaan')
    verification_note = models.TextField(max_length=2000, blank=True)
    npwp_perusahaan = EncryptedCharField(max_length=30, verbose_name='NPWP Perusahaan')
    email_perusahaan = EncryptedCharField(max_length=30, verbose_name='Email Perusahaan')
    nib_perusahaan = EncryptedCharField(max_length=30, verbose_name='NIB Perusahaan')
    active = models.BooleanField()
    surat_kuasa = models.FileField(upload_to="uploads/bidder/",  verbose_name='File Surat Kuasa', null=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="bidder_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="bidder_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.nama_perusahaan)

class Users(AbstractUser):
    
    # Fields
    isactive = models.BooleanField(default=False)
    pending = models.BooleanField(default=False)
    email = EncryptedCharField(max_length=100, verbose_name='Email')
    username =  models.CharField(max_length=100, unique=True, verbose_name='Nama user')
    password = models.TextField(max_length=100, verbose_name='Password', blank=True)
    mobile_number = EncryptedCharField(max_length=100, verbose_name='No HP user')
    nama_lengkap = models.CharField(max_length=100, verbose_name='Nama lengkap')
    user_type=models.CharField(max_length=30, verbose_name='Jenis User', choices=tipeuser.choices)
    #jabatan_dalam_tim = models.CharField(max_length=30, verbose_name='Jabtan dalam Tim', choices=jabatan.choices,)
    # bidder = models.TextField(max_length=100, verbose_name='Nama lengkap')
    bidder = models.ForeignKey(bidder, on_delete = models.CASCADE, null=True)
    masaberlaku1 = models.DateField(blank=True, null=False)
    masaberlaku2 = models.DateField(blank=True, null=False)
    password_terlihat = models.TextField(max_length=100, verbose_name='password_terlihat', blank=True, null=True)
    first_login = models.BooleanField(default=False)
    customGroup = models.ManyToManyField('userman.CustomGroup', blank=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="userss_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="userss_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, null=True)
    session_data = models.JSONField(default=dict, blank=True)

    class Meta:
        pass

    def __str__(self):
        return "{} ({} / {})".format(self.nama_lengkap,self.username,self.email)

class tim_lelang(models.Model):

    # Fields
    sk_pengangkatan = models.FileField(upload_to="uploads/timlelang/",  verbose_name='File SK Pengangkatan')
    nip = models.CharField(max_length=30, verbose_name='NIP Anggota TIM')
    jabatan_dalam_tim = models.CharField(max_length=30, verbose_name='Jabtan dalam Tim', choices=jabatan.choices,)
    jabatan = models.CharField(max_length=255, verbose_name='Jabatan di UnOr yang menugaskan')
    users = models.OneToOneField(Users, on_delete = models.CASCADE, blank=True)
    active = models.BooleanField(default=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="tim_lelang_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="tim_lelang_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, null=True)
    class Meta:
        pass

    def __str__(self):
         return "{} ({})".format(self.users.nama_lengkap, self.users.username, )
        # return str(self.users.nama_lengkap)

class bidder_user(models.Model):

    # Fields
    users = models.OneToOneField(Users, on_delete = models.CASCADE, blank=True)
    bidder = models.ForeignKey('userman.bidder', on_delete = models.CASCADE, blank=True)
    active = models.BooleanField(default=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="bidder_user_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="bidder_user_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, null=True)
    class Meta:
        pass

    def __str__(self):
        return "{} ({})".format(self.bidder.nama_perusahaan, self.users.username)

class dokumen_perusahaan(models.Model):

    # Relationships
    verified_by = models.IntegerField(blank=True)
    id_perusahaan = models.ForeignKey("userman.bidder", on_delete=models.CASCADE)

    # Fields
    # dokumen = models.FileField(upload_to="upload/bidder/")
    dokumen = models.FileField(upload_to="upload/bidder/",  verbose_name='File Dokumen')
    nama_dokumen = models.CharField(max_length=30, verbose_name='Nama Dokumen Perusahaan')
    verification_note = models.TextField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    verified_at = models.DateTimeField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    verified = models.BooleanField(default=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="dokumen_perusahaan_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="dokumen_perusahaan_diubah_oleh")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
    
class admin(models.Model):

    # Fields
    sk_pengangkatan = models.FileField(upload_to="uploads/admin/",  verbose_name='File SK Pengangkatan')
    nip = models.CharField(max_length=30, verbose_name='NIP Anggota TIM')
    jabatan_dalam_tim = models.CharField(max_length=30, verbose_name='Jabtan dalam Tim', choices=jabatan.choices,)
    jabatan = models.CharField(max_length=255, verbose_name='Jabatan di UnOr yang menugaskan')
    users = models.OneToOneField(Users, on_delete = models.CASCADE, blank=True)
    active = models.BooleanField(default=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="admin_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="admin_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
    
class viewers(models.Model):

    # Fields
    sk_pengangkatan = models.FileField(upload_to="uploads/viewers/",  verbose_name='File SK Pengangkatan')
    nip = models.CharField(max_length=30, verbose_name='NIP Anggota TIM')
    jabatan_dalam_tim = models.CharField(max_length=30, verbose_name='Jabtan dalam Tim', choices=jabatan.choices,)
    jabatan = models.CharField(max_length=255, verbose_name='Jabatan di UnOr yang menugaskan')
    users = models.OneToOneField(Users, on_delete = models.CASCADE, blank=True)
    active = models.BooleanField(default=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="viewers_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="viewers_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, null=True)
    
    class Meta:
        pass

    def __str__(self):
        # return str(self.users.nama_lengkap)
        return "{} ({})".format(self.users.nama_lengkap, self.users.username, )

class bidder_list(models.Model):

    # Fields
    # sk_pengangkatan = models.FileField(upload_to="uploads/bidders/",  verbose_name='File SK Pengangkatan')
    nip = models.CharField(max_length=30, verbose_name='NIP Anggota TIM')
    jabatan_dalam_tim = models.CharField(max_length=30, verbose_name='Jabtan dalam Tim')
    jabatan = models.CharField(max_length=255, verbose_name='Jabatan di UnOr yang menugaskan')
    users = models.OneToOneField(Users, on_delete = models.CASCADE, blank=True)
    active = models.BooleanField(default=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="bidder_list_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="bidder_list_diubah_oleh")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class bidder_perwakilan(models.Model):

    # Fields
    bidder= models.ForeignKey("userman.bidder_user", on_delete=models.CASCADE, blank=True, null=True, related_name="bidder_perwakilan_bidder")
    nama_lengkap = models.CharField(max_length=100, verbose_name='Nama lengkap', unique=True, default="")
    nik_perwakilan = models.CharField(max_length=30, verbose_name='NIK')
    email = EncryptedCharField(max_length=100, verbose_name='Email', blank=True)
    mobile_number = EncryptedCharField(max_length=100, verbose_name='No HP user', blank=True)
    jabatan = models.CharField(max_length=255, verbose_name='Jabatan', blank=True)
    active = models.BooleanField(default=False, blank=True)
    
    ip_address = models.GenericIPAddressField(null=True)
    peruri_ttd = models.TextField(null=True, blank=True, verbose_name='ttd')
    
    sk_pengangkatan = models.FileField(upload_to="uploads/bidders/",  verbose_name='File SK Pengangkatan', blank=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="bidder_perwakilan_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="bidder_perwakilan_diubah_oleh")
    ttd = models.ImageField(upload_to="uploads/bidders/",  verbose_name='Tanda Tangan Digital', blank=True)
    profil_peruri = models.CharField(max_length=100, verbose_name='Profil Peruri', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, null=True)
    
    class Meta:
        # ordering = ['-id']
        pass

    def __str__(self):
        return "{} ({})".format(self.bidder.bidder.nama_perusahaan,self.nama_lengkap)

# baru  
MenuType= (("A", "Admin"),
    ("V", "Viewer"),
    ("B", "Bidder"),
    ("C", "Auctioner"))
class UserMenu(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='menu name')
    slug = models.SlugField(max_length=50, unique=True)
    additional_text = models.CharField(max_length=1000, null=True, blank=True)
    additional_text2 = models.CharField(max_length=1000, null=True, blank=True)
    additional_text3 = models.CharField(max_length=1000, null=True, blank=True)
    additional_text4 = models.CharField(max_length=1000, null=True, blank=True)
    icon_class =models.CharField(max_length=128, null=True, blank=True)
    style_class=models.CharField(max_length=128, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    link = models.CharField(max_length=128, null=True, blank=True, help_text='URL')
    menu_type = MultiSelectField(choices=MenuType, null=True, max_choices=4,max_length=4)
    enabled = models.BooleanField(default=True, blank=True, null=True)
    order = models.IntegerField( blank=True, null=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="UserMenu_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="UserMenu_diubah_oleh")
    tahapan = TreeForeignKey("adm_lelang.tahapan_lelang2", on_delete=models.DO_NOTHING, blank=True,null=True, related_name="UserMenu_tahapan")
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, null=True)
    class MPTTMeta:
        order_insertion_by = ['order']
    
    def __str__(self):
        return self.name

class UserMenuGroup(models.Model):
    menu = models.ForeignKey(UserMenu, on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey('userman.CustomGroup', on_delete=models.CASCADE, blank=True, null=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="UserMenuGroup_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="UserMenuGroup_diubah_oleh")

class menugroup_map(models.Model):
    menu = models.ForeignKey(UserMenu, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50, unique=True, verbose_name='menu name')
    menuid = models.IntegerField( blank=True, null=True)
    parent_id = models.IntegerField( blank=True, null=True)

    class Meta:
        managed = False

class CustomGroup(Group):
    keterangan = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False, null=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="CustomGroup_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="CustomGroup_diubah_oleh")


NotificationType= (
    ("U", "Undangan"),
    ("B", "BA"),
    ("O","Lain-lain")
)

class Notifikasi(models.Model):
    email = models.CharField(max_length=50, verbose_name='Email', default="")
    id_undangan = models.IntegerField(default=0)
    id_ba = models.IntegerField(default=0)
    subyek = models.CharField(max_length=255, verbose_name='Subyek', default="")
    notifikasi= models.CharField(max_length=1024, verbose_name='Notifikasi')
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    read = models.BooleanField(default=False)
    email_status = models.CharField(max_length=30, verbose_name='Status Email')
    expire_date = models.DateTimeField(null=True)
    notification_type = models.CharField(choices=NotificationType, null=True, max_length=1, default='U')
