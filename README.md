musicPlayer
===========
你需要修改config.ini中的mp3路径

Dependencies
============
需要configparser 库

eassy_install configparse

本代码在python3.3 +qt5.1上开发，均为64位

图片都为图片格式，未转二进制，方便大家好看哈，各位看官可自行改着玩就好了


打包成EXE
============
1、如果你要打包成EXE你将需要cx_Freeze包

2、打包完成后你需要 将mediaservice文件夹复制到你打包好的程序位置

3、mediaservice为QT的，你可以从你本面上复制 ，如（C:\Python33\Lib\site-packages\PyQt5\plugins\mediaservice）

4、还要将img文件夹和config.ini文件复制到你打包好的位置

5、打包

5.1 在CMD里运行python setup.py install --install-exe exedist



未完成功能
============
1、清空列表

2、添加目录

3、添加文件

4、解析图片


已完成功能
============
1、播放系列操作

2、记录播放内容（第二次打开接上次关闭时的状态）

3、各按钮状态

4、预览功能（列表中的歌曲每首放10秒）

5、单曲循环

6、随机播放/顺序播放

7、静音状态显示

8、点击列表播放

9、预览时状态




