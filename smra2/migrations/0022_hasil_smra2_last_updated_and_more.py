# Generated by Django 4.2.2 on 2023-09-06 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smra2', '0021_price_increase_detail_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='hasil_smra2',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='round_smra2',
            name='status_round',
            field=models.CharField(choices=[('STA', 'START'), ('STO', 'STOP'), ('SUS', 'SUSPEND'), ('CLO', 'CLOSED'), ('FIN', 'FINAL'), ('INI', 'INIT'), ('NON', 'NONE'), ('WAI', 'WAIT')], default='NON', max_length=3),
        ),
    ]
