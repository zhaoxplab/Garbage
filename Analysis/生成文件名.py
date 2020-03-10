import os
import shutil
import mysql.connector

# for s in r:
#     shutil.copy('./old/four_B.xls', './old/{0}.xls'.format(s[0]))



db_connect = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='Work'
)
cursors = db_connect.cursor()
cursors.execute('select 门店 from 门店')
read = cursors.fetchall()
for hh in read:
    shutil.copy('./data/模板.xls', './old/{0}.xls'.format(hh[0]))

