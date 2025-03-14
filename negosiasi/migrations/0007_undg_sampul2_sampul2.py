# Generated by Django 4.2.2 on 2023-07-10 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0012_alter_item_lelang_tayang'),
        ('userman', '0033_usermenu_order'),
        ('negosiasi', '0006_form_esampul2_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='undg_sampul2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor', models.CharField(blank=True, null=True)),
                ('judul', models.CharField(blank=True, null=True)),
                ('tanggal', models.DateTimeField(blank=True, null=True)),
                ('tempat', models.TextField(blank=True, null=True)),
                ('agenda', models.CharField(blank=True, null=True)),
                ('keterangan', models.TextField(blank=True, null=True)),
                ('link_teleconference', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to='upload/files/')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bidder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder')),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='sampul2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sampul2', models.CharField(blank=True, max_length=100, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bidder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder')),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
    ]
