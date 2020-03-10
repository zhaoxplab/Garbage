from wuxiang.Modular import imitate_login
import csv

session = imitate_login()
def r():
    link = 'https://cy.wuuxiang.com/cy7center/dbi/shop/shoptree?_dc=1571211683292&isShowCenter=true&isShowSingleCooperateShop=true&isShowShop=true&limitVersion=&dimensionType=city&bigGroupId=-1&node=root'
    res = session.get(link).json()
    all = res[0]
    for info in all['children'][1:]:
        # print(info)
        city = info['text']
        # print(city)
        for d in info['children']:
            c = d['text']
            w(c, city)

def w(c, city):
    with open('./city.csv', 'a+', encoding='utf-8', newline='') as f:
        write = csv.writer(f)
        write.writerow([c, city])

if __name__ == '__main__':
    r()
    print('success')