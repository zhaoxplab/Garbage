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
exitFlag = 0
class MyThread(threading.Thread):
    def __init__(self, threadID, name, que):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.que = que
        self.headers = {'Host': 'baike.baidu.com',
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    def run(self):
        print("开启线程：" + self.name)
        get_i(self.name, self.que, self.headers)
        print("Exiting ", self.name)
        pass

def get_i(name, data_queue, head):

    p = {'https': '171.41.122.70:9999'}
    url = 'https://baike.baidu.com/item/'
    # 第3个字段是店铺id, 拼接url和id得出url
    while not exitFlag:
        queueLock.acquire()
        if not data_queue.empty():
            city = data_queue.get()
            queueLock.release()
            try:
                link = url + city
                try:
                    response = requests.get(link, headers=head).content.decode()
                    # 总人口，单位转换：大于3000 /10000，北上广深人口没超过2500万，所以取3000，正则匹配有修改余地
                    rk_list = re.findall(r'人口(\d+[.]?\d{0,3})[万]?[人]?', response)
                    r_list = []
                    rk = None
                    # 将列表的str类型转换为数字类型，方便取最大值
                    rk_m = map(float, rk_list)
                    # print(list(rk_m))
                    for r in rk_m:
                        if r < 3000:
                            r_list.append(r)
                        else:
                            r = r / 10000
                            r_list.append(r)
                    if r_list:
                        # 人口总值趋势一般不会降低，取最大值
                        rk = max(r_list)

                    # 面积
                    # mj = re.findall(r'面积(\d+[.]?\d{0,3})平方[公里]{0,2}[千米]{0,2}', response)

                    # 地区生产总值
                    dq_list = re.findall(
                        r'[地区]{0,2}生产总值[GDP]{0,4}[\u4e00-\u9fa5]{0,10}[（GDP）]{0,6}(\d+[.]?\d{0,3})亿[\u4e00-\u9fa5]{0,2}元|[地区]{0,2}生产总值[GDP]{0,4}[\u4e00-\u9fa5]{0,10}[（GDP）]{0,6}(\d+[.]?\d{0,3})万元',
                        response)
                    d_list = []
                    dq_money = None
                    if dq_list:
                        # 匹配到数据即为True，执行下一步
                        for dq_t in dq_list:
                            # dq_t是tuple，第一个元素单位是万，所以除以10000来统一单位
                            if dq_t[1]:
                                d_list.append(float(dq_t[1]) / 10000)
                            else:
                                # 无需转换单位，直接加入d_list
                                d_list.append(float(dq_t[0]))
                    if d_list:
                        # 生产总值趋势一般不会降低，所以取最大值
                        dq_money = max(d_list)

                    #  人均生产总值
                    rj_list = re.findall(
                        r'人均[GDP]{0,3}[\u4e00-\u9fa5]{0,3}[生产总值]{0,4}[\u4e00-\u9fa5]{0,2}(\d+[.]?\d{0,3})元|人均[GDP]{0,3}[\u4e00-\u9fa5]{0,3}[生产总值]{0,4}[\u4e00-\u9fa5]{0,2}(\d+[.]?\d{0,3})万元',
                        response)
                    r_list = []
                    rj_money = None
                    if rj_list:
                        for r_t in rj_list:
                            # 转换单位
                            if r_t[1]:
                                r_list.append(float(r_t[1]) * 10000)
                            else:
                                r_list.append(float(r_t[0]))
                    if r_list:
                        rj_money = max(r_list)

                    # 人均可支配收入，单位是 “元”
                    zp_list = re.findall(r'人均可支配收入[\u4e00-\u9fa5]{0,5}(\d+[.]?\d{0,3})元', response)
                    z_list = []
                    zp_max = None
                    zp_min = None
                    if zp_list:
                        for zp in zp_list:
                            # 转换单位并添加到list
                            z_list.append(float(zp))
                    if zp_list:
                        # 城镇居民max（相对准确)，乡村min（不保证绝对准确）
                        zp_max = max(z_list)
                        zp_min = min(z_list)

                    # 社会消费品零售总额，单位 “万元”
                    shls_list = re.findall(r'社会消费品零售总额(\d+[.]?\d{0,3})亿元|社会消费品零售总额(\d+[.]?\d{0,3})万元', response)
                    ls_list = []
                    shls = None
                    if shls_list:
                        for shls_t in shls_list:
                            # 单位转换代码块
                            if shls_t[1]:
                                ls_list.append(float(shls_t[1]) / 10000)
                            else:
                                ls_list.append(float(shls_t[0]))
                    if ls_list:
                        # 老规矩，为保证数据准确性，依旧取最大值
                        shls = max(ls_list)

                    write_db(c, rk, dq_money, rj_money, zp_max, zp_min, shls, link)
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

def write_db(c, rk, dq_money, rj_money, zp_max, zp_min, shls, link):
    sql = '''
        INSERT IGNORE INTO c_info(名称,
        人口,
        地区生产总值,人均生产总值,
        城镇居民支配收入,乡镇居民可支配收入,
        社会消费品零售总额,
        Link) VALUES('{0}',
        '{1}',
        '{2}','{3}',
        '{4}','{5}',
        '{6}',
        '{7}')
    '''
    sqlA = sql.format(c, rk, dq_money, rj_money, zp_max, zp_min, shls, link)
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='Test'
    )
    cursor = mydb.cursor()
    try:
        cursor.execute(sqlA)
        mydb.commit()
    except Exception as w:
        print('数据写入异常 ---- E --- R --- R --- O --- R ----> ', w)



def get_c():
    # 获取城市
    f_u = 'http://www.mca.gov.cn/article/sj/xzqh/2018/201804-12/20181201301111.html'
    res = requests.get(f_u).text
    # print(res)
    c_l = re.findall(r'<td class=xl7015800>([\u4e00-\u9fa5]{1,15})</td>', res)
    for cit in c_l:
        data_queue.put(cit)

if __name__ == '__main__':

    start_time = time.time()
    # 连接数据库
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='test'
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
        # time.sleep(1)
        threadID += 1

    queueLock.acquire()
    # 从数据库获取待爬取的数据
    get_c()
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
