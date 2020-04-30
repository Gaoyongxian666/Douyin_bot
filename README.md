# 抖音视频下载小助手 V 0.15
### 仅适用于最新版本 抖音 V10.9.0
### 需要电脑和手机，需要手机打开调试  自动化项目   

 * 项目就在douyin.py ,最后使用pyinstaller打包exe，大约19M
 * V0.12 更新无水印   
 * V0.13 修复Android10无法剪贴  https://ww.lanzous.com/ibzphjc 
 * V0.14 抖音app V10.9.0  https://ww.lanzous.com/ic3kbsj   
 * V0.15 抖音app V10.9.0  修复BUG，使用水印下载更稳定 https://ww.lanzous.com/ic4mxpg   


### 项目如何打包 
> 在output 文件夹中有发布的范本，例如打算发布版本V0.13  
> 蓝奏云： https://ww.lanzous.com/ic08qqh

1. 在output中复制一份重命名 douyin_v0.13  
2. 检查pip安装的包 requirements.txt  注意 humanize==0.5.1  
3. 打开命令行，切换到你的环境
4. cd D:\python_project\Douyin_bot\output\douyin_v0.13 
5. 压缩打包：pyinstaller -F -i f.ico D:\python_project\Douyin_bot\douyin.py
6. dist文件夹中是解压出的exe  
> 说明：download文件夹,download.txt不重要，adb等都是重要的不可删除  





 软件截图
 ![image](test/test1.png)

 下载的文件  
 ![image](test/test2.png)
 
 手机被控制的效果  
 ![image](test/test3.gif)

 





                                            抖音视频下载小助手 V 0.11
                    注意：抖音app版本必须是最新版本 V10.8.0  更新时间：2020-4-25
                    Github地址：https://github.com/Gaoyongxian666/Douyin_bot
                    公众号：我的光印象  QQ群：1056916780 下载目录：解压目录/download
                    功能：批量下载（包括本地下载限制）  文件命名：从001开始
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