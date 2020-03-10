import mysql.connector
import time

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='cy'
)

sql1 = "select * from cp"
sql2 = "insert ignore into cpd(就餐人数,消费金额,bsId,tsId,消费明细) values({0},{1},'{2}','{3}','{4}')"

st = time.time()
cursor = mydb.cursor()
cursor.execute(sql1)
f = cursor.fetchall()
for i in f:
    # print(i)
    cursor.execute(sql2.format(i[1], i[3], i[4], i[5], i[6]))
    mydb.commit()
et = time.time()

print(et-st)