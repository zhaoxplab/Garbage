import mysql.connector
import time

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='cy'
)
cursor = mydb.cursor()

def shaixuan():
    for p in range(1, 15):
        sql = "select 红汤绝配 from zj where 就餐人数={}"
        sqls = sql.format(p)
        cursor.execute(sqls)
        c = cursor.fetchall()
        # print(c)
        peo = len(c) * p
        l = []
        for b in c:
            # print(b)
            i = b[0].split(',')
            for j in i:
                l.append(j)
        num = len(l)
        org = num / peo
        print('人数: ', p, org)

def zhanbi():
    for p in range(1, 15):

        sql = "select 红汤绝配 from zj where 就餐人数={}"
        sqls = sql.format(p)
        cursor.execute(sqls)
        c = cursor.fetchall()
        # print(len(c))
        zb = len(c) / 5591
        print(zb)

if __name__ == '__main__':
    zhanbi()