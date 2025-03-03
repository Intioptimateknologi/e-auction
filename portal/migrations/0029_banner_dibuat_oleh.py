# Generated by Django 4.2.5 on 2023-10-05 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0028_aturan_lelang_dibuat_oleh_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='dibuat_oleh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dibuat_oleh_banner', to=settings.AUTH_USER_MODEL),
        ),
    ]
