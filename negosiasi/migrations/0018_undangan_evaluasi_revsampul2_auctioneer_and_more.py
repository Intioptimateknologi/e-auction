# Generated by Django 4.2.2 on 2023-07-19 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0033_usermenu_order'),
        ('negosiasi', '0017_rename_sampul2_form_esampul2_sampul_2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='undangan_evaluasi_revsampul2',
            name='auctioneer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.tim_lelang'),
        ),
        migrations.AddField(
            model_name='undangan_revsampul2',
            name='auctioneer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.tim_lelang'),
        ),
        migrations.AddField(
            model_name='undg_sampul2',
            name='auctioneer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.tim_lelang'),
        ),
    ]
