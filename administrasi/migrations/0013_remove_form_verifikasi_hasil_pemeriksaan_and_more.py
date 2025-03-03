# Generated by Django 4.2.2 on 2023-07-10 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrasi', '0012_alter_form_pemeriksaan_hasil_pemeriksaan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form_verifikasi',
            name='hasil_pemeriksaan',
        ),
        migrations.AlterField(
            model_name='form_pemeriksaan',
            name='bidbond',
            field=models.CharField(blank=True, choices=[('Ada', 'Ada'), ('Tidak Ada', 'Tidak Ada'), ('na', 'N/A')], default='na', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='form_pemeriksaan',
            name='sampul1',
            field=models.CharField(blank=True, choices=[('Ada', 'Ada'), ('Tidak Ada', 'Tidak Ada'), ('na', 'N/A')], default='na', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='form_pemeriksaan',
            name='sampul2',
            field=models.CharField(blank=True, choices=[('Ada', 'Ada'), ('Tidak Ada', 'Tidak Ada'), ('na', 'N/A')], default='na', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='form_verifikasi',
            name='bidbond',
            field=models.CharField(blank=True, choices=[('Ada', 'Ada'), ('Tidak Ada', 'Tidak Ada'), ('na', 'N/A')], default='na', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='form_verifikasi',
            name='sampul1',
            field=models.CharField(blank=True, choices=[('Ada', 'Ada'), ('Tidak Ada', 'Tidak Ada'), ('na', 'N/A')], default='na', max_length=10, null=True),
        ),
    ]
