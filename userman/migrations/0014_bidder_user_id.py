# Generated by Django 4.2 on 2023-05-19 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0013_alter_bidder_jenis_penyelenggara'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidder',
            name='user_id',
            field=models.FileField(max_length=30, null=True, upload_to='', verbose_name='user_id'),
        ),
    ]
