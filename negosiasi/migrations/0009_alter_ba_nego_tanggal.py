# Generated by Django 4.2.2 on 2023-07-11 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('negosiasi', '0008_undangan_revsampul2_undangan_evaluasi_revsampul2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ba_nego',
            name='tanggal',
            field=models.DateField(blank=True, null=True),
        ),
    ]
