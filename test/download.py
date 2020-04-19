import pycurl
from bs4 import BeautifulSoup
import certifi

with open("download.txt", 'wb') as f:
    c = pycurl.Curl()
    c.setopt(pycurl.USERAGENT,
             "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1")  # 配置请求HTTP头的User-Agent
    c.setopt(c.URL, "https://aweme.snssdk.com/aweme/v1/playwm/?s_vid=93f1b41336a8b7a442dbf1c29c6bbc56dd72b9fd8c74ecbe8363072634fe6cafdbc569c29e701c158887087966aa3865bfd72df7001f2322ebd6f6b54ea9672f&line=0")
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.WRITEDATA, f)
    c.perform()
    c.close()

with open("download.txt","r") as f:
    line=f.read()
    print(line)
    video_soup=BeautifulSoup(line,"lxml")
    url=video_soup.a["href"]
    print(url)
    with open("download2.mp4", 'wb') as f:
        c = pycurl.Curl()
        c.setopt(pycurl.USERAGENT,
                 "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1")  # 配置请求HTTP头的User-Agent
        c.setopt(c.URL,url)
        c.setopt(c.CAINFO, certifi.where())
        c.setopt(c.NOPROGRESS, False)
        # c.setopt(c.XFERINFOFUNCTION, self.progress)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()
