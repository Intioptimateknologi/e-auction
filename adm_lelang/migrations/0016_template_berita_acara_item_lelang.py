# Generated by Django 4.2.2 on 2023-07-26 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0015_rename_template_bertia_acara_template_berita_acara'),
    ]

    operations = [
        migrations.AddField(
            model_name='template_berita_acara',
            name='item_lelang',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.item_lelang'),
        ),
    ]
