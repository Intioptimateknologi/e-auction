# Generated by Django 4.2.2 on 2023-08-22 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0020_alter_history_lelang_tahun_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history_lelang',
            name='tahun',
            field=models.DateField(blank=True, null=True),
        ),
    ]
