# Generated by Django 4.2.5 on 2023-10-10 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userman', '0068_users_dibuat_oleh_users_diubah_oleh_users_pending'),
        ('pasca_seleksi', '0037_form_ps_sanggahan_keterangan'),
    ]

    operations = [
        migrations.AddField(
            model_name='sanggahan',
            name='bidder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder_perwakilan'),
        ),
        migrations.AddField(
            model_name='sanggahan',
            name='dibuat_oleh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dibuat_oleh_paska_sanggahan', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sanggahan',
            name='diubah_oleh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='diubah_oleh_paska_sanggahan', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sanggahan',
            name='keterangan',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sanggahan',
            name='waktu_sanggahan',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='sanggahan',
            name='status_sanggahan',
            field=models.CharField(blank=True, choices=[('Ada', 'Sanggah'), ('Tidak Ada', 'Tidak Sanggah'), ('na', 'N/A')], default='na', max_length=10, null=True),
        ),
    ]
