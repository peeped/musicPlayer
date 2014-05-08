__author__ = 'liaojie'
#!/usr/bin/env python
#coding:utf-8
import os,random
import configparser
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import (QMediaPlayer,QMediaContent,QMediaMetaData)
class EventAction():
    def __init__(self):
        #self.parent = parent
        self.isLoop = 0         #0循环列表，1单曲循环
        self.isRandom = 0       #0不随机，1随机
        self.fileList = []      #曲目名称列表
        self.randomList =[]     #播放列表
        self.soundID = 0        #当前歌曲ID
        self.playStat = False  #当前播放状态 （0未播放，1播放）
        self.openPath = "F:/mp3/" #歌曲目录
        self.isPreview = 0       #试用开关，0正常播放，1列表中的歌曲每首歌曲放10秒
        self.currentVolume = 0.1#默认的起始音量
        self.isInitPlay = 1     #是否是初始播放
        #==>>打开目录
        self.config=configparser.ConfigParser()
        self.config.read('config.ini')
        self.openDir()
        #打开目录<<==
        self.playObj = QMediaPlayer()



    #打开歌曲目录
    def openDir(self):
        self.openPath = self.config.get('Save','musicPath')
        isMusicDir = os.path.isdir(self.openPath)#检查是否为目录
        if isMusicDir:
            dirFile = os.listdir(self.openPath)#目录中的所有文件
            #遍历有效音乐文件
            i=0;
            for file in dirFile:
                fileName,fileType=os.path.splitext(file)
                if fileType==".mp3" or fileType==".wav":
                    self.fileList.append(file)
                    self.randomList.append(i)
                    i+=1
        if self.isRandom==1:
            self.shuffleMusic(1)

    #随机（打乱播放顺序）
    def shuffleMusic(self,isshuffle):
        if isshuffle:
            random.shuffle(self.randomList)#乱序
        else:
            self.randomList.sort()#排序

    #初始化播放
    def initPlay(self):
        self.soundID = int(self.config.get('Save','soundID'))
        self.playStat = self.config.get('Save','playStat')
        self.pastTime = self.config.getint('Save','pastTime')
        self.currentVolume = self.config.getint('Save','volume')
        self.isRandom = self.config.getint('Save','isRandom')
        self.isLoop = self.config.getint('Save','isLoop')

        if self.soundID!="":
            self.play(self.soundID)
        if self.isRandom:#打乱列表
            self.shuffleMusic(1)
        self.playObj.setVolume(self.currentVolume)


    #播放
    def play(self,i):
        if i<0 or i>=len(self.randomList):
            i=0
        source = self.openPath + self.fileList[i]
        self.playObj.setMedia(QMediaContent(QUrl.fromLocalFile(source)))
        self.playObj.play()


        # self.fileObj = pyglet.media.load(source)
        # self.playObj = self.fileObj.play()
        # self.playObj._set_eos_action("stop")


        # self.kkk=self.fileObj.play()
        # kkk.pause()
        # self.fileObj.delete()
        #print("zhe1")
        #self.playObj = pyglet.media.StaticSource(self.fileObj)
        #print("zhe2")
        #self.currentPlay = self.playObj.play()
        #print("zhe3")
        #self.currentPlay.volume = self.currentVolume

        #aaaa = pyglet.media.get_source_loader()
        # print( "zhe:::",pyglet.media.Source.audio_format)

    def testPlay(self):
        #ps =QMediaMetaData()
        #print("QMediaMetaData",ps)
        print("metaData",self.playObj.metaData(QMediaMetaData.Title))
        



    #换歌之前先停止，释放内存
    def stopPlay(self):
        # print("文件全长:::",self.fileObj.duration)
        # print("已播放:::",self.playObj.time)
        # print("状态:::",self.playObj.playing)
        # print("名称:::",self.fileObj.info.title)
        # self.playObj.stop()
        self.playObj.pause()
        # self.playObj.on_player_eos()
        # self.playObj.on_source_group_eos()
        # self.playObj.on_eos()

    #上一首
    def prevPlay(self):
        self.stopPlay()
        if self.isRandom:
            key = self.searchID(self.soundID)-1
            if key<0:
                key=0
            self.soundID = self.randomList[key]
        else:
            self.soundID-=1
            if self.soundID< 0:
                self.soundID = len(self.randomList)-1
        self.play(self.soundID)

    #下一首
    def nextPlay(self):
        self.stopPlay()
        if self.isRandom:
            key = self.searchID(self.soundID)+1
            if key>(len(self.randomList)-1):
                key=len(self.randomList)-1
            self.soundID = self.randomList[key]
        else:
            self.soundID+=1
            if self.soundID > (len(self.randomList)-1):
                self.soundID = 0
        print("next:::",self.soundID)
        self.play(self.soundID)

    #快退
    def rewindPlay(self):
        rewindTime = int(self.playObj.position()) - 10*1000
        if rewindTime < 0:
            rewindTime = 0
        self.playObj.setPosition(rewindTime)

    #快进
    def forwardPlay(self):
        forwardTime = int(self.playObj.position()) + 10*1000
        if forwardTime > int(self.playObj.position()):
            forwardTime = int(self.playObj.position())
        self.playObj.setPosition(forwardTime)

    #播放/暂停
    def playORpause(self):
        if self.playObj.state()==1:
            self.playObj.pause()
        else:
            self.playObj.play()

    #音量加
    def raisevolPlay(self):
        self.playObj.setVolume(self.playObj.volume()+10)
        self.currentVolume = self.playObj.volume()
    #音量减
    def lowervolPlay(self):
        self.playObj.setVolume(self.playObj.volume()-10)
        self.currentVolume = self.playObj.volume()

    #静音
    def mutePlay(self):
        if self.playObj.isMuted():
            self.playObj.setMuted(False)
        else:
            self.playObj.setMuted(True)
    #volume

    #跟据v找K
    def searchID(self,v):
        for index, item in enumerate(self.randomList):
            if item ==v:
                return index
        return 0