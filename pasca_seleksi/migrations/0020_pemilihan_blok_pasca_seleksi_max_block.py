# Generated by Django 4.2.2 on 2023-07-26 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasca_seleksi', '0019_pemilihan_blok_pasca_seleksi_penawaran_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pemilihan_blok_pasca_seleksi',
            name='max_block',
            field=models.IntegerField(null=True, verbose_name='Jatah Blok'),
        ),
    ]
