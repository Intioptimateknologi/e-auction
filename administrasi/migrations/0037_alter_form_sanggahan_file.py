# Generated by Django 4.2.5 on 2023-10-06 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrasi', '0036_alter_form_sanggahan_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form_sanggahan',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='upload/files/'),
        ),
    ]
