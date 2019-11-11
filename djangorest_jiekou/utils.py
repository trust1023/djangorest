import yagmail
import time
from djangorest.settings import email_host,email_user,email_pwd

def send_email(context):
    while 1:
        try:
            yag = yagmail.SMTP(user=email_user, password=email_pwd, host=email_host)
            contents = [context]
            yag.send(email_host, '测试发送', contents)
            break
        except Exception as e:
            print(e.args)
            time.sleep(5)