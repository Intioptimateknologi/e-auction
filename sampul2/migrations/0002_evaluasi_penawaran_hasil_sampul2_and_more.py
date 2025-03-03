# Generated by Django 4.2.6 on 2024-05-27 06:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0061_alter_alamat_panitia_status_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userman', '0069_alter_users_nama_lengkap_alter_users_user_type_and_more'),
        ('sampul2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='evaluasi_penawaran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hasil', models.CharField(blank=True, choices=[('Diterima', 'Diterima'), ('Tidak Diterima', 'Tidak Diterima')], max_length=110, null=True)),
                ('catatan', models.TextField()),
                ('dokumen', models.FileField(blank=True, upload_to='upload/files/')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('dibuat_oleh', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sampul2_esampul_dibuat_oleh', to=settings.AUTH_USER_MODEL)),
                ('diubah_oleh', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sampul2_esampul_diubah_oleh', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='hasil_sampul2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('harga', models.FloatField()),
                ('ranking', models.IntegerField()),
                ('bidder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder_user')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.detail_itemlelang')),
            ],
        ),
        migrations.CreateModel(
            name='obyek_seleksi_sampul2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('bidder_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='userman.bidder_user', verbose_name='Bidder')),
                ('dibuat_oleh', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sampul2_obyek_dibuat_oleh', to=settings.AUTH_USER_MODEL)),
                ('diubah_oleh', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sampul2_obyek_diubah_oleh', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adm_lelang.detail_itemlelang', verbose_name='Obyek Seleksi')),
            ],
        ),
        migrations.CreateModel(
            name='penawaran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dokumen_penawaran', models.FileField(upload_to='upload/files/')),
                ('harga', models.FloatField()),
                ('blok', models.IntegerField()),
                ('verified', models.BooleanField(default=False)),
                ('verified_at', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('bidder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder_user')),
                ('dibuat_oleh', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sampul2_penawaran_dibuat_oleh', to=settings.AUTH_USER_MODEL)),
                ('diubah_oleh', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sampul2_penawaran_diubah_oleh', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.detail_itemlelang')),
                ('perwakilan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='userman.bidder_perwakilan')),
                ('verified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sampul2_verified_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='form_pemeriksaan',
            name='bidder',
        ),
        migrations.RemoveField(
            model_name='form_pemeriksaan',
            name='dibuat_oleh',
        ),
        migrations.RemoveField(
            model_name='form_pemeriksaan',
            name='diubah_oleh',
        ),
        migrations.RemoveField(
            model_name='form_pemeriksaan',
            name='item',
        ),
        migrations.RemoveField(
            model_name='form_verifikasi',
            name='bidder',
        ),
        migrations.RemoveField(
            model_name='form_verifikasi',
            name='dibuat_oleh',
        ),
        migrations.RemoveField(
            model_name='form_verifikasi',
            name='diubah_oleh',
        ),
        migrations.RemoveField(
            model_name='form_verifikasi',
            name='item',
        ),
        migrations.DeleteModel(
            name='form_evaluasi',
        ),
        migrations.DeleteModel(
            name='form_pemeriksaan',
        ),
        migrations.DeleteModel(
            name='form_verifikasi',
        ),
        migrations.AddField(
            model_name='evaluasi_penawaran',
            name='penawaran',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sampul2.penawaran'),
        ),
    ]
