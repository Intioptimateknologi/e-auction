# Generated by Django 4.2.2 on 2023-08-01 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0011_aturan_lelang_keterangan_aturan_lelang_tanggal'),
    ]

    operations = [
        migrations.AddField(
            model_name='portal_block',
            name='judul',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]
