# Generated by Django 4.2.2 on 2023-08-13 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0047_alter_users_nama_lengkap'),
        ('adm_lelang', '0028_undangan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder_lelang',
            name='bidder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder_user'),
        ),
    ]
