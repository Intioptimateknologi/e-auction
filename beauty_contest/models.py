from django.db import models
from django.urls import reverse
from adm_lelang.models import item_lelang, detail_itemlelang
from userman.models import bidder, tim_lelang


class parameter_evaluasi(models.Model):

    # Fields
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, null=True)
    parameter = models.CharField(max_length=100, null=True)
    bobot = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="param_eval_bc_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="param_eval_bc_diubah_oleh")

    class Meta:
        pass

    def __str__(self):
        return str(self.parameter)

    def get_absolute_url(self):
        return reverse("beauty_contest_parameter_evaluasi_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("beauty_contest_parameter_evaluasi_update", args=(self.pk,))


class format_dokumen_bc(models.Model):
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    fotmat_doc = models.FileField(upload_to="upload/files/")
    format_xls = models.FileField(upload_to="upload/files/")
    judul = models.TextField()
    nomor = models.CharField(max_length=100, null=True, blank=True)
    tgl_penetapan = models.DateTimeField(editable=True)
    keterangan = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="format_bc_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="format_bc_diubah_oleh")

class obyek_seleksi_bc(models.Model):
    bidder_user=models.ForeignKey('userman.bidder_user', on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="Bidder")
    item = models.ForeignKey(detail_itemlelang, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="Obyek Seleksi")
    block = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="bc_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="bc_diubah_oleh")
    def __str__(self):
        return "{}".format(self.item)

class dokumen_bc(models.Model):

    # Fields
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dokumen_bc = models.FileField(upload_to="upload/files/")
    bidder = models.ForeignKey('userman.bidder_user', on_delete=models.CASCADE, null=True)
    perwakilan = models.ForeignKey('userman.bidder_perwakilan', models.DO_NOTHING, blank=True, null=True)
    nama_dok = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="dokumen_bc_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="dokumen_bc_diubah_oleh")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("beauty_contest_dokumen_bc_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("beauty_contest_dokumen_bc_update", args=(self.pk,))

    
class penilaian_bc(models.Model):

    # Fields
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, null=True)
    bidder  = models.ForeignKey('userman.bidder_user', on_delete=models.CASCADE, null=True)
    parameter  = models.ForeignKey("beauty_contest.parameter_evaluasi", on_delete=models.CASCADE, null=True)
    penilaian = models.FloatField(null=True, blank=True)
    bobot = models.IntegerField(null=True, blank=True)
    hasil_evaluasi = models.BooleanField(default=True,null=True, blank=True)
    keterangan = models.TextField(max_length=2000, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="penilaian_bc_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="penilaian_bc_diubah_oleh")

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class hasil_beauty_contest(models.Model):
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, null=True)
    bidder  = models.ForeignKey('userman.bidder_user', on_delete=models.CASCADE, null=True)
    parameter  = models.ForeignKey("beauty_contest.parameter_evaluasi", on_delete=models.CASCADE, null=True)
    penilaian = models.FloatField(null=True, blank=True)
    ranking = models.IntegerField(null=True, blank=True)

class sum_penilaian(models.Model):
    id = models.BigIntegerField(primary_key=True)
    bidder = models.ForeignKey('userman.bidder_user', on_delete=models.CASCADE, blank=True, null=True)
    sum= models.FloatField()
    item =models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed= False

    def __str__(self):
        return "{}".format(self.pk)