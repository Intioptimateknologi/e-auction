# Generated by Django 4.2.2 on 2023-06-22 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smra', '0008_remove_round_schedule_smra_durasi_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidding_round_smra',
            name='start_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
