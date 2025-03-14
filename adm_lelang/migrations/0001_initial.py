# Generated by Django 4.2.2 on 2023-06-19 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userman', '0033_usermenu_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='item_lelang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tayang', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('nama_lelang', models.TextField(max_length=100)),
                ('keterangan', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='sanggahan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sangahan', models.TextField()),
                ('jawaban_sanggahan', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='viewers_lelang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
                ('viewer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.viewers')),
            ],
        ),
        migrations.CreateModel(
            name='release_lelang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('versi', models.TextField(max_length=100)),
                ('released', models.BooleanField(default=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('signature', models.TextField(max_length=100)),
                ('judul', models.TextField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('tgl_release', models.DateField()),
                ('dokumen', models.FileField(upload_to='upload/release/')),
                ('release_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='persyaratan_lelang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persyaratan', models.CharField(max_length=255, null=True)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='pengumuman',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomor', models.CharField(max_length=255, null=True)),
                ('judul', models.CharField(max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('pengumuman', models.TextField(null=True)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='penetapan_pemenang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='panitia_seleksi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='jadwal_seleksi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agenda', models.CharField(max_length=100)),
                ('tanggal', models.DateField()),
                ('status', models.CharField(choices=[('ditutup', 'ditutup'), ('dibuka', 'dibuka')], default='ditutup', max_length=20)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='detail_itemlelang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('teknologi', models.TextField(max_length=100)),
                ('reserved_price', models.FloatField()),
                ('band', models.TextField(max_length=100)),
                ('rentang_frekuensi', models.TextField(max_length=100)),
                ('eligibility_point_per_block', models.IntegerField(default=0)),
                ('max_block', models.IntegerField(default=0)),
                ('spectrum_cap', models.IntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('emd_price_per_block', models.IntegerField(default=0)),
                ('item_lelang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='dasar_hukum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=255)),
                ('attachment', models.FileField(null=True, upload_to='upload/dasar_hukum/')),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='bidder_lelang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('eligibility', models.IntegerField(default=0)),
                ('bidder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder')),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='auctioner_lelang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('auctioner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.tim_lelang')),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
    ]
