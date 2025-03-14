# Generated by Django 4.2.6 on 2023-11-17 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0031_alter_aturan_lelang_nama_kebijakan_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='history_lelang',
            name='image',
            field=models.ImageField(default=1, upload_to='upload/images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='banner',
            name='nama_banner',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='banner',
            name='tag',
            field=models.CharField(choices=[('front', 'Aktif'), ('back', 'Non Aktif')], max_length=120),
        ),
    ]
