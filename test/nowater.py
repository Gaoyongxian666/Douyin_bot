# Chrome用开发者模拟移动设备打开短链接  https://v.douyin.com/sLvq6P/
# 过滤item_ids字段和dytk字段，组装视频播放url
# 打开里面的play_addr，即可得到无水印视频播放地址，复制url到手机浏览器打开即得无水印视频

# 视频播放长链接组装规则
# "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?
#     item_ids="+item_ids[0]+"&dytk="+dytk[0]

import requests
import re

# 设置浏览器代{过}{滤}理，一定要是移动设备，安卓/iOS均可
headers = {
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}

print("===>欢迎使用抖音视频去水印提取工具")
print("===>请输入抖音链接中的短链接（eg：https://v.douyin.com/sLvq6P/）")
input_url = input("===>")
# 根据粘贴的分享内容，提取视频短链接
preurl = re.findall(r'(?<=douyin.com\/)\w+\/', input_url, re.I | re.M)

# print("https://v.douyin.com/"+preurl[0])
# 组装短链接url
url = "https://v.douyin.com/" + preurl[0]

# 请求短链接，获得itemId和dytk
get = requests.get(url, headers=headers)
html = get.content
# print(html)
itemId = re.findall(r"(?<=itemId:\s\")\d+", str(html))
# print(itemId[0])
dytk = re.findall(r"(?<=dytk:\s\")(.*?)(?=\")", str(html))
# print(dytk[0])

# 组装视频长链接
videourl = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?\
item_ids=" + itemId[0] + "&dytk=" + dytk[0]
# print(videourl)

# 请求长链接，获取play_addr
videoopen = requests.get(videourl, headers=headers)
vhtml = videoopen.text
# print(vhtml)
uri = re.findall(r'(?<=\"uri\":\")\w{32}(?=\")', str(vhtml))
# print(uri[0])

# 长链接的格式其实是固定的，唯一变动的就是video_id，上面提取出uri后进行组装即可得到最终链接
play_addr = "https://aweme.snssdk.com/aweme/v1/play/?video_id=" + uri[0] + \
            "&line=0&ratio=540p&media_type=4&vr_type=0&improve_bitrate=0&is_play_url=1&is_support_h265=0&source=PackSourceEnum_PUBLISH"
print("===>复制下面的长链接到手机浏览器打开即可得到无水印视频\n===>" + play_addr)

# 自定义文件名保存短视频
name = input("===>正在下载保存视频,请输入视频名称：")
video = requests.get(url=play_addr, headers=headers)
with open(name + ".mp4", 'wb')as file:
    file.write(video.content)
    file.close()
    print("===>视频下载完成！")

# 完事后退出程序
input("===>press enter key to exit!")