# Generated by Django 4.2.5 on 2023-10-08 03:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0029_banner_dibuat_oleh'),
    ]

    operations = [
        migrations.AddField(
            model_name='history_lelang',
            name='dibuat_oleh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dibuat_oleh_histori_lelang', to=settings.AUTH_USER_MODEL),
        ),
    ]
