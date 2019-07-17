from PyQt5.QtGui import QPainter,QColor,QFont,QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QApplication
import sys
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import numpy as np
import datetime
class graph(GraphicsLayoutWidget):
    def __init__(self,time,*args, **kwargs):
        super(graph,self).__init__(*args, **kwargs)
        self.label = pg.LabelItem(justify='right')
        self.addItem(self.label)
        self.analyse = self.addPlot(row=1, col=0)
        self.current_temp = self.addPlot(row=2, col=0)
        self.data_analyse=[]
        self.drawLine()
        self.analyse.scene().sigMouseMoved.connect(self.mouseMoved)
        self.vb=self.analyse.vb
        self.starttime=time
    def drawLine(self):
        self.vline = pg.InfiniteLine(angle=90, movable=False)
        self.hline = pg.InfiniteLine(angle=0, movable=False)
        self.analyse.addItem(self.vline, ignoreBounds=True)
        self.analyse.addItem(self.hline, ignoreBounds=True)
    def mouseMoved(self,evt):
        if self.analyse.sceneBoundingRect().contains(evt):
            mousePoint = self.vb.mapSceneToView(evt)
            self.index = int(mousePoint.x()+0.5)
            if self.index > 0 and self.index < len(self.data_analyse):
                time=self.starttime+datetime.timedelta(seconds=self.index)
                strtime=time.strftime('%Y年%m月%d日 %H:%M:%S')
                self.label.setText("<span style='color: green'>x=%s<span style='color: red'>      y=%0.1f°C</span>" % (strtime,self.data_analyse[self.index]))
            
            if len(self.data_analyse)==0:
                self.vline.setPos(mousePoint.x())
                self.hline.setPos(mousePoint.y())
            else:
                self.vline.setPos(self.index)
                self.hline.setPos(self.data_analyse[self.index])
    def analyse_plot(self):
        self.analyse.clear()
        self.drawLine()
        self.analyse.plot(self.data_analyse,pen='r')
        
    def current_temp_plot(self,data):
        self.current_temp.clear()
        self.current_temp.plot(data,pen='r')


if __name__=='__main__':
    app=QApplication(sys.argv)
    myform=Drawing()
    myform.show()
    app.exec_()
    sys.exit()
