# Generated by Django 4.2.2 on 2023-07-19 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smra2', '0006_alter_price_increase_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price_increase',
            name='rentang',
        ),
        migrations.AddField(
            model_name='price_increase',
            name='rentang_max',
            field=models.FloatField(null=True, verbose_name='Rentang Atas'),
        ),
        migrations.AddField(
            model_name='price_increase',
            name='rentang_min',
            field=models.FloatField(null=True, verbose_name='Rentang Bawah'),
        ),
        migrations.AlterField(
            model_name='price_increase',
            name='kenaikan',
            field=models.FloatField(verbose_name='Kenaikan (%)'),
        ),
    ]
