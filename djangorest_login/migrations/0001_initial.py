# Generated by Django 2.2.6 on 2019-10-24 11:32

from django.db import migrations, models
import djangorest_login.validate


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=100, validators=[djangorest_login.validate.validate_str], verbose_name='密码')),
                ('mobile', models.CharField(max_length=11, unique=True, verbose_name='手机号')),
                ('usertype', models.IntegerField(choices=[(1, 'normal'), (2, 'vip'), (3, 'svip')], default=1, verbose_name='用户等级')),
            ],
            options={
                'verbose_name': '用户信息表',
                'verbose_name_plural': '用户信息表',
                'db_table': 'djangorest_login_user',
            },
        ),
    ]
