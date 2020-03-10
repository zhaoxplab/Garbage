import urllib
import random
import time
import pandas as pd
import json
import mysql.connector
import csv
from wuxiang.Modular import imitate_login

sessions = imitate_login()


def date():
    months = 10
    for month in range(1, months):
        beginTime = '2019-{}-01'.format(month)
        endTime = '2019-{}-01'.format(month+1)
        # print(start_month, end_month)
        get_all(beginTime, endTime)
    pass


def get_all(beginTime, endTime):
    url = 'https://cy.wuuxiang.com/cy7center/canyin/report/a03/a03?_dc={0}&reportType=ShopDms&DIMProperty=shopDms&data={1}&formCode=03010106&page=1&start=0&limit=100'
    b = {"mngType": "",
         "dateType": "",
         "dateInterval": "",
         "beginDate": beginTime,
         "beginTime": "10:00",
         "endDate": endTime,
         "endTime": "10:00",
         "shift": "",
         "week": "",
         "timeType": 1,
         "sellType": [1],
         "pointType": "",
         "discounted": "false",
         "isMissShift": "false",
         "isIncludePresent": "on",
         "newShopType": "",
         "isUseStd": "false",
         "remark": "",
         "city": "",
         "brand": "",
         "shop": "",
         "areas": "",
         "pos": "",
         "curEmp": "赵翔鹏",
         "curShop": "河南巴庄餐饮管理有限公司",
         "cityNames": "",
         "shopNames": ""}
    # dict转str，data进行encede
    db = json.dumps(b)
    da = urllib.parse.quote(db)
    ts = int(time.time() * 1000)
    link = url.format(ts, da)
    res = sessions.get(link).json()
    # print(res['root'])
    if len(res['root']):
        for info in res['root']:
            # print(info)
            recType = info['recType']
            YearMonth = beginTime[:-3]
            bsOrigMoney = info['bsOrigMoney']
            bsIncomeMoney = info['bsIncomeMoney']
            bsCount = info['bsCount']
            peopleQty = info['peopleQty']
            avgTable = info['avgTable']
            avgPeople = info['avgPeople']
            openRate = info['openRate'] / 100
            peopleRate = info['peopleRate'] / 100
            avgTime = info['avgTime']
            remove = recType + '-' + YearMonth
            # print(recType, YearMonth, bsOrigMoney, bsIncomeMoney, bsCount, avgTable, avgPeople, openRate, peopleRate, avgTime, remove)
            sql = """
            INSERT IGNORE INTO MonthTurnover (
            门店,年和月,营业额,纯收金额,开台数,客流量,桌均,人均,开台率,上座率,平均就餐时间,去重判断
            ) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')
            """
            # print(sql)
            cursors.execute(sql.format(recType, YearMonth, bsOrigMoney, bsIncomeMoney, bsCount, peopleQty, avgTable, avgPeople, openRate, peopleRate, avgTime, remove))
            dbConnect.commit()
            time.sleep(1)


if __name__ == '__main__':
    dbConnect = mysql.connector.connect(
        host='47.97.166.98',
        user='root',
        password='100798',
        database='wuxiang'
    )
    cursors = dbConnect.cursor()
    date()
    print('success')
