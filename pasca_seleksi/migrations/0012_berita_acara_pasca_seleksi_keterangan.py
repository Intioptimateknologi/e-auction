# Generated by Django 4.2.2 on 2023-07-13 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasca_seleksi', '0011_alter_berita_acara_pasca_seleksi_nomor'),
    ]

    operations = [
        migrations.AddField(
            model_name='berita_acara_pasca_seleksi',
            name='keterangan',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
