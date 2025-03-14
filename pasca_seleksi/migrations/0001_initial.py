# Generated by Django 4.2.2 on 2023-07-05 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userman', '0033_usermenu_order'),
        ('adm_lelang', '0012_alter_item_lelang_tayang'),
    ]

    operations = [
        migrations.CreateModel(
            name='seleksi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor', models.IntegerField()),
                ('judul', models.CharField(max_length=100)),
                ('tanggal', models.DateField()),
                ('keterangan', models.TextField()),
                ('file_link', models.FileField(upload_to='upload/files/pasca_seleksi/seleksi/')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='sanggahan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_sanggahan', models.BooleanField(default=False)),
                ('file_link', models.FileField(upload_to='upload/files/pasca_seleksi/sanggahan/')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='pemenang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keterangan', models.TextField()),
                ('file_link', models.FileField(upload_to='upload/files/pasca_seleksi/pemenang/')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
                ('nama_perusahaan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder')),
            ],
        ),
        migrations.CreateModel(
            name='blok',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor', models.IntegerField()),
                ('judul', models.CharField(max_length=100)),
                ('tanggal', models.DateField()),
                ('tempat', models.CharField(max_length=100)),
                ('waktu', models.DateTimeField()),
                ('agenda', models.TextField()),
                ('link_teleconference', models.TextField()),
                ('keterangan', models.TextField()),
                ('link_file', models.FileField(upload_to='upload/files/pasca_seleksi/blok/')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
    ]
