from PyQt5.QtGui import QPainter,QColor,QFont,QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QApplication
import sys
class Drawing(QWidget):
    def __init__(self,*args, **kwargs):
        super(Drawing,self).__init__(*args, **kwargs)
        #由打印机传入x,y,z坐标点
        self.x=0
        self.y=0
        self.z=0
        #打印机长、宽和高
        self.w=150
        self.h=150
        self.zAxis=150
    def paintEvent(self,event):
        rect=event.rect()
        qp=QPainter()
        qp.begin(self)
        self.getPoint(event.rect())
        self.drawXYZ(qp)
        self.drawAxis(qp)
        self.drawLabel(qp)
        qp.end()
    def drawText(self,qp,x,y,text,size=15):
        qp.setPen(Qt.black)
        qp.setFont(QFont('SimSun',size))
        qp.drawText(x,y,text)
    def drawLabel(self,qp):
        self.drawText(qp,self.XY_x-15,self.XY_y,'y')
        self.drawText(qp,self.XY_x-15,self.XY_y+self.XY_h+20,'0')
        self.drawText(qp,self.XY_x+self.XY_w-5,self.XY_y+self.XY_h+18,'x')
        self.drawText(qp,self.Z_x1-5,self.Z_y2+18,'z')
    def getPoint(self,rect):
        rect_h=rect.height()
        self.XY_h=rect_h*0.55
        self.XY_w=self.XY_h
        self.XY_x=0.1*rect_h
        self.XY_y=self.XY_x+20
        self.Z_x1=0.85*rect_h
        self.Z_y1=self.XY_y
        self.Z_x2=self.Z_x1
        self.Z_y2=self.XY_y+self.XY_h
    def drawXYZ(self,qp):
        qp.setPen(QPen(Qt.black,2,Qt.SolidLine))
        qp.drawRect(self.XY_x,self.XY_y,self.XY_w,self.XY_h)
        qp.drawLine(self.Z_x1,self.Z_y1,self.Z_x2,self.Z_y2)
    #绘制轴对应的点
    def drawAxis(self,qp):
        x=self.XY_w/self.w*self.x+self.XY_x
        y=-self.XY_h/self.h*self.y+self.XY_y+self.XY_h
        z=(self.Z_y1-self.Z_y2)/self.zAxis*self.z+self.Z_y2
        qp.setPen(QPen(Qt.black,0.5,Qt.SolidLine))
        qp.drawLine(self.XY_x,y,self.XY_x+self.XY_w,y)
        qp.drawLine(x,self.XY_y,x,self.XY_y+self.XY_h)
        qp.setPen(QPen(Qt.red,10,Qt.SolidLine))
        qp.drawPoint(x,y)
        qp.drawPoint(self.Z_x1,z)
        #text_xy='('+str(self.x)+','+str(self.y)+')'
        text_xy='(%.2f,%.2f)'%(self.x,self.y)
        text_z='(%.2f)'%self.z
        self.drawText(qp,x+10,y-10,text_xy,10)
        self.drawText(qp,self.Z_x1+5,z+5,text_z,10)
    def changeXYZ_Relative(self,x=0,y=0,z=0):
        self.x=self.x+x
        self.y=self.y+y
        self.z=self.z+z
        if self.x>self.w:
            self.x=self.w
        if self.y>self.h:
            self.y=self.h
        if self.z>self.zAxis:
            self.z=self.zAxis
if __name__=='__main__':
    app=QApplication(sys.argv)
    myform=Drawing()
    myform.show()
    app.exec_()
    sys.exit()
