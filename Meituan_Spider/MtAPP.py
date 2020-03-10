import requests
import json
import re
import queue
import threading
import mysql.connector
import pymysql
import urllib3
import time
from fake_useragent import UserAgent
urllib3.disable_warnings()

ua = UserAgent()
sessions = requests.session()
u = '3d485720-25d8-4929-9ef8-494a8f7b6fe4'
c = 'uuid={0}; ci=245; rvct=245; meishi_ci=245; cityid=245; cityname=%E5%AE%89%E9%98%B3'
c1 = 'uuid=57f3874ed29d45988631.1571813297.1.0.0; ci=245; rvct=245; meishi_ci=245; cityid=245; cityname=%E5%95%86%E4%B8%98'
exitFlag = 0
class MyThread(threading.Thread):
    def __init__(self, threadID, name, que):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.que = que
        self.headers = {
            'Host': 'www.meituan.com',
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': c.format(u),
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0, no-cache',
            'Pragma': 'no-cache'
        }
    def run(self):
        print("开启线程：" + self.name)
        get_i(self.name, self.que, self.headers)
        print("Exiting ", self.name)
        pass

def get_i(name, data_queue, head):

    url = 'https://www.meituan.com/meishi/{}/'
    p = {'https': 'https://60.13.42.3:9999'}

    # 第3个字段是店铺id, 拼接url和id得出url
    while not exitFlag:
        queueLock.acquire()
        if not data_queue.empty():
            data = data_queue.get()
            queueLock.release()
            try:
                u = url.format(data[2])
                print(name + ' 开始爬取>>> ',u)
                r = sessions.get(u, headers=head, verify=False)
                response = r.content.decode()
                print(r)
                i = re.findall(r'<script>window._appState = (.*?);</script>', response, re.S)
                # 数据来源为网页源代码
                # print(i[0])
                tg_list = []
                tj_dict = {}
                if len(i):
                    f = json.loads(i[0], encoding='utf-8')
                    # print(f)
                    address = f['detailInfo']['address']  # 地址
                    phone = f['detailInfo']['phone']  # 电话
                    openTime = f['detailInfo']['openTime']  # 营业时间
                    extraInfo = [e['text'] for e in f['detailInfo']['extraInfos']]  # 概述
                    extraInfos = ','.join(extraInfo)
                    # print(extraInfos)
                    # 推荐
                    cname = [r['name'] for r in f['recommended']]  # 推荐菜名
                    tPrice = [r['price'] for r in f['recommended']]  # 价格
                    for n, j in zip(cname, tPrice):
                        tj_dict[n] = j
                    # 团购
                    title = [d['title'] for d in f['dealList']['deals']]  # 团购
                    price = [d['price'] for d in f['dealList']['deals']]  # 现价
                    value = [d['value'] for d in f['dealList']['deals']]  # 门市价
                    soldNum = [d['soldNum'] for d in f['dealList']['deals']]  # 销量
                    for t, p, v, s in zip(title, price, value, soldNum):
                        # print(t,p,v,s)
                        dic = {"title": t, "price": p, "value": v, "soldNum": s}
                        tg_list.append(dic)

                    tg = {"dealList": tg_list}
                    tj = {"recommended": tj_dict}
                    dealList = json.dumps(tg, ensure_ascii=False)  # 团购
                    recommended = json.dumps(tj, ensure_ascii=False)  # 推荐菜品
                    # print(type(address), type(phone), type(openTime), type(extraInfos), type(dealList), type(recommended))
                    # print(address, phone, openTime, extraInfos, dealList, recommended)
                    # 商家信息入库
                    tsql = """
                                                INSERT IGNORE INTO anyang(店铺名称,
                                                店铺id,
                                                人均,评分,
                                                美食类别,类别,
                                                电话,营业时间,商家概述,
                                                标签,人气,
                                                纬度,经度,店铺地址,
                                                商圈,区域,
                                                团购优惠,
                                                推荐菜品,
                                                ctPoi,店铺logo) VALUES("{0}",
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
                    # print(sql)
                    # insert(sql, data[2])
                    try:
                        queueLock.acquire()
                        cursor.execute(sql)
                        # mydb.commit()
                        dsql = 'DELETE FROM ceshi WHERE poiid={}'.format(data[2])
                        cursor.execute(dsql)
                        mydb.commit()
                        queueLock.release()
                    except Exception as w:
                        print("数据写入异常 ---- E --- R --- R --- O --- R ----> ", w)
                        queueLock.release()
                    # 双数据库去重，人工智障
                else:
                    print(u, ' ---- E --- 无 --- 数 --- 据 --- R ---->', name)
            except Exception as e:
                print('爬取异常 ---- E --- R --- R --- O --- R ----> ', e)
                data_queue.put(data)
                # print(response)

        else:
            queueLock.release()


def insert(sql, data):
    try:
        queueLock.acquire()
        cursor.execute(sql)
        # mydb.commit()
        dsql = 'DELETE FROM ceshi WHERE poiid={}'.format(data)
        cursor.execute(dsql)
        mydb.commit()
        queueLock.release()
    except Exception as w:
        print("数据写入异常 ---- E --- R --- R --- O --- R ----> ", w)
        queueLock.release()

def get_d():
    # 条件查询
    cursor.execute('select * from ceshi')
    # fetchall 查询全部
    datas = cursor.fetchall()
    print(len(datas))
    for data in datas:
        data_queue.put(data)

if __name__ == '__main__':

    start_time = time.time()
    # 连接数据库
    mydb = mysql.connector.connect(
        host='47.97.166.98',
        user='root',
        password='100798',
        database='Meituan'
    )
    cursor = mydb.cursor()

    crawlList = ["crawl-1", "crawl-2", "crawl-3", "crawl-4", "crawl-5", "crawl-6", "crawl-7", "crawl-8"]

    queueLock = threading.Lock()
    data_queue = queue.Queue()
    threads = []
    threadID = 1

    for name in crawlList:
        thread = MyThread(threadID, name, data_queue)
        thread.start()
        threads.append(thread)
        threadID += 1

    queueLock.acquire()
    # 从数据库获取待爬取的数据
    get_d()
    queueLock.release()

    while not data_queue.empty():
        pass
    exitFlag = 1

    for t in threads:
        t.join()
    print("退出主线程")
    end_time = time.time()
    run_time = (end_time - start_time)
    print(run_time)
