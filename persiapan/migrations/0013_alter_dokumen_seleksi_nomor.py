# Generated by Django 4.2.2 on 2023-07-10 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persiapan', '0012_alter_aanwizing_nomor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dokumen_seleksi',
            name='nomor',
            field=models.CharField(blank=True, null=True),
        ),
    ]
