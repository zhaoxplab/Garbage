import requests
from fake_useragent import UserAgent
import re
from lxml import etree

url = "http://www.tianqihoubao.com"

url_l = ["/lishi/zhoukou/month/201801.html", "/lishi/zhoukou/month/201802.html", "/lishi/zhoukou/month/201803.html",
         "/lishi/zhoukou/month/201804.html", "/lishi/zhoukou/month/201805.html", "/lishi/zhoukou/month/201806.html",
         "/lishi/zhoukou/month/201807.html", "/lishi/zhoukou/month/201808.html", "/lishi/zhoukou/month/201809.html",
         "/lishi/zhoukou/month/201810.html", "/lishi/zhoukou/month/201811.html", "/lishi/zhoukou/month/201812.html"]

ua = UserAgent()

for u in url_l:
    print(url+u, ua)
    info = requests.get(url+u, headers={"User-Agent": ua.random}).text
    # print(info)
    weather_re = re.compile(r'<tr><td><a href="/\w+/\w+/\d+.[a-zA-Z]+" title=(.*?)>(.*?)</a></td></tr>', re.M | re.S)
    weather = re.findall(weather_re, info)
    for w in weather:
        print(w)