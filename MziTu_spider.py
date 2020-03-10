import queue
import threading
import requests
import os
import re
import time
from fake_useragent import UserAgent

# https://cn.pornhub.com/view_video.php?viewkey=ph5c3da39c1434b
ua = UserAgent()
session = requests.session()

url = "https://www.mzitu.com/all/"
proxy = {'https': 'https://60.13.42.3:9999'}
ts = int(time.time())
c = 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c={0}; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c={1}'
head1 = {
            'Host': 'i5.meizitu.net',
            "User-Agent": ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
exitFlag = 0

class MyThread(threading.Thread):
    def __init__(self, threadID, name, que):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.que = que
        self.headers = {
            'Host': 'www.mzitu.com',
            "User-Agent": ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': c.format(ts, ts),
            'Upgrade-Insecure-Requests': '1'
        }
        self.proxy = {'https': '60.13.42.3:9999'}
        pass

    def run(self):
        print("开启线程：" + self.name)
        photo_page(self.name, self.que, self.headers)
        print("Exiting ", self.name)


def photo_page(name, photos_info_queue, head):
    while not exitFlag:
        queueLock.acquire()
        if not photos_info_queue.empty():
            photos_info = photos_info_queue.get()
            queueLock.release()
            print(photos_info)
            # 套图链接为 photo_info 第一个参数e
            photos_link = photos_info[0]
            # 套图名为 photo_info 第二个参数
            photos_name = photos_info[1].replace(":", " ").replace("?", "")
            # 请求套图页面
            time.sleep(5)
            img_page = session.get(photos_link, headers=head).text
            print(name + "即将开始下载>>>" + photos_name)
            # 正则匹配页面图片数量
            img_pattern = re.compile(r'<div class="pagenavi">(.*?)</div>', re.M | re.S)
            kk = re.findall(img_pattern, img_page)
            for last in kk:
                # print(next)
                # 匹配页面图片链接
                last_pattern = re.compile(r'https://www.mzitu.com/\d+/\d+')
                last_link = re.findall(last_pattern, last)
                # 倒数第二个是最后一张图片链接
                last_photo = last_link[-2]
                # print(last_photo)
                # 图片页码
                last_page = last_photo.split('/')[-1]
                #
                for i in range(1, int(last_page) + 1):
                    # 拼接需要请求页面的 url
                    img_url = photos_link + "/" + str(i)
                    # 标记
                    down(img_url, photos_name)
            print("{0}>>>下载完成".format(photos_name))
        else:
            queueLock.release()
        time.sleep(1)


def down(img_url, photos_name):
    print(img_url)
    photo_info = requests.get(img_url, headers=head1).text
    print(photo_info)
    # 匹配所有图片地址
    img_pattern = re.compile(r'https://i5.meizitu.net/\d+/\d+/[a-z0-9-]+.[a-zA-Z]+')
    lujing = re.findall(img_pattern, photo_info)
    # 图片下载地址
    path = lujing[0]

    img_name = path.split('/')[-1]

    download(path, img_name, photos_name)


def download(path, img_name, photos_name):
    mouth = path.split('/')[-2]
    year = path.split('/')[-3]
    root = "D:\Coding\MziTu" + "\\" + year + "\\" + mouth + "\\" + photos_name

    if not os.path.exists(root):
        os.makedirs(root)
        print("{}>>创建成功".format(root))
        return True
    else:
        with open(root + "\\" + img_name, "wb")as f:
            data = session.get(path)
            f.write(data.content)
            print("{0}>>保存成功".format(path))
            f.close()
        return False


crawlList = ["crawl-1", "crawl-2", "crawl-3", "crawl-4", "crawl-5", "crawl-6", "crawl-7", "crawl-8"]

# first_page = requests.get(url)
# first_code = first_page.text
# # print(first_code)
# # 获得所有的 url
# photos_url_pattern = re.compile(r'<a href="(https://www.mzitu.com/\d+)" target="_blank">(.*?)</a>', re.M | re.S)
# photos_url = re.findall(photos_url_pattern, first_code)
# print(len(photos_url))

listA = []
with open("./2019.html", newline="", encoding="utf-8")as h:
    for inf in h:
        photos_url_pattern = re.compile(r'<a href="(https://www.mzitu.com/\d+)" target="_blank">(.*?)</a>', re.M | re.S)
        photos_url = re.findall(photos_url_pattern, inf)[0]
        # print(photos_url)
        listA.append(photos_url)

queueLock = threading.Lock()
photos_info_queue = queue.Queue()
threads = []
threadID = 1
#创建新线程
for name in crawlList:
    thread = MyThread(threadID, name, photos_info_queue)
    thread.start()
    threads.append(thread)
    threadID += 1

queueLock.acquire()
# for photo_info in photos_url:
#     print(photo_info)
#     photos_info_queue.put(photo_info)

for gj in listA:
    # print(gj)
    photos_info_queue.put(gj)

queueLock.release()

while not photos_info_queue.empty():
    pass
exitFlag = 1

for t in threads:
    t.join()
print("退出主线程")
