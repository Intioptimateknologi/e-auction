# Generated by Django 4.2 on 2023-05-19 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userman', '0015_alter_bidder_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sk_pengangkatan', models.FileField(upload_to='uploads/timlelang/', verbose_name='File SK Pengangkatan')),
                ('nip', models.CharField(max_length=30, verbose_name='NIP Anggota TIM')),
                ('jabatan_dalam_tim', models.CharField(max_length=30, verbose_name='Jabtan dalam Tim')),
                ('jabatan', models.CharField(max_length=30, verbose_name='Jabatan di UnOr yang menugaskan')),
                ('active', models.BooleanField(default=False)),
                ('users', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
