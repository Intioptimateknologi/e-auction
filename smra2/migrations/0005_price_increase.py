# Generated by Django 4.2.2 on 2023-07-19 00:50

import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0013_alter_pengumuman_tgl_release'),
        ('smra2', '0004_signature2_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='price_increase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rentang', django.contrib.postgres.fields.ranges.DecimalRangeField()),
                ('kenaikan', models.FloatField()),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='adm_lelang.detail_itemlelang')),
            ],
        ),
    ]
