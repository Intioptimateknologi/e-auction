# Generated by Django 4.2.5 on 2023-10-06 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0055_persyaratan_lelang_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='persyaratan_lelang',
            name='keterangan',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='persyaratan_lelang',
            name='no_urut',
            field=models.CharField(max_length=255, null=True, verbose_name='Nomor Urut'),
        ),
    ]
