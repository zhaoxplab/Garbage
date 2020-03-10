import time
import json
import re
import ast
import random

str = '[{"discFlg":0,"price":45.0000,"lastQty":1.0000,"discScale":1.0000,"unitName":"份","name":"牛油辣+野山菌汤+骨汤","code":"010101","lastSubtotal":45.0000},{"discFlg":0,"price":5.0000,"lastQty":1.0000,"discScale":1.0000,"unitName":"份","name":"香油蒜泥","code":"020201","lastSubtotal":5.0000},{"discFlg":0,"price":45.0000,"lastQty":1.0000,"discScale":1.0000,"unitName":"份","name":"巴庄脆毛肚","code":"030312","lastSubtotal":45.0000},{"discFlg":0,"price":35.0000,"lastQty":0.5000,"discScale":1.0000,"unitName":"份","name":"无骨鲜鸭掌","code":"030310","lastSubtotal":17.0000},{"discFlg":0,"price":19.0000,"lastQty":1.0000,"discScale":1.0000,"unitName":"份","name":"富硒紫薯川粉","code":"030313","lastSubtotal":19.0000},{"discFlg":0,"price":42.0000,"lastQty":1.0000,"discScale":1.0000,"unitName":"份","name":"极品肥牛","code":"040402","lastSubtotal":42.0000},{"discFlg":0,"price":29.0000,"lastQty":1.0000,"discScale":1.0000,"unitName":"份","name":"乌鸡卷","code":"040407","lastSubtotal":29.0000},{"discFlg":0,"price":26.0000,"lastQty":0.5000,"discScale":1.0000,"unitName":"份","name":"鲜脑花","code":"040408","lastSubtotal":13.0000},{"discFlg":0,"price":10.0000,"lastQty":0.5000,"discScale":1.0000,"unitName":"份","name":"茼蒿","code":"050514","lastSubtotal":5.0000},{"discFlg":1,"price":5.0000,"lastQty":2.0000,"discScale":1.0000,"unitName":"份","name":"椰冻爽","code":"081474","lastSubtotal":0.0000},{"discFlg":0,"methodText":"冰镇","price":3.0000,"lastQty":1.0000,"discScale":1.0000,"unitName":"听","name":"可乐听装330ml","code":"081267","lastSubtotal":3.0000},{"discFlg":0,"price":5.0000,"lastQty":1.0000,"discScale":1.0000,"unitName":"份","name":"麻酱","code":"020202","lastSubtotal":5.0000}]'

s = re.findall(r'({.*?})', str)
print(s)
for i in s:
    print(i)
    d = ast.literal_eval(i)
    print(type(d))
    print(d['name'])

