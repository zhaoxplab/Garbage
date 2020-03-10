import queue
import os
import csv
import requests
import re

url = "https://www.mzitu.com/all/"

def write(photos_url):
    with open("./Mzitu6.csv", "w", newline="", encoding="utf-8")as csv_file:
        f = csv.writer(csv_file)
        for i in photos_url:
            print(i)
            f.writerow(i)
        csv_file.close()
    print("Scucess")

def read():
    listA = []
    with open("./Mzitu3.csv", newline="", encoding="utf-8")as file:
        for line in file:
            listA.append(line)
    for info in listA:
        # k = info.split(",")[0]
        # j = info.split(",")[1]
        # o = j.strip()
        photos_info = info.strip()
        # photo_page(photos_info)
        # print(photos_info)
        # 套图链接为 photo_info 第一个参数
        photos_link = photos_info.split(",")[0]
        # 套图名为 photo_info 第二个参数
        photos_name = photos_info.split(",", 1)[1]
        print(photos_link, photos_name)

def get_all_url():
    # first_page = requests.get(url)
    # first_code = first_page.text
    # print(first_code)
    listB = []
    with open("./2017.html", newline="", encoding="utf-8")as h:
        for inf in h:
            listB.append(inf.strip())
    # print(listB)
    for gj in listB:
        photos_url_pattern = re.compile(r'<a href="(https://www.mzitu.com/\d+)" target="_blank">(.*?)</a>', re.M | re.S)
        photos_url = re.findall(photos_url_pattern, gj)[0]
        print(photos_url)
        # photo_url.reverse()
        # print(len(photos_url))
        # write(photos_url)
        # for i in photos_url:
        #     print(i)
            # test_queue.put(i)

def writes(photos_url):
    print(type(adta))
    with open("./Mzitu6.csv", "w", newline="", encoding="utf-8")as csv_file:
        f = csv.writer(csv_file)
        f.writerow(photos_url)
    csv_file.close()
    print(photos_url)

test_queue = queue.Queue()
get_all_url()
# if not test_queue.empty():
#     adta = test_queue.get()
#
#
#     writes(adta)
# print("完了")



# if __name__ == '__main__':
    # if not os.path.exists("./Mizitu3.csv"):
    #     get_all_url(url)
    # else:
    #     read()


