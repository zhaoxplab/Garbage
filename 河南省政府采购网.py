import requests
from lxml import etree
import re

url = "http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0101&bz=0&pageSize=20&pageNo=4"

field = "http://www.hngp.gov.cn"

user_agent = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
       "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/64.0"]
IProxy = [{'http': '119.101.114.249:9999'},
          {'http': '144.123.69.12:35677'},
          {'http': '119.101.117.139:9999'},
          {'http': '119.101.118.4:9999'}]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/64.0"
        }

res = requests.get(url, headers=headers).text
# print(res)
html = etree.HTML(res)
times = html.xpath('//li/span/text()')
links = html.xpath('//li/a/@href')
titles = html.xpath('//li/a/text()')
#print(times, links, titles)
for time, link, title in zip(times, links, titles):
    print(time, link, title)

    page = requests.get(field+link, headers=headers).text
    o = etree.HTML(page)
    cont = html.xpath('//div[@id="content"]/text()')
    print(cont)


