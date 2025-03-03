# Generated by Django 4.2 on 2023-05-18 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0012_alter_tim_lelang_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidder',
            name='jenis_penyelenggara',
            field=models.CharField(choices=[('JSB', 'Jaringan Bergerak Seluler'), ('JKS', 'Jaringan Tetap Lokal Packet Switched')], default='JSB', max_length=3, verbose_name='Jenis Pengelenggara'),
        ),
    ]
