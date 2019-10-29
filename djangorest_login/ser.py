from rest_framework import serializers
from .models import User,Code
from .validate import validate_str
import os
import datetime

class CreateUser(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64,min_length=6, write_only=True,validators=[validate_str])
    password2 = serializers.CharField(max_length=64,min_length=6,  write_only=True)
    mobile = serializers.CharField(max_length=11, min_length=11, write_only=True)
    sec_key = serializers.CharField(max_length=64, write_only=True)
    snscode = serializers.CharField(max_length=10,write_only=True)

    def validate(self, attrs):
        key = os.environ['sec_key']
        sec_key = attrs['sec_key']
        if key != sec_key:
            raise serializers.ValidationError('验证密钥失败')
        password = attrs['password']
        password2 = attrs['password2']
        if password != password2:
            raise serializers.ValidationError('两次密码不一致，请重新输入')
        return attrs

    def validate_mobile(self, value):
        import re
        if not re.match('1[3-9]\d{9}', value):
            raise serializers.ValidationError('手机号码格式不正确')
        return value

    def validate_snscode(self, code):
        verify_records = Code.objects.filter(mobile=self.initial_data['mobile'])
        if verify_records:
            last_record = verify_records[0]
            # 判断验证码是否过期
            two_minutes_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=2, seconds=0)  # 获取5分钟之前的时间
            if last_record.add_time < two_minutes_ago:
                raise serializers.ValidationError('验证码过期')
            # 判断验证码是否正确
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
            # 不用将code返回到数据库中，只是做验证
            # return code
        else:
            raise serializers.ValidationError('验证码错误')

    def create(self, validated_data):
        del validated_data['password2']
        del validated_data['sec_key']
        del validated_data['snscode']
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        print(user)
        return user

    class Meta:
        model = User
        fields = '__all__'


class UserInfoSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','mobile')
