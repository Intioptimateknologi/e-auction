from django.db import models
from django.urls import reverse
from userman.models import Users, bidder, tim_lelang
from adm_lelang.models import item_lelang, detail_itemlelang

"""class bid_bidder_smra(models.Model):
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

class auction_summary_smra(models.Model):
    id = models.BigIntegerField(primary_key=True)
    max_block= models.IntegerField()
    band= models.TextField()
    item_id=models.IntegerField()
    spectrum_cap= models.IntegerField()
    eligibility_point_per_block= models.IntegerField()
    reserved_price= models.FloatField()
    count= models.IntegerField()
    class Meta:
        managed=False
    def __str__(self):
        return "{}".format(self.pk)"""


class round_cca2(models.Model):
    class STATUS(models.TextChoices):
        START = "STA", "START"
        STOP = "STO", "STOP"
        SUSPEND = "SUS", "SUSPEND"
        CLOSED = "CLO", "CLOSED"
        INIT = "INI","INIT"
        NONE = "NON","NONE"
        WAIT = "WAI","WAIT"

    class JENIS(models.TextChoices):
        CLOCK = "CLK", "CLOCK"
        SUPL = "SUP", "SUPPLEMENTAL"
        WIN = "WIN", "WINNIND"

    round = models.IntegerField()
    price = models.FloatField()
    block = models.IntegerField()
    bidder = models.ForeignKey(bidder, models.DO_NOTHING, blank=True, null=True)
    item = models.ForeignKey(detail_itemlelang, models.DO_NOTHING)
    item_lelang = models.IntegerField(null=True)
    prev_price = models.FloatField(null=True)
    prev_block = models.IntegerField(null=True)
    min_price = models.FloatField(null=True)

    status_round = models.CharField(max_length=3, choices=STATUS.choices, default=STATUS.NONE)
    mulai = models.DateTimeField(editable=True)
    selesai = models.DateTimeField(editable=True)
    lock= models.BooleanField(default=False)
    jenis = models.CharField(max_length=3, choices=JENIS.choices, default=JENIS.CLOCK)
    penawaran = models.FloatField(null=True)
    
    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.round)

class round_cca2_sum(models.Model):
    round = models.IntegerField()
    bidder = models.ForeignKey(bidder, models.DO_NOTHING, blank=True, null=True)
    item = models.ForeignKey(item_lelang, models.DO_NOTHING, blank=True, null=True)
    price = models.JSONField(null=True)
    prev_price = models.JSONField(null=True)
    activity = models.IntegerField(null=True)
    corrected = models.BooleanField(default=False)
    
    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.round)

class hasil_cca2(models.Model):
    round = models.IntegerField()
    price = models.FloatField()
    block = models.IntegerField()
    bidder = models.ForeignKey(bidder, models.DO_NOTHING, blank=True, null=True)
    item = models.ForeignKey(detail_itemlelang, models.DO_NOTHING)
    item_lelang = models.IntegerField(null=True)
    submit = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    penawaran = models.FloatField(null=True)
    valid = models.BooleanField(default=False)

    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.round)
    #@property
    #def detail(self):
    #    return self.item.band


class bidding_round_smra(models.Model):
    class STATUS(models.TextChoices):
        START = "STA", "START"
        STOP = "STO", "STOP"
        SUSPEND = "SUS", "SUSPEND"
        CLOSED = "CLO", "CLOSED"
        INIT = "INI","INIT"
        NONE = "NON","NONE"
        WAIT = "WAI","WAIT"

    last_updated = models.DateTimeField(auto_now=True, editable=False, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    round_state = models.IntegerField()
    item = models.OneToOneField(item_lelang, models.DO_NOTHING, primary_key=True)
    start_time = models.DateTimeField(null=True)
    stop_time = models.DateTimeField(null=True)
    status_round = models.CharField(max_length=3, choices=STATUS.choices, default=STATUS.NONE)

    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.round_state)


DAY_OF_THE_WEEK = {
    '1' : 'Senin',
    '2' : 'Selasa',
    '3' : 'Rabu',
    '4' : 'Kamis',
    '5' : 'Jumat',
    '6' : 'Sabtu', 
    '7' : 'Minggu',
}

class DayOfTheWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices']=tuple(sorted(DAY_OF_THE_WEEK.items()))
        kwargs['max_length']=1 
        super(DayOfTheWeekField,self).__init__(*args, **kwargs)


class round_schedule_smra(models.Model):
    mulai = models.TimeField(editable=True)
    selesai = models.TimeField(editable=True)
    hari = DayOfTheWeekField(null=True)
    item = models.ForeignKey(item_lelang, models.DO_NOTHING)
    dibuat_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="round_schedule_dibuat_oleh")
    diubah_oleh = models.ForeignKey("userman.Users", on_delete=models.CASCADE, null=True, related_name="round_schedule_diubah_oleh")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False, verbose_name="Diubah Terakhir")
    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.pk)

class round_smra(models.Model):
    round = models.IntegerField()
    price = models.FloatField()
    block = models.IntegerField()
    bidder = models.ForeignKey(bidder, models.DO_NOTHING, blank=True, null=True)
    item = models.ForeignKey(detail_itemlelang, models.DO_NOTHING, blank=True, null=True)
    prev_price = models.FloatField(null=True)
    prev_block = models.IntegerField(null=True)
    min_price = models.FloatField(null=True)

    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.round)

class round_smra_temp(models.Model):
    round = models.IntegerField()
    price = models.FloatField()
    block = models.IntegerField()
    bidder = models.ForeignKey(bidder, models.DO_NOTHING, blank=True, null=True)
    item = models.ForeignKey(detail_itemlelang, models.DO_NOTHING, blank=True, null=True)
    prev_price = models.FloatField(null=True)
    prev_block = models.IntegerField(null=True)
    min_price = models.FloatField(null=True)

    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.round)

class round_smra_sum(models.Model):
    round = models.IntegerField()
    bidder = models.ForeignKey(bidder, models.DO_NOTHING, blank=True, null=True)
    item = models.ForeignKey(item_lelang, models.DO_NOTHING, blank=True, null=True)
    price = models.FloatField(null=True)
    activity = models.IntegerField(null=True)
    corrected = models.BooleanField(default=False)

    class Meta:
        pass
    def __str__(self):
        return "{}".format(self.round)

class eli_round(models.Model):
    id = models.BigIntegerField(primary_key=True)
    round= models.IntegerField()
    item_id=models.IntegerField()
    bidder_id=models.IntegerField()
    pbpp = models.FloatField(null=True)
    cbpp = models.FloatField(null=True)
    pbcp = models.FloatField(null=True)
    cbcp = models.FloatField(null=True)
    class Meta:
        managed=False
    def __str__(self):
        return "{}".format(self.pk)
    
class undangan_smra_cca(models.Model):
    OWNER_CHOICES = (
        ("SMRA", "SMRA"),
        ("CCA", "CCA"),
        ("BC", "Beauty Contest"),
        ("PBC", "Penilaian Beauty Contest"),
        ("GABUNGAN", "Gabungan"),
        ("UNKNOWN", "Unknown"),
    )

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    #bidder = models.ForeignKey(bidder, on_delete=models.CASCADE, null=True)
    bidder = models.ManyToManyField('userman.bidder')
    auctioneer = models.ManyToManyField('userman.tim_lelang')
    #auctioneer = models.ForeignKey(tim_lelang, on_delete=models.CASCADE, blank=True, null=True)

    # Fields
    nomor = models.CharField()
    judul = models.CharField(max_length=100)
    tanggal = models.DateTimeField()
    tempat = models.CharField(max_length=100)
    agenda = models.TextField()
    link_teleconference = models.TextField(verbose_name="Link Teleconference")
    keterangan = models.TextField()
    link_file = models.FileField(upload_to="upload/files/pasca_seleksi/sanggahan_jawaban/", verbose_name="Link Undangan")
    owner = models.TextField(max_length=100, null=True, blank=True, choices=OWNER_CHOICES, default="UNKNOWN")


    # default
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
    
# berita acara
class berita_acara_lelang(models.Model):
    OWNER_CHOICES = (
        ("SMRA", "SMRA"),
        ("CCA", "CCA"),
        ("BC", "Beauty Contest"),
        ("PBC", "Penilaian Beauty Contest"),
        ("GABUNGAN", "Gabungan"),
        ("UNKNOWN", "Unknown"),
    )

    # foreign key
    item_lelang = models.ForeignKey(item_lelang, on_delete=models.CASCADE, null=True)
    bidder = models.ForeignKey(bidder, on_delete=models.CASCADE, null=True)
    auctioneer = models.ForeignKey(tim_lelang, on_delete=models.CASCADE, blank=True, null=True)

    # Fields
    nomor = models.CharField(null=True, blank=True)
    judul = models.CharField( null=True, blank=True)
    tanggal = models.DateTimeField( null=True, blank=True)
    keterangan = models.TextField( null=True, blank=True)
    file = models.FileField(upload_to="upload/files/")
    owner = models.TextField(max_length=100, null=True, blank=True, choices=OWNER_CHOICES, default="UNKNOWN")
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)