# Generated by Django 4.2.2 on 2023-06-23 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0006_bidder_lelang_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder_lelang',
            name='ip_address',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
