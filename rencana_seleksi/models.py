from django.db import models

# Create your models here.
class tahun_integrasi_users(models.Model):

    id_user = models.IntegerField(null = True)
    id_tahun_judul = models.IntegerField(null = True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

class jadwal_seleksinya(models.Model):
    STATUS_CHOICES =(
        ('Selesai', 'Selesai'),
        ('Dimulai', 'Dimulai'),
    )
    nama_seleksi = models.CharField(max_length=250, null=True, blank=True)
    tanggal_mulai = models.DateField(blank=True, null=True)
    tanggal_selesai = models.DateField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES,max_length=120)
    class Meta:
        pass
    def __str__(self):
        return str(self.pk)

class rencana_seleksinya(models.Model):
    judul = models.CharField(max_length=250, null=True, blank=True)
    tahun = models.DateField(blank=True, null=True)

