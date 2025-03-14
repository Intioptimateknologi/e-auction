# Generated by Django 4.2.2 on 2023-09-07 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0052_alter_detail_itemlelang_harga_minimal'),
        ('gabungan', '0010_penentuan_parameter_bobot2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='penentuan_parameter',
            name='obyek_bc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gabungan_obyekbc', to='adm_lelang.detail_itemlelang'),
        ),
        migrations.AlterField(
            model_name='penentuan_parameter',
            name='obyek_smra',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gabungan_obyeksmra', to='adm_lelang.detail_itemlelang'),
        ),
        migrations.DeleteModel(
            name='sum_gabungan',
        ),
    ]
