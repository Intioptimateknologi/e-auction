# Generated by Django 4.2.2 on 2023-07-13 05:42

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
            name='bid_bidder_smra',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('penawaran', models.FloatField()),
                ('round', models.IntegerField()),
                ('available_block', models.IntegerField()),
                ('band', models.TextField()),
                ('spectrum_cap', models.IntegerField()),
                ('eligibility_point_per_block', models.IntegerField()),
                ('block', models.IntegerField()),
                ('prev_block', models.IntegerField()),
                ('bidder_id', models.IntegerField()),
                ('object_id', models.IntegerField()),
                ('item_id', models.IntegerField()),
                ('reserved_price', models.FloatField()),
                ('prev_price', models.FloatField()),
                ('min_price', models.FloatField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='sum_round_smra2',
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
            name='round_smra2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField()),
                ('price', models.FloatField()),
                ('block', models.IntegerField()),
                ('prev_price', models.FloatField(null=True)),
                ('prev_block', models.IntegerField(null=True)),
                ('item_lelang', models.IntegerField(null=True)),
                ('min_price', models.FloatField(null=True)),
                ('status_round', models.CharField(choices=[('STA', 'START'), ('STO', 'STOP'), ('SUS', 'SUSPEND'), ('CLO', 'CLOSED'), ('INI', 'INIT'), ('NON', 'NONE'), ('WAI', 'WAIT')], default='NON', max_length=3)),
                ('mulai', models.DateTimeField()),
                ('selesai', models.DateTimeField()),
                ('lock', models.BooleanField(default=False)),
                ('khusus', models.BooleanField(default=False)),
                ('penawaran', models.FloatField(null=True)),
                ('bidder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='userman.bidder')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='adm_lelang.detail_itemlelang')),
            ],
        ),
        migrations.CreateModel(
            name='hasil_smra2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField()),
                ('price', models.FloatField()),
                ('block', models.IntegerField()),
                ('item_lelang', models.IntegerField(null=True)),
                ('submit', models.DateTimeField(auto_now_add=True, null=True)),
                ('penawaran', models.FloatField(null=True)),
                ('valid', models.BooleanField(default=False)),
                ('bidder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='userman.bidder')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='adm_lelang.detail_itemlelang')),
            ],
        ),
    ]
