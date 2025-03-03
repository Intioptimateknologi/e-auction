# Generated by Django 4.2.2 on 2023-06-22 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smra', '0010_bidding_round_smra_stop_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidding_round_smra',
            name='status_round',
            field=models.CharField(choices=[('STA', 'START'), ('STO', 'STOP'), ('SUS', 'SUSPEND'), ('CLO', 'CLOSED'), ('INI', 'INIT'), ('NON', 'NONE'), ('WAI', 'WAIT')], default='NON', max_length=3),
        ),
    ]
