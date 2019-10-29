import random

def getCode():
    codeList = [i for i in range(10)]
    m = ''
    for _ in range(4):
        x = random.choice(codeList)
        m += str(x)
    return m

def sendSns(code):
    #短信验证码平台发送
    pass