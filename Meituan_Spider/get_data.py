import csv
import json
import mysql.connector
from xpinyin import Pinyin

pinyin = Pinyin()

db_connect = mysql.connector.connect(
    host='47.97.166.98',
    user='root',
    password='100798',
    database='Meituan'
)
cursor = db_connect.cursor()


def group_buy(city, area, cla):
    sql = 'select 店铺名称,人均,评分,美食类别,团购优惠 from {} where 区域 like "%{}%" and 美食类别 like "%{}%"'.format(pinyin.get_pinyin(city, ''), area, cla)
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    print('查询结果: ', len(data))
    for d in data:
        # print(d)
        n = d[0]
        avg = d[1]
        p = d[2]
        l = d[3]
        sl = []
        t = json.loads(d[4])
        # print(t)
        for x in t['dealList']:
            # print(x['soldNum'])
            sl.append(x['soldNum'])
        s = sum(sl)
        # print(n, avg, p, l, s)
        dl = [n, avg, p, l, s]
        wr(dl)
    pass


def wr(dl):
    # newline的作用是防止每次插入都有空行
    with open('汤阴.csv', 'a+', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 以读的方式打开csv 用csv.reader方式判断是否存在标题
        with open('汤阴.csv', 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            if not [row for row in reader]:
                writer.writerow(['店铺名称', '人均', '评分', '美食类别', '团购销量'])
                writer.writerow(dl)
            else:
                writer.writerow(dl)


if __name__ == '__main__':
    group_buy(city='安阳', area='汤阴', cla='')
    pass
