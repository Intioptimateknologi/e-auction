# Generated by Django 4.2.2 on 2023-09-12 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smra2', '0025_hasil2_smra_ranking_alter_hasil2_smra_submit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hasil2_smra',
            name='ranking',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
