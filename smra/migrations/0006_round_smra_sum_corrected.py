# Generated by Django 4.2.2 on 2023-06-20 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smra', '0005_eli_round_round_smra_temp_min_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='round_smra_sum',
            name='corrected',
            field=models.BooleanField(default=False),
        ),
    ]
