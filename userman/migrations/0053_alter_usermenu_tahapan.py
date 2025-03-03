# Generated by Django 4.2.2 on 2023-08-13 10:47

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0029_alter_bidder_lelang_bidder'),
        ('userman', '0052_usermenu_tahapan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermenu',
            name='tahapan',
            field=mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='UserMenu_tahapan', to='adm_lelang.tahapan_lelang2'),
        ),
    ]
