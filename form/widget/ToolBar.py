from PyQt5.QtGui import QPainter,QColor,QFont,QPen,QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton
import sys
class ToolBar(QWidget):
    def __init__(self,parent=None):
        super(ToolBar,self).__init__(parent)
        self.btn=QPushButton(self)
        #self.setStyleSheet("background-color: rgb(214, 214, 214);")
        #self.setObjectName("widget_22")
        self.rect1=self.rect()
        #self.btn=QPushButton(self)
        
        
        print(self.rect1)
    def paintEvent(self,event):
        self.rect1=event.rect()
        print("new rect:",self.rect1)


        
    def drawImage(self,qp):
        qp.drawPixmap(self.x,self.plunger*1.5+self.y,self.w,self.h,self.image_plunger)
        qp.drawPixmap(self.x,self.y,self.w,self.h,self.image_inject_disabled)
    def drawText(self,qp,x,y,text,size=15):
        qp.setPen(Qt.black)
        qp.setFont(QFont('SimSun',size))
        qp.drawText(x,y,text)
    def getPoint(self,event):
        self.x=event.rect().x()
        self.y=event.rect().y()
        self.w=event.rect().width()
        self.h=event.rect().height()
        
    
