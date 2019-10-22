from django.db import models
from django.contrib.auth.hashers import make_password,check_password
from .validate import validate_str
import jwt
import datetime
from django.conf import settings

# Create your models here.

class User(models.Model):
    User_Type = ((1, 'normal'), (2, 'vip'), (3, 'svip'))

    username = models.CharField(max_length=32,unique=True,verbose_name='用户名')
    password = models.CharField(max_length=100,verbose_name='密码',validators=[validate_str])
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    usertype = models.IntegerField(choices=User_Type,verbose_name='用户等级',default=1)

    class Meta:
        db_table = 'djangorest_login_user'
        verbose_name = '用户信息表'
        verbose_name_plural = '用户信息表'

    def __str__(self):
        return self.username

    def set_password(self,password):
        self.password = make_password(password)
        return

    def check_pwd(self,password):
        return check_password(self.password,password)

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'data': {
                'username': self.username
            }
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


