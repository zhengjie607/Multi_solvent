from PyQt5.QtGui import QPainter,QColor,QFont,QPen,QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QApplication
import sys
class Inject(QWidget):
    def __init__(self,*args, **kwargs):
        super(Inject,self).__init__(*args, **kwargs)
        self.plunger=0#注射器中液体容量，单位为ml
        self.image_inject_enabled=QPixmap()
        self.image_inject_disabled=QPixmap()
        self.image_plunger=QPixmap()
        '''self.image_inject_enabled.load('resource\\Inject\\inject_enabled.png')
        self.image_inject_disabled.load('resource\\Inject\\inject_disabled.png')
        self.image_plunger.load('resource\\Inject\\plunger.png')'''
        self.image_inject_enabled.load('resource/Inject/inject_enabled.png')
        self.image_inject_disabled.load('resource/Inject/inject_disabled.png')
        self.image_plunger.load('resource/Inject/plunger.png')
        self.drawpixmap=self.image_inject_disabled
    def paintEvent(self,event):
        qp=QPainter()
        qp.begin(self)
        self.getPoint(event)
        self.drawImage(qp,self.drawpixmap)
        '''text="%.2fmL"%self.plunger
        self.drawText(qp,self.x+20,self.plunger*1.5+25+self.y,text,10)'''
        qp.end()
    def drawImage(self,qp,d):
        qp.drawPixmap(self.x,self.plunger*1.5+self.y,self.w,self.h,self.image_plunger)
        qp.drawPixmap(self.x,self.y,self.w,self.h,d)
    def drawText(self,qp,x,y,text,size=15):
        qp.setPen(Qt.black)
        qp.setFont(QFont('SimSun',size))
        qp.drawText(x,y,text)
    def getPoint(self,event):
        self.x=event.rect().x()
        self.y=event.rect().y()
        self.w=event.rect().width()
        self.h=event.rect().height()
        
    
