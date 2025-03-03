# Generated by Django 4.2.2 on 2023-06-19 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userman', '0033_usermenu_order'),
        ('adm_lelang', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='penilaian_bc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('penilaian', models.IntegerField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='pengumuman_bc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('keterangan', models.TextField(max_length=100)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='parameter_evaluasi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter', models.TextField(max_length=100, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='dokumen_bc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('dokumen_bc', models.FileField(upload_to='upload/files/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bidder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder')),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
        migrations.CreateModel(
            name='berita_acara_bc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dokumen_ba', models.FileField(upload_to='upload/files/')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('item_lelang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang')),
            ],
        ),
    ]
