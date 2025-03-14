# Generated by Django 4.2.2 on 2023-08-29 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('smra', '0023_remove_undangan_smra_cca_auctioneer_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='auction_summary_smra',
        ),
        migrations.DeleteModel(
            name='bid_bidder_smra',
        ),
        migrations.AddField(
            model_name='round_schedule_smra',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='round_schedule_smra',
            name='dibuat_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='round_schedule_dibuat_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='round_schedule_smra',
            name='diubah_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='round_schedule_diubah_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='round_schedule_smra',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Diubah Terakhir'),
        ),
    ]
