# import pycurl
#
# import certifi
#
# # url="https://v.douyin.com/wefLC5/"
# url="https://aweme.snssdk.com/aweme/v1/play/?video_id=v0200f740000bqfv300858lofvtlni90&line=0&ratio=540p&media_type=4&vr_type=0&improve_bitrate=0&is_play_url=1&is_support_h265=0&source=PackSourceEnum_PUBLISH"
# with open("download.txt", 'wb') as f:
#     c = pycurl.Curl()
#     c.setopt(pycurl.USERAGENT,
#              "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")  # 配置请求HTTP头的User-Agent
#     c.setopt(c.URL, url)
#     c.setopt(c.CAINFO, certifi.where())
#     c.setopt(c.WRITEDATA, f)
#     c.perform()
#     c.close()

# Chrome用开发者模拟移动设备打开短链接  https://v.douyin.com/sLvq6P/
# 过滤item_ids字段和dytk字段，组装视频播放url
# 打开里面的play_addr，即可得到无水印视频播放地址，复制url到手机浏览器打开即得无水印视频

# 视频播放长链接组装规则
# "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?
#     item_ids="+item_ids[0]+"&dytk="+dytk[0]

import requests
import re



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
    print("===>复制下面的长链接到手机浏览器打开即可得到无水印视频\n===>" + play_addr)

    return play_addr


get_play_addr("https://v.douyin.com/wed1r3/")
