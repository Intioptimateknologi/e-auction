# Generated by Django 4.2.6 on 2023-11-13 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0030_history_lelang_dibuat_oleh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aturan_lelang',
            name='nama_kebijakan',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='aturan_lelang',
            name='nomor',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='history_lelang',
            name='tahun',
            field=models.TextField(blank=True, null=True),
        ),
    ]
