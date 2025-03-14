# Generated by Django 4.2.6 on 2023-11-17 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0058_jadwal_seleksi_created_jadwal_seleksi_last_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail_itemlelang',
            name='band',
            field=models.CharField(max_length=10, verbose_name='Pita (MHz)'),
        ),
        migrations.AlterField(
            model_name='detail_itemlelang',
            name='bandwidth',
            field=models.CharField(blank=True, max_length=100, verbose_name='Lebar Pita (MHz)'),
        ),
        migrations.AlterField(
            model_name='detail_itemlelang',
            name='cakupan',
            field=models.CharField(blank=True, max_length=100, verbose_name='Cakupan'),
        ),
        migrations.AlterField(
            model_name='detail_itemlelang',
            name='keterangan',
            field=models.TextField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='undangan',
            name='agenda',
            field=models.CharField(blank=True, null=True, verbose_name='Agenda'),
        ),
        migrations.AlterField(
            model_name='undangan',
            name='file',
            field=models.FileField(upload_to='upload/files/', verbose_name='Berkas'),
        ),
        migrations.AlterField(
            model_name='undangan',
            name='judul',
            field=models.CharField(blank=True, null=True, verbose_name='Judul'),
        ),
        migrations.AlterField(
            model_name='undangan',
            name='nomor',
            field=models.CharField(blank=True, null=True, verbose_name='Nomor'),
        ),
    ]
