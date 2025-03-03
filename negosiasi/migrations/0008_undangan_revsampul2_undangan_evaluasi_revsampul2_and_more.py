# Generated by Django 4.2.2 on 2023-07-11 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0033_usermenu_order'),
        ('adm_lelang', '0012_alter_item_lelang_tayang'),
        ('negosiasi', '0007_undg_sampul2_sampul2'),
    ]

    operations = [
        migrations.CreateModel(
            name='undangan_revsampul2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor', models.CharField(blank=True, null=True)),
                ('judul', models.CharField(blank=True, null=True)),
                ('tanggal', models.DateTimeField(blank=True, null=True)),
                ('tempat', models.TextField(blank=True, null=True)),
                ('agenda', models.CharField(blank=True, null=True)),
                ('link_teleconference', models.TextField(blank=True, null=True)),
                ('keterangan', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to='upload/files/')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bidder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder')),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='undangan_evaluasi_revsampul2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor', models.CharField(blank=True, null=True)),
                ('judul', models.CharField(blank=True, null=True)),
                ('tanggal', models.DateTimeField(blank=True, null=True)),
                ('tempat', models.TextField(blank=True, null=True)),
                ('agenda', models.CharField(blank=True, null=True)),
                ('link_teleconference', models.TextField(blank=True, null=True)),
                ('keterangan', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to='upload/files/')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bidder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder')),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='form_revsampul2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sampul2', models.CharField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
                ('nama_perusahaan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder')),
            ],
        ),
        migrations.CreateModel(
            name='form_evaluasi_revsampul2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sampul2', models.CharField(blank=True, choices=[('Diterima', 'Diterima'), ('Tidak Diterima', 'Tidak Diterima')], max_length=110, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
                ('nama_perusahaan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder')),
            ],
        ),
    ]
