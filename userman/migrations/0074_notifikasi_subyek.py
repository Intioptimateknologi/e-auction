# Generated by Django 5.1.6 on 2025-02-15 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userman", "0073_remove_notifikasi_bidder_notifikasi_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="notifikasi",
            name="subyek",
            field=models.CharField(default="", max_length=255, verbose_name="Email"),
        ),
    ]
