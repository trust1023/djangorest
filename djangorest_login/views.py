from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView
from .ser import CreateUser,UserInfoSer
from .models import User
from .jwtMiddleware import TokenAuth
# Create your views here.

class UserRegister(CreateAPIView):
    serializer_class = CreateUser

class UserLogin(APIView):
    def post(self,request):
        data = request.data
        username = data.get('username')
        pwd = data.get('password')
        if not all([username,pwd]):
            return Response({'msg':'参数不完整','code':400})
        user = User.objects.get(username=username)
        user.check_pwd(pwd)
        res = {'msg': 'success', 'code': 200,'token':user.token}
        res['data'] = UserInfoSer(user).data
        return Response(res)


class UserinfoList(ListAPIView):
    authentication_classes = [TokenAuth]
    serializer_class = UserInfoSer
    queryset = User.objects.all()


