# Generated by Django 4.2.2 on 2023-08-11 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adm_lelang', '0022_tahapan_lelang2'),
    ]

    operations = [
        migrations.DeleteModel(
            name='flow_state',
        ),
        migrations.RemoveField(
            model_name='item_lelang',
            name='state',
        ),
        migrations.AddField(
            model_name='alamat_panitia',
            name='dibuat_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alamat_panitia_dibuat_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='alamat_panitia',
            name='diubah_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alamat_panitia_diubah_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auctioner_lelang',
            name='dibuat_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auctioner_lelang_dibuat_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auctioner_lelang',
            name='diubah_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auctioner_lelang_diubah_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bidder_lelang',
            name='dibuat_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidder_lelang_dibuat_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bidder_lelang',
            name='diubah_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidder_lelang_diubah_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dasar_hukum',
            name='dibuat_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dasar_hukum_dibuat_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dasar_hukum',
            name='diubah_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dasar_hukum_diubah_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='detail_itemlelang',
            name='dibuat_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detail_itemlelang_dibuat_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='detail_itemlelang',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='detail_itemlelang',
            name='diubah_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detail_itemlelang_diubah_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item_lelang',
            name='dibuat_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_lelang_dibuat_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item_lelang',
            name='diubah_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_lelang_diubah_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jadwal_seleksi',
            name='dibuat_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jadwal_seleksi_dibuat_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jadwal_seleksi',
            name='diubah_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jadwal_seleksi_diubah_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pengumuman',
            name='dibuat_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pengumuman_dibuat_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='persyaratan_lelang',
            name='dibuat_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='persyaratan_lelang_dibuat_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='persyaratan_lelang',
            name='diubah_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='persyaratan_lelang_diubah_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tahapan_lelang2',
            name='dibuat_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tahapan_lelang2_dibuat_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tahapan_lelang2',
            name='diubah_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tahapan_lelang2_diubah_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='viewers_lelang',
            name='dibuat_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='viewers_lelang_dibuat_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='viewers_lelang',
            name='diubah_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='viewers_lelang_diubah_oleh', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pengumuman',
            name='diubah_oleh',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pengumuman_diubah_oleh', to=settings.AUTH_USER_MODEL),
        ),
    ]
