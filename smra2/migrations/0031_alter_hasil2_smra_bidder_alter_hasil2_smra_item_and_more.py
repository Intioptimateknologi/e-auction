# Generated by Django 5.1.6 on 2025-02-10 09:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("adm_lelang", "0061_alter_alamat_panitia_status_and_more"),
        ("smra2", "0030_hasil_smra2_fin_round_smra2_vi_and_more"),
        ("userman", "0071_alter_usermenugroup_group_alter_usermenugroup_menu"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hasil2_smra",
            name="bidder",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="userman.bidder_user",
            ),
        ),
        migrations.AlterField(
            model_name="hasil2_smra",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="adm_lelang.detail_itemlelang",
            ),
        ),
        migrations.AlterField(
            model_name="hasil2_smra",
            name="perwakilan",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="userman.bidder_perwakilan",
            ),
        ),
        migrations.AlterField(
            model_name="hasil_smra2",
            name="bidder",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="userman.bidder_user",
            ),
        ),
        migrations.AlterField(
            model_name="hasil_smra2",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="adm_lelang.detail_itemlelang",
            ),
        ),
        migrations.AlterField(
            model_name="hasil_smra2",
            name="perwakilan",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="userman.bidder_perwakilan",
            ),
        ),
        migrations.AlterField(
            model_name="obyek_seleksi_smra",
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
            model_name="obyek_seleksi_smra",
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
            model_name="price_increase",
            name="detail_item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="adm_lelang.detail_itemlelang",
            ),
        ),
        migrations.AlterField(
            model_name="price_increase",
            name="item",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="adm_lelang.item_lelang",
            ),
        ),
        migrations.AlterField(
            model_name="round_smra2",
            name="bidder",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="userman.bidder_user",
            ),
        ),
        migrations.AlterField(
            model_name="round_smra2",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="adm_lelang.detail_itemlelang",
            ),
        ),
        migrations.AlterField(
            model_name="round_smra2",
            name="perwakilan",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="userman.bidder_perwakilan",
            ),
        ),
    ]
