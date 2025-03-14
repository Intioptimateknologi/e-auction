# Generated by Django 4.2.2 on 2023-08-20 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0060_alter_users_customgroup'),
        ('smra2', '0014_obyek_seleksi_smra_ipaddress_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='round_smra2',
            name='perwakilan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='userman.bidder_perwakilan'),
        ),
        migrations.AlterField(
            model_name='obyek_seleksi_smra',
            name='ipaddress',
            field=models.CharField(blank=True, max_length=25, verbose_name='Alamat IP'),
        ),
        migrations.AlterField(
            model_name='obyek_seleksi_smra',
            name='is_block_ip',
            field=models.BooleanField(default=False, verbose_name='IP Diblok?'),
        ),
    ]
