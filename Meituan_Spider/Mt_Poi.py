import requests
import json
import re
import mysql.connector
import urllib3
import time
from fake_useragent import UserAgent
urllib3.disable_warnings()

ua = UserAgent()
session = requests.session()


def get_D(areaId, area):
    # post参数内容,需要修改
    u = '3d485720-25d8-4929-9ef8-494a8f7b6fe4'
    # 代理ip，要不要无所谓
    p = {'https': 'https://60.13.42.3:9999'}
    # post请求link
    url = 'http://meishi.meituan.com/i/api/channel/deal/list'
    # cookie，需要修改，后期自动获取
    c = 'uuid={0}; ci=238; rvct=238; meishi_ci=238; cityid=238; cityname=%E5%AE%89%E9%98%B3'
    # referer
    referer = 'http://meishi.meituan.com/i/?ci=238&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1'
    # 请求头
    head = {'Host': 'meishi.meituan.com',
            'User-Agent': ua.random,
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
            'x-requested-with': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Content-Length': '410',
            'Referer': referer,
            'Cookie': c.format(u)
            }
    # 需要修改
    data = {"uuid":u,"version":"8.2.0","platform":3,"app":"","partner":126,"riskLevel":1,"optimusCode":10,"originUrl":referer,"offset":0,"limit":15,"cateId":1,"lineId":0,"stationId":0,"areaId":areaId,"sort":"default","deal_attr_23":"","deal_attr_24":"","deal_attr_25":"","poi_attr_20043":"","poi_attr_20033":""}
    time.sleep(1.5)
    result = session.post(url, headers=head, data=json.dumps(data), proxies=p).json()
    print(result)
    # 获取该分区店铺总数，计算出要翻的页数
    totalcount = result['data']['poiList']['totalCount']
    # 店铺信息
    datas = result['data']['poiList']['poiInfos']
    print(len(datas), totalcount)
    for d in datas:
        write(d, area)
        # info_list.append()
    print('Page: 1')

    offset = 0
    if totalcount > 15:
        totalcount -= 15
        while offset < totalcount:
            offset += 15
            m = offset/15 + 1
            print('Page: ', m)
            # 需要修改
            data2 = {"uuid":u,"version":"8.2.0","platform":3,"app":"","partner":126,"riskLevel":1,"optimusCode":10,"originUrl":referer,"offset":offset,"limit":15,"cateId":1,"lineId":0,"stationId":0,"areaId":areaId,"sort":"default","deal_attr_23":"","deal_attr_24":"","deal_attr_25":"","poi_attr_20043":"","poi_attr_20033":""}
            try:
                time.sleep(0.5)
                result = session.post(url, headers=head, data=json.dumps(data2), proxies=p).json()
                datas = result['data']['poiList']['poiInfos']
                print(len(datas))
                for d in datas:
                    write(d, area)
            except Exception as e:
                print('爬取出错 ---- E --- R --- R --- O --- R ----> ', e)
                time.sleep(10)


def write(d, area):
    smartTags = None
    openHours = 0
    avgPrice = d['avgPrice']  # 人均
    avgScore = d['avgScore']  # 评分
    cateName = d['cateName']  # 菜品类别
    channel = d['channel']  # 分类?
    frontImg = d['frontImg']  # 店铺logo
    lat = d['lat']  # 纬度
    lng = d['lng']  # 经度
    name = d['name']  # 店铺名
    poiid = d['poiid']  # 店铺id
    areaName = d['areaName']  # 地区或商圈?
    ctPoi = d['ctPoi']  # 后面有用
    if 'smartTags' in d:
        s = d['smartTags'][0]['text']['content']  # 排名标签
        smartTag = re.findall(r'^\w+\d+名$', s)
        for tag in smartTag:
            # print(tag)
            smartTags = tag
    if 'openHours' in d:
        r = d['openHours']['text']['content']  # 当前人气
        openHour = re.findall(r'\d+', r)
        for hour in openHour:
            openHours = hour
    print(name,poiid,avgPrice,avgScore,cateName,channel,lat,lng,area,areaName,smartTags,openHours,ctPoi,frontImg)

    sql = '''
            INSERT IGNORE INTO ceshi (
            avgPrice,
            avgScore,
            cateName,
            channel,
            frontImg,
            lat,
            lng,
            name,
            poiid,
            areaName,
            ctPoi,
            smartTags,
            openHours,
            area
            ) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
    try:
        cursor.execute(sql, (avgPrice,
                             avgScore,
                             cateName,
                             channel,
                             frontImg,
                             lat,
                             lng,
                             name,
                             poiid,
                             areaName,
                             ctPoi,
                             smartTags,
                             openHours,
                             area
                             ))
        mydb.commit()
    except Exception as w:
        print("数据库写入出错 ---- E --- R --- R --- O --- R ----> ", w)
        time.sleep(3)


def read_city():
    # 读取外部城市及商圈文件
    load = './city.json'
    area_list = []
    with open(load, 'r', encoding='utf8')as f:
        file = json.load(f)
        # print(file)
        for data in file['areas']:
            # 区名
            a = data['name']
            # 商圈
            # for d in data['subAreas'][1:]:
            #     # area_list.append(d['id'])
            #     print(d)
            #     # 爬取函数
            #     get_D(d['id'], a)
                # print(d['id'], cookie)
            # 全部
            get_D(data['subAreas'][0]['id'], a)


if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host='47.97.166.98',
        user='root',
        password='100798',
        database='Meituan'
    )
    cursor = mydb.cursor()
    read_city()