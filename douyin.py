import os
import pycurl
import queue
import sys
from threading import Thread
import certifi
import uiautomator2 as u2
import random
import re
from bs4 import BeautifulSoup
import requests
import time



def downloadFile(name, url):
    headers = {'Proxy-Connection': 'keep-alive',
               "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
    r = requests.get(url, stream=True, headers=headers)
    length = float(r.headers['content-length'])
    f = open("download/" + name, 'wb')
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

                print("\033[1;93m下载视频线程：" + name + ': ' + formatFloat(p) + '%' + ' Speed: ' + formatFloat(
                    speed) + 'M/S' + "\033[0m")
                time1 = time.time()
    f.close()

def formatFloat(num):
    return '{:.2f}'.format(num)


def download2File(name, url):
    with open("download.txt", 'wb') as f:
        c = pycurl.Curl()
        c.setopt(pycurl.USERAGENT,
                 "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1")  # 配置请求HTTP头的User-Agent
        c.setopt(c.URL, url)
        c.setopt(c.CAINFO, certifi.where())
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

    with open("download.txt", "r") as f:
        line = f.read()
        video_soup = BeautifulSoup(line, "lxml")
        url = video_soup.a["href"]
        with open("download/" + name, 'wb') as f:
            c = pycurl.Curl()
            c.setopt(pycurl.USERAGENT,
                     "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1")  # 配置请求HTTP头的User-Agent
            c.setopt(c.URL, url)
            c.setopt(c.CAINFO, certifi.where())
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()


def task():
    time.sleep(2)
    flag=1
    mflag=0
    while flag:
        if not q.empty():
            line = q.get()
            try:
                url_list = re.findall(pattern, line)
                html_url = url_list[0]
                header = random.choice(header_list)
                html = requests.get(html_url, headers=header).text

                soup = BeautifulSoup(html, "lxml")

                # #pageletReflowVideo > div > div.info-box.fl > div.video-info > p
                p = soup.select("#pageletReflowVideo > div > div.info-box.fl > div.video-info > p")[0].string
                file_name = p.replace(" ", "")
                file_name = re.sub('[\/:*?"<>|]', '-', file_name)

                raw_video = str(soup.find_all("script")[-1])
                video_url = re.findall(pattern, raw_video)[0]
                img_url = re.findall(pattern, raw_video)[1]
                download2File(file_name + ".mp4", video_url)
                print("\033[1;93m下载视频线程：" + file_name + ".mp4：下载完成" + "\033[0m")
            except:
                print("下载视频线程：" + line + "下载失败")
            mflag=0

        else:
            print("\033[1;93m下载视频线程：当前下载队列为空" + "\033[0m")
            if mflag==1:
                flag=0
            mflag=mflag+1
            time.sleep(10)


if __name__ == "__main__":
    print("设置ADB环境变量。。。。")
    # line = os.path.dirname(sys.argv[0]) + r'/adb.exe  devices'
    # os.system("cd " + sys.argv[0])
    work_dir=os.path.dirname(sys.argv[0])
    print(work_dir)
    os.chdir(work_dir)
    line = 'adb.exe  devices'
    print(line)
    os.system(line)
    q = queue.Queue()
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    header_list = [
        # 遨游
        {"user-agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
        # 火狐
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
        # 谷歌
        {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
    ]

    if not os.path.exists("download"):
        os.mkdir("download")

    print('''
************************************************************************************************************************
                                            抖音视频下载小助手 V 0.1
                    Github地址：
                    公众号：我的光印象  QQ群：1056916780
                    功能：他人作品，他人喜欢，自己作品，自己喜欢，设置本地下载限制的
                    注意：抖音app版本必须是最新版本 V10.7.0  更新时间：2020-4-19
                    特点：因为是模拟手机操作，本软件可以一直使用，除非你进行了抖音APP升级。
                    说明：本软件基于开源项目uiautomator2项目，所以本项目也是开源的，自己也可进行更改，项目很简单。

                    使用方法：
                    1.初始化：手机打开调试模式，在首次运行本软件出现弹框点击一直允许，USB计算机连接选择传输文件
                    2.首次运行会弹出需要安装2个APP，点击安装,这两个APP都是开源项目可以保证安全性。第一次由于
                    需要初始化，所以比较慢，以后运行不需要这一步会很快的。当看到"设备连接成功"，说明设备初始化成功。
                    
                    3.开始下载：打开本软件之后第一件事是打开第一个视频（原理是从当前视频开始向上滑动一个一个下载，
                    下滑的次数即下载个数），必须输入视频数量（在自己的主页或者他人主页可以看到数量，或者自定义）
************************************************************************************************************************
    ''')

    num = input("本次下载视频的数量（不输入默认20，输入完回车,记得看使用方法）：")
    d = u2.connect()
    print(d.info)
    print("设备连接成功！")
    if num != "":
        num = int(num) + int(num) % 10
        print(num)
    else:
        num = 20

    p = Thread(target=task)
    p.start()

    for i in range(num):
        # 点击分享按钮
        d(resourceId="com.ss.android.ugc.aweme:id/dbx").click()

        # 一次水平拖不到底
        # 多个水平滚动的
        d(className="android.support.v7.widget.RecyclerView", resourceId="com.ss.android.ugc.aweme:id/az",
          scrollable=True).fling.horiz.toEnd()
        d(className="android.support.v7.widget.RecyclerView", resourceId="com.ss.android.ugc.aweme:id/az",
          scrollable=True).fling.horiz.toEnd()

        # 点击复制
        d(text="复制链接").click()

        # 获取链接，好像有延时，所以
        time.sleep(0.3)
        raw_url = d.clipboard
        print("\033[1;36m获取分享链接：" + raw_url + "\033[0m")
        q.put(raw_url)

        # 向上滑动,获取下一个
        d(resourceId="com.ss.android.ugc.aweme:id/bam").swipe("up", steps=14)
    os.system("pause")

# 适用于最新版本 抖音V10.7.0 版本
# 不是这个版本的使用不了，因为抖音每个版本APP控件的ID会有一定变化
# 主要是这两个 d(resourceId="com.ss.android.ugc.aweme:id/bam").swipe("up", steps=20)     d(resourceId="com.ss.android.ugc.aweme:id/dbx").click()
# 根据输入的视频数量做程序终止判断
