# Generated by Django 4.2.2 on 2023-08-13 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0050_users_customgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermenugroup',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='userman.customgroup'),
        ),
    ]
