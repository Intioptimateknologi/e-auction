# Generated by Django 4.2.2 on 2023-08-14 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0055_admin_created_admin_last_updated_viewers_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tim_lelang',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='tim_lelang',
            name='last_updated',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
