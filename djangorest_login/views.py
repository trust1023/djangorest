from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView
from .ser import CreateUser,UserInfoSer,MySer
from .models import User,Code
from .jwtMiddleware import TokenAuth,MyAuthentication
from .validate import validate_mobile
from .utils import getCode,sendSns
import datetime
from django.http.response import JsonResponse
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
import pymongo
from django.views.decorators.cache import cache_page
from rest_framework_extensions.cache.decorators import cache_response
from djangorest import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from .throttle import NormalThrottle, UserThrottle
from .permi import ViPPermission
import os
import json
# Create your views here.




class UserRegister(CreateAPIView):
    serializer_class = CreateUser

class UserLogin(APIView):
    def post(self,request):
        data = request.data
        username = data.get('username')
        pwd = data.get('password')
        if not all([username,pwd]):
            return Response({'msg':'参数不完整','code':401})
        user = User.objects.get(username=username)
        if not user.check_pwd(pwd):
            return Response({'msg': '密码错误', 'code': 401})
        res = {'msg': 'success', 'code': 200,'token':user.token}
        res['data'] = UserInfoSer(user).data
        return Response(res)


#class UserinfoList(ListAPIView):
class UserinfoList(CacheResponseMixin,ListModelMixin,GenericViewSet):
    authentication_classes = [TokenAuth]
    serializer_class = UserInfoSer
    queryset = User.objects.all()

@api_view(['POST'])
def sns(request):
    mobile = request.POST.get('mobile')
    if not mobile:
        return JsonResponse({'msg':'参数不完整','code':401})
    if not validate_mobile(mobile):
        return JsonResponse({'msg':'手机号不正确','code':401})
    user = User.objects.filter(mobile=mobile).first()
    if user:
        return JsonResponse({'msg':'该手机号已注册','code':401})
    snscode = getCode()
    codeUser = Code.objects.filter(mobile=mobile).first()
    if not codeUser:
        Code.objects.create(mobile=mobile,code=snscode)
    else:
        # 验证码发送频率
        one_minute_age = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1, seconds=0)
        print(one_minute_age)
        if Code.objects.filter(add_time__gt=one_minute_age, mobile=mobile).count():
            return JsonResponse({'msg': '请一分钟后再发送', 'code': 401})
        else:
            codeUser.code = snscode
            codeUser.save()
    sendSns(snscode)
    return Response({'msg': '验证码已发送', 'code': 200})


@cache_page(timeout=60)
@api_view(['GET'])
def loadtest(request):
    '''
    测试数据接口，测试负载
    :param request:
    :return:
    '''
    host = settings.myhost
    user = settings.pymongo_user
    password = settings.pymongo_pwd
    client = pymongo.MongoClient(host=host)
    db = client.test
    db.authenticate(user, password)
    collection = db['city_list']
    data = collection.find()
    city_list = [each['city'] for each in list(data)]
    return Response({'msg': '成功', 'code': 200,'data':city_list})

class Mytest(APIView):
    authentication_classes = [MyAuthentication]
    throttle_classes = [NormalThrottle, UserThrottle]
    def get(self,request):
        return Response({'code':200,'msg':'测试'})

class VipList(APIView):
    authentication_classes = [TokenAuth]
    permission_classes = [ViPPermission]
    def get(self,request):
        host = settings.myhost
        user = settings.pymongo_user
        password = settings.pymongo_pwd
        client = pymongo.MongoClient(host=host)
        db = client.test
        db.authenticate(user, password)
        collection = db['city_list']
        data = collection.find()
        city_list = [each['city'] for each in list(data)]
        return Response({'msg': '成功', 'code': 200, 'data': city_list})





