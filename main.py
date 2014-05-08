__author__ = 'liaojie'
#!/usr/bin/env python
#coding:utf-8

import sys,time,os
from PyQt5.QtWidgets import QApplication
import configparser
#==========自定义包
import colors
from mainWindow import Ui_MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    colors.CONFIGFILE=configparser.ConfigParser()
    colors.CONFIGFILE.read('%sconfig.ini'%(colors.SYSPATH))
    print(colors.CONFIGFILE.sections())
    ######
    mainWindow = Ui_MainWindow()
    mainWindow.setFocus()

    if str(colors.CONFIGFILE.get('Properties',"fullscreen"))=="True":
        mainWindow.showFullScreen()
    else:
        mainWindow.show()
    sys.exit(app.exec_())
