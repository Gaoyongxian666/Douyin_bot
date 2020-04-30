# import pycurl
# from bs4 import BeautifulSoup
# import certifi
#
# with open("download.txt", 'wb') as f:
#     c = pycurl.Curl()
#     c.setopt(pycurl.USERAGENT,
#              "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1")  # 配置请求HTTP头的User-Agent
#     c.setopt(c.URL, "https://aweme.snssdk.com/aweme/v1/playwm/?s_vid=93f1b41336a8b7a442dbf1c29c6bbc56dd72b9fd8c74ecbe8363072634fe6cafdbc569c29e701c158887087966aa3865bfd72df7001f2322ebd6f6b54ea9672f&line=0")
#     c.setopt(c.CAINFO, certifi.where())
#     c.setopt(c.WRITEDATA, f)
#     c.perform()
#     c.close()
#
# with open("download.txt","r") as f:
#     line=f.read()
#     print(line)
#     video_soup=BeautifulSoup(line,"lxml")
#     url=video_soup.a["href"]
#     print(url)
#     with open("download2.mp4", 'wb') as f:
#         c = pycurl.Curl()
#         c.setopt(pycurl.USERAGENT,
#                  "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1")  # 配置请求HTTP头的User-Agent
#         c.setopt(c.URL,url)
#         c.setopt(c.CAINFO, certifi.where())
#         c.setopt(c.NOPROGRESS, False)
#         # c.setopt(c.XFERINFOFUNCTION, self.progress)
#         c.setopt(c.WRITEDATA, f)
#         c.perform()
#         c.close()
import re

import requests
from urllib.parse import urlparse
import json

html_url='https://v.douyin.com/wnPsxa/'
header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Mobile Safari/537.36'
}
r=requests.get(html_url, headers=header)
matchObj = re.match(r'.*dytk:.*?"(.*?)".*', r.text, re.M | re.I | re.S)
dytk = matchObj.group(1)

reditList = r.history
last_url=reditList[len(reditList)-1].headers["location"]


path = urlparse(last_url).path
item_ids=path.split("/")[3]
js_url="https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids="+item_ids+"&dytk="+dytk

html=requests.get(js_url, headers=header).text

mydict=json.loads(html)
video_url=mydict["item_list"][0]["video"]["play_addr"]["url_list"][0]




# print(f'获取重定向最终的url：{}')

