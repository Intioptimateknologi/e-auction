# Generated by Django 4.2.2 on 2023-07-25 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasca_seleksi', '0017_blok_pasca_seleksi_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pemilihan_blok_pasca_seleksi',
            name='pilih_blok',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='blok_pasca_seleksi',
            name='nama_block',
            field=models.CharField(max_length=100, verbose_name='Nama Blok'),
        ),
    ]
