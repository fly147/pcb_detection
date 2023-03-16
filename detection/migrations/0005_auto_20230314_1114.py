# Generated by Django 3.2.18 on 2023-03-14 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0004_auto_20230313_1845'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_time', models.DateField(verbose_name='检测时间')),
                ('defect_type', models.CharField(max_length=256, verbose_name='缺陷类型')),
                ('origin_picture', models.CharField(max_length=256, verbose_name='原始图片')),
                ('check_picture', models.CharField(max_length=256, verbose_name='检测图片')),
                ('check_pepole', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detection.user', verbose_name='检测人员')),
            ],
            options={
                'verbose_name': 'PCB检测信息',
                'verbose_name_plural': 'PCB检测信息',
            },
        ),
    ]