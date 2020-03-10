import re
import os
import json

def re_test():
    str = """
    <div class="cname"> 
                <a target="_blank" href="/publish/forecast/AHA/zhengzhou.html">郑州</a> 
               </div> 
               <div class="weather">
                 多云 
               </div> 
               <div class="temp">
                34/27℃
               </div> </li> 
              <li> 
               <div class="cname"> 
                <a target="_blank" href="/publish/forecast/AHA/xiayi.html">夏邑</a> 
               </div> 
               <div class="weather">
                 小雨 
               </div> 
               <div class="temp">
                33/27℃
               </div> </li> 
              <li style="padding-right:0;"> 
               <div class="cname"> 
                <a target="_blank" href="/publish/forecast/AHA/shangcaixian.html">上蔡县</a> 
               </div> 
    """
    s = re.findall(r'<a target="_blank" href="(.*?)">(.*?)</a>', str)
    print(s)

# 写入json文件
def write(data):
    info_list = []
    info_list.append(data)
    root = "ShangJia.json"
    if not os.path.exists(root):
        with open(root, "w", encoding='utf-8')as f:
            json.dump(info_list, f, ensure_ascii=False)
            print("success")
            f.close()
        return True
    else:
        with open(root, "w", encoding='utf-8')as f:
            json.dump(info_list, f, ensure_ascii=False)
            print("success")
            f.close()
        return False


if __name__ == '__main__':
    re_test()