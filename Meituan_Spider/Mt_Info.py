import requests
import json
import re
import queue
import asyncio
from aiohttp import ClientSession
import mysql.connector
import pymysql
import urllib3
from fake_useragent import UserAgent
urllib3.disable_warnings()

ua = UserAgent()

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='Test'
)
cursor = mydb.cursor()

# A = [item for item in datas if item not in set(Ok_list)]

def get_d():
    # 条件查询
    cursor.execute('select * from info_tbl')
    # fetchall 查询全部
    datas = cursor.fetchall()
    print(len(datas))
    for data in datas:
        print(data)
        get_i(data)


#  这里应该搞一个队列先将数据计入队列，从队列里取数据(后边改进)
def get_i(data):

    tj_list = []
    tg_list = []
    url = 'http://www.meituan.com/meishi/{}/'
    p = {'https': 'https://171.41.122.70:9999'}

    c = '__mta=142546573.1561628052344.1563350378670.1563788203865.28; __mta=142546573.1561628052344.1563787303623.1563787417788.29; iuuid=3B66FD71AE7F212FF738A700B94C33C375E559BD1E1EE4561359A2210AC57A83; _lxsdk_cuid=16b9847c8b6c8-0408e576b22c29-37c143e-144000-16b9847c8b62f; _lxsdk=3B66FD71AE7F212FF738A700B94C33C375E559BD1E1EE4561359A2210AC57A83; webp=1; _hc.v=ca8cb434-363b-a3d0-861f-c4104d1a019a.1561628048; __utmz=74597006.1561630184.2.2.utmcsr=meishi.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/i/; a2h=4; _ga=GA1.2.122797472.1561628000; rvct=60%2C73; __utma=74597006.122797472.1561628000.1563349421.1563351369.10; latlng=34.75832,113.766959,1563351520585; cityname=%E9%9D%92%E5%B2%9B; i_extend=C_b1Gimthomepagecategory11H__a; client-id=01b1b1df-e0e4-45f4-9493-24bd0980cacf; _lx_utm=utm_source%3Dmeishi.meituan.com%26utm_medium%3Dreferral%26utm_content%3D%252Fi%252F; uuid=0d8977b4-9215-431f-8298-e476587df9e6; ci=104; meishi_ci=104; logan_custom_report=; logan_session_token=j2kyxybecuaa346ztnos; _lxsdk_s=16c18e24af8-20f-f51-fd%7C%7C14'

    head = {'Host': 'www.meituan.com',
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cookie': c,
            'Upgrade-Insecure-Requests': '1'
            }
    # 第3个字段是店铺id, 拼接url和id得出url
    try:
        u = url.format(data[2])
        print(u)
        response = requests.get(u, headers=head, proxies=p, allow_redirects=False).content.decode()
        # print(response)
        i = re.findall(r'<script>window._appState = (.*?);</script>', response, re.S)
        # 数据来源为网页源代码
        print(i[0])
        f = json.loads(i[0], encoding='utf-8')
        # print(f)
        address = f['detailInfo']['address']  # 地址
        phone = f['detailInfo']['phone']  # 电话
        openTime = f['detailInfo']['openTime']  # 营业时间
        extraInfo = [e['text'] for e in f['detailInfo']['extraInfos']]  # 概述
        extraInfos = ','.join(extraInfo)
        # print(extraInfos)
        name = [r['name'] for r in f['recommended']]  # 推荐菜名
        tPrice = [r['price'] for r in f['recommended']]  # 价格
        for n, j in zip(name, tPrice):
            c = {"name": n, "price": j}
            tj_list.append(c)

        title = [d['title'] for d in f['dealList']['deals']]  # 团购
        price = [d['price'] for d in f['dealList']['deals']]  # 现价
        value = [d['value'] for d in f['dealList']['deals']]  # 门市价
        soldNum = [d['soldNum'] for d in f['dealList']['deals']]  # 销量
        for t, p, v, s in zip(title, price, value, soldNum):
            # print(t,p,v,s)
            dic = {"title": t, "price": p, "value": v, "soldNum": s}
            tg_list.append(dic)

        tg = {"dealList": tg_list}
        tj = {"recommended": tj_list}
        dealList = json.dumps(tg, ensure_ascii=False)  # 团购
        recommended = json.dumps(tj, ensure_ascii=False)  # 推荐菜品
        # print(type(address), type(phone), type(openTime), type(extraInfos), type(dealList), type(recommended))
        print(address, phone, openTime, extraInfos, dealList, recommended)
        # requests.get(url.format(d[3]))
        # 爬取过后写入
        tsql = """
            INSERT IGNORE INTO ly_info(店铺名称,
            店铺id,
            人均,评分,
            美食类别,类别,
            电话,营业时间,商家概述,
            标签,人气,
            纬度,经度,店铺地址,
            商圈,区域,
            团购优惠,
            推荐菜品,
            ctPoi,店铺logo) VALUES('{0}',
            '{1}',
            '{2}','{3}',
            '{4}','{5}',
            '{6}','{7}','{8}',
            '{9}','{10}',
            '{11}','{12}','{13}',
            '{14}','{15}',
            '{16}',
            '{17}',
            '{18}','{19}')
            """
        sql = tsql.format(data[1],
                          data[2],
                          data[4], data[5],
                          data[6], data[7],
                          phone, openTime, extraInfos,
                          data[12], data[13],
                          data[8], data[9], address,
                          data[10], data[-1],
                          pymysql.escape_string(dealList),
                          pymysql.escape_string(recommended),
                          data[11], data[3]
                          )
        try:
            cursor.execute(sql)
            mydb.commit()
            dsql = 'DELETE FROM luoyang WHERE poiid={}'.format(data[2])
            cursor.execute(dsql)
            mydb.commit()
        except Exception as e:
            print(e)
        # 爬取过的从原表删除

    except Exception as er:
        print(er)
    # finally:
    #     get_d()
    #     pass


if __name__ == '__main__':
    get_d()

