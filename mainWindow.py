# -*- coding: utf-8 -*-
from PyQt5.QtCore import (QRectF,QPointF,QPoint, QRect, qRound, Qt,QTimer,pyqtSlot)
from PyQt5.QtWidgets import (QGraphicsView,QApplication,QWidget,QGraphicsScene,QMessageBox,QFrame)
from PyQt5.QtGui import  (QImage,QPixmap,QPainter,QColor,QIcon,QPen,QBrush)

from PyQt5.QtCore import QByteArray, QIODevice, Qt, QTimer, QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import (QMediaPlayer,QMediaContent,QMediaPlaylist)

# import win32gui
#==========自定义包
#from colors import Colors
#from modules.buttonPixmap import ButtonPixmap
#from uiAction.mainUi import MainUi
#from modules.mainMod import MainMod
from musicWidget import MusicWidget
from buttonPixmap import ButtonPixmap
from eventAction import EventAction
import colors
class Ui_MainWindow(QGraphicsView):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        # print(colors.CONFIGFILE.options('Save'))
        print(colors.CONFIGFILE.sections())
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
        # print(self.homeAction.fileList)
        # print(self.homeAction.randomList)
        self.homeAction.initPlay()
        #初始化播放<<==

        #self.homeAction.nextPlay()
        # player = QMediaPlayer()
        # player.setMedia(QMediaContent(QUrl.fromLocalFile("E:/mp3/蒋雅文-爱的故事上集.mp3")))
        # player.setVolume(50)
        # # player.setMuted(False)
        # player.play()
        # player.position()
        #######################模块/api
        ##操作参数载入
        #self.mod = MainMod(self)

        #启动默认预载程序
        #self.starting = ButtonPixmap(QPixmap(Colors.ImgPath+'main/starting.png'),"starting")
        #xOff = (self.sceneRect().width()-self.starting.boundingRect().width())/2
        #yOff = (self.sceneRect().height()- self.starting.boundingRect().height())/2
        #self.starting.setPos(QPointF(xOff,yOff))
        #播放界面UI
        musicPlayWidget = MusicWidget(self.homeAction)
        self.scene().addWidget(musicPlayWidget)
        #self.startTimer = QTimer()
        #self.startTimer.timeout.connect(self.defaultMod)
        #self.startTimer.start(30)

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
                            'pause':lambda :self.playEvent(),
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
        play  = ButtonPixmap(QPixmap('%simg/player/play.png' % (colors.SYSPATH)),"play")
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
        #self.setMachine()

        self.muteStatView = ButtonPixmap(QPixmap('%simg/player/menuStat.png' % (colors.SYSPATH)),"muteStat")
        self.muteStatView.setObjectName("muteStat")
        self.muteStatView.setPos(QPointF(70, 449))

    #def mouseReleaseEvent(self, QMouseEvent):
    #    print("鼠标释放")
    #    #self.scene().addItem(self.muteStatView)
    #    self.scene().removeItem(self.muteStatView)


    @pyqtSlot(str,str)
    def setValue_OneParameter(self,nIndex,type):
        print("aaaaaaaaaaaaaaaaaaaaaaaaa",nIndex,type)
        try:
            # if type=="鼠标释放":
            print("aaaaa::::",nIndex)
            self.command_dic[nIndex]()
        except EOFError:
            print("no such command.",EOFError)

    #全屏事件
    def toggleFullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


    #def mouseDoubleClickEvent(self, QMouseEvent):
    #    print("鼠标双击")
    ##def mouseMoveEvent(self, QMouseEvent):
    ##    print("鼠标移动")
    #def mouseReleaseEvent(self, QMouseEvent):
    #    print("鼠标释放")
    #def mousePressEvent(self, QMouseEvent):
    #    print("鼠标按下")



    #绘制背景像素图
    def drawBackgroundToPixmap(self):
        r = self.sceneRect()
        self.background = QPixmap(qRound(r.width()), qRound(r.height()))
        self.background.fill(Qt.black)
        painter = QPainter(self.background)
        bg = QImage("%sBG.png" % (colors.SYSPATH))
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
            s = "这是一个正在开发的东西，慢慢来吧：\n"
            w = QWidget()
            s += "\n[色位深度]: %d" % w.depth()
            s += "\n[动画支持]: "
            #s += ["on", "off"][Colors.noAnimations]
            QMessageBox.information(None, "【F1】你想知道什么：", s)
        super(Ui_MainWindow, self).keyPressEvent(event)
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #def defaultMod(self):
    #    #self.scene().addText("正在启动预设程序……")
    #    if Colors.WinampID ==0:
    #        Colors.WinampID = win32gui.FindWindow('Winamp v1.x', None)
    #        self.mod.w.hWinamp = Colors.WinampID
    #    else:
    #        self.startTimer.stop()
    #        #移出程序启动中图
    #        self.starting.setPos(QPointF(800,self.starting.boundingRect().height()))
    #        #载入主场景UI
    #        self.mainUi = MainUi(self)