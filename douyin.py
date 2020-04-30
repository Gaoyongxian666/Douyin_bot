import os
import pycurl
import queue
import sys
import traceback
from threading import Thread
import certifi
import uiautomator2 as u2
import random
import re
from bs4 import BeautifulSoup
import requests
import time
import requests
from urllib.parse import urlparse
import json


def get_play_addr(input_url):
    headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }


    # 请求短链接，获得itemId和dytk
    get = requests.get(input_url, headers=headers)
    html = get.content

    itemId = re.findall(r"(?<=itemId:\s\")\d+", str(html))
    dytk = re.findall(r"(?<=dytk:\s\")(.*?)(?=\")", str(html))

    # 组装视频长链接
    videourl = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + itemId[0] + "&dytk=" + dytk[0]

    # 请求长链接，获取play_addr
    videoopen = requests.get(videourl, headers=headers)
    vhtml = videoopen.text
    uri = re.findall(r'(?<=\"uri\":\")\w{32}(?=\")', str(vhtml))

    # 长链接的格式其实是固定的，唯一变动的就是video_id，上面提取出uri后进行组装即可得到最终链接
    play_addr = "https://aweme.snssdk.com/aweme/v1/play/?video_id=" + uri[0] + \
                "&line=0&ratio=540p&media_type=4&vr_type=0&improve_bitrate=0&is_play_url=1&is_support_h265=0&source=PackSourceEnum_PUBLISH"
    return play_addr


# video_url 是带水印的
#         c.setopt(c.URL, play_addr)
def download2File(name, video_url,html_url):
    play_addr=get_play_addr(html_url)
    with open("download.txt", 'wb') as f:
        c = pycurl.Curl()
        c.setopt(pycurl.USERAGENT,
                 "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")  # 配置请求HTTP头的User-Agent
        c.setopt(c.URL, play_addr)
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
                     "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")  # 配置请求HTTP头的User-Agent
            c.setopt(c.URL, url)
            c.setopt(c.CAINFO, certifi.where())
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()


def downloadFile(name, video_url,html_url):
    play_addr=video_url
    with open("download.txt", 'wb') as f:
        c = pycurl.Curl()
        c.setopt(pycurl.USERAGENT,
                 "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")  # 配置请求HTTP头的User-Agent
        c.setopt(c.URL, play_addr)
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
                     "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")  # 配置请求HTTP头的User-Agent
            c.setopt(c.URL, url)
            c.setopt(c.CAINFO, certifi.where())
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()

def fileNum(path):
    fileNum=0
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        if os.path.isfile(sub_path):
            fileNum = fileNum + 1  # 统计文件数量
    return fileNum

def android10_task(warter):
    time.sleep(2)
    flag=1
    mflag=0
    while flag:
        if not q.empty():
            line = q.get()
            try:
                url_list = re.findall(pattern, line)
                html_url = url_list[0]
                # print(url_list)

                header = random.choice(header_list)
                r = requests.get(html_url, headers=header)

                matchObj = re.match(r'.*dytk:.*?"(.*?)".*', r.text, re.M | re.I | re.S)
                dytk = matchObj.group(1)

                reditList = r.history
                last_url = reditList[len(reditList) - 1].headers["location"]

                path = urlparse(last_url).path
                item_ids = path.split("/")[3]
                js_url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + item_ids + "&dytk=" + dytk

                html = requests.get(js_url, headers=header).text

                mydict = json.loads(html)
                video_url = mydict["item_list"][0]["video"]["play_addr"]["url_list"][0]

                matchObj = re.match(r'(.*)data="(.*?)https.*', line, re.M | re.I |re.S)
                # print(matchObj)
                p=matchObj.group(2)

                # #pageletReflowVideo > div > div.info-box.fl > div.video-info > p
                # #pageletReflowVideo > div > div.info-box.fl > div.video-info > p
                # p = soup.select("#pageletReflowVideo > div > div.info-box.fl > div.video-info > p")[0].string
                file_name = p.replace(" ", "")
                file_name=file_name.strip()
                file_name = re.sub('[\/:*?"<>|]', '-', file_name)
                # #theVideo


                myfileNum = fileNum("download")
                k = "%03d" % (myfileNum + 1)
                if warter=="y":
                    download2File( str(k)+file_name + ".mp4", video_url,html_url)
                else:
                    downloadFile( str(k)+file_name + ".mp4", video_url,html_url)

                print("\033[1;93m下载视频线程：" + file_name + ".mp4：下载完成" + "\033[0m")
            except:
                print(traceback.format_exc())
                print("下载视频线程：" + line + "下载失败")
            mflag=0

        else:
            print("\033[1;93m下载视频线程：当前下载队列为空" + "\033[0m")
            if mflag==5:
                flag=0
            mflag=mflag+1
            time.sleep(10)
    os.system("pause")


def task(warter):
    time.sleep(2)
    flag=1
    mflag=0
    while flag:
        if not q.empty():
            line = q.get()
            try:
                url_list = re.findall(pattern, line)
                html_url = url_list[0]
                # print(url_list)

                header = random.choice(header_list)
                r = requests.get(html_url, headers=header)

                matchObj = re.match(r'.*dytk:.*?"(.*?)".*', r.text, re.M | re.I | re.S)
                dytk = matchObj.group(1)

                reditList = r.history
                last_url = reditList[len(reditList) - 1].headers["location"]

                path = urlparse(last_url).path
                item_ids = path.split("/")[3]
                js_url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=" + item_ids + "&dytk=" + dytk

                html = requests.get(js_url, headers=header).text

                mydict = json.loads(html)
                video_url = mydict["item_list"][0]["video"]["play_addr"]["url_list"][0]


                matchObj = re.match(r'(.*)https.*', line, re.M | re.I |re.S)
                # print(matchObj)
                p=matchObj.group(1)

                # #pageletReflowVideo > div > div.info-box.fl > div.video-info > p
                # #pageletReflowVideo > div > div.info-box.fl > div.video-info > p
                # p = soup.select("#pageletReflowVideo > div > div.info-box.fl > div.video-info > p")[0].string
                file_name = p.replace(" ", "")
                file_name=file_name.strip()
                file_name = re.sub('[\/:*?"<>|]', '-', file_name)


                myfileNum = fileNum("download")
                k = "%03d" % (myfileNum + 1)
                if warter=="y":
                    download2File( str(k)+file_name + ".mp4", video_url,html_url)
                else:
                    downloadFile( str(k)+file_name + ".mp4", video_url,html_url)
                print("\033[1;93m下载视频线程：" + file_name + ".mp4：下载完成" + "\033[0m")
            except:
                print(traceback.format_exc())
                print("下载视频线程：" + line + "下载失败")
            mflag=0

        else:
            print("\033[1;93m下载视频线程：当前下载队列为空" + "\033[0m")
            if mflag==5:
                flag=0
            mflag=mflag+1
            time.sleep(10)
    os.system("pause")



def android10_do(warter):
    app_list=d.app_list_running()
    if "ca.zgrs.clipper" not in app_list:
        d.app_install("https://github.com/majido/clipper/releases/download/v1.2.1/clipper.apk")
    print("开始下载：请先打开第一个要下载的视频（可以暂停）")
    if d.app_current()["package"]!="com.ss.android.ugc.aweme":
        print("\033[1;91m开始下载：请先打开抖音APP，然后输入下载视频数量"+ "\033[0m")
    num = input("开始下载：本次下载视频的数量（不输入默认20，输入完回车）：")
    print(
        "***************************************************************************************************************************")

    if num != "":
        num = int(num) + int(num) % 10
    else:
        num = 20

    p = Thread(target=android10_task,args=(warter,))
    p.start()

    for i in range(num):
        try:
            # 点击分享按钮
            d(resourceId="com.ss.android.ugc.aweme:id/dbv").click()

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


            d.app_start("ca.zgrs.clipper",wait=True)
            result=d.adb_shell("am broadcast -a clipper.get")
            d.app_start("com.ss.android.ugc.aweme",wait=True)

            # raw_url = d.jsonrpc.getClipboard()
            # print(raw_url)
            print("\033[1;36m获取分享链接：" + result + "\033[0m")
            q.put(result)

            # raw_url=result
            # if raw_url not in raw_url_list:
            #     raw_url_list.append(raw_url)
            #     q.put(raw_url)
            # else:
            #     print("\033[1;36m获取分享链接：获取分享链接重复" + "\033[0m")

            # 向上滑动,获取下一个
            d(resourceId="com.ss.android.ugc.aweme:id/b0q").swipe("up", steps=14)
        except Exception:
            print(traceback.format_exc())
            print("\033[1;36m获取分享链接：获取分享链接失败" + "\033[0m")
            time.sleep(4)

def do(warter):
    print("开始下载：请先打开第一个要下载的视频（可以暂停）")
    if d.app_current()["package"]!="com.ss.android.ugc.aweme":
        print("\033[1;91m开始下载：请先打开抖音APP，然后输入下载视频数量"+ "\033[0m")
    num = input("开始下载：本次下载视频的数量（不输入默认20，输入完回车）：")
    print(
        "***************************************************************************************************************************")

    if num != "":
        num = int(num) + int(num) % 10
    else:
        num = 20

    p = Thread(target=task,args=(warter,))
    p.start()

    for i in range(num):
        try:
            # 点击分享按钮
            d(resourceId="com.ss.android.ugc.aweme:id/dbv").click()

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


            # d.app_start("ca.zgrs.clipper",wait=True)
            # result=d.adb_shell("am broadcast -a clipper.get")
            # d.app_start("com.ss.android.ugc.aweme",wait=True)

            raw_url = d.jsonrpc.getClipboard()
            # print(raw_url)
            # raw_url_list.append(raw_url)
            print("\033[1;36m获取分享链接：" + raw_url + "\033[0m")
            q.put(raw_url)

            # if raw_url not in raw_url_list:
            #     raw_url_list.append(raw_url)
            #     q.put(raw_url)
            # else:
            #     print("\033[1;36m获取分享链接：获取分享链接重复" + "\033[0m")
            # 向上滑动,获取下一个
            d(resourceId="com.ss.android.ugc.aweme:id/b0q").swipe("up", steps=14)
        except Exception:
            print(traceback.format_exc())
            print("\033[1;36m获取分享链接：获取分享链接失败" + "\033[0m")
            time.sleep(4)


if __name__ == "__main__":
    raw_url_list=[]
    # print("设置ADB环境变量。。。。")
    work_dir=os.path.dirname(sys.argv[0])
    os.chdir(work_dir)
    line = 'adb.exe  devices'
    os.popen(line)
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
***************************************************************************************************************************
                                            抖音视频下载小助手 V 0.15
                    注意：抖音app版本必须是最新版本 V10.9.0  更新时间：2020-4-30
                
                    Github地址：https://github.com/Gaoyongxian666/Douyin_bot
                    公众号：我的光印象  QQ群：1056916780 下载目录：解压目录/download
                    功能：批量下载（包括本地下载限制） 无水印   文件命名：从001开始,
                    说明：本软件基于开源项目uiautomator2项目，本项目也是开源的，可自行更改，就是个简单的自动化项目。
                    原理：是从当前视频开始，模拟操作向上滑动获取分享链接，然后通过电脑一个一个下载，（下滑的次数
                    即下载个数），必须输入视频数量（在自己的主页或者他人主页可以看到数量，或者自定义）

                    环境搭建：
                    1.打开USB调试，USB计算机连接选择传输文件 
                    2.安装两个APP ，最后出现：设备连接成功
                    
                    开始下载：
                    3.打开第一个要下载的视频（可以暂停）  
                    4.最后输入要下载的视频个数  最后出现：看到电脑控制手机

                    使用方法：
                    1.初始化：手机打开调试模式，在首次运行本软件出现弹框点击一直允许，USB计算机连接选择传输文件
                    2.首次运行会弹出需要安装2个APP，点击安装,这两个APP都是开源项目可以保证安全性。第一次由于
                    需要初始化，所以比较慢，以后运行不需要这一步会很快的。当看到"设备连接成功"，说明设备初始化成功。
                    
                    3.开始下载：打开本软件之后第一件事是打开第一个视频（原理是从当前视频开始向上滑动一个一个下载，
                    下滑的次数即下载个数），必须输入视频数量（在自己的主页或者他人主页可以看到数量，或者自定义）
***************************************************************************************************************************''')
    try:
        print("环境搭建：测试连接中。。")
        d = u2.connect()
        print(d.device_info)
        print("环境搭建：设备连接成功！")
        print("***************************************************************************************************************************")
        android  = input("开始下载：android版本是否是10以上（y/n）：")
        water  = input("开始下载：是否下载无水印：默认带水印，带水印稳定性高（y/n）：")

        if android=="y":
            android10_do(water)
        else:
            do(water)

    except :
        print("环境搭建：测试连接失败")
        os.system("pause")





