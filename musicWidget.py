__author__ = 'liaojie'
#!/usr/bin/env python
#coding:utf-8
from PyQt5.QtCore import (QPointF, QRect, QRectF,Qt,QTimer,pyqtSignal,pyqtSlot,QUrl)
from PyQt5.QtWidgets import (QWidget,QListWidget,QLineEdit,QFileDialog ,QApplication)
from PyQt5.QtGui import (QPainter,QImage,QPolygonF,QPen,QFont,QColor,QDesktopServices)
from PyQt5.QtMultimedia import (QMediaMetaData)
import time

import colors

class MusicWidget(QWidget):
    clicked = pyqtSignal(str)
    def __init__(self,homeAction, parent=None):
        super(MusicWidget, self).__init__(parent)
        #载入控制
        self.homeAction = homeAction
        #窗口rect
        self.setGeometry(QRect(0,53,800,374))
        #设置背景透明无边框
        self.setStyleSheet("background: transparent;border:none;")
        #设置背景颜色
        #self.setStyleSheet("background-color:#eac715;")
        #设置窗口计时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(120)

        #==>载入按钮坐标
        self.setMousePot()
        #歌曲列表界面
        self.tracksList = TracksList(self)

        #print(self.homeAction.fileList,"\n",  self.homeAction.randomList)
    ##计算桌面矩型
    #def countWwindowRect(self):
    #    #获取系统桌面尺寸大小
    #    desktop = QApplication.desktop()
    #    screenRect = desktop.screenGeometry(desktop.primaryScreen())
    #    #窗口默认尺寸
    #    windowRect = QRect(0, 0, 800,480)
    #    #如果系统桌面宽小于默认值，窗口宽度将被设为系统桌面的宽度
    #    if screenRect.width() < 800:
    #        windowRect.setWidth(screenRect.width())
    #    #如果系统桌面高小于默认值，窗口高度将被设为系统桌面的高度
    #    if screenRect.height() < 480:
    #        windowRect.setHeight(screenRect.height())
    #    #移动中心点为系统中心点
    #    windowRect.moveCenter(screenRect.center())
    #    self.windowRect = windowRect

        ##设置按钮焦点
        #self.setMousePot()

        ##播放(排序ID)
        #self.soundID=0
        ##播放表序
        #self.queue=[]

        #-------<
        #self.filePath=filePath
        #self.fileList = fileList
        #print(self.fileList)
        #self.config=configparser.ConfigParser()
        #self.config.read('config.ini')



        #self.playerObj = pyglet.media.Player()
        #self.sourceList = []
        #for filename in self.fileList:
        #     source = pyglet.media.load(self.filePath + filename)
        #     self.sourceList.append(source)
        #     self.playerObj.queue(source)
        #self.playStart(70)
        #------>

        #event
        #self.eventAction =EventAction(self)



    def setMousePot(self):
        #按钮焦点
        self.buttonCoordinate=[]
        self.buttonCoordinate.append(QRectF(50,272,410,10))#播放轨道焦点范围
        self.buttonCoordinate.append(QRectF(531,1,75,39))#预览按钮焦点
        self.buttonCoordinate.append(QRectF(607,1,75,39))#随机按钮焦点
        self.buttonCoordinate.append(QRectF(683,1,74,39))#循环按钮焦点
        self.buttonCoordinate.append(QRectF(760,1,38,27))#列表向上焦点
        self.buttonCoordinate.append(QRectF(760,345,38,27))#列表向下焦点
        self.buttonCoordinate.append(QRectF(531,334,75,39))#清空列表焦点
        self.buttonCoordinate.append(QRectF(607,334,75,39))#增加文件焦点
        self.buttonCoordinate.append(QRectF(683,334,74,39))#增加文件夹

    #鼠标按下焦点事件
    def mousePressEvent(self, event):
        #print("音乐界面按鼠标：")
        for(i,rect) in enumerate(self.buttonCoordinate):
            if self.checkCoordinate(rect,event.pos()):
                self.eventHandle(i,event)
    #
    def mouseDoubleClickEvent(self, QMouseEvent):
        print("鼠标双击")
    def mouseMoveEvent(self, QMouseEvent):
        print("鼠标移动")
    def mouseReleaseEvent(self, QMouseEvent):
        print("鼠标释放")

    #检查鼠标按下时是否在铵钮的坐标上
    def checkCoordinate(self,a,b):
        startX =a.x()
        endX = a.x()+a.width()
        startY = a.y()
        endY = a.y()+a.height()
        if b.x() >= startX and b.x() <= endX and b.y() >= startY and b.y() <= endY:
            return True

    #按钮事件
    def eventHandle(self,eventID,event):
        if eventID == 0:
            print("移动播放轨道进度",event.pos().x())
            # #当前歌曲（总长）
            # print(self.homeAction.playObj.duration()/1000)
            # totalDuration = int(self.homeAction.playObj.duration()/1000)
            # #当前歌曲(已播放时间)
            # pastTime = int(self.homeAction.playObj.position())
            # location =(event.pos().x()-51)/self.section
            # if location>=totalDuration:
            #     location =totalDuration
            # if location<100:
            #     location=100
            # self.homeAction.playObj.setPosition(location*100)
            print("移动播放轨道进度",event.pos().x())
            #当前歌曲（总长）
            totalDuration = int(self.homeAction.playObj.duration()/100)
            #当前歌曲(已播放时间)
            # pastTime = int(self.homeAction.playObj.time*10)
            location =int((event.pos().x()-51)/self.section)
            print("sssssssssss",location,self.homeAction.playObj.duration(),totalDuration)

            if location>=totalDuration*100:
                location =totalDuration
            if location<100:
                location=100
            self.homeAction.playObj.setPosition(int(location))
        if eventID == 1:
            print("点击预览按钮",event.pos().x())
            if self.homeAction.isPreview:
                self.homeAction.isPreview =0
            else:
                self.homeAction.isPreview =1
        if eventID == 2:
            print("点击随机按钮",event.pos().x())
            if self.homeAction.isRandom:
                #将随机改为顺序
                self.homeAction.isRandom = 0
                self.homeAction.shuffleMusic(0)
                print(self.homeAction.randomList)
            else:
                #将顺序改为随机
                self.homeAction.isRandom = 1
                self.homeAction.shuffleMusic(1)
                print(self.homeAction.randomList)
        if eventID == 3:
            print("点击循环按钮",event.pos().x())
            if self.homeAction.isLoop:
                self.homeAction.isLoop = 0
            else:
                self.homeAction.isLoop = 1
        if eventID == 4:
            print("点击列表向上按钮",event.pos().x())
            upPos = self.tracksList.verticalScrollBar().value()-9
            if upPos<0:
                upPos=0
            self.tracksList.verticalScrollBar().setValue(upPos)
        if eventID == 5:
            print("点击列表向下按钮",event.pos().x())
            downPos = self.tracksList.verticalScrollBar().value()+9
            if downPos<0:
                downPos=0
            self.tracksList.verticalScrollBar().setValue(downPos)

    ##播放控制
    #def playStart(self,i):
    #    if self.isRandom==0:
    #        pass
    #    self.soundID=i
    #    source = self.filePath + self.fileList[i]
    #    print(source)
    #    self.fileObj = pyglet.media.load(source)
    #    self.playObj = pyglet.media.StaticSource(self.fileObj)
    #    self.currentPlay = self.playObj.play()
    #    self.currentPlay.pause()
    #    self.currentPlay.eos_action=self.currentPlay.EOS_STOP
    #    print("a",self.playObj.audio_format)
    #    print("b",self.currentPlay._groups)
    #
    ##播放控制 （上一首）
    #def prevPlay(self):
    #    pass
    #def xxte(self,event):
    #    print(event)


    def paintEvent(self, event):
        painter=QPainter(self)
        #设置渲染:开启抗锯齿,老机器很占cpu!
        painter.setRenderHint(QPainter.Antialiasing)

        #第一次使用，就使用一次,用来检测打开播放器时，读取上次关闭时的记录 ==>
        if self.homeAction.playObj.bufferStatus()==100 and self.homeAction.isInitPlay:#判断载入歌曲是否100% ，并且是第一打开播放器
            self.homeAction.isInitPlay=0
            self.homeAction.playObj.setPosition(self.homeAction.pastTime)
            if self.homeAction.playStat=="False":
                self.homeAction.playObj.pause()
        #第一次使用，用来检测打开播放器时，读取上次关闭时的记录<<==

    #当前歌曲信息及播放完毕后的事件==>>
        #当前歌曲（总长）
        totalDuration = int(self.homeAction.playObj.duration())
        #当前歌曲(已播放时间)
        pastTime = int(self.homeAction.playObj.position())
        #当前歌曲（剩余时长）
        laveTime = totalDuration - pastTime
        # if pastTime>=totalDuration:
        if self.homeAction.playObj.mediaStatus()==7:
            print("zhe::::")
            if self.homeAction.isLoop==1:#是否单循环
                self.homeAction.playObj.setPosition(0)
                self.homeAction.playObj.play()
            else:
                self.homeAction.nextPlay()
            self.tracksList.setCurrentRow(self.homeAction.soundID)
    #当前歌曲信息及播放完毕后的事件结束<<==

    #记录播放信息==>>
        colors.CONFIGFILE.set("Save","soundID",str(self.homeAction.soundID))
        # colors.CONFIGFILE.set("Save","playStat",str(self.homeAction.playObj.playing))
        if self.homeAction.playObj.state()==1:
            playStat="True"
        else:
            playStat="False"
        colors.CONFIGFILE.set("Save","playStat",playStat)
        colors.CONFIGFILE.set("Save","pastTime",str(pastTime))
        colors.CONFIGFILE.set("Save","volume",str(self.homeAction.currentVolume))
        colors.CONFIGFILE.set("Save","isRandom",str(self.homeAction.isRandom))
        colors.CONFIGFILE.set("Save","isLoop",str(self.homeAction.isLoop))
        colors.CONFIGFILE.write(open('config.ini', "w"))
    #记录播放信息结束<<==

    #播放轨道条==>>
        painter.setPen(QPen(Qt.NoPen))#设置样式
        painter.setBrush(QColor(230,230,219,120))#设置颜色
        #画播放轨道背景
        painter.drawRoundedRect(QRectF(40,257,450,42),5.0, 5.0)
        #画播放轨道(未播放状态)
        painter.setPen(QPen(Qt.white,0.1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(QRectF(50,272,410,10))
        #画播放轨道（计算并画已播放状态）
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QColor(0,173,239,255))
        self.section = 408*10 / (totalDuration*10)
        past = pastTime* self.section
        currentPosition = past
        if currentPosition > 408:
            currentPosition=408
        #画出已播放状态）
        painter.drawRect(QRectF(51,273,currentPosition,8))
    #播放轨道条结束<<===

    #播放轨道条右侧的播放/暂停的小图标，小三角或两竖<<===
        if self.homeAction.playObj.state()==1:
            #画播放状态标（三角形）
            points = [QPointF(476.0, 277.0),QPointF(468.0, 273.0),QPointF(468.0, 281.0)]
            painter.drawPolygon(QPolygonF(points))#三角形
        else:
            #画暂停状态标（两竖）
            painter.drawRect(QRectF(468,273,3,8))#暂停第一竖
            painter.drawRect(QRectF(473,273,3,8))#暂停第二竖
    #播放轨道条右侧的播放/暂停的小图标，小三角或两竖结束<<===

    #画轨道条上面的照片背景==>
        painter.setBrush(Qt.white)
        painter.setPen(QPen(QColor(176,178,177,255),1))
        painter.drawRect(QRect(270,105,160,160))
        #painter.setBrush(Qt.white)
        #painter.setPen(QPen(Qt.gray,0.5))
        #painter.drawRect(QRect(276,111,148,148))
        painter.drawImage(QRectF(275,110,150,150), QImage("%simg/music/nonePhoto.png" % (colors.SYSPATH)), QRectF(0.0, 0.0, 150.0, 150.0))#测试照片
    #画轨道条上面的照片背景END<<==

    #添加艺术家图标和歌曲标题图标==>
        painter.drawImage(QRectF(40,150,20,20), QImage("%simg/music/icon.png" % (colors.SYSPATH)), QRectF(0.0, 0.0, 20.0, 20.0))#艺术家
        painter.drawImage(QRectF(40,175,20,20), QImage("%simg/music/icon.png" % (colors.SYSPATH)), QRectF(0.0, 20.0, 20.0, 20.0))#歌曲标题一
        painter.drawImage(QRectF(40,200,20,20), QImage("%simg/music/icon.png" % (colors.SYSPATH)), QRectF(0.0, 40.0, 20.0, 20.0))#歌曲标题二
        painter.drawImage(QRectF(40,225,20,20), QImage("%simg/music/icon.png" % (colors.SYSPATH)), QRectF(0.0, 60.0, 20.0, 20.0))#时间进度
    #添加艺术家图标和歌曲标题图标END<<==

    #当前播放歌曲的信息==>>
        #<--剩余时间
        painter.setFont(QFont("Verdana",8))
        painter.setPen(QColor(0,173,239,255))
        painter.drawText(QPointF(425,281),str(time.strftime("%M:%S", time.localtime(laveTime/1000))))#剩余时间
        #剩余时间-->
        painter.setFont(QFont("Verdana",12))
        painter.drawText(QPointF(70,243),str(time.strftime("%M:%S", time.localtime(totalDuration/1000))) + " /")#总时长
        painter.drawText(QPointF(135,243),str(time.strftime("%M:%S", time.localtime(pastTime/1000))))#已播放时间
        painter.drawText(QPointF(110,217),"%d/%d" %(self.homeAction.soundID,len(self.homeAction.randomList)-1))#曲目  x/x

        painter.setFont(QFont("微软雅黑",12))
        painter.drawText(QPointF(70,166),self.homeAction.playObj.metaData(QMediaMetaData.Author))#艺术家
        painter.drawText(QPointF(70,190),self.homeAction.playObj.metaData(QMediaMetaData.Title))#曲目名
        painter.drawText(QPointF(70,216),"曲目")#曲目
    #当前播放歌曲的信息END<<==

    #画试听、随机、循环按钮背景==>>
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(70,72,76,220))
        painter.drawRect(QRect(531,1,75,39))#循环
        painter.drawRect(QRect(607,1,75,39))#随机
        painter.drawRect(QRect(683,1,74,39))#预览

        painter.drawRect(QRect(531,334,75,39))#清空列表
        painter.drawRect(QRect(607,334,75,39))#增加文件夹
        painter.drawRect(QRect(683,334,74,39))#增加文件
    #画试听、随机、循环按钮背景END<<==

    #按扭文字 循环  随机 预览 清空列表 增加文件夹 增加文件  ==>>
        painter.setPen(Qt.white)
        painter.setFont(QFont("微软雅黑",10))
        painter.drawText(QPointF(715,25),"循环")#循环
        painter.drawText(QPointF(640,25),"随机")#随机
        painter.drawText(QPointF(565,25),"预览")#预览

        painter.drawText(QPointF(715,358),"打开")#循环
        painter.drawText(QPointF(640,358),"添加")#随机
        painter.drawText(QPointF(565,358),"清空")#随机
    #按扭文字 循环  随机 预览 清空列表 增加文件夹 增加文件  END<<==

    #画右侧列表背景 ==>
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QColor(230,230,219,120))
        painter.drawRect(QRect(531,41,226,292))
    #画右侧列表背景END<<==

    #画右侧列表滚动条背景 ==>>
        painter.setBrush(QColor(71,73,76,255))
        painter.drawRect(QRect(758,1,42,372))
        painter.setBrush(QColor(43,46,49,255))
        painter.drawRoundedRect(QRectF(770,1,18,372),20.0, 20.0)
    #画右侧列表滚动条背景 END<<==

    #列表向上  向下 按钮 ==>>
        painter.drawImage(QRectF(770,1,18,27), QImage("%simg/music/up.png" % (colors.SYSPATH)), QRectF(0.0, 0.0, 18.0, 27.0))#列表向上
        painter.drawImage(QRectF(770,345,18,27), QImage("%simg/music/down.png" % (colors.SYSPATH)), QRectF(0.0, 0.0, 18.0, 27.0))#列表向下
    #列表向上  向下 按钮 END<<==

    #滚动条位置（顶端：24，底端：298，可移动范围：300）===>>
        try:
            if self.tracksList.count()>5:
                #pp = 274*1000/self.tracksList.count()
                pp = 300*1000/self.tracksList.count()
                oo = int(self.tracksList.verticalScrollBar().value()*pp/1000)+24
                if oo>298:
                    oo=298
                painter.drawImage(QRectF(770,oo,18,53), QImage("%simg/music/scroll.png" % (colors.SYSPATH)), QRectF(0.0, 0.0, 18.0, 53.0))
        except :
            pass
    #滚动条位置（顶端：24，底端：298，可移动范围：274）END<<===


    #画按钮的图标 循环  随机 预览 清空列表 增加文件夹 增加文件  ==>>
        #画试听图标
        if self.homeAction.isPreview:
            if pastTime >10:
                self.homeAction.nextPlay()
            if int(pastTime)%2 == 0:
                #print("偶数",int(pastTime)%2)
                painter.setPen(Qt.red)
                painter.setFont(QFont("微软雅黑",10))
                painter.drawText(QPointF(565,25),"预览")#随机
                painter.drawImage(QRectF(540,9.5,20,20), QImage("%simg/music/icon.png" % (colors.SYSPATH)), QRectF(40.0, 40.0, 20.0, 20.0))#画预览图标
            else:
                painter.drawImage(QRectF(540,9.5,20,20), QImage("%simg/music/icon.png" % (colors.SYSPATH)), QRectF(20.0, 40.0, 20.0, 20.0))#画预览图标
        else:
            painter.drawImage(QRectF(540,9.5,20,20), QImage("%simg/music/icon.png" % (colors.SYSPATH)), QRectF(20.0, 40.0, 20.0, 20.0))#画预览图标

        #画随机图标
        if self.homeAction.isRandom == 1:
            painter.drawImage(QRectF(615,9.5,20,20), QImage("%simg/music/icon.png" % (colors.SYSPATH)), QRectF(40.0, 20.0, 20.0, 20.0))#画随机图标
        else:
            painter.drawImage(QRectF(615,9.5,20,20), QImage("%simg/music/icon.png" % (colors.SYSPATH)), QRectF(20.0, 20.0, 20.0, 20.0))#画随机图标

        #画循环图标
        if self.homeAction.isLoop  == 1:
            painter.drawImage(QRectF(690,9.5,20,20), QImage("%simg/music/icon.png" % (colors.SYSPATH)), QRectF(40.0, 00.0, 20.0, 20.0))#画循环图标
        else:
            painter.drawImage(QRectF(690,9.5,20,20), QImage("%simg/music/icon.png" % (colors.SYSPATH)), QRectF(20.0, 00.0, 20.0, 20.0))#画循环图标

        #清空列表图标
        painter.drawImage(QRectF(540,342,20,20), QImage("%smusic/icon.png" % (colors.SYSPATH)), QRectF(60.0, 00.0, 20.0, 20.0))#清空列表图标
        painter.drawImage(QRectF(615,344,20,20), QImage("%smusic/icon.png" % (colors.SYSPATH)), QRectF(60.0, 20.0, 20.0, 20.0))#增加文件
        painter.drawImage(QRectF(690,342.5,20,20), QImage("%smusic/icon.png" % (colors.SYSPATH)), QRectF(60.0, 40.0, 20.0, 20.0))#增加文件夹
    #画按钮的图标 循环  随机 预览 清空列表 增加文件夹 增加文件  END<<==


#播放列表显示
class TracksList(QListWidget):
    def __init__(self, parent=None):
        super(TracksList, self).__init__(parent)
        self.parent = parent
        self.setGeometry(QRect(531,41,226,292))
        #设置背景透明无边框
        self.setStyleSheet("background: transparent;border:none;")
        #self.setStyleSheet("background-color:#eac715;")
        #设置水平滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #设置垂直滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setFont(QFont("微软雅黑",14))
        self.refreshList()

    @pyqtSlot(int)
    def setValue_OneParameter(self,nIndex):
        #临时这样写吧！播放点击列表中的歌曲
        clickedTracksId = int(nIndex.text().split('.')[0])
        print("点击：",clickedTracksId)
        self.parent.homeAction.stopPlay()
        self.parent.homeAction.soundID = clickedTracksId
        self.parent.homeAction.play(clickedTracksId)

    def refreshList(self):
        aab = self.parent.homeAction.fileList
        for i in range(len(aab)):
            name = "%d. %s" % (i,aab[i])
            #name = str(i+1)+". "+aab[i]
            self.addItem(name)
            if i%2 == 0:
                self.item(i).setBackground(QColor(230,230,219,30))
            self.item(i).setForeground(QColor(0,173,239,255))
        self.itemClicked.connect(self.setValue_OneParameter,Qt.QueuedConnection)
