# Generated by Django 4.2.2 on 2023-07-24 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gabungan', '0004_penilaian_gabungan_bidder_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='penilaian_gabungan',
            name='parameter',
            field=models.CharField(choices=[('1', 'SMRA'), ('2', 'CCA'), ('3', 'Beauty Contest')], default='1', max_length=1),
        ),
    ]
