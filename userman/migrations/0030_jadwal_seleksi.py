# Generated by Django 4.2 on 2023-06-05 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0029_users_first_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='jadwal_seleksi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_seleksi', models.CharField(blank=True, max_length=250, null=True)),
                ('tanggal_mulai', models.DateField(blank=True, null=True)),
                ('tanggal_selesai', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Selesai', 'Selesai'), ('Dimulai', 'Dimulai')], max_length=120)),
            ],
        ),
    ]
