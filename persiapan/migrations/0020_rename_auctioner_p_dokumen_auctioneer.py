# Generated by Django 4.2.2 on 2023-07-13 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persiapan', '0019_alter_p_dokumen_auctioner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='p_dokumen',
            old_name='auctioner',
            new_name='auctioneer',
        ),
    ]
