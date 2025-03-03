# Generated by Django 4.2.2 on 2023-07-31 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0035_remove_usermenugroup_id_perusahaan'),
        ('pasca_seleksi', '0026_remove_pemenang_nama_perusahaan_pemenang_bidder_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blok_pasca_seleksi',
            name='bidder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to='userman.bidder', verbose_name='Nama Perusahaan'),
        ),
        migrations.AlterField(
            model_name='blok_pasca_seleksi',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='userman.bidder', verbose_name='Pemilih'),
        ),
    ]
