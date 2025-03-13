from django.db import models
from django.urls import reverse
from userman.models import Users, bidder, bidder_user
from adm_lelang.models import item_lelang, detail_itemlelang
from django.contrib.postgres.fields import DecimalRangeField


class price_increase(models.Model):
    item=models.ForeignKey(item_lelang, on_delete=models.CASCADE, blank=True, null=True)
    detail_item=models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, blank=True, null=True)
    rentang_min = models.FloatField(verbose_name="Rentang Bawah", null=True)
    rentang_max = models.FloatField(verbose_name="Rentang Atas", null=True)
    kenaikan =  models.FloatField(verbose_name="Kenaikan (%)")
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="price_increase_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="price_increase_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Tanggal Dibuat")
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Tanggal Diubah")

class obyek_seleksi_smra(models.Model):
    bidder_user=models.ForeignKey('userman.bidder_user', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Bidder")
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Obyek Seleksi")
    ipaddress = models.CharField(max_length=25, blank=True, verbose_name="Alamat IP")
    blok_awal = models.IntegerField(blank=True, verbose_name="Blok Awal")
    is_block_ip = models.BooleanField(default=False, verbose_name="IP Diblok?")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="smra_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="smra_diubah_oleh")
    def __str__(self):
        return "{}".format(self.item)        

class bid_bidder_smra(models.Model):
    id = models.BigIntegerField(primary_key=True)
    penawaran = models.FloatField()
    round= models.IntegerField()
    available_block= models.IntegerField()
    band= models.TextField()
    spectrum_cap= models.IntegerField()
    eligibility_point_per_block= models.IntegerField()
    block= models.IntegerField()
    prev_block= models.IntegerField()
    bidder_id= models.IntegerField()
    object_id= models.IntegerField()
    item_id= models.IntegerField()
    reserved_price = models.FloatField()
    prev_price = models.FloatField()
    min_price= models.FloatField()
    class Meta:
        managed=False
    def __str__(self):
        return "{}".format(self.pk)

class sum_round_smra2(models.Model):
    class STATUS(models.TextChoices):
        START = "STA", "START"
        STOP = "STO", "STOP"
        SUSPEND = "SUS", "SUSPEND"
        CLOSED = "CLO", "CLOSED"
        FINAL = "FIN", "FINAL"
        INIT = "INI","INIT"
        NONE = "NON","NONE"
        WAIT = "WAI","WAIT"
        NOSCHEDULE = "NSC","NOSCHEDULE"

    id = models.BigIntegerField(primary_key=True)
    round= models.IntegerField()
    item=models.ForeignKey(detail_itemlelang, on_delete=models.SET_NULL, blank=True, null=True)
    status_round = models.CharField(max_length=3, choices=STATUS.choices)
    item_lelang= models.IntegerField()
    count= models.IntegerField()
    mulai1= models.CharField(max_length=25)
    selesai1= models.CharField(max_length=25)
    min_price = models.FloatField()
    prev_price = models.FloatField()
    khusus = models.BooleanField(default=False)
    class Meta:
        managed=False
    def __str__(self):
        return "{}".format(self.pk)

class round_smra2(models.Model):
    class STATUS(models.TextChoices):
        START = "STA", "START"
        STOP = "STO", "STOP"
        SUSPEND = "SUS", "SUSPEND"
        CLOSED = "CLO", "CLOSED"
        FINAL = "FIN", "FINAL"
        INIT = "INI","INIT"
        NONE = "NON","NONE"
        WAIT = "WAI","WAIT"
        NOSCHEDULE = "NSC","NOSCHEDULE"

    round = models.IntegerField()
    price = models.FloatField()
    block = models.IntegerField()
    bidder = models.ForeignKey('userman.bidder_user', on_delete=models.CASCADE, blank=True, null=True)
    perwakilan = models.ForeignKey('userman.bidder_perwakilan', on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE)
    otp = models.BooleanField(default=False)
    prev_price = models.FloatField(null=True)
    prev_block = models.IntegerField(null=True)
    item_lelang = models.IntegerField(null=True)
    min_price = models.FloatField(null=True)
    status_round = models.CharField(max_length=3, choices=STATUS.choices, default=STATUS.NONE)
    mulai = models.DateTimeField(editable=True)
    selesai = models.DateTimeField(editable=True)
    lock= models.BooleanField(default=False)
    vi= models.BooleanField(default=True)
    khusus = models.BooleanField(default=False)
    penawaran = models.FloatField(null=True)
    ext_data = models.JSONField(blank=True, null=True)
    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.round)
    
DAY_OF_THE_WEEK = {
    '0' : 'Senin',
    '1' : 'Selasa',
    '2' : 'Rabu',
    '3' : 'Kamis',
    '4' : 'Jumat',
    '5' : 'Sabtu', 
    '6' : 'Minggu',
}

class DayOfTheWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices']=tuple(sorted(DAY_OF_THE_WEEK.items()))
        kwargs['max_length']=1 
        super(DayOfTheWeekField,self).__init__(*args, **kwargs)

class round_schedule_smra2(models.Model):
    mulai = models.TimeField(editable=True)
    selesai = models.TimeField(editable=True)
    hari = DayOfTheWeekField(null=True)
    item = models.ForeignKey(item_lelang, models.DO_NOTHING)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="round_schedule2_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="round_schedule2_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Diubah Terakhir")
    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.pk)

class hasil_smra2(models.Model):
    class JENIS_PUTARAN(models.TextChoices):
        NORMAL = "NORMAL", "NORMAL"
        KHUSUS = "KHUSUS", "KHUSUS"
    round = models.IntegerField()
    mulai = models.DateTimeField(editable=True, null=True)
    selesai = models.DateTimeField(editable=True, null=True)
    price = models.FloatField()
    block = models.IntegerField()
    bidder = models.ForeignKey('userman.bidder_user', on_delete=models.CASCADE, blank=True, null=True)
    perwakilan = models.ForeignKey('userman.bidder_perwakilan', on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE)
    item_lelang = models.IntegerField(null=True)
    submit = models.DateTimeField(auto_now=False, editable=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=True, editable=False)
    penawaran = models.FloatField(null=True)
    valid = models.BooleanField(default=False)
    berita_acara = models.FileField(upload_to="upload/bidder")
    berita_acara_unsigned = models.FileField(blank=True,upload_to="upload/bidder")
    jenis = models.CharField(max_length=6, choices=JENIS_PUTARAN.choices, default=JENIS_PUTARAN.NORMAL)
    berlaku= models.BooleanField(default=False, blank=True, null=True)
    fin = models.BooleanField(default=False)
    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.round)

class hasil2_smra(models.Model):
    class JENIS_PUTARAN(models.TextChoices):
        NORMAL = "NORMAL", "NORMAL"
        KHUSUS = "KHUSUS", "KHUSUS"
    round = models.IntegerField()
    price = models.FloatField()
    mulai = models.DateTimeField(editable=True, null=True)
    selesai = models.DateTimeField(editable=True, null=True)
    ranking = models.IntegerField(null=True, blank=True)
    ranking_putaran = models.IntegerField(null=True, blank=True)
    bidder = models.ForeignKey('userman.bidder_user', on_delete=models.CASCADE, blank=True, null=True)
    perwakilan = models.ForeignKey('userman.bidder_perwakilan', on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE)
    item_lelang = models.IntegerField(null=True)
    submit = models.DateTimeField(null=True)
    last_updated = models.DateTimeField(auto_now_add=True, editable=False)
    penawaran = models.FloatField(null=True)
    valid = models.BooleanField(default=False)
    jenis = models.CharField(max_length=6, choices=JENIS_PUTARAN.choices, default=JENIS_PUTARAN.NORMAL)
    berlaku= models.BooleanField(default=False, blank=True, null=True)
    
    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.round)


class auctioner_hasil(models.Model):
    id = models.BigIntegerField(primary_key=True)
    round= models.IntegerField(verbose_name="Putaran")
    item_lelang= models.ForeignKey(item_lelang, on_delete=models.CASCADE, blank=True, null=True)
    item=models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, blank=True, null=True)
    block = models.IntegerField()
    # peserta = models.IntegerField() #sementara saya komen dulu ngikutin dari kominfo2 yg gaada kolom pesertanya
    harga= models.FloatField()

    class Meta:
        managed= False

    def __str__(self):
        return "{}".format(self.pk)
    def delete(self, using=None, keep_parents=False):
        #super().delete(using=using, keep_parents=keep_parents)
        None

class hasil_auctioner_maxmin(models.Model):
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

class hasil_highest(models.Model):
    id = models.BigIntegerField(primary_key=True)
    #bidder = models.ForeignKey('userman.bidder_user', on_delete=models.CASCADE, blank=True, null=True,verbose_name="Peserta") #error
    bidder = models.ForeignKey('userman.bidder_user', on_delete=models.DO_NOTHING, blank=True, null=True,verbose_name="Peserta")
    item_lelang=models.IntegerField(null=True)
    item=models.ForeignKey(detail_itemlelang, on_delete=models.CASCADE, blank=True, null=True)
    price= models.FloatField(verbose_name="Harga",null=True)
    round = models.FloatField(verbose_name="Putaran",null=True)
    block =  models.FloatField(verbose_name="Jumlah Blok",null=True)
    submit = models.DateTimeField(editable=True)

    class Meta:
        managed=False

    def __str__(self):
        return "{}".format(self.pk)