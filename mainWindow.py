# -*- coding: utf-8 -*-
from PyQt5.QtCore import (QPointF,QPoint,QRectF, QRect, qRound, pyqtSlot,Qt, QTimer,QUrl)
from PyQt5.QtWidgets import (QGraphicsView,QWidget,QGraphicsScene,QMessageBox,QFrame,QApplication)
from PyQt5.QtGui import  (QImage,QPixmap,QPainter,QIcon,QPen,QBrush,QColor)
from PyQt5.QtMultimedia import (QMediaPlayer,QMediaContent,QMediaResource,QMediaPlaylist,QAudioDeviceInfo,QMediaMetaData)
import time

#==========自定义包
from musicWidget import MusicWidget
from buttonPixmap import ButtonPixmap
from eventAction import EventAction
import colors
class Ui_MainWindow(QGraphicsView):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        #计算系统桌面尺寸
        self.countWwindowRect()
        #窗口默认尺寸
        self.setGeometry(self.windowRect)
        #窗口最小尺寸
        self.setMinimumSize(colors.CONFIGFILE.getint('Properties',"WindowMinWidth"), colors.CONFIGFILE.getint('Properties',"WindowMinHeight"))
        #背景
        self.background = QPixmap()
        #窗品标题
        self.setWindowTitle("你是一个王八蛋")
        #设置水平滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #设置垂直滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #设置框架样式
        self.setFrameStyle(QFrame.NoFrame)
        #设置ICON
        self.setWindowIcon(QIcon(colors.CONFIGFILE.get('Properties',"imgPath")+"icon/05.png"))
        #设置边框
        self.setStyleSheet("background: transparent;border:None")
        ######################场景
        self.setScene(QGraphicsScene())
        self.setSceneRect(0, 0,colors.CONFIGFILE.getint('Properties',"WindowWidth"),colors.CONFIGFILE.getint('Properties',"WindowHeight"))
        #禁用索引管理元素
        self.scene().setItemIndexMethod(QGraphicsScene.NoIndex)
        #绘制背景像素图
        self.drawBackgroundToPixmap()



        #载入
        self.homeAction = EventAction()
        #==>初始化播放
        self.homeAction.initPlay()
        #初始化播放<<==

        #载入播放界面UI
        musicPlayWidget = MusicWidget(self.homeAction)
        self.scene().addWidget(musicPlayWidget)

        #按钮索引
        self.buttonList = []
        self.command_dic = {'full':lambda :self.toggleFullscreen(),
                            'mute':lambda :self.homeAction.mutePlay(),
                            'lowervol':lambda :self.homeAction.lowervolPlay(),
                            'prev':lambda :(self.homeAction.prevPlay(),musicPlayWidget.tracksList.setCurrentRow(self.homeAction.soundID)),
                            'rewind':lambda :self.homeAction.rewindPlay(),
                            'play':lambda :self.homeAction.playORpause(),
                            'forward':lambda :self.homeAction.forwardPlay(),
                            'next':lambda :(self.homeAction.nextPlay(),musicPlayWidget.tracksList.setCurrentRow(self.homeAction.soundID)),
                            'raisevol':lambda :self.homeAction.raisevolPlay(),
                            'settings':lambda :self.homeAction.testPlay(),
                            'muteStat':lambda :self.muteEvent(),
                            'pause':lambda :self.homeAction.playORpause(),
                            'quit':lambda :self.sysQuit(),
                            'back':lambda :self.backEvent(),
                            'calendar':lambda :self.calendarEvent(),
                            'maps':lambda :self.mapsEvent(),
                            'camera':lambda :self.cameraEvent(),
                            'carInfo':lambda :self.carInfoEvent(),
                            'music':lambda :self.musicEvent(),
                            'musicAdd':lambda :self.musicAddEvent(),
                            'video':lambda :self.videoEvent(),
                            'radio':lambda :self.radioEvent(),
                            'phone':lambda :self.phoneEvent(),
                            }
        #===================================================================
        #画个顶部背景
        #self.parent.scene().addRect(QRectF(0,0,800,53),QPen(Qt.NoPen),QBrush(QPixmap(Colors.ImgPath+'topImg/topBG.png')))
        self.scene().addRect(QRectF(0,0,800,53),QPen(Qt.NoPen),QBrush(QColor(230,230,219,120)))
        #画个顶部和底部透明背景
        self.scene().addRect(QRectF(0,427,800,53),QPen(Qt.NoPen),QBrush(QColor(230,230,219,120)))

        #底部按钮
        #底部按钮::静音
        mute  = ButtonPixmap(QPixmap('%simg/player/mute.png' % (colors.SYSPATH)),"mute")
        self.buttonList.append(mute)
        #底部按钮::音量减
        lowervol  = ButtonPixmap(QPixmap('%simg/player/lowervol.png' % (colors.SYSPATH)),"lowervol")
        self.buttonList.append(lowervol)
        #底部按钮::上一首
        prev  = ButtonPixmap(QPixmap('%simg/player/prev.png' % (colors.SYSPATH)),"prev")
        self.buttonList.append(prev)
        #底部按钮::快退
        rewind  = ButtonPixmap(QPixmap('%simg/player/rewind.png' % (colors.SYSPATH)),"rewind")
        self.buttonList.append(rewind)
        #底部按钮::播放
        play  = ButtonPixmap(QPixmap('%simg/player/new_play.png' % (colors.SYSPATH)),"play")
        self.buttonList.append(play)
        #底部按钮::快进
        forward  = ButtonPixmap(QPixmap('%simg/player/forward.png' % (colors.SYSPATH)),'forward')
        self.buttonList.append(forward)
        #底部按钮::下一首
        next  = ButtonPixmap(QPixmap('%simg/player/next.png' % (colors.SYSPATH)),"next")
        self.buttonList.append(next)
        #底部按钮::音量加
        raisevol  = ButtonPixmap(QPixmap('%simg/player/raisevol.png' % (colors.SYSPATH)),"raisevol")
        self.buttonList.append(raisevol)
        #底部按钮::设置
        settings  = ButtonPixmap(QPixmap('%simg/player/settings.png' % (colors.SYSPATH)),"settings")
        self.buttonList.append(settings)
        #底部按钮::装载底部按钮
        #x起点
        startPointX =0
        for _,img in enumerate(self.buttonList):
            startPointX += img.boundingRect().width()
        startPointX = (self.sceneRect().width() -startPointX ) /2
        #y起点
        startPointY = self.sceneRect().height()-53 +((53-settings.boundingRect().height() )/2)
        #装载
        for i in range(len(self.buttonList)):
            if i>0:
                startPointX +=self.buttonList[i-1].boundingRect().width()
            self.buttonList[i].setPos(QPointF(startPointX, startPointY))
            self.scene().addItem(self.buttonList[i])
            self.buttonList[i].clicked.connect(self.setValue_OneParameter,Qt.QueuedConnection)

        #执行主状态机

        #按钮状态索引
        self.buttonStatList = {}
        muteStatView = ButtonPixmap(QPixmap('%simg/player/menuStat.png' % (colors.SYSPATH)),"muteStat")
        #muteStatView.setObjectName("muteStat")
        muteStatView.setPos(QPointF(70, 449))
        self.buttonStatList["mute"] =  muteStatView
        #音量减状态
        lowervolStat = ButtonPixmap(QPixmap('%simg/player/lowervol_status.png' % (colors.SYSPATH)),"lowervolStat")
        lowervolStat.setPos(QPointF(147, 441))
        self.buttonStatList["lowervol"] =  lowervolStat
        #上一首状态
        prevStat = ButtonPixmap(QPixmap('%simg/player/prev_status.png' % (colors.SYSPATH)),"prevStat")
        prevStat.setPos(QPointF(227, 441))
        self.buttonStatList["prev"] =  prevStat
        #快退状态
        rewindStat = ButtonPixmap(QPixmap('%simg/player/rewind_status.png' % (colors.SYSPATH)),"rewindStat")
        rewindStat.setPos(QPointF(307, 441))
        self.buttonStatList["rewind"] =  rewindStat
        #播放状态

        #快进状态
        forwardStat = ButtonPixmap(QPixmap('%simg/player/forward_status.png' % (colors.SYSPATH)),"forwardStat")
        forwardStat.setPos(QPointF(467, 441))
        self.buttonStatList["forward"] =  forwardStat
        #下一首状态
        nextStat = ButtonPixmap(QPixmap('%simg/player/forward_status.png' % (colors.SYSPATH)),"nextStat")
        nextStat.setPos(QPointF(547, 441))
        self.buttonStatList["next"] =  nextStat
        #音量加状态
        raisevolStat = ButtonPixmap(QPixmap('%simg/player/raisevol_status.png' % (colors.SYSPATH)),"raisevolStat")
        raisevolStat.setPos(QPointF(627, 441))
        self.buttonStatList["raisevol"] =  raisevolStat
        #设置状态
        settingsStat = ButtonPixmap(QPixmap('%simg/player/settings_status.png' % (colors.SYSPATH)),"settingsStat")
        settingsStat.setPos(QPointF(707, 441))
        self.buttonStatList["settings"] =  settingsStat
        #播放时点击状态
        playStat = ButtonPixmap(QPixmap('%simg/player/new_play_to_pause.png' % (colors.SYSPATH)),"playStat")
        playStat.setPos(QPointF(360, 430))
        self.buttonStatList["play"] =  playStat
        #暂停时点击状态
        pauseStat = ButtonPixmap(QPixmap('%simg/player/new_pause_to_play.png' % (colors.SYSPATH)),"pauseStat")
        pauseStat.setPos(QPointF(360, 430))
        self.buttonStatList["pause"] =  pauseStat
        ########################
        ########################
        ########################
        #暂停图标
        self.pause = ButtonPixmap(QPixmap('%simg/player/new_pause.png' % (colors.SYSPATH)),"pause")
        self.pause.setObjectName("pause")
        self.pause.setPos(QPointF(800, 430))
        self.scene().addItem(self.pause)
        self.pause.clicked.connect(self.setValue_OneParameter,Qt.QueuedConnection)
        #静音图标
        self.muteStatViews = ButtonPixmap(QPixmap('%simg/player/menuStat.png' % (colors.SYSPATH)),"muteStats")
        self.muteStatViews.setObjectName("muteStats")
        self.muteStatViews.setPos(QPointF(70, 449))
        self.scene().addItem(self.muteStatViews)
        self.muteStatViews.clicked.connect(self.setValue_OneParameter,Qt.QueuedConnection)

        #视窗刷新开始(调用状态检测方法)
        self.isStatTimer = QTimer()
        self.isStatTimer.timeout.connect(self.isStat)
        self.isStatTimer.start(30)

    @pyqtSlot(str,str)
    def setValue_OneParameter(self,nIndex,type):
        try:
            if type=="release":
                self.command_dic[nIndex]()
                self.delItem(nIndex)
            if type=="press":
                self.loadItem(nIndex)
        except EOFError:
            pass
            #print("no such command.",EOFError)

    #全屏事件
    def toggleFullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def loadItem(self,itemName):#点击按钮时载入
        self.scene().addItem(self.buttonStatList[itemName])
    def delItem(self,itemName):#松开鼠标时移出
        self.scene().removeItem(self.buttonStatList[itemName])

    #播放和暂停 与静音状态
    def isStat(self):
        if self.homeAction.playObj.state() == 1:
            self.buttonList[4].setPos(QPointF(360, 429))
            self.pause.setPos(QPointF(800, 430))
        else:
            self.pause.setPos(QPointF(360, 430))
            self.buttonList[4].setPos(QPointF(800, 430))

        if self.homeAction.playObj.isMuted():
            if int(time.time())%2:
                self.muteStatViews.setPos(QPointF(70, 449))
            else:
                self.muteStatViews.setPos(QPointF(800, 449))
        else:
            self.muteStatViews.setPos(QPointF(800, 449))
    #绘制背景像素图
    def drawBackgroundToPixmap(self):
        r = self.sceneRect()
        self.background = QPixmap(qRound(r.width()), qRound(r.height()))
        self.background.fill(Qt.black)
        painter = QPainter(self.background)
        bg = QImage("%simg/BG.png" % (colors.SYSPATH))
        painter.drawImage(0, 0, bg)

    #背景载入到场景
    def drawBackground(self, painter, rect):
        painter.drawPixmap(QPoint(0, 0), self.background)

    #计算桌面矩型
    def countWwindowRect(self):
        #获取系统桌面尺寸大小
        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry(desktop.primaryScreen())
        #窗口默认尺寸
        windowRect = QRect(0, 0,colors.CONFIGFILE.getint('Properties',"WindowWidth"), colors.CONFIGFILE.getint('Properties',"WindowHeight"))
        #如果系统桌面宽小于默认值，窗口宽度将被设为系统桌面的宽度
        if screenRect.width() < colors.CONFIGFILE.getint('Properties',"WindowWidth"):
            windowRect.setWidth(screenRect.width())
        #如果系统桌面高小于默认值，窗口高度将被设为系统桌面的高度
        if screenRect.height() < colors.CONFIGFILE.getint('Properties',"WindowHeight"):
            windowRect.setHeight(screenRect.height())
        #移动中心点为系统中心点
        windowRect.moveCenter(screenRect.center())
        self.windowRect = windowRect
    #窗品方大或缩小事件
    def resizeEvent(self, event):
        self.resetTransform()
        self.scale(event.size().width() / colors.CONFIGFILE.getint('Properties',"WindowWidth"), event.size().height() / colors.CONFIGFILE.getint('Properties',"WindowHeight"))
        super(Ui_MainWindow,self).resizeEvent(event)

    #直接按X关闭窗口事件
    #def closeEvent(self, event):
    #    self.closeEvent(event)

    #键盘事件
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()
        elif event.key() == Qt.Key_Q:
            QApplication.quit()
        elif event.key() == Qt.Key_F:
            self.toggleFullscreen()
        elif event.key() == Qt.Key_F1:
            #playList=QMediaPlaylist()
            #playList.setPlaybackMode(QMediaPlaylist.Loop)
            #playList.addMedia(QMediaContent(QUrl.fromLocalFile("f:/mp3/qh.mp3")))
            #player = QMediaPlayer()
            #player.setPlaylist(playList)
            #player.play()
            #print(player.metaData(QMediaMetaData.Author))
            #
            #m_device = QAudioDeviceInfo.defaultOutputDevice()
            #print(m_device)
            #self.xxx = QMediaPlayer()

            #self.xxx.setMedia(QMediaContent(QUrl.fromLocalFile("yinpin.wav")))
            #self.xxx.setMedia(QMediaContent(QUrl.fromUserInput("http://192.168.20.200/qh.mp3")))
            #self.xxx.play()
            #qq = QUrl()
            #qq.setPath("f:/mp3/")
            #qq = QUrl.fromUserInput("http://192.168.20.200/qh.mp3")

            #print(qq)
            #ss=QMediaContent(QUrl.fromLocalFile("yinpin.wav"))
            #sss=QMediaContent(QUrl.fromLocalFile(""))
            s = "这是一个正在开发的东西，慢慢来吧：\n"
            w = QWidget()
            s += "\n[色位深度]: %d" % w.depth()
            s += "\n[动画支持]: "
            s += "\n[bufferStatus]: "+str(self.homeAction.playObj.bufferStatus())
            s += "\n[position]: "+str(self.homeAction.playObj.position())
            s += "\n[state]: "+str(self.homeAction.playObj.state())
            s += "\n[filePath]: "+self.homeAction.openPath
            #s += "\n[xxxx]: "+str(ss)
            #s += "\n[sss]: "+str(sss)
            #s += "\n[qqq]: "+qq.scheme()
            #s += ["on", "off"][Colors.noAnimations]
            QMessageBox.information(None, "【F1】你想知道什么：", s)
        super(Ui_MainWindow, self).keyPressEvent(event)
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
