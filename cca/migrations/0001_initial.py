# Generated by Django 4.2.2 on 2023-07-25 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adm_lelang', '0013_alter_pengumuman_tgl_release'),
        ('userman', '0033_usermenu_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='auctioner_hasil_cca',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('round', models.IntegerField(verbose_name='Putaran')),
                ('item_lelang', models.IntegerField()),
                ('block', models.IntegerField()),
                ('harga', models.FloatField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='hasil_highest_smra',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('item_lelang', models.IntegerField(null=True)),
                ('price', models.FloatField(null=True, verbose_name='Harga')),
                ('round', models.FloatField(null=True, verbose_name='Putaran')),
                ('block', models.FloatField(null=True, verbose_name='Jumlah Blok')),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='sum_round_cca',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('round', models.IntegerField()),
                ('status_round', models.CharField(choices=[('STA', 'START'), ('STO', 'STOP'), ('SUS', 'SUSPEND'), ('CLO', 'CLOSED'), ('INI', 'INIT'), ('NON', 'NONE'), ('WAI', 'WAIT')], max_length=3)),
                ('item_lelang', models.IntegerField()),
                ('count', models.IntegerField()),
                ('mulai1', models.CharField(max_length=25)),
                ('selesai1', models.CharField(max_length=25)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='round_cca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField()),
                ('price', models.FloatField(null=True)),
                ('block', models.IntegerField(null=True)),
                ('item_lelang', models.IntegerField(null=True)),
                ('prev_price', models.FloatField(null=True)),
                ('prev_block', models.IntegerField(null=True)),
                ('min_price', models.FloatField(null=True)),
                ('spectrum_cap', models.IntegerField(null=True)),
                ('max_block', models.IntegerField(null=True)),
                ('status_round', models.CharField(choices=[('STA', 'START'), ('STO', 'STOP'), ('SUS', 'SUSPEND'), ('CLO', 'CLOSED'), ('INI', 'INIT'), ('NON', 'NONE'), ('WAI', 'WAIT')], default='NON', max_length=3)),
                ('mulai', models.DateTimeField(null=True)),
                ('selesai', models.DateTimeField(null=True)),
                ('lock', models.BooleanField(default=False)),
                ('penawaran', models.JSONField(null=True)),
                ('status_sah', models.BooleanField(default=False)),
                ('jenis', models.CharField(choices=[('CLOCK', 'CLOCK'), ('SUPLE', 'SUPLEMENTAL')], default='CLOCK', max_length=5)),
                ('bidder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='userman.bidder')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adm_lelang.detail_itemlelang')),
            ],
        ),
        migrations.CreateModel(
            name='price_increase_cca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rentang_min', models.FloatField(null=True, verbose_name='Rentang Bawah')),
                ('rentang_max', models.FloatField(null=True, verbose_name='Rentang Atas')),
                ('kenaikan', models.FloatField(verbose_name='Kenaikan (%)')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='hasil_cca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField()),
                ('price', models.FloatField()),
                ('block', models.IntegerField()),
                ('item_lelang', models.IntegerField(null=True)),
                ('submit', models.DateTimeField(auto_now_add=True, null=True)),
                ('penawaran', models.FloatField(null=True)),
                ('valid', models.BooleanField(default=False)),
                ('berita_acara', models.FileField(upload_to='upload/bidder')),
                ('jenis', models.CharField(choices=[('CLOCK', 'CLOCK'), ('SUPLE', 'SUPLEMENTAL')], default='CLOCK', max_length=5)),
                ('bidder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='userman.bidder')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='adm_lelang.detail_itemlelang')),
            ],
        ),
    ]
