"""
通过百度百科获取全国县市数据；
数据提取基本上就这样了；
市县城市信息不全；
字段目前有人口数、地区生产总值、人均生产总值、人均可支配收入以及、社会消费品零售总额；
面积数据意义不大，产业信息数据复杂，留一个百科的链接；
城市跟人物或是其他东西重复问题暂未解决；
"""

import re
import requests
import csv
import mysql.connector
from fake_useragent import UserAgent

ua = UserAgent()
head = {
            'Host': 'baike.baidu.com',
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
url = 'https://baike.baidu.com/item/'
p = {'https': 'https://113.121.21.233:9999'}

def city():
    with open('c.html', 'r', encoding='utf-8')as f:
        c = re.findall(r'<td class=xl7015800>([\u4e00-\u9fa5]{1,15})</td>', f.read())
        return c
    #     print(len(c))
    # with open('ci.txt', 'r', encoding='utf-8')as f:
    #     for x in f:
    #         city = x.split(',')
    #         return city

def baike():
    for c in city():
        link = url+c
        print(c)
        try:
            response = requests.get(link, headers=head).content.decode()
            # 总人口，单位转换：大于3000 /10000，北上广深人口没超过2500万，所以取3000，正则匹配有修改余地
            # rk_list = re.findall(r'人口[为]{0,1}(\d+[.]?\d{0,3})[万]?[人]?', response)
            rk_list = re.findall(r'人口[为]?[约]?(\d+[.]?\d{0,3})万[人]?|人口[为]?[约]?(\d+[.]?\d{0,3})人|(\d+[.]?\d{0,3})万[人]?[（\d）]', response)
            r_list = []
            rk = None
            if rk_list:
                for rk_t in rk_list:
                    if rk_t[1]:
                        r_list.append(float(rk_t[1]) / 10000)
                    elif rk_t[2]:
                        r_list.append(float(rk_t[2]))
                    else:
                        r_list.append(float(rk_t[0]))
            # 人口总值趋势一般不会降低，取最大值
            if r_list:
                rk = max(r_list)

            # 面积
            # mj = re.findall(r'面积(\d+[.]?\d{0,3})平方[公里]{0,2}[千米]{0,2}', response)

            # 地区生产总值
            dq_list = re.findall(r'[地区]{0,2}生产总值[GDP]{0,4}[\u4e00-\u9fa5]{0,10}[（GDP）]{0,6}[\u4e00-\u9fa5]{0,10}(\d+[.]?\d{0,3})亿[\u4e00-\u9fa5]{0,2}元|[地区]{0,2}生产总值[GDP]{0,4}[\u4e00-\u9fa5]{0,10}[（GDP）]{0,6}[\u4e00-\u9fa5]{0,10}(\d+[.]?\d{0,3})万元', response)
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
            rj_list = re.findall(r'人均[GDP]{0,3}[\u4e00-\u9fa5]{0,3}[生产总值]{0,4}[\u4e00-\u9fa5]{0,2}(\d+[.]?\d{0,3})元|人均[GDP]{0,3}[\u4e00-\u9fa5]{0,3}[生产总值]{0,4}[\u4e00-\u9fa5]{0,2}(\d+[.]?\d{0,3})万元', response)
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

            # 城镇化率
            czhl_list = re.findall(r'城镇化率[达到]{0,2}(\d+[.]?\d{0,3}%)', response)
            czhl = None
            if czhl_list:
                czhl = czhl_list[0]

            # 城镇人口
            czrk_list = re.findall(r'城镇人口[为]?(\d+[.]?\d{0,3})万人|城镇人口[为]?(\d+[.]?\d{0,3})人', response)
            czrk = None
            # print(czrk_list)
            if czrk_list:
                for czrk_t in czrk_list:
                    if czrk_t[1]:
                        czrk = float(czrk_t[1]) / 10000
                    else:
                        czrk = czrk_t[0]

            #乡村人口
            xcrk_list = re.findall(r'乡村人口[为]?(\d+[.]?\d{0,3})万人|乡村人口[为]?(\d+[.]?\d{0,3})人', response)
            # print(xcrk_list)
            xcrk = None
            if xcrk_list:
                for xcrk_t in xcrk_list:
                    if xcrk_t[1]:
                        xcrk = float(xcrk_t[1]) / 10000
                    else:
                        xcrk = xcrk_t[0]

            print(c, rk, dq_money, rj_money, zp_max, zp_min, shls, czhl, czrk, xcrk, link)
            # print(type(c), type(rk), type(dq_money), type(rj_money), type(zp_max), type(zp_min), type(shls), type(link))
            # write_db(c, rk, dq_money, rj_money, zp_max, zp_min, shls, link)
            write_csv(c, rk, dq_money, rj_money, zp_max, zp_min, shls, czhl, czrk, xcrk, link)
        except Exception as e:
            print('爬取、解析异常 ---- E --- R --- R --- O --- R ----> ', e)

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


def write_csv(c, rk, dq_money, rj_money, zp_max, zp_min, shls, czhl, czrk, xcrk, link):
    with open('c_info.csv', 'a', encoding='utf-8', newline='')as f:
        f_csv = csv.writer(f)
        f_csv.writerow([c, rk, dq_money, rj_money, zp_max, zp_min, shls, czhl, czrk, xcrk, link])


if __name__ == '__main__':
    baike()
