# Generated by Django 4.2.2 on 2023-06-23 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persiapan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='berita_acara_persiapan',
            name='owner',
            field=models.TextField(blank=True, choices=[('PEMBUKAAN', 'Pembukaan'), ('DOKUMEN', 'Dokumen'), ('PERTANYAA', 'Pertanyaan'), ('AANWIZING', 'Aanwizing'), ('SIMULASI', 'Simulasi'), ('ADDENDUM', 'Addendum'), ('UNKNOWN', 'Unknown')], default='UNKNOWN', max_length=100, null=True),
        ),
    ]
