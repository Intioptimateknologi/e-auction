# Generated by Django 5.1.6 on 2025-02-10 09:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("adm_lelang", "0061_alter_alamat_panitia_status_and_more"),
        ("negosiasi", "0030_revisi_penawaran_keterangan"),
        ("userman", "0071_alter_usermenugroup_group_alter_usermenugroup_menu"),
    ]

    operations = [
        migrations.AlterField(
            model_name="obyek_seleksi_nego",
            name="bidder_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="userman.bidder_user",
                verbose_name="Bidder",
            ),
        ),
        migrations.AlterField(
            model_name="obyek_seleksi_nego",
            name="item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="adm_lelang.detail_itemlelang",
                verbose_name="Obyek Seleksi",
            ),
        ),
        migrations.AlterField(
            model_name="penawaran",
            name="bidder",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="nego_penawaran_bidder",
                to="userman.bidder_user",
            ),
        ),
        migrations.AlterField(
            model_name="penawaran",
            name="item",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="nego_penawaran_item",
                to="adm_lelang.detail_itemlelang",
            ),
        ),
        migrations.AlterField(
            model_name="penawaran",
            name="perwakilan",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="nego_penawaran_perwakilan",
                to="userman.bidder_perwakilan",
            ),
        ),
        migrations.AlterField(
            model_name="revisi_penawaran",
            name="bidder",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="nego_revisi_bidder",
                to="userman.bidder_user",
            ),
        ),
        migrations.AlterField(
            model_name="revisi_penawaran",
            name="item",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="nego_revisi_item",
                to="adm_lelang.detail_itemlelang",
            ),
        ),
        migrations.AlterField(
            model_name="revisi_penawaran",
            name="perwakilan",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="nego_revisi_perwakilan",
                to="userman.bidder_perwakilan",
            ),
        ),
    ]
