__author__ = 'liaojie'
#!/usr/bin/env python
#coding:utf-8
import os,random,string,time
import configparser
from PyQt5.QtCore import QUrl,QFile,QIODevice

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

        self.currentImg = ""    #当前图片
        self.songText = {}      #歌词
        self.songTextKey=[]     #歌词KEY



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
        source = self.openPath + self.fileList[i]
        self.playObj.setMedia(QMediaContent(QUrl.fromLocalFile(source)))
        #解析文件中的ID3V2
        self.currentImg = ""
        f = QFile(source)
        if f.open(QIODevice.ReadOnly):
            #读取标签
            headData = f.read(10)
            data = headData[:0]
            if self.id3v2(headData):#检测是否有ID3
                #标签的大小计算
                tag = headData[6:10]
                tagSize = (tag[0]&0x7f)*0x200000+(tag[1]&0x7f)*0x4000+(tag[2]&0x7f)*0x80+(tag[3]&0x7f)
                data =f.read(tagSize)
                while len(data)>10:
                    data = self.resolve(data)
        f.close()
        self.playObj.play()

    def testPlay(self):
        #ps =QMediaMetaData()
        #print("QMediaMetaData",ps)
        #print("metaData",self.playObj.metaData(QMediaMetaData.Title))
        #print("position",self.playObj.position())
        #print("playlist",self.playObj.playlist)
        #print("availability",self.playObj.availability())
        #print("bufferStatus",self.playObj.bufferStatus())
        #print("currentMedia",self.playObj.currentMedia())
        #print("currentNetworkConfiguration",self.playObj.currentNetworkConfiguration())
        #print("duration",self.playObj.duration())
        #print("error",self.playObj.error())
        #print("errorString",self.playObj.errorString())
        #print("isAudioAvailable",self.playObj.isAudioAvailable())
        #print("isMuted",self.playObj.isMuted())
        #print("isSeekable",self.playObj.isSeekable())
        #print("media",self.playObj.media())
        #print("media:::::::A",self.playObj.media().canonicalResource().audioBitRate())
        #print("media:::::::B",self.playObj.media().canonicalResource().audioCodec())
        #print("media:::::::C",self.playObj.media().canonicalResource().channelCount())
        #print("media:::::::D",self.playObj.media().canonicalResource().dataSize())
        #print("media:::::::e",self.playObj.media().canonicalResource().isNull())
        #print("media:::::::f",self.playObj.media().canonicalResource().language())
        #print("media:::::::g",self.playObj.media().canonicalResource().mimeType())
        #print("media:::::::h",self.playObj.media().canonicalResource().request())
        #print("isVideoAvailable",self.playObj.isVideoAvailable())
        #print("mediaStatus",self.playObj.mediaStatus())
        #print("mediaStream",self.playObj.mediaStream())
        #print("playbackRate",self.playObj.playbackRate())
        #print("state",self.playObj.state())
        #print("volume",self.playObj.volume())
        # print("volume",self.playObj.filename)
        pass



    #换歌之前先停止，释放内存
    def stopPlay(self):
        self.playObj.pause()

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
        #print("next:::",self.soundID)
        self.play(self.soundID)

    #快退
    def rewindPlay(self):
        #print("<<")
        rewindTime = int(self.playObj.position()) - 10*1000
        if rewindTime < 0:
            rewindTime = 0
        self.playObj.setPosition(rewindTime)

    #快进
    def forwardPlay(self):
        #print(">>")
        forwardTime = int(self.playObj.position()) + 10*1000
        if forwardTime > int(self.playObj.duration()):
            forwardTime = int(self.playObj.duration())
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

    #解析文件中是否有id3v2
    def id3v2(self,headData):
        if str(headData[:3],encoding=("utf-8")) != "ID3":
            return False
        return True

    #解析文件中的歌词与图片
    def resolve(self,data):
        tagName =  str(data[:4],encoding=("utf-8"))
        size = data[4:8]
        #sizeS = size[0]*0x1000000 + size[1]*0x10000 + size[2]*0x100 + size[3]
        sizeS=int.from_bytes(size, byteorder='big')
        flags = data[8:10]
        tagContent = data[10:sizeS+10]

        if tagName=="TEXT":#歌词
            #print("歌词")
            condingType=int.from_bytes(tagContent[:1], byteorder='big')
            if condingType == 0:#0代表字符使用ISO-8859-1编码方式；
                try:
                    content = str(tagContent[1:],encoding="gbk")
                except:
                    content =""
            elif condingType == 1:#1代表字符使用UTF-16编码方式；
                try:
                    content = str(tagContent[1:],encoding="UTF-16")
                except:
                    content =""
            elif condingType == 2:#2代表字符使用 UTF-16BE编码方式；
                content =""
            elif condingType == 3:#3代表字符使用UTF-8编码方式。
                try:
                    content = str(tagContent[1:],encoding="UTF-8")
                except:
                    content =""
            if content!="":
                temp={}
                self.songTextKey=[]
                contentSplit = content.splitlines()
                for k in range(len(contentSplit)):
                    if contentSplit[k][1].isdigit():
                        xxx = contentSplit[k].split("]")
                        tempKey = "%d" %(int(xxx[0][1:3])*60 +int(xxx[0][4:6]) )
                        temp[str(tempKey)] = xxx[1]
                        self.songTextKey.append(tempKey)
                    else:
                        endKey = contentSplit[k].find("]",0)
                        self.songTextKey.append(k)
                        temp[str(k)] = contentSplit[k][1:endKey]
                self.songText = temp
            else:
                self.songText = {}
        elif tagName=="APIC":#图片
            #print("图片")
            self.currentImg = tagContent[17:]
        return data[10+sizeS:]