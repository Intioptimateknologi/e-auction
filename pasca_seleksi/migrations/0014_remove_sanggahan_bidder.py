# Generated by Django 4.2.2 on 2023-07-13 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pasca_seleksi', '0013_sanggahan_bidder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sanggahan',
            name='bidder',
        ),
    ]
