# 下载
import random
import re
from bs4 import BeautifulSoup
import requests
import time


pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
header_list = [
    #遨游
    {"user-agent" : "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
    #火狐
    {"user-agent" : "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
    #谷歌
    {"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
]




def downloadFile(name, url):
    headers = {'Proxy-Connection': 'keep-alive',
               "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
    r = requests.get(url, stream=True, headers=headers)
    length = float(r.headers['content-length'])
    f = open(name, 'wb')
    count = 0
    count_tmp = 0
    time1 = time.time()
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
            count += len(chunk)
            if time.time() - time1 > 2:
                p = count / length * 100
                speed = (count - count_tmp) / 1024 / 1024 / 2
                count_tmp = count
                print(name + ': ' + formatFloat(p) + '%' + ' Speed: ' + formatFloat(speed) + 'M/S')
                time1 = time.time()
    f.close()


def formatFloat(num):
    return '{:.2f}'.format(num)




with open("douyin.txt","r",encoding="utf8") as f:
    raw_list=f.readlines()
    for raw in raw_list:
        url_list = re.findall(pattern, raw)
        html_url=url_list[0]
        print(html_url)

        header = random.choice(header_list)
        html=requests.get(html_url,headers=header).text

        soup=BeautifulSoup(html,"lxml")

        # #pageletReflowVideo > div > div.info-box.fl > div.video-info > p
        p=soup.select("#pageletReflowVideo > div > div.info-box.fl > div.video-info > p")[0].string
        file_name=p.replace(" ","")
        file_name = re.sub('[\/:*?"<>|]', '-', file_name)

        raw_video=str(soup.find_all("script")[-1])
        print(type(raw_video))
        video_url = re.findall(pattern, raw_video)[0]
        img_url=re.findall(pattern, raw_video)[1]
        print(video_url)
        downloadFile(file_name+".mp4",video_url)
        print(file_name+".mp4：下载完成")

        # time.sleep(1110)


def download2File(self, name, url, iid, article_url, tree):


        tree.item(iid, values=(self.name, size, "下载中"))
        with open("download/"+name, 'wb') as f:
            c = pycurl.Curl()
            c.setopt(c.URL,url)
            c.setopt(c.CAINFO, certifi.where())
            c.setopt(c.NOPROGRESS, False)
            c.setopt(c.XFERINFOFUNCTION, self.progress)
            c.setopt(c.WRITEDATA, f)
            tree.item(iid, values=(name, size, "下载中"))
            c.perform()
        tree.item(iid, values=(name, size, "完成"))

        line_dict = {'url': article_url, 'title': name, "size": size, "speed": "", "state": "完成",
                     "download_url": url,
                     "iid": iid}
        with open("url_list.txt", "r") as f:
            lines = f.readlines()
        with open("url_list.txt", "w") as f_w:
            for line in lines:
                if iid in line:
                    f_w.write(json.dumps(line_dict))
                    f_w.write("\n")
                else:
                    f_w.write(line)
