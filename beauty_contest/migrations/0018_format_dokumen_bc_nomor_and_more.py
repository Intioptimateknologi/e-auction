# Generated by Django 4.2.5 on 2023-10-10 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty_contest', '0017_dokumen_bc_nama_dok'),
    ]

    operations = [
        migrations.AddField(
            model_name='format_dokumen_bc',
            name='nomor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='format_dokumen_bc',
            name='tgl_penetapan',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
