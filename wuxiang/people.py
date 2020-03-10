import requests
import urllib
import random
import time
import json
import csv
from wuxiang.Modular import imitate_login

session = imitate_login()

def shop_id(beginTime, endTime):
    shop_u = 'https://cy.wuuxiang.com/cy7center/canyin/report/common/rptcommon/shops'
    # post请求没有值，就是这样的
    p_info = {"searchName": "", "ifShowDeleted": ""}
    shop_info = session.post(shop_u, data=json.dumps(p_info)).json()
    # print(shop_info)
    # 表类型
    func = input('1:营业额，2:客流量，3:人均，4:开台数，5:开台数占比\n')
    if func == '1':
        types = 'origTotal'
    elif func == '2':
        types = 'peopleQty'
    elif func == '3':
        types = 'avg'
    elif func == '4':
        types = 'count'
    elif func == '5':
        types = 'rate'
    else:
        print('重新输入')
    for info in shop_info:
        # print(info)
        # shopid是门店id，shopname是门店名称
        shopId = info['columnID']
        shopName = info['columnName']
        body = {
            "mngType": "",
            "dateType": "",
            "beginDate": beginTime,
            "beginTime": "10:00",
            "endDate": endTime,
            "endTime": "10:00",
            "shift": "",
            "week": "",
            "city": "",
            "brand": "",
            "shop": shopId,
            "curEmp": "赵翔鹏",
            "curShop": "河南巴庄餐饮管理有限公司",
            "cityNames": "",
            "shopNames": shopName
        }
        # dict转str，data进行encede
        db = json.dumps(body)
        da = urllib.parse.quote(db)
        # print(type(da), da)

        # 二级请求
        url = 'https://cy.wuuxiang.com/cy7center/canyin/report/a23/a23?_dc={0}&reportType=&DIMProperty=&data={1}&formCode=03020102&page=1&start=0&limit=25'
        dc = int(time.time() * 1000)
        link = url.format(dc, da)
        # print(link)
        time.sleep(0.3)
        res = session.get(link).json()
        # print(res)
        type_l = [shopName, ]
        if len(res['root']):
            for p in range(0, len(res['root'])):
                """
                0: 1~2，1: 3~4，2: 5~6，3: 7~8，4: 9~12，5: 13~
                origTotal:营业额，peopleQty:客流量，avg:人均，count:开台数，rate:开台数占比
                """
                if types == 'rate':
                    type_l.append(str(res['root'][p][types])+'%')
                else:
                    type_l.append(res['root'][p][types])
            print(type_l)
        write_csv(types, type_l)


def write_csv(types, type_l):
    # newline的作用是防止每次插入都有空行
    with open('data/'+types+'.csv', 'a+', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 以读的方式打开csv 用csv.reader方式判断是否存在标题
        with open('data/'+types+'.csv', 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            if not [row for row in reader]:
                writer.writerow(['店面', '1 ~ 2', '3 ~ 4', '5 ~ 6', '7 ~ 8', '9 ~ 12', '13~'])
                writer.writerow(type_l)
            else:
                writer.writerow(type_l)


if __name__ == '__main__':
    # 时间日期示例 '2019-09-17'
    beginTime = "2018-5-01"
    endTime = "2018-5-23"
    shop_id(beginTime=beginTime, endTime=endTime)