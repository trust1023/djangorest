import operator
import pymongo
import pandas as pd
from io import BytesIO
from urllib.parse import quote
import time

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from djangorest import settings
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .ser import ProductSerializer
from rest_framework.generics import ListAPIView
import django_filters
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework_extensions.cache.decorators import cache_response
# Create your views here.

class MyPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 5
    page_query_param = 'page'
    #page_size_query_param = 'size'

class Mydplist(APIView):
    '''
    分页
    '''
    #@cache_response(timeout=60)  # 分页不缓存,否则无论第几页都是第一页的数据
    def get(self,request):
        host = settings.myhost
        user = settings.pymongo_user
        password = settings.pymongo_pwd
        client = pymongo.MongoClient(host=host)
        db = client.test
        db.authenticate(user, password)
        collection = db['dianping_shop__changsha']
        data = collection.find()[:100]
        shop_list = [{'shopid':each['shopid'],'shop_name':each['shop_name']} for each in list(data)]
        page = MyPagination()
        page_roles = page.paginate_queryset(queryset=shop_list, request=request, view=self)
        #print(page_roles)
        result = {'msg': '成功', 'code': 200, 'data': page_roles}
        #roles_ser = MySer(instance=page_roles,many=True)
        #return Response(result)  # 只返回数据
        return page.get_paginated_response(result)
        #return page.get_paginated_response(roles_rer.data)
        #return Response({'msg': '成功', 'code': 200, 'data': shop_list})

class ProductFilter(django_filters.rest_framework.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    # 行为: 名称中包含某字符，且字符不区分大小写
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['name', 'is_hot', 'min_price', 'max_price','category']

class Myproudctlist(ListAPIView):
    '''
    搜索，过滤，排序
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filter_class = ProductFilter
    search_fields = ('name','category')
    ordering_fields = ('price',) #http://127.0.0.1:8000/api/myfilter/?ordering=-price




class Myfind(APIView):
    '''
    get参数查询 过滤 排序
    eg:http://127.0.0.1:8000/api/myfind/?cat_name=面包甜点&business_name=新民路
    '''
    def get(self,request):
        filter_fields = ['cat_name','region_name','business_name']
        ordering_fields = ['review_count', 'shopid']
        print(request._request.GET)
        params = request._request.GET
        query = dict()
        for ff in filter_fields:
            if params.get(ff):
                query[ff] = params.get(ff)
        host = settings.myhost
        user = settings.pymongo_user
        password = settings.pymongo_pwd
        client = pymongo.MongoClient(host=host)
        db = client.test
        db.authenticate(user, password)
        collection = db['dianping_shop__changsha']
        data = collection.find(query)[:10]
        shop_list = [{'shopid': each['shopid'], 'shop_name': each['shop_name'], 'region_name': each['region_name'],
                      'cat_name': each['cat_name'],'business_name':each['business_name'],'review_count':each['review_count']} for each in list(data)]
        # sl = sorted(shop_list,key=operator.itemgetter('shopid'))
        # slf = sorted(sl,key=operator.itemgetter('review_count'))
        for orderf in ordering_fields[::-1]:
            shop_list = sorted(shop_list,key=operator.itemgetter(orderf))
        return Response({'code': 200, 'msg': '成功', 'data': shop_list})

class Myexcel(APIView):
    '''
    excel下载
    get参数查询结果生成excel
    '''
    def get(self,request):
        filter_fields = ['cat_name', 'region_name', 'business_name']
        params = request._request.GET
        query = dict()
        for ff in filter_fields:
            if params.get(ff):
                query[ff] = params.get(ff)
        host = settings.myhost
        user = settings.pymongo_user
        password = settings.pymongo_pwd
        client = pymongo.MongoClient(host=host)
        db = client.test
        db.authenticate(user, password)
        collection = db['dianping_shop__changsha']
        data = collection.find(query)[:100]
        shop_list = [{'shopid': each['shopid'], 'shop_name': each['shop_name'], 'region_name': each['region_name'],
                      'cat_name': each['cat_name'], 'business_name': each['business_name'],
                      'review_count': each['review_count']} for each in list(data)]
        df = pd.DataFrame(shop_list)
        out = BytesIO()
        writer = pd.ExcelWriter(out)
        df.to_excel(excel_writer=writer, index=False, sheet_name='part1')
        writer.save()
        now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        filename = '测试数据'
        ff = 'attachment;filename=' + quote(filename) + now_time + '.xlsx'
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = ff  # 'attachment;filename=test201910121810.xlsx'
        print(response['Content-Disposition'])
        response.write(out.getvalue())
        # print(out.getvalue())
        return response

