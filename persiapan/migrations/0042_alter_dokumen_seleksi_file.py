# Generated by Django 4.2.6 on 2023-11-01 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persiapan', '0041_alter_daftar_hadir_bidder_perwakilan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dokumen_seleksi',
            name='file',
            field=models.FileField(upload_to='upload/files/persiapan/dokumen_seleksi/', verbose_name='Pengambilan Dokumen Seleksi'),
        ),
    ]
