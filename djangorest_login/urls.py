from django.urls import path
from .views import *

urlpatterns = [path('register/',UserRegister.as_view()),
               path('login/',UserLogin.as_view()),
    path('info/', UserinfoList.as_view({'get':'list'})),
               path('sns/',sns),
               path('loadtest/',loadtest),
               ]