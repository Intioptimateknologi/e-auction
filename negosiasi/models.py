from django.db import models
from django.urls import reverse
from adm_lelang.models import item_lelang, detail_itemlelang
from userman.models import bidder, tim_lelang, bidder_user, bidder_perwakilan
from datetime import date, datetime
from django.utils import timezone

class obyek_seleksi_nego(models.Model):
    bidder_user=models.ForeignKey('userman.bidder_user', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Bidder")
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Obyek Seleksi")
    block = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="nego_obyek_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="nego_obyek_diubah_oleh")
    def __str__(self):
        return "{}".format(self.item)

class penawaran(models.Model):

    # Fields
    dokumen_penawaran = models.FileField(upload_to="upload/files/")
    harga = models.FloatField()
    blok = models.IntegerField()
    bidder = models.ForeignKey(
        "userman.bidder_user",
        on_delete=models.CASCADE,
        null=True,
        related_name="nego_penawaran_bidder"
    )
    item = models.ForeignKey(
        "adm_lelang.detail_itemlelang",
        on_delete=models.CASCADE,
        null=True,
        related_name="nego_penawaran_item"
    )
    perwakilan = models.ForeignKey(
        "userman.bidder_perwakilan",
        on_delete=models.CASCADE,
        null=True,
        related_name="nego_penawaran_perwakilan"
    )

    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="nego_verified_by")
    verified_at = models.DateTimeField(auto_now_add=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="nego_penawaran_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="nego_penawaran_diubah_oleh")

    class Meta:
        pass

    def __str__(self):
        return str("{},{}".format(self.bidder,self.item))

class revisi_penawaran(models.Model):

    # Fields
    bidder = models.ForeignKey(
        "userman.bidder_user",
        on_delete=models.CASCADE,
        null=True,
        related_name="nego_revisi_bidder"
    )
    item = models.ForeignKey(
        "adm_lelang.detail_itemlelang",
        on_delete=models.CASCADE,
        null=True,
        related_name="nego_revisi_item"
    )
    perwakilan = models.ForeignKey(
        "userman.bidder_perwakilan",
        on_delete=models.CASCADE,
        null=True,
        related_name="nego_revisi_perwakilan"
    )

    dokumen_penawaran = models.FileField(upload_to="upload/files/")
    harga = models.FloatField()
    blok = models.IntegerField()
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="nego_rev_verified_by")
    verified_at = models.DateTimeField(auto_now_add=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    keterangan = models.TextField(blank=True, null=True)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="nego_rpenawaran_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="nego_rpenawaran_diubah_oleh")

    class Meta:
        pass

    def __str__(self):
        return str("{},{}".format(self.bidder,self.item))

class evaluasi_penawaran(models.Model):
    SAMPUL2_CHOICES =(
        ("Diterima", "Diterima"),
        ("Tidak Diterima", "Tidak Diterima"),
    )
     # foreign key
    penawaran = models.ForeignKey("negosiasi.penawaran", on_delete=models.CASCADE, blank=True, null=True)
    hasil = models.CharField(choices=SAMPUL2_CHOICES,max_length=110, null=True, blank=True )
    catatan = models.TextField()
    dokumen = models.FileField(upload_to="upload/files/", blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="nego_esampul_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="nego_esampul_diubah_oleh")
#     # Fields

class evaluasi_revisi_penawaran(models.Model):
    SAMPUL2_CHOICES =(
        ("Diterima", "Diterima"),
        ("Tidak Diterima", "Tidak Diterima"),
    )
    # foreign key
    revisi_penawaran = models.ForeignKey("negosiasi.revisi_penawaran", on_delete=models.CASCADE, null=True)
    hasil = models.CharField(choices=SAMPUL2_CHOICES,max_length=110, null=True, blank=True )
    catatan = models.TextField()
    dokumen = models.FileField(upload_to="upload/files/", blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="nego_rsampul_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="nego_rsampul_diubah_oleh")
#     # Fields

    
class hasil_negosiasi(models.Model):
    bidder = models.ForeignKey("userman.bidder_user", on_delete=models.CASCADE, null=True)
    item = models.ForeignKey("adm_lelang.detail_itemlelang", on_delete=models.CASCADE, null=True)
    harga = models.FloatField()
    ranking = models.IntegerField()
