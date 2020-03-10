# -*- coding:utf-8 -*-

import requests
import sys
from urllib import request
import chardet
import random
import pymongo
import time
from fake_useragent import UserAgent
import urllib
import re
import os
from urllib import parse
from lxml import etree
# 禁用安全请求警告
import urllib3
urllib3.disable_warnings()


Form_Data = {}
qq_url = []
list_matcher2_url7 = []
list_matcher2_url8 =[]
list_matcher2_url9 = []
q = []
# 屏蔽的文件
data = []
#  re匹配href
list_url = []
list_keyword = []
list_Description = []
list_phone_url = []
list_De = []
list_matcher2_url4 = []
list_phone = []
list_matcher1_url = []
name_response_url = []
list_matcher1_url2 = []
list_matcher2_url2 = []
list_sign = []
sign = []
mydict = {}
list_matcher2_url5 = []
list_matcher2_url6 = []
# 打印联系我们链接
# 定义c 首次拼接
c = []
# d最后链接
d = []
f = []
list_matcher2_url3 = []
title = []
# kw = parse.unquote(kw)
t = "wpa.qq.com/msgrd"
p = "tencent:"

# def ip_pool():
#
#     ip_pool = ['222.171.251.43:40149',
#                 '119.101.115.11:9999',
#                 '119.101.113.249:9999',
#                 '119.101.113.218:9999',
#                 '119.101.113.150:9999',
#                 '112.98.126.100:33421',
#                 '59.37.33.62:50686',
#                 '24.115.192.181:22225',
#                 '76.109.210.184:22225',
#                 '70.171.171.71:22225',
#                 '173.212.14.188:22225',
#                 '49.67.149.191:404',
#                 '49.67.149.59:405',
#                 '121.226.45.147:401',
#                 '121.226.45.139:406',
#                 '180.121.115.182:403',
#                 '121.226.45.100:402',
#                 '183.148.128.204:448',
#                 '125.126.199.49:447',
#                 '183.148.132.153:446',
#                 '36.26.225.254:445',]
#     ip_pool = random.choices(ip_pool)
#     return ip_pool
# print(ip_pool())

def run(url, start_page,end_page,kw):
    # dict_one = {}
    # idcard = request.values.get("wd")
    # page_start = request.values.get("page_start")
    # end_page = request.values.get("end_page")
    for i in range(start_page, end_page):
        # os.system("./adsl-stop.sh")

        # proxies = {'HTTP': "127.0.0.1:20268"}
        # proxies = {'HTTP': 'http://' + "20268"}
        headers = dict()
        headers["User-Agent"] = UserAgent().random
        # print(headers)

        response = requests.get(url.format(kw, i*10), headers=headers,params=kw, timeout=15)
        # requests.
        html = response.text
        one_html = etree.HTML(html)

        one_html =one_html.xpath('//div[@class="result c-container "]')
        for i_one_html in one_html:

            try:
                # 获取title
                title_title = i_one_html.xpath('.//h3[1]/a//text()')
                title.append("".join(title_title))

                # print("".join(name_links))
                # 获取标志
                # print(i)
                if i_one_html.xpath('.//a[contains(@class,"c-icon c-icon-v")]/@href'):
                    list_sign.append(1)
                else:
                    list_sign.append(0)
                name_links = i_one_html.xpath(".//h3[@class='t']/a/@href")

                for name_link in name_links:
                    # 获取页面数据
                    name_link_response = requests.get(name_link, headers=headers, timeout=15,verify = False)
                    # 获取域名
                    link_url = name_link_response.url
                    list_url.append(link_url)
                    # 页面编码
                    charset = chardet.detect(name_link_response.content)
                    # 获取编码格式
                    a = charset["encoding"]
                    # 进行编码
                    name_link_response.encoding = a
                    # 获取页面源码
                    name_link_respons = name_link_response.text
                    # print(name_link_html)

                    # 获取xpath路径
                    name_link_html = etree.HTML(name_link_respons)
                    # 获取公司名字
                    level_Description = name_link_html.xpath('//meta[contains(@name,"escription")]/@content')
                    # 打印公司名字
                    list_Description.append(level_Description)

                    # print("%s:%s" % ("list_Description", list_Description))
                    # print("%s:%s" % ("公司名字", level_Description))
                    # 获取公司介绍
                    level_Keywords = name_link_html.xpath('//meta[contains(@name,"eywords")]/@content')
                    # 打印公司介绍
                    list_keyword.append(level_Keywords)
                    # 获取页面数据
                    name_phone_html = name_link_response.text
                    # 获取联系我们链接re
                    p1 = r'<a\b[^>]+\bhref="([^"]*)"[^>]*>联系[\u4e00-\u9fa5][\u4e00-\u9fa5]</a>'
                    pattern1 = re.compile(p1, re.S)
                    matcher1 = re.findall(pattern1, name_phone_html)
                    list_matcher1_url.append(matcher1)
                    # print("%s:%s" % ("level_Keywords", level_Description))
                    # print("%s:%s" % ("公司介绍", level_Keywords))
                    # print("%s:%s" % ("title", title))

                    # print("%s:%s" % ("sign", sign))
                    # print("%s:%s" % ("list_sign", list_sign))
                    # print("%s:%s" % ("matcher1", matcher1))
                    # print("%s:%s" % ("list_matcher1_url", list_matcher1_url))
                    # print("%s:%s" % ("isauth", list_sign))

                time.sleep(2)
                # dict_one["idcaed"] = idcard
            except Exception as e:
                print("出现异常-->" + str(e))
                os.system("./adsl-start.sh")
                # os.system("./adsl-stop.sh")
            continue
                # print(list_Description,list_keyword,list_matcher1_url,list_url)
    return list_Description,list_keyword,list_matcher1_url,list_url, list_sign,title
# 拼接
def jiont(list_matcher1_url,list_url):
    for i in range(len(list_matcher1_url)):
        list_matcher1_url[i] = str(list_matcher1_url[i])
        for j in range(len(list_matcher1_url[i])):
            if list_url[i] + list_matcher1_url[i] not in c:
                c.append(list_url[i] + list_matcher1_url[i])
    # print("c",c)
    # print("%s%s"%("首次拼接", c))
    for i in range(len(c)):
        if "['." in c[i]:
            a = c[i].split("['.")
            t = "http"
            if t in a[1]:
                d.append(a[1])
            else:
                d.append(a[0]+a[1])

        elif "['" in c[i]:
            a = c[i].split("['")
            t= "http"
            if t in a[1]:
                d.append(a[1])
            else:
                d.append(a[0] + a[1])
        elif "[" in c[i]:
            a = c[i].split("[")
            d.append(a[0])

    for i in range(len(d)):
        p1 = r"(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?"
        pattern1 = re.compile(p1)
        matcher1 = re.search(pattern1, d[i])
        q.append(matcher1.group(0))
    # print("q", q)
    return q
# 进入页面
def two_html(q):
    for i in q:
        try:
            headers = dict()
            headers["User-Agent"] = UserAgent().random
            i_response = requests.get(i, headers=headers, timeout=5, verify=False)
            charset = chardet.detect(i_response.content)
            # 获取编码格式
            a = charset["encoding"]
            # 进行编码
            i_response.encoding = a
            # 获取页面源码
            phone_link_html = i_response.text
            phone_link_html = etree.HTML(phone_link_html)

            qq_link = phone_link_html.xpath(".//a/@href")
            p6 = r"\w+://[a-z.]+/[a-z?]+=\d+&[a-zA-Z;]+=[a-z0-9.]+[&a-z;=]*&[a-zA-Z;]+=yes"
            pattern6 = re.compile(p6)
            matcher6 = re.findall(pattern6, ''.join(qq_link))
            list_matcher2_url7.append(matcher6)
            # print("list_matcher2_url7",list_matcher2_url7)
            # for qq in list_matcher2_url7:
            #     p7 = r"[1-9][0-9]{8,11}"
            #     pattern7 = re.compile(p7)
            #     matcher7 = re.findall(pattern7, ''.join(qq))
            #     print("matcher7",matcher7)

            phone_link_html1 = phone_link_html.xpath(".//body//text()")
            # print("phone_link_html", phone_link_html1)
            # re匹配手机数据
            p2 = r'(?:13|14|15|17|18|19)[0-9]{9}'
            pattern2 = re.compile(p2)
            matcher2 = re.findall(pattern2, ','.join(phone_link_html1))
            # print("%s%s"%("手机号：",matcher2))
            list_matcher2_url2.append(matcher2)
            # re匹配邮箱
            p3 = r"\w[-\w.+]*@(?:[A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}"
            # p3 = r"^\w+@[0-9a-zA-z]+\.[com,cn]{1,2}"
            pattern3 = re.compile(p3)
            matcher3 = re.findall(pattern3, ','.join(phone_link_html1))
            list_matcher2_url3.append(matcher3)
            # re匹配座机号
            p4 = r"0\d{2,3}-\d{7,8}"
            pattern4 = re.compile(p4)
            matcher4 = re.findall(pattern4, ','.join(phone_link_html1))
            # print("%s%s"%("手机号：",matcher4))
            list_matcher2_url4.append(matcher4)
            # 匹配qq号
            p5 = r"[1-9]\d{4,10}"

            pattern5 = re.compile(p5, re.I | re.M | re.X)
            matcher5 = re.findall(pattern5, ','.join(phone_link_html1))
            # print("%s%s"%("qq：",matcher5))
            list_matcher2_url5.append(matcher5)
            # print("qq1",list_matcher2_url5)

            time.sleep(2)
        except Exception as e:
            print("出现异常one-->" + str(e))
            os.system("./adsl-start.sh")
            # os.system("./adsl-stop.sh")
            pass

        # continue
    # print("qq_url", qq_url)
    # print("qq2", list_matcher2_url7)
    return list_matcher2_url2,list_matcher2_url3,list_matcher2_url4,list_matcher2_url5,list_matcher2_url7

# qq合并
def qq_merge(list_matcher2_url7,list_matcher2_url5):
    for i in list_matcher2_url7:
        # print("i",i)
        # 匹配QQ号
        p8 = r"[1-9]\d{7,11}"
        pattern8 = re.compile(p8)
        matcher8 = re.findall(pattern8, ''.join(i))
        # print("%s%s"%("qq：",matcher5))
        list_matcher2_url8.append(matcher8)
        # print("list_matcher2_url8",list_matcher2_url8)
        # print("list_matcher2_url8",len(list_matcher2_url8))
    for j in range(len(list_matcher2_url8)):
        # print("list_matcher2_url8",list_matcher2_url8)
        # print("list_matcher2_url8",list_matcher2_url5)
        list_matcher2_url9.append(list_matcher2_url8[j]+list_matcher2_url5[j])
    print("list_matcher2_url9",list_matcher2_url9)
    return list_matcher2_url9


# def storage(list_Description, list_keyword, list_matcher2_url2, list_matcher2_url3,list_matcher2_url4, list_url,list_matcher2_url5,list_sign,new_batch_id,title):
def storage(list_Description, list_keyword, list_matcher2_url2, list_matcher2_url3, list_matcher2_url4, list_url,list_matcher2_url9, list_sign, new_batch_id, title):
    # 创建数据库连接
    myclient = pymongo.MongoClient('localhost', 27017)
    rent_info = myclient['rent_info']  # 给数据库命名
    # rent_info.authenticate("admin","aidb1920")
    mycol = rent_info['search_result']  # 创建表单
    for i in range(len(list_sign)):
        # print("list_matcher2_url8[i]", list_matcher2_url8[i])
        a = list(set(list_matcher2_url9[i]))
        print("a",a)
        # try:
        mydict = {"keyword": ''.join(list_keyword[i]),
                  "domain":"".join(list_url[i]),
                  "tel": ','.join(list_matcher2_url2[i]),
                  "description": ''.join(list_Description[i]),
                  "title":"".join(title[i]),
                  "is_auth":list_sign[i] ,
                  "qq":",".join(a),
                  "email":"".join(list_matcher2_url3[i][:1]),
                  "batch_id":new_batch_id,
                  "phone":",".join(list_matcher2_url4[i][:1]),}
        for j in data:
            if str(j) in mydict["domain"]:
                mydict.clear()
            else:
                pass
            x = mycol.insert_one(mydict)

            print(x)
        # except Exception as e:
        #     print("出现异常two-->" + str(e))
        #     pass




def send_request():
    data = bytes(urllib.parse.urlencode(query_data), encoding='utf8')
    res = urllib.request.urlopen(request_url, data=data)
# server.run(port=1688, debug=True, host='0.0.0.0')



if __name__ == '__main__':
    os.system("./adsl-start.sh")
    # 关键字
    # kw = sys.argv[1]
    kw = "长城"
    # print(kw)
    kw = parse.unquote(kw)

    # start_page = int(input('请输入起始页码：'))
    start_page = 0
    # 老的id
    old_batch_id = 2
    # old_batch_id = sys.argv[2]
    # 新的id
    # new_batch_id = sys.argv[3]
    new_batch_id = 1
    # 结束页码
    end_page = int(1)
    # end_page = int(sys.argv[4])
    print(True)
    # end_page = 1
    # 接收到的
    # start_time = datetime.now()
    # print("开始时间", start_time)
    url = 'https://www.baidu.com/s?wd={}&pn={}&oq=企业站&tn=02003390_8_hao_pg&ie=utf-8&usm=1&rsv_pq=92bde9540006e976&rsv_t=e08941%2F1NIezOJFcUYSWTvFe%2B1AiKpVnQp0dLvegw3EH2Oqk%2FM%2FNEAtDx0imkCDqCFVlt8lFZBE'
    # print(run(url,start_page,end_page,kw,ip_pool))
    # # print(len(run(url,start_page,end_page,kw,ip_pool)))
    # print(jiont(list_matcher1_url,list_url))
    # print(two_html(q, ip_pool))
    # # print(storage(list_Description,list_keyword,list_matcher2_url2))
    # print(list_Description)
    # print(list_sign)
    # print(storage(list_Description, list_keyword, list_matcher2_url2, list_matcher2_url3,list_matcher2_url4,list_url,list_matcher2_url5,list_sign))
    # print(len(list_Description))

    for line in open(r"./shield", "r"):  # 设置文件对象并读取每一行文件
        data.append(line[:-1])
    # request_url = "http://ai.hatidc.com/home/home/getSearchTaskResult"
    # query_data = {"new_batch_id": new_batch_id, "old_batch_id": old_batch_id}
    run(url,start_page,end_page,kw)
    jiont(list_matcher1_url,list_url)
    two_html(q)
    qq_merge(list_matcher2_url7,list_matcher2_url5)
    storage(list_Description, list_keyword, list_matcher2_url2, list_matcher2_url3,list_matcher2_url4, list_url, list_matcher2_url9, list_sign,new_batch_id,title)
    send_request()