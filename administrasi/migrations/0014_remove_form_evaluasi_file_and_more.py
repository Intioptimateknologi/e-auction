# Generated by Django 4.2.2 on 2023-07-10 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrasi', '0013_remove_form_verifikasi_hasil_pemeriksaan_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form_evaluasi',
            name='file',
        ),
        migrations.AlterField(
            model_name='form_verifikasi',
            name='bidbond',
            field=models.CharField(blank=True, choices=[('Ada', 'Sesuai'), ('Tidak Ada', 'Tidak Sesuai'), ('na', 'N/A')], default='na', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='form_verifikasi',
            name='sampul1',
            field=models.CharField(blank=True, choices=[('Ada', 'Sesuai'), ('Tidak Ada', 'Tidak Sesuai'), ('na', 'N/A')], default='na', max_length=10, null=True),
        ),
    ]
