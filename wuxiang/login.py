import requests
import urllib3
from fake_useragent import UserAgent
urllib3.disable_warnings()

ua = UserAgent()
"""
head = {'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'cy.wuuxiang.com',
        'Referer': 'https://cy.wuuxiang.com/cy7center/canyin/report/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
        }
url = 'https://cy.wuuxiang.com/cy7center/platform/login/login/logincheck'
data = {
    "shopId": 3451,
    "userName": 6306,
    "passWord": 6306,
    "checkCode": ""
}
session = requests.session()
session.post(url, headers=head, data=data, verify=False)
res = session.get('https://cy.wuuxiang.com/cy7center/canyin/report/').text
print(res)
"""

def imitate_login(link):
    # 创建session对象
    session = requests.session()
    # 请求头
    head = {'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'cy.wuuxiang.com',
            'Referer': 'https://cy.wuuxiang.com/cy7center/canyin/report/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
            }
    # login 页面
    login_url = 'https://cy.wuuxiang.com/cy7center/platform/login/login/logincheck'
    # 登陆及用户信息
    u_info = {
        "shopId": 3451,
        "userName": 6306,
        "passWord": 6306,
        "checkCode": ""
    }
    session.post(login_url, headers=head, data=u_info, verify=False)
    response = session.get(link).text
    return response