# Generated by Django 4.2.2 on 2023-08-09 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0039_customgroup_last_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidder_perwakilan',
            name='bidder_id',
        ),
        migrations.AddField(
            model_name='bidder_perwakilan',
            name='bidder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder'),
        ),
    ]
