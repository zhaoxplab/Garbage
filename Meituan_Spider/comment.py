import requests
import csv
import urllib
import json
import re
import mysql.connector
import urllib3
import time
from fake_useragent import UserAgent
urllib3.disable_warnings()

ua = UserAgent()
session = requests.session()

c = '_ci=245; rvct=245%2C1; uuid=3d485720-25d8-4929-9ef8-494a8f7b6fe4'
p = {'https': 'https://60.13.42.3:9999'}


def print_url(poi, u):
    head = {'Host': 'www.meituan.com',
            'User-Agent': ua.random,
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://www.meituan.com/meishi/{0}/'.format(poi),
            'Cookie': c.format(u),
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
            }
    url = 'https://www.meituan.com/meishi/api/poi/getMerchantComment?uuid={0}&platform=1&partner=126&originUrl=https://www.meituan.com/meishi/{1}/&riskLevel=1&optimusCode=10&id={2}&offset={3}&pageSize=20&sortType=1'
    page = 0
    x = 1100
    while x:
        page += 1
        offset = (page - 1) * 20
        link = url.format(u, poi, poi, offset)
        print(link)
        get(link, head)
        x -= 1


def get(link, head):
    response = session.get(link, headers=head).json()
    # print(response)
    if len(response['data']['comments']):
        for comment_info in response['data']['comments']:
            userId = comment_info['userId']
            username = comment_info['userName']
            avgPrice = comment_info['avgPrice']
            star = comment_info['star']
            menu = comment_info['menu']
            comment = comment_info['comment']
            commentTime = comment_info['commentTime']
            commentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(commentTime)/1000))
            comments = [userId, username, avgPrice, star, menu, comment, commentTime, commentTime]
            wr(comments)
    else:
        print('OVER')


def wr(comments):
    # newline的作用是防止每次插入都有空行
    with open('data/' + str(poi) + '.csv', 'a+', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 以读的方式打开csv 用csv.reader方式判断是否存在标题
        with open('data/' + str(poi) + '.csv', 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            if not [row for row in reader]:
                writer.writerow(['用户Id', '用户名', '平均', '评分', '套餐', '评价', '时间戳', '标准时间'])
                writer.writerow(comments)
            else:
                writer.writerow(comments)



if __name__ == '__main__':
    poi = 164591091
    u = '3d485720-25d8-4929-9ef8-494a8f7b6fe4'
    print_url(poi=poi, u=u)