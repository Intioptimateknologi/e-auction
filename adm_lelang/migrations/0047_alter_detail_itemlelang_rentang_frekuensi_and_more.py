# Generated by Django 4.2.2 on 2023-08-24 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0046_dasar_hukum_tanggal_alter_dasar_hukum_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail_itemlelang',
            name='rentang_frekuensi',
            field=models.CharField(blank=True, max_length=100, verbose_name='Range (Dari MHz s/d MHz)'),
        ),
        migrations.AlterField(
            model_name='detail_itemlelang',
            name='teknologi',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
