import mysql.connector
import re

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='test'
)

cursor = mydb.cursor()
city_list = []
def read():
    with open('.\ci.txt', newline="", encoding='utf-8')as f:
        print(f)
        for x in f:
            city = x.split(',')
            return city

def select():
    city_list = read()
    sql = "select * from c_info where 名称 like '%{}%'"
    for city in city_list:
        # print(city)
        # print(sql.format(city))
        cursor.execute(sql.format(city))
        c_info = cursor.fetchall()
        # print(c_info)
        for info in c_info:
            print(info)


if __name__ == '__main__':
    select()