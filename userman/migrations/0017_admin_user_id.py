# Generated by Django 4.2 on 2023-05-19 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0016_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='user_id',
            field=models.CharField(max_length=30, null=True, verbose_name='user_id'),
        ),
    ]
