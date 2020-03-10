from selenium import webdriver
# 指定火狐路径模块
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import requests
from fake_useragent import UserAgent
import urllib3
urllib3.disable_warnings()

ua = UserAgent()
def get_cookie_s():
    url = "http://i.meituan.com/yantai/"
    # 指定火狐路径
    fire_path = FirefoxBinary(r'D:\Application\Mozilla Firefox\firefox.exe')
    browser = webdriver.Firefox(firefox_binary=fire_path)

    try:
        browser.get(url)
        time.sleep(3)
        cookie_list = browser.get_cookie(url)
        for cookie in cookie_list:
            cookie_dict[cookie['name']] = cookie['value']
        time.sleep(5)
        browser.close()
    except:
        browser.quit()

def get_cookie():
    url = "https://cy.wuuxiang.com/cy7center/canyin/report/a10lv1/a10?type=detail&_dc=1565946540122&data=%7B%22mngType%22%3A%22%22%2C%22dateType%22%3A%22thisYear%22%2C%22dateInterval%22%3A%22%22%2C%22beginDate%22%3A%222019-01-01%22%2C%22beginTime%22%3A%2210%3A00%22%2C%22endDate%22%3A%222020-01-01%22%2C%22endTime%22%3A%2210%3A00%22%2C%22shift%22%3A%22%22%2C%22week%22%3A%22%22%2C%22sellType%22%3A%22%22%2C%22pointType%22%3A%22%22%2C%22invoiceState%22%3A%22%22%2C%22city%22%3A%22150%22%2C%22brand%22%3A%22%22%2C%22shop%22%3A%2210970%22%2C%22areas%22%3A%22%22%2C%22pos%22%3A%22%22%2C%22payway%22%3A%22%22%2C%22paywayType%22%3A%22%22%2C%22curEmp%22%3A%22%5Cu8d75%5Cu7fd4%5Cu9e4f%22%2C%22curShop%22%3A%22%5Cu6cb3%5Cu5357%5Cu5df4%5Cu5e84%5Cu9910%5Cu996e%5Cu7ba1%5Cu7406%5Cu6709%5Cu9650%5Cu516c%5Cu53f8%22%2C%22cityNames%22%3A%22%5Cu6d1b%5Cu9633%5Cu5e02%22%2C%22shopNames%22%3A%22%5Cu5b9c%5Cu9633%5Cu5e97%22%7D&lv=2&DIMProperty=shopDms&paramId=10970&page=3&start=50&limit=25"
    head = {'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': c,
            'Host': 'cy.wuuxiang.com',
            'Referer': 'https://cy.wuuxiang.com/cy7center/canyin/report/',
            'User-Agent': ua.random,
            'X-Requested-With': 'XMLHttpRequest'
            }
    coo = requests.get(url, headers=head).cookies
    # if coo.status_code == 200:
    #     print(coo.cookies)
    #     for cookie in coo.cookies:
    #         print(cookie)
    cookiedict = requests.utils.dict_from_cookiejar(coo)
    print(coo)
    print(type(coo))
    print(cookiedict)

if __name__ == '__main__':
    get_cookie()
