from django.db import models
from django.urls import reverse
from adm_lelang.models import item_lelang,detail_itemlelang
from userman.models import bidder, tim_lelang
from beauty_contest.models import obyek_seleksi_bc
from smra2.models import obyek_seleksi_smra

PARAM_GABUNGAN_CHOICES = [
    ("1", "SMRA"),
    ("2", "CCA"),
    ("3", "Beauty Contest"),
]
class penentuan_parameter(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    obyek_bc = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, null=True,related_name="gabungan_obyekbc")
    obyek_smra = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, null=True,related_name="gabungan_obyeksmra")
    bobot = models.FloatField()
    bobot2 = models.FloatField(blank=True)
    item = models.ForeignKey("adm_lelang.item_lelang", on_delete=models.CASCADE, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.p_parameter)

class ba_gabungan(models.Model):

    # Fields
    item_lelang = models.ForeignKey("adm_lelang.item_lelang", on_delete=models.CASCADE, null=True)
    dokumen_ba = models.FileField(upload_to="upload/files/")
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gabungan_ba_gabungan_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gabungan_ba_gabungan_update", args=(self.pk,))


class penilaian_gabungan(models.Model):

    # Fields
    item = models.ForeignKey("adm_lelang.detail_itemlelang", on_delete=models.CASCADE, null=True)
    bidder  = models.ForeignKey("userman.bidder_user", on_delete=models.CASCADE, null=True)
    parameter  = models.CharField(
        max_length=1,
        choices=PARAM_GABUNGAN_CHOICES,
        default="1",
    )
    penilaian = models.FloatField(null=True, blank=True)
    bobot = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class hasil_gabungan(models.Model):

    # Fields
    item = models.ForeignKey("adm_lelang.detail_itemlelang", on_delete=models.CASCADE, null=True)
    bidder  = models.ForeignKey("userman.bidder_user", on_delete=models.CASCADE, null=True)
    total = models.FloatField(null=True, blank=True)
    ranking = models.IntegerField(null=True, blank=True)
    harga = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class hasil2_gabungan(models.Model):

    # Fields
    item = models.ForeignKey("adm_lelang.detail_itemlelang", on_delete=models.CASCADE, null=True)
    bidder  = models.ForeignKey("userman.bidder_user", on_delete=models.CASCADE, null=True)
    total = models.FloatField(null=True, blank=True)
    harga = models.FloatField(null=True, blank=True)
    ranking = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
#class sum_gabungan(models.Model):
#    id = models.BigIntegerField(primary_key=True)
#    bidder = models.ForeignKey(bidder, models.DO_NOTHING, blank=True, null=True)
#    sum= models.FloatField(verbose_name="Nilai Akhir")
#    item =models.ForeignKey(detail_itemlelang, models.DO_NOTHING, blank=True, null=True)

#    class Meta:
#        managed: False

#    def __str__(self):
#        return "{}".format(self.pk)