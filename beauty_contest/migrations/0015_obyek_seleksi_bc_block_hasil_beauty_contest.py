# Generated by Django 4.2.2 on 2023-09-13 04:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adm_lelang', '0053_alter_pengumuman_tgl_release_alter_undangan_judul_and_more'),
        ('userman', '0067_alter_admin_jabatan_alter_bidder_list_jabatan_and_more'),
        ('beauty_contest', '0014_format_dokumen_bc_keterangan'),
    ]

    operations = [
        migrations.AddField(
            model_name='obyek_seleksi_bc',
            name='block',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='hasil_beauty_contest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('penilaian', models.FloatField(blank=True, null=True)),
                ('ranking', models.IntegerField(blank=True, null=True)),
                ('bidder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userman.bidder_user')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adm_lelang.detail_itemlelang')),
                ('parameter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='beauty_contest.parameter_evaluasi')),
            ],
        ),
    ]
