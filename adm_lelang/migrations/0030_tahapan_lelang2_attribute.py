# Generated by Django 4.2.2 on 2023-08-14 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0029_alter_bidder_lelang_bidder'),
    ]

    operations = [
        migrations.AddField(
            model_name='tahapan_lelang2',
            name='attribute',
            field=models.JSONField(null=True),
        ),
    ]
