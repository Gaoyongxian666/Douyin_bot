import time
import uiautomator2 as u2


d = u2.connect() # alias for u2.connect_wifi('10.0.0.1')
print(d.info)





for i in range(0,111):
    # 向上滑动,获取下一个
    d(resourceId="com.ss.android.ugc.aweme:id/ayy").swipe("up", steps=20)

    # 点击分享按钮
    d(resourceId="com.ss.android.ugc.aweme:id/dbv").click()

    # 一次水平拖不到底
    # 多个水平滚动的
    d(className="android.support.v7.widget.RecyclerView", resourceId="com.ss.android.ugc.aweme:id/az",scrollable=True).fling.horiz.toEnd()
    d(className="android.support.v7.widget.RecyclerView", resourceId="com.ss.android.ugc.aweme:id/az",scrollable=True).fling.horiz.toEnd()

    # 点击复制
    d(text="复制链接").click()

    # 获取链接，好像有延时，所以
    time.sleep(0.3)
    with open("douyin.txt","a+",encoding="utf8") as f:
        raw_url=d.clipboard
        f.write(raw_url+"\n")
        print(raw_url)

