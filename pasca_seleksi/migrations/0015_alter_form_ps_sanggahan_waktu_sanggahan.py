# Generated by Django 4.2.2 on 2023-07-17 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasca_seleksi', '0014_remove_sanggahan_bidder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form_ps_sanggahan',
            name='waktu_sanggahan',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
