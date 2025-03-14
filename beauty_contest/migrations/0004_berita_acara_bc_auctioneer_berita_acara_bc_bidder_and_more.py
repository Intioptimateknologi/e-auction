# Generated by Django 4.2.2 on 2023-07-18 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0033_usermenu_order'),
        ('beauty_contest', '0003_penilaian_bc_bidder_penilaian_bc_parameter'),
    ]

    operations = [
        migrations.AddField(
            model_name='berita_acara_bc',
            name='auctioneer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.tim_lelang'),
        ),
        migrations.AddField(
            model_name='berita_acara_bc',
            name='bidder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder'),
        ),
        migrations.AddField(
            model_name='berita_acara_bc',
            name='judul',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='berita_acara_bc',
            name='keterangan',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='berita_acara_bc',
            name='nomor',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='berita_acara_bc',
            name='tanggal',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
