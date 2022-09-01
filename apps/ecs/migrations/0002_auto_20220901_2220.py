# Generated by Django 2.0 on 2022-09-01 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecs',
            name='batch_id',
            field=models.CharField(default='', max_length=32, verbose_name='操作的批次号'),
        ),
        migrations.AddField(
            model_name='ecs',
            name='code',
            field=models.CharField(default='', max_length=32, verbose_name='唯一标识'),
        ),
        migrations.AddField(
            model_name='ecs',
            name='cpu',
            field=models.CharField(default='', max_length=32, verbose_name='cpu型号'),
        ),
        migrations.AddField(
            model_name='ecs',
            name='disk',
            field=models.CharField(default='', max_length=32, verbose_name='硬盘存储大小'),
        ),
        migrations.AddField(
            model_name='ecs',
            name='memory',
            field=models.CharField(default='', max_length=32, verbose_name='内存大小'),
        ),
        migrations.AddField(
            model_name='ecs',
            name='original_specs',
            field=models.CharField(default='', max_length=256, verbose_name='原始上传配置的文件oss地址'),
        ),
        migrations.AddField(
            model_name='ecs',
            name='user_id',
            field=models.IntegerField(default=0, verbose_name='用户id'),
        ),
    ]