# Generated by Django 4.2 on 2023-05-30 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0025_rename_bidder_bidder_perwakilan_bidder_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder_perwakilan',
            name='bidder_id',
            field=models.TextField(blank=True, max_length=30),
        ),
    ]
