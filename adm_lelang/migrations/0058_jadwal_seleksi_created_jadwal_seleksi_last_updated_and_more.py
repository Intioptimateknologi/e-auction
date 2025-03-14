# Generated by Django 4.2.2 on 2023-10-17 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0057_detail_itemlelang_urutan'),
    ]

    operations = [
        migrations.AddField(
            model_name='jadwal_seleksi',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Tanggal Dibuat'),
        ),
        migrations.AddField(
            model_name='jadwal_seleksi',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Tanggal Diubah'),
        ),
        migrations.AlterField(
            model_name='berita_acara',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Tanggal Diubah'),
        ),
        migrations.AlterField(
            model_name='dasar_hukum',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Tanggal Diubah'),
        ),
        migrations.AlterField(
            model_name='detail_itemlelang',
            name='bandwidth',
            field=models.CharField(blank=True, max_length=255, verbose_name='Lebar Pita (MHz)'),
        ),
        migrations.AlterField(
            model_name='detail_itemlelang',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Tanggal Diubah'),
        ),
        migrations.AlterField(
            model_name='detail_itemlelang',
            name='rentang_frekuensi',
            field=models.CharField(blank=True, max_length=100, verbose_name='Rentang (Dari MHz s/d MHz)'),
        ),
        migrations.AlterField(
            model_name='penangung_jawab_seleksi',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Tanggal Diubah'),
        ),
        migrations.AlterField(
            model_name='pengumuman',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Tanggal Diubah'),
        ),
        migrations.AlterField(
            model_name='persyaratan_lelang',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Tanggal Diubah'),
        ),
    ]
