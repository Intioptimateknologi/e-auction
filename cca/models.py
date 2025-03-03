from django.db import models
from django.urls import reverse
from userman.models import Users, bidder, bidder_user
from adm_lelang.models import item_lelang, detail_itemlelang

class obyek_seleksi_cca(models.Model):
    bidder_user=models.ForeignKey('userman.bidder_user', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Bidder")
    item = models.ForeignKey(item_lelang, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Obyek Seleksi")
    ipaddress = models.CharField(max_length=25, blank=True, verbose_name="Alamat IP")
    eli_awal = models.IntegerField(blank=True, verbose_name="Eligibility Awal")
    is_block_ip = models.BooleanField(default=False, verbose_name="IP Diblok?")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="cca_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="cca_diubah_oleh")
    def __str__(self):
        return "{}".format(self.item)

class round_cca2(models.Model):
    round = models.IntegerField()
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, blank=True, null=True,related_name="round_cca_dibuat_oleh")
    item = models.ForeignKey(item_lelang, on_delete=models.CASCADE, blank=True, null=True,related_name="round_cca_dibuat_oleh")
    price = models.JSONField(null=True)
    prev_price = models.JSONField(null=True)
    activity = models.IntegerField(null=True)
    corrected = models.BooleanField(default=False)
    
    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.round)

class cca_price_increase(models.Model):
    item=models.ForeignKey(item_lelang, on_delete=models.CASCADE, blank=True, null=True)
    detail_item=models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, blank=True, null=True)
    rentang_min = models.IntegerField(verbose_name="Rentang Bawah", null=True)
    rentang_max = models.IntegerField(verbose_name="Rentang Atas", null=True)
    kenaikan =  models.FloatField(verbose_name="Kenaikan (%)")
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="cca_price_increase_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="cca_price_increase_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Dibuat Pertama")
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Diubah Terakhir")

class hasil_cca(models.Model):
    class JENIS_PUTARAN(models.TextChoices):
        CLOCK = "CLOCK", "CLOCK"
        SUPLEMENTAL = "SUPLE", "SUPLEMENTAL"
        ASSIGNMENT = "ASSI", "ASSIGNMENT"
    round = models.IntegerField()
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, blank=True, null=True)
    item_lelang = models.IntegerField(null=True)
    submit = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    valid = models.BooleanField(default=False)
    berita_acara = models.FileField(upload_to="upload/bidder")
    jenis = models.CharField(max_length=5, choices=JENIS_PUTARAN.choices, default=JENIS_PUTARAN.CLOCK)
    perwakilan = models.ForeignKey('userman.bidder_perwakilan', on_delete=models.CASCADE, blank=True, null=True)
    berita_acara = models.FileField(upload_to="upload/bidder")
    berita_acara_unsigned = models.FileField(blank=True,upload_to="upload/bidder")
    activity = models.IntegerField(default=0)
    eli = models.IntegerField(default=0)
    revelaled = models.BooleanField(default=False)
    mulai = models.DateTimeField(null=True,editable=True)
    selesai = models.DateTimeField(null=True,editable=True)
    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.round)

class hasil_detail_cca(models.Model):
    parent = models.ForeignKey(hasil_cca, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, blank=True, null=True)
    price = models.FloatField()
    block = models.IntegerField()
    submit = models.DateTimeField(editable=False, null=True)

    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.pk)

class hasil2_detail_cca(models.Model):
    parent = models.ForeignKey(hasil_cca, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, blank=True, null=True)
    price = models.FloatField()
    ranking = models.IntegerField(null=True, blank=True)
    ranking_putaran = models.IntegerField(null=True, blank=True)
    berlaku = models.BooleanField(default=False, null=True)
    submit = models.DateTimeField(editable=False, null=True)

    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.pk)


class auctioner_hasil_cca(models.Model):
    id = models.BigIntegerField(primary_key=True)
    round= models.IntegerField(verbose_name="Putaran")
    item_lelang= models.ForeignKey(item_lelang, on_delete=models.CASCADE, blank=True, null=True)
    item=models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, blank=True, null=True)
    block = models.IntegerField()
    harga= models.FloatField()

    class Meta:
        managed= False

    def __str__(self):
        return "{}".format(self.pk)

class hasil_auctioner_maxmin_cca(models.Model):
    id = models.BigIntegerField(primary_key=True)
    round= models.IntegerField(verbose_name="Putaran")
    item_lelang= models.IntegerField()
    item=models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, blank=True, null=True)
    block = models.IntegerField()
    harga_max= models.FloatField()
    harga_min= models.FloatField()
    block_max= models.FloatField()
    block_min= models.FloatField()
    max_block = models.IntegerField()
    harga_minimal = models.FloatField()
    spectrum_cap = models.IntegerField()
    persen1 = models.FloatField()

    class Meta:
        managed= False

    def __str__(self):
        return "{}".format(self.pk)


class round_cca(models.Model):
    class STATUS(models.TextChoices):
        START = "STA", "START"
        STOP = "STO", "STOP"
        SUSPEND = "SUS", "SUSPEND"
        CLOSED = "CLO", "CLOSED"
        FINAL = "FIN", "FINAL"
        INIT = "INI","INIT"
        NONE = "NON","NONE"
        WAIT = "WAI","WAIT"
    class JENIS_PUTARAN(models.TextChoices):
        CLOCK = "CLOCK", "CLOCK"
        SUPLEMENTAL = "SUPLE", "SUPLEMENTAL"
        ASSIGNMENT = "ASSI", "ASSIGNMENT"

    round = models.IntegerField()
    bidder = models.ForeignKey(bidder_user, on_delete=models.CASCADE, blank=True, null=True)
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True,verbose_name="Judul Seleksi")
    eli_point = models.IntegerField(verbose_name="Eligibility",null=True)
    activity = models.IntegerField(verbose_name="Aktivitas",null=True)

    status_round = models.CharField(max_length=3, choices=STATUS.choices, default=STATUS.NONE)
    mulai = models.DateTimeField(null=True,editable=True)
    selesai = models.DateTimeField(null=True,editable=True)
    lock= models.BooleanField(default=False)
    status_sah = models.BooleanField(default=False)
    jenis = models.CharField(max_length=5, choices=JENIS_PUTARAN.choices, default=JENIS_PUTARAN.CLOCK)

    
    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.round)

class sum_round_cca(models.Model):
    class STATUS(models.TextChoices):
        START = "STA", "START"
        STOP = "STO", "STOP"
        SUSPEND = "SUS", "SUSPEND"
        CLOSED = "CLO", "CLOSED"
        FINAL = "FIN", "FINAL"
        INIT = "INI","INIT"
        NONE = "NON","NONE"
        WAIT = "WAI","WAIT"
    id = models.BigIntegerField(primary_key=True)
    round= models.IntegerField()
    item_lelang=models.ForeignKey(item_lelang, on_delete=models.CASCADE, blank=True, null=True)
    status_round = models.CharField(max_length=3, choices=STATUS.choices)
    count= models.IntegerField()
    mulai= models.CharField(max_length=25)
    selesai= models.CharField(max_length=25)
    class Meta:
        managed=False
    def __str__(self):
        return "{}".format(self.pk)



class round_detail_cca(models.Model):
    parent = models.ForeignKey(round_cca, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, blank=True, null=True)
    price = models.FloatField()
    block = models.IntegerField()
    prev_price = models.FloatField()
    prev_block = models.IntegerField()
    eli_per_block = models.IntegerField()
    spectrum_cap = models.IntegerField(null=True)
    max_blok = models.IntegerField(null=True)
    harga_minimal = models.FloatField(null=True)
    valid = models.BooleanField(default=False)

    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.pk)


class matrix_hasil_cr(models.Model):
    id = models.BigIntegerField(primary_key=True)
    parent=models.ForeignKey(hasil_cca, on_delete=models.CASCADE, blank=True, null=True)
    json_agg = models.JSONField()
    kombinasi= models.JSONField()
    total = models.FloatField()
    class Meta:
        managed=False
    def __str__(self):
        return "{}".format(self.parent)

class matrix2_cr(models.Model):
    id = models.BigIntegerField(primary_key=True)
    parent=models.ForeignKey(hasil_cca, on_delete=models.CASCADE, blank=True, null=True)
    json_agg = models.JSONField()
    kombinasi= models.JSONField()
    total = models.FloatField()
    class Meta:
        managed=False
    def __str__(self):
        return "{}".format(self.parent)