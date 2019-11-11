#执行定时查询数据发送邮件任务
import pymongo
from djangorest.celery import app
from djangorest import settings
from .utils import send_email
import pymysql
import time



@app.task
def tsend_email():
    print('start')
    dbs = pymysql.connect(host=settings.myhost, user=settings.mysql_user, password=settings.mysql_pwd, port=3306, db=settings.mysql_db)
    cursor = dbs.cursor()
    today = time.strftime('%Y-%m-%d',time.localtime())
    sql = 'select city from soldtable where sold>100 and date=%s'
    cursor.execute(sql,(today,))
    data = cursor.fetchall()
    print('data is',data)
    city_list = []
    for city in data:
        print(city)
        city_list.append(city[0])
    send_email('今天销量超过100w的城市有%s'%str(city_list))
