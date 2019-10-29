# Generated by Django 2.2.6 on 2019-10-28 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangorest_login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32, verbose_name='验证码')),
                ('mobile', models.CharField(max_length=11, unique=True, verbose_name='手机号')),
                ('add_time', models.DateTimeField(auto_now=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '短信验证码',
                'verbose_name_plural': '短信验证码',
            },
        ),
    ]