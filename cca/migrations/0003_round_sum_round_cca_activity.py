# Generated by Django 4.2.2 on 2023-07-26 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cca', '0002_round_cca_eli_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='round_sum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField()),
                ('item_lelang', models.IntegerField()),
                ('status_round', models.CharField(choices=[('STA', 'START'), ('STO', 'STOP'), ('SUS', 'SUSPEND'), ('CLO', 'CLOSED'), ('INI', 'INIT'), ('NON', 'NONE'), ('WAI', 'WAIT')], max_length=3)),
                ('mulai', models.DateTimeField(null=True)),
                ('selesai', models.DateTimeField(null=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='round_cca',
            name='activity',
            field=models.IntegerField(null=True),
        ),
    ]
