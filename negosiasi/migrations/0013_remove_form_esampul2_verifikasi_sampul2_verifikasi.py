# Generated by Django 4.2.2 on 2023-07-17 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('negosiasi', '0012_form_esampul2_verifikasi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form_esampul2',
            name='verifikasi',
        ),
        migrations.AddField(
            model_name='sampul2',
            name='verifikasi',
            field=models.CharField(blank=True, choices=[('Sesuai', 'Sesuai'), ('Tidak Sesuai', 'Tidak Sesuai')], max_length=110, null=True),
        ),
    ]
