from django.db import models
from django.urls import reverse
from adm_lelang.models import item_lelang, detail_itemlelang
from userman.models import bidder, tim_lelang, bidder_user, bidder_perwakilan
from datetime import date, datetime
from django.utils import timezone

class obyek_seleksi_sampul2(models.Model):
    bidder_user=models.ForeignKey('userman.bidder_user', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Bidder")
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Obyek Seleksi")
    block = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="sampul2_obyek_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="sampul2_obyek_diubah_oleh")
    def __str__(self):
        return "{}".format(self.item)

class penawaran(models.Model):

    # Fields
    dokumen_penawaran = models.FileField(upload_to="upload/files/")
    harga = models.FloatField()
    blok = models.IntegerField()
    bidder = models.ForeignKey("userman.bidder_user", on_delete=models.CASCADE, null=True)
    item = models.ForeignKey("adm_lelang.detail_itemlelang", on_delete=models.CASCADE, null=True)
    perwakilan = models.ForeignKey("userman.bidder_perwakilan", on_delete=models.CASCADE, null=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="sampul2_verified_by")
    verified_at = models.DateTimeField(auto_now_add=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="sampul2_penawaran_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="sampul2_penawaran_diubah_oleh")

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
    penawaran = models.ForeignKey("sampul2.penawaran", on_delete=models.CASCADE, blank=True, null=True)
    hasil = models.CharField(choices=SAMPUL2_CHOICES,max_length=110, null=True, blank=True )
    catatan = models.TextField()
    dokumen = models.FileField(upload_to="upload/files/", blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="sampul2_esampul_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="sampul2_esampul_diubah_oleh")
#     # Fields

    
class hasil_sampul2(models.Model):
    bidder = models.ForeignKey("userman.bidder_user", on_delete=models.CASCADE, null=True)
    item = models.ForeignKey("adm_lelang.detail_itemlelang", on_delete=models.CASCADE, null=True)
    harga = models.FloatField()
    ranking = models.IntegerField()
