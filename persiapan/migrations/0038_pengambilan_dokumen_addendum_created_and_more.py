# Generated by Django 4.2.2 on 2023-08-25 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persiapan', '0037_daftar_hadir_bidder_perwakilan'),
    ]

    operations = [
        migrations.AddField(
            model_name='pengambilan_dokumen_addendum',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='pengambilan_dokumen_addendum',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Tanggal Diubah'),
        ),
        migrations.AddField(
            model_name='pengambilan_dokumen_seleksi',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='pengambilan_dokumen_seleksi',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Tanggal Diubah'),
        ),
    ]
