# Generated by Django 5.1.6 on 2025-02-16 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userman", "0076_alter_notifikasi_email_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="notifikasi",
            name="expire_date",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="notifikasi",
            name="notification_type",
            field=models.CharField(
                choices=[("U", "Undangan"), ("B", "BA"), ("O", "Lain-lain")],
                default="U",
                max_length=1,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="notifikasi",
            name="email_status",
            field=models.CharField(max_length=30, verbose_name="Status Email"),
        ),
    ]
