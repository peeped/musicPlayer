__author__ = 'lj'
#!/usr/bin/env python
#coding:utf-8
from PyQt5.QtCore import (QPointF,QRectF,QSizeF,pyqtSignal)
from PyQt5.QtWidgets import (QGraphicsObject)
from PyQt5.QtGui import QPixmap

class ButtonPixmap(QGraphicsObject):
    clicked = pyqtSignal(str,str)
    def __init__(self, pix,name=None):
        super(ButtonPixmap, self).__init__()
        self.p = QPixmap(pix)
        self.name = name

    def paint(self, painter, option, widget):
        painter.drawPixmap(QPointF(), self.p)

    def boundingRect(self):
        return QRectF(QPointF(0, 0), QSizeF(self.p.size()))

    def mousePressEvent(self, event):
        #print("鼠标按下:::",self.name)
        self.clicked.emit(self.name,"press")
        event.accept()
    def mouseReleaseEvent(self, event):
        #print("鼠标释放:::",self.name)
        self.clicked.emit(self.name,"release")
        event.accept()

    def setGeometry(self, rect):
        super(ButtonPixmap, self).setGeometry(rect)
        if rect.size().width() > self.p.size().width():
            self.p = self.p.scaled(rect.size().toSize())
        else:
            self.p = QPixmap(self.p)