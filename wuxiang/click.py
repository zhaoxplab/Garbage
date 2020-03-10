import urllib
import random
import time
import pandas as pd
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
    func = input('1:销售数量，2:点击率，3:实收金额\n')
    if func == '1':
        types = 'lastQty'
    elif func == '2':
        types = 'rate'
    elif func == '3':
        types = 'grossProfit'
    else:
        print('重新输入')
    for info in shop_info[13:]:
        # print(info)
        # shopid是门店id，shopname是门店名称
        shopId = info['columnID']
        shopName = info['columnName']
        body = {
            "mngType": "",
            "dateType": "",
            "dateInterval": "",
            "beginDate": beginTime,
            "beginTime": "10:00",
            "endDate": endTime,
            "endTime": "10:00",
            "shift": "",
            "week": "",
            "itemType": 10,
            "isMergeBySize": "false",
            "isIncludePresent": "on",
            "isOnlyIncludePack": "false",
            "isNotIncludePack": "false",
            "sellType": [1],
            "deFrom": "",
            "city": "",
            "brand": "",
            "shop": shopId,
            "itemBigClass": "345100000000000209",
            "itemSmallClass": "",
            "items": "",
            "areas": "",
            "curEmp": "赵翔鹏",
            "curShop": "河南巴庄餐饮管理有限公司",
            "cityNames": "",
            "shopNames": shopName
        }
        # ————————————————————————————————————————————————————————————————————————————————————————————————
        url = 'https://cy.wuuxiang.com/cy7center/canyin/report/a25/a25?_dc={0}&reportType=&DIMProperty=&data={1}&formCode=03020601&page=1&start=0&limit=25'
        # 生成_dc，时间戳 + 3位数字
        num = random.randint(100, 999)
        dc = str(int(time.time())) + str(num)
        # dict转str，urlencode转换
        da = urllib.parse.quote(json.dumps(body))
        link = url.format(dc, da)
        time.sleep(0.3)
        res = session.get(link).json()
        type_l = [shopName, ]
        type_d = {}
        red_l = ['无骨鲜鸭掌', '德清虾滑', '巴庄脆毛肚', '富硒紫薯川粉', '巴庄鲜鸭血', '冰鲜鸭肠', '藤椒小酥肉', '天然黑豆面筋', '鲜切牛上脑', '本色千层肚', '鲜打牛肉丸']
        if len(res['root']):
            type_d['门店'] = shopName
            """
            自我实现的沙雕算法，实现销量为0菜品的处理，
            首先用返回数据与红汤绝配的元素对比，如果返回元素在list里，那么返回元素的价格就是它的值，反之值则为0
            """
            '''
            # dict
            for i in res['root']:
                for red in red_l:
                    # print(red, i, red_l)
                    if red == i['name']:
                        type_d[i['name']] = i[types]
                        red_l.remove(red)
                        # print(red_l)
                        break
                    else:
                        type_d[red] = None
            print(type_d)
            '''
            for i in res['root']:
                for red in red_l:
                    # print(red, i, red_l)
                    if red == i['name']:
                        # type_d[i['name']] = i[types]
                        red_l.remove(red)
                        # print(red_l)
                        if types == 'rate':
                            type_l.append(str(i[types])+'%')
                        else:
                            type_l.append(i[types])
                        break
                    else:
                        # type_d[red] = None
                        type_l.append(None)
            print(type_l)
            # write_csv(types, type_l)

def write_csv(types, type_l):
    # newline的作用是防止每次插入都有空行
    with open('red/' + types + '.csv', 'a+', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 以读的方式打开csv 用csv.reader方式判断是否存在标题
        with open('red/' + types + '.csv', 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            if not [row for row in reader]:
                writer.writerow(['门店', '无骨鲜鸭掌', '德清虾滑', '巴庄脆毛肚', '富硒紫薯川粉', '巴庄鲜鸭血', '冰鲜鸭肠', '藤椒小酥肉', '天然黑豆面筋', '鲜切牛上脑', '本色千层肚', '鲜打牛肉丸'])
                writer.writerow(type_l)
            else:
                writer.writerow(type_l)

def wr(types, type_d):
    header = ['门店', '无骨鲜鸭掌', '德清虾滑', '巴庄脆毛肚', '富硒紫薯川粉', '巴庄鲜鸭血', '冰鲜鸭肠', '藤椒小酥肉', '天然黑豆面筋', '鲜切牛上脑', '本色千层肚', '鲜打牛肉丸']
    with open('data/'+types+'.csv', 'a+', encoding='utf-8', newline='') as csvfile:
        w = csvfile.DictWrite
        df = pd.DataFrame.from_dict(type_d, orient='index.html').T.to_csv(types+'.csv', mode='a+', index=False, index_label=False)
        print(df)
        pass

if __name__ == '__main__':
    # 时间日期示例 '2019-09-17'
    beginTime = "2019-10-01"
    endTime = "2019-10-23"
    shop_id(beginTime=beginTime, endTime=endTime)