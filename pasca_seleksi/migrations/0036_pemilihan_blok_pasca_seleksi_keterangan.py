# Generated by Django 4.2.5 on 2023-10-10 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasca_seleksi', '0035_pemenang_dibuat_oleh_pemenang_diubah_oleh_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pemilihan_blok_pasca_seleksi',
            name='keterangan',
            field=models.TextField(blank=True, null=True),
        ),
    ]
