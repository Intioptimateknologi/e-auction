# Generated by Django 4.2.2 on 2023-07-05 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0012_alter_item_lelang_tayang'),
        ('userman', '0033_usermenu_order'),
        ('pasca_seleksi', '0003_pemilihan_blok_pasca_seleksi'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='pemilihan_blok',
            new_name='jawaban_atas_sanggahan',
        ),
    ]
