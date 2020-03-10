import mysql.connector
import time

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='cy'
)
cursor = mydb.cursor()

def renjun():
    for p in range(1, 15):
        sql = "select 消费金额 from zj where 就餐人数={}"
        sqls = sql.format(p)
        cursor.execute(sqls)
        c = cursor.fetchall()
        # print(len(c))
        m_all = 0
        for m in c:
            # print(type(m[0]))
            m_all += m[0]
        # print(m_all)
        # print(p*len(c))
        rj = m_all / (len(c)*p)
        # print(rj)
        b = round(float(len(c)/5591 *100), 2)
        print(str(p) + '人就餐, 数量:' + str(len(c))+'台, 占比:' + str(b)+'%, 人均: ' + str(int(rj)))


if __name__ == '__main__':
    renjun()