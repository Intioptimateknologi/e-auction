# Generated by Django 4.2.2 on 2023-09-07 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('negosiasi', '0026_revisi_penawaran_verified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluasi_penawaran',
            name='dokumen',
            field=models.FileField(blank=True, upload_to='upload/files/'),
        ),
        migrations.AddField(
            model_name='evaluasi_revisi_penawaran',
            name='dokumen',
            field=models.FileField(blank=True, upload_to='upload/files/'),
        ),
    ]
