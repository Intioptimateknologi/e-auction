# Generated by Django 4.2.2 on 2023-07-27 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasca_seleksi', '0023_blok_pasca_seleksi_approved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blok_pasca_seleksi',
            name='pilih_blok',
            field=models.BooleanField(default=False, verbose_name='Pilih Blok'),
        ),
        migrations.AddField(
            model_name='blok_pasca_seleksi',
            name='sudah_pilih',
            field=models.BooleanField(default=False, verbose_name='Sudah Memilih'),
        ),
    ]
