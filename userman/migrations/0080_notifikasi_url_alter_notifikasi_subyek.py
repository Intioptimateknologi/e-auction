# Generated by Django 5.1.6 on 2025-03-12 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userman", "0079_bidder_perwakilan_peruri_ttd"),
    ]

    operations = [
        migrations.AddField(
            model_name="notifikasi",
            name="url",
            field=models.CharField(
                default="", max_length=255, null=True, verbose_name="URL"
            ),
        ),
        migrations.AlterField(
            model_name="notifikasi",
            name="subyek",
            field=models.CharField(default="", max_length=255, verbose_name="Subyek"),
        ),
    ]
