# Generated by Django 4.2.2 on 2023-08-18 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0059_bidder_user_created_bidder_user_last_updated'),
        ('persiapan', '0027_remove_p_pertanyaan_nama_perusahaan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='p_dokumen',
            name='auctioneer',
            field=models.ManyToManyField(blank=True, to='userman.tim_lelang'),
        ),
        migrations.AlterField(
            model_name='p_dokumen',
            name='bidder',
            field=models.ManyToManyField(blank=True, to='userman.bidder'),
        ),
    ]
