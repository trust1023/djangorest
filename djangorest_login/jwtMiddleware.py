from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
import jwt
from django.conf import settings
from .models import User

class TokenAuth(BaseAuthentication):
    def authenticate(self, request):
        try:
            auth = request.META.get('HTTP_AUTHORIZATION').split()
        except:
            raise AuthenticationFailed('authenticate header wrong')
            #return JsonResponse({"code": 401, "message": "authenticate header wrong"})
            #只能raise return无效

            # 用户通过 API 获取数据验证流程
        if auth[0] != 'JWT':
            raise AuthenticationFailed('标识错误')
        try:
            dict = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
            username = dict.get('data').get('username')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token expired')
        except Exception:
            raise AuthenticationFailed('Can not get user object')
        token_query = User.objects.filter(username=username)
        if not token_query:
            raise AuthenticationFailed('username不存在')
        return (username,auth[1])