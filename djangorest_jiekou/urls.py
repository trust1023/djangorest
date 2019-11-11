from django.urls import path
from .views import *

urlpatterns = [path('myfilter/',Myproudctlist.as_view()),
path('myfind/',Myfind.as_view()),
path('myexcel/',Myexcel.as_view()),
path('mydplist/',Mydplist.as_view()),
               ]