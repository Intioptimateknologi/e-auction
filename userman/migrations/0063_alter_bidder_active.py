# Generated by Django 4.2.2 on 2023-08-22 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0062_alter_usermenu_tahapan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder',
            name='active',
            field=models.BooleanField(),
        ),
    ]
