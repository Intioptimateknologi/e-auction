# Generated by Django 4.2.2 on 2023-06-22 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smra', '0009_alter_bidding_round_smra_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidding_round_smra',
            name='stop_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='bidding_round_smra',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
