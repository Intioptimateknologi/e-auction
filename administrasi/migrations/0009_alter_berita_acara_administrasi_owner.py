# Generated by Django 4.2.2 on 2023-06-26 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrasi', '0008_alter_berita_acara_administrasi_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='berita_acara_administrasi',
            name='owner',
            field=models.TextField(blank=True, choices=[('PERMOHONAN', 'Permohonan'), ('PEMERIKSAAN', 'Pemeriksaan'), ('VERIFIKASI', 'Verifikasi'), ('HASIL', 'Hasil'), ('SANGGAHAN', 'Sanggahan'), ('EVALUASI', 'Evaluasi'), ('AKUN', 'Akun'), ('UNKNOWN', 'Unknown')], default='UNKNOWN', max_length=100, null=True),
        ),
    ]
