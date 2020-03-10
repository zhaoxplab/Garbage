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

url = 'http://meishi.meituan.com/i/api/channel/deal/list'

c = 'Cookie: uuid=57f3874ed29d45988631.1571813297.1.0.0; ci=245; rvct=245; meishi_ci=245; cityid=245; cityname=%E5%95%86%E4%B8%98'

head = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Origin': 'http://meishi.meituan.com',
    'Referer': 'http://meishi.meituan.com/i/?ci=245&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1',
    'User-Agent': ua.random,
    'x-requested-with': 'XMLHttpRequest',
    'Cookie': c
}
info = {"uuid":"57f3874ed29d45988631.1571813297.1.0.0","version":"8.2.0","platform":3,"app":"","partner":126,"riskLevel":1,"optimusCode":10,"originUrl":"http://meishi.meituan.com/i/?ci=245&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1","offset":0,"limit":15,"cateId":1,"lineId":0,"stationId":0,"areaId":0,"sort":"default","deal_attr_23":"","deal_attr_24":"","deal_attr_25":"","poi_attr_20043":"","poi_attr_20033":""}

response = session.post(url, headers=head, data=json.dumps(info), verify=False).json()
print(response)
