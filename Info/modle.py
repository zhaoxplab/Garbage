import mysql.connector
import time
import json
from collections import Counter

import csv

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='cy'
)
cursor = mydb.cursor()
# 红汤绝配
Ht = ['巴庄脆毛肚', '本色千层肚', '鲜切牛上脑', '德清虾滑', '无骨鲜鸭掌', '巴庄鲜鸭血', '冰鲜鸭肠', '藤椒小酥肉',
      '天然黑豆面筋', '富硒紫薯川粉', '鲜打牛肉丸']
# 酒水
Js = ['牛栏山陈酿42°500ML', '江小白100ML', '江小白300ML', '劲酒125ML', '百威啤酒', '青岛崂山', '青岛纯生', '青岛经典',
      '金桔茉莉', '红柚乳酸菌', '秘制青梅汁', '蔓越莓绿茶', '桂花布丁奶',
      '果粒橙1.25L', '加多宝', '可乐听装330ml', '雪碧听装330ml', '花花牛酸奶', '椰冻爽',
      '农夫山泉', '皮带面', '绿豆面', '方便面', '水果拼盘', '香油蒜泥', '麻酱', '餐巾纸']
# 锅底
Gd = ['牛油辣+野山菌汤+骨汤', '青椒辣+野山菌汤+骨汤', '番茄+牛油辣+野山菌汤']
# 赠送相关
Zs = ['新版小料', '长寿面', '芙蓉蛋', '辣椒圈']

def Fl():
    for p in range(1, 15):
        # 这个是啥来着
        c_li = []
        p2 = "select 消费明细,消费金额 from cpd where 就餐人数={} and 消费明细 like '%野山菌汤%'".format(p)
        cursor.execute(p2)
        info = cursor.fetchall()
        print(p, len(info))
        # for index.html, i in zip(range(0, len(info)), info[0]):
        for i in info:
            mx = json.loads(i[0])
            # all,这个是点的菜
            dl = []
            # 菜品
            i_l = []
            for k in mx['cp']:
                # print(k.keys())
                i_l.append(list(k.keys())[0])
            # print(i_l)
            # 剔除酒水什么的, 差集
            dl = list(set(i_l).difference(set(Js), set(Gd), set(Zs)))
            # print(dl)
            # 红汤绝配交集
            ret = list(set(dl).intersection(set(Ht)))
            # print(ret)
            r = ','.join(ret)
            ot = list(set(dl).difference(set(ret)))
            # print(ot)
            o = ','.join(ot)
            # print(o)
            sql = "insert into zj(就餐人数, 消费金额, 红汤绝配数, 全部菜品数, 红汤绝配, 其他) values({0},{1},{2},{3},'{4}','{5}')"
            if len(ret):
                # print('%s人台,%s个红汤绝配,红汤绝配占比%s,占所点菜品%s' % (p, len(ret), (len(ret)/len(Ht) *100), len(ret)/len(dl)))
                cursor.execute(sql.format(p, i[1], len(ret), len(dl), r, o))
                mydb.commit()
            else:
                cursor.execute(sql.format(p, i[1], 0, len(dl), r, o))
                mydb.commit()
                # print('%s人台,%s个红汤绝配,红汤绝配占比%s,占所点菜品%s' % (p, 0, 0, 0))
            # 个数、占比

            #     d = {index.html: mx['cp']}
            #     # print(d)
            #     c_li.append(d)
            # ss = {p: c_li}
            # print(ss)

def count():
    for p in range(1, 15):
        hl =[]
        ql = []
        sql1 = "select 红汤绝配 from zj where 就餐人数={}"
        sql2 = "select 其他 from zj where 就餐人数={}"
        sql3 = "select 消费金额 from zj where 就餐人数={}"
        cursor.execute(sql1.format(p))
        a = cursor.fetchall()
        cursor.execute(sql2.format(p))
        b = cursor.fetchall()
        cursor.execute(sql3.format(p))
        c = cursor.fetchall()
        for i, j in zip(a, b):
            h = i[0].split(',')
            q = j[0].split(',')
            # print(h, q)
            for x, y in zip(h, q):
                hl.append(x)
                ql.append(y)
        # print(ql)
        result1 = Counter(hl).most_common()
        result2 = Counter(ql).most_common()
        print(result2)
        for r1 in result1:
            hName, hNum = r1[0], r1[1]
            rowt = [p, hName]
            rowz = [len(c), hNum]
            with open('ht.csv', 'a', encoding='utf8')as f:
                f_csv = csv.writer(f)
                f_csv.writerow(rowt)
                f_csv.writerow(rowz)
        for r2 in result2:
            qName, qNum = r2[0], r2[1]
        # for r1, r2 in zip(result1, result2):
        #     hName, hNum = r1[0], r1[1]
        #     qName, qNum = r2[0], r2[1]
            # print(p, len(c), hName, hNum, qName, qNum)
            row1 = [p, qName]
            row2 = [len(c), qNum]
            with open('qt.csv', 'a', encoding='utf8')as f:
                f_csv = csv.writer(f)
                f_csv.writerow(row1)
                f_csv.writerow(row2)


if __name__ == '__main__':
    count()