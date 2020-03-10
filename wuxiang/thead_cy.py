import requests
import json
import re
import queue
import threading
import mysql.connector
import pymysql
import urllib3
import time
import ast
import random
from fake_useragent import UserAgent
urllib3.disable_warnings()

ua = UserAgent()
c = 'isNewVersion=0; JSESSIONID=A863D48FC9E66C410FB2A05C0B722732; sessionid=A863D48FC9E66C410FB2A05C0B722732; loginedShopId=; loginedUsername=; success=true; UM_distinctid=16b987d692e74-06df07ec012f44-37c143e-144000-16b987d692f4cd; CNZZDATA1275514722=1671585256-1561631485-null%7C1566259719'
c1 = 'iuuid=E144D021C195D8BA745B9EBE8B3A9E585DA41D4E365CD3E4C2C7F0A0F543E7DB; cityname=%E7%83%9F%E5%8F%B0; a2h=1; _lxsdk_cuid=16b9d78d3fac8-070a29db040fd7-4c312d7d-144000-16b9d78d3fbc8; _lxsdk=E144D021C195D8BA745B9EBE8B3A9E585DA41D4E365CD3E4C2C7F0A0F543E7DB; webp=1; i_extend=C_b1Gimthomepagecategory11H__a; __utma=74597006.1871727516.1561715071.1565330860.1566028595.15; __utmz=74597006.1565078913.11.5.utmcsr=meishi.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/i/; _hc.v=169c254a-c860-cdff-a6c5-01ddc88ec849.1561715189; rvct=224%2C104%2C857%2C60; __mta=42834586.1564562496363.1565942527327.1566026459900.4; _lx_utm=utm_source%3Dmeishi.meituan.com%26utm_medium%3Dreferral%26utm_content%3D%252Fi%252F; uuid=49fce474c5984e808bba.1566026458.1.0.0; ci=104; IJSESSIONID=jw89zm16997n1o3itzf82nrao; latlng=34.771479,113.767018,1566028595868; __utmc=74597006; ci3=1; meishi_ci=104; cityid=104; _lxsdk_s=16c9eb74b13-197-1d2-579%7C%7C1'
exitFlag = 0
class MyThread(threading.Thread):
    def __init__(self, threadID, name, que):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.que = que
        self.headers = {'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': c,
            'Host': 'cy.wuuxiang.com',
            'Referer': 'https://cy.wuuxiang.com/cy7center/canyin/report/',
            'User-Agent': ua.random,
            'X-Requested-With': 'XMLHttpRequest'
        }
    def run(self):
        print("开启线程：" + self.name)
        get_i(self.name, self.que, self.headers)
        print("Exiting ", self.name)
        pass

def get_i(name, data_queue, head):

    p = {'https': '171.41.122.70:9999'}
    u = 'https://cy.wuuxiang.com/cy7center/canyin/report/a11/doconsumptionlist?id={}&_dc={}&page=1'
    # 第3个字段是店铺id, 拼接url和id得出url
    while not exitFlag:
        queueLock.acquire()
        if not data_queue.empty():
            bsi = data_queue.get()
            queueLock.release()
            try:
                num = random.randint(100, 999)
                c = str(int(time.time())) + str(num)
                url = u.format(bsi[4], c)
                print(name + ' 开始爬取>>> ',url)
                res = requests.get(url, headers=head, allow_redirects=False).text
                detail = re.findall(r'({.*?})', res)
                c_list = []
                for inf in detail:
                    info = ast.literal_eval(inf)
                    cp_name = info['name']
                    lastQty = info['lastQty']
                    c_list.append({cp_name: lastQty})
                    # print(c_list)
                caipin = {'cp': c_list}
                CpList = json.dumps(caipin, ensure_ascii=False)

                tsql = """
                        INSERT IGNORE INTO cp(就餐人数,消费金额,bsId,tsId,消费明细) VALUES({0},{1},'{2}','{3}','{4}')
                        """
                try:
                    queueLock.acquire()
                    sql = tsql.format(bsi[1],
                                      bsi[3],
                                      bsi[4],
                                      bsi[5],
                                      pymysql.escape_string(CpList))
                    # print(sql)
                    cursor.execute(sql)
                    dsql = 'DELETE FROM caipin_copy WHERE bsId={}'.format(bsi[4])
                    cursor.execute(dsql)
                    mydb.commit()
                    queueLock.release()
                    time.sleep(0.2)
                except Exception as w:
                    print("数据写入异常 ---- E --- R --- R --- O --- R ----> ", w)
                    queueLock.release()

            except Exception as e:
                print('爬取异常 ---- E --- R --- R --- O --- R ----> ', e)
                # data_queue.put(url)
                # print(response)

        else:
            queueLock.release()

def get_d():
    # 条件查询
    start = 0
    u = 'https://cy.wuuxiang.com/cy7center/canyin/report/a11/doconsumptionlist?id={}&_dc={}&page=1'
    ssql = 'select * from caipin'
    cursor.execute(ssql)
    bsl = cursor.fetchall()
    for bs in bsl:
        data_queue.put(bs)

if __name__ == '__main__':

    start_time = time.time()
    # 连接数据库
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='cy'
    )
    cursor = mydb.cursor()

    crawlList = ["crawl-1", "crawl-2", "crawl-3", "crawl-4", "crawl-5", "crawl-6", "crawl-7", "crawl-8", "crawl-9", "crawl-10", "crawl-11", "crawl-12"]

    queueLock = threading.Lock()
    data_queue = queue.Queue()
    threads = []
    threadID = 1

    for name in crawlList:
        thread = MyThread(threadID, name, data_queue)
        thread.start()
        threads.append(thread)
        # time.sleep(1)
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
