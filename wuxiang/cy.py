import re
import requests
import mysql.connector
import json
from fake_useragent import UserAgent

ua = UserAgent()
url = 'https://cy.wuuxiang.com/cy7center/canyin/report/'

data = {"mngType":"",
        "dateType":"",
        "dateInterval":"",
        "beginDate":"2019-08-05", "beginTime":"10:00",
        "endDate":"2019-08-12", "endTime":"10:00",
        "shift":"","week":"","sellType":"","pointType":"","invoiceState":"",
        "isOnlyRenew":"false","settleState":"false",
        "dept":"",
        "city":"150","brand":"","shop":"10970","areas":"","pos":"","payway":"","paywayType":"","operator":"",
        "curEmp":"\u8d75\u7fd4\u9e4f",
        "curShop":"\u6cb3\u5357\u5df4\u5e84\u9910\u996e\u7ba1\u7406\u6709\u9650\u516c\u53f8",
        "cityNames":"\u6d1b\u9633\u5e02",
        "shopNames":"\u5b9c\u9633\u5e97"}

u = 'https://cy.wuuxiang.com/cy7center/canyin/report/a10lv1/a10?type=detail&_dc=1565946540122&data=%7B%22mngType%22%3A%22%22%2C%22dateType%22%3A%22thisYear%22%2C%22dateInterval%22%3A%22%22%2C%22beginDate%22%3A%222019-01-01%22%2C%22beginTime%22%3A%2210%3A00%22%2C%22endDate%22%3A%222020-01-01%22%2C%22endTime%22%3A%2210%3A00%22%2C%22shift%22%3A%22%22%2C%22week%22%3A%22%22%2C%22sellType%22%3A%22%22%2C%22pointType%22%3A%22%22%2C%22invoiceState%22%3A%22%22%2C%22city%22%3A%22150%22%2C%22brand%22%3A%22%22%2C%22shop%22%3A%2210970%22%2C%22areas%22%3A%22%22%2C%22pos%22%3A%22%22%2C%22payway%22%3A%22%22%2C%22paywayType%22%3A%22%22%2C%22curEmp%22%3A%22%5Cu8d75%5Cu7fd4%5Cu9e4f%22%2C%22curShop%22%3A%22%5Cu6cb3%5Cu5357%5Cu5df4%5Cu5e84%5Cu9910%5Cu996e%5Cu7ba1%5Cu7406%5Cu6709%5Cu9650%5Cu516c%5Cu53f8%22%2C%22cityNames%22%3A%22%5Cu6d1b%5Cu9633%5Cu5e02%22%2C%22shopNames%22%3A%22%5Cu5b9c%5Cu9633%5Cu5e97%22%7D&lv=2&DIMProperty=shopDms&paramId=10970&page=3&start=50&limit=25'

c = 'isNewVersion=0; JSESSIONID=6FAD6C6EB6395380E72337E0AAAEFB8B; sessionid=6FAD6C6EB6395380E72337E0AAAEFB8B; loginedShopId=; loginedUsername=; success=true; UM_distinctid=16b987d692e74-06df07ec012f44-37c143e-144000-16b987d692f4cd; CNZZDATA1275514722=1671585256-1561631485-null%7C1566192536'

coo = {
}

head = {'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': c,
        'Host': 'cy.wuuxiang.com',
        'Referer': 'https://cy.wuuxiang.com/cy7center/canyin/report/',
        'User-Agent': ua.random,
        'X-Requested-With': 'XMLHttpRequest'
        }

def first():
    res = requests.get(u, headers=head).text
    if len(res):
        detail = json.loads(res)
        for i in detail['root']:
            # print(i)
            # print(i['bsId'], i['tsId'], i['dinnerType'], i['peopleQty'], i['origTotal'])
            peopleQty = i['peopleQty']
            origTotal = i['origTotal']
            bsId = i['bsId']
            tsId = i['tsId']
            tsql = """
                    INSERT IGNORE INTO caipin(就餐人数,消费金额,bsId,tsId) VALUES('{0}','{1}','{2}','{3}')
                    """


if __name__ == '__main__':
    first()