import requests
import json
import re
import queue
import mysql.connector
import pymysql
import urllib3
from fake_useragent import UserAgent
urllib3.disable_warnings()

ua = UserAgent()


# d = {'smartTags': [['x','y'],'55']}
# dict = {'smartTags': [['x','y'],'我是人第55名'], 'openHours': ['人气99']}
# # print(dict['smartTags'][0][1])
# li = []
# if 'smartTags' in dict:
#     # print(dict['smartTags'][1])
#     s = re.findall(r'^\w+\d+名$',dict['smartTags'][1])
#     print(s)
#     # li.append(dict['smartTags'])
#
# if 'openHours' in dict:
#     t = re.findall(r'\d+', dict['openHours'][0])

# else:
#     print('error')


# with open('.\city.json', 'r', encoding='utf8')as f:
#     file = json.load(f)
#     # print(file)
#     for data in file['areas']:
#         # print(data)
#         print(data['name'])
#         # for d in data['subAreas'][1:]:
#         #     print(d['id'])
p = {'https': 'https://113.121.21.221:9999'}

def get_detail():
    u = '259b88220a5e46d3afb5.1563329278.1.0.0'
    url = 'https://www.meituan.com/meishi/180648788/'

    cookie = 'iuuid=3B66FD71AE7F212FF738A700B94C33C375E559BD1E1EE4561359A2210AC57A83; _lxsdk_cuid=16b9847c8b6c8-0408e576b22c29-37c143e-144000-16b9847c8b62f; _lxsdk=3B66FD71AE7F212FF738A700B94C33C375E559BD1E1EE4561359A2210AC57A83; webp=1; _hc.v=ca8cb434-363b-a3d0-861f-c4104d1a019a.1561628048; __utmz=74597006.1561630184.2.2.utmcsr=meishi.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/i/; a2h=4; _ga=GA1.2.122797472.1561628000; _lx_utm=utm_source%3Dmeishi.meituan.com%26utm_medium%3Dreferral%26utm_content%3D%252Fi%252F; rvct=60%2C73; mtcdn=K; client-id=7110106b-0a52-4489-bd55-91d83b5aafb3; __utma=74597006.122797472.1561628000.1563349421.1563351369.10; latlng=34.75832,113.766959,1563351520585; cityname=%E9%9D%92%E5%B2%9B; i_extend=C_b1Gimthomepagecategory11H__a; uuid=77eb81e80fb64fab84c6.1563412152.1.0.0; __mta=55344660.1563329280904.1563329280904.1563412152328.2; ci=60; lat=36.304949; lng=120.407791; _lxsdk_s=16c02d13440-0d6-8c8-1a3%7C%7C2'
    head = {'Host': 'www.meituan.com',
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': cookie,
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'}

    r = requests.get(url=url, headers=head, proxies=p).text
    i = re.findall(r'<script>window._appState = {(.*?)};</script>', r, re.S)
    print(i)

def pipei():
    tj_list = []
    tg_list = []

    with open('.\d.html', 'r', encoding='utf-8')as h:
        i = re.findall(r'<script>window._appState = (.*?);</script>', h.read(), re.S)
        f = json.loads(i[0], encoding='utf-8')
        # print(f)
        address = f['detailInfo']['address']  #地址
        phone = f['detailInfo']['phone']  # 电话
        openTime = f['detailInfo']['openTime']  # 营业时间
        extraInfo = [e['text'] for e in f['detailInfo']['extraInfos']]  # 概述
        extraInfos = ','.join(extraInfo)
        print(extraInfos)
        name = [r['name'] for r in f['recommended']]  # 推荐菜名
        tPrice = [r['price'] for r in f['recommended']]  # 价格
        for n, j in zip(name, tPrice):
            c = {"name": n, "price": j}
            tj_list.append(c)

        title = [d['title'] for d in f['dealList']['deals']]  # 团购
        price = [d['price'] for d in f['dealList']['deals']]  # 现价
        value = [d['value'] for d in f['dealList']['deals']]  # 门市价
        soldNum = [d['soldNum'] for d in f['dealList']['deals']]  # 销量
        for t,p,v,s in zip(title,price,value,soldNum):
            # print(t,p,v,s)
            dic = {"title": t, "price": p, "value": v, "soldNum": s}
            tg_list.append(dic)

        tg = {"dealList": tg_list}
        tj = {"recommended": tj_list}
        dealList = json.dumps(tg, ensure_ascii=False)
        recommended = json.dumps(tj, ensure_ascii=False)
        print(type(address), type(phone), type(openTime), type(extraInfos), type(dealList), type(recommended))
        print(address, phone, openTime, extraInfos, dealList, recommended)

        sqlt = """
        INSERT INTO js_t (deal,rem) VALUES('{}','{}')
        """
        sql = sqlt.format(pymysql.escape_string(dealList), pymysql.escape_string(recommended))
        # print(sql)
        try:
            cursor.execute(sql)
            mydb.commit()
        except Exception as e:
            print(e)

def ip_t():
    t = requests.get('http://www.baidu.com', timeout=3, proxies=p)
    print(requests)
    print(t.text)

if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='Test'
    )
    cursor = mydb.cursor()
    # ip_t()
    # get_detail()
    pipei()