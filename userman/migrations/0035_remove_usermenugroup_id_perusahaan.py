# Generated by Django 4.2.2 on 2023-07-31 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0034_menugroup_map_usermenugroup_id_perusahaan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermenugroup',
            name='id_perusahaan',
        ),
    ]
