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
        self.analyse.showGrid(x=True, y=True)
        self.analyse.setLabel("left","Temperature","℃")
        self.analyse.setLabel("bottom","Time","s")
        self.analyse.addLegend()#增加图标
        self.analyse.plot([0],pen=(0,128,0),symbolBrush=(0,128,0),  symbol='t', symbolSize=14,name="\\      开始打印")
        self.analyse.plot([0],pen=(237,177,32),symbolBrush=(237,177,32),  symbol='star', symbolSize=14,name="\\      暂停打印")
        self.analyse.plot([0],pen=(195,46,212),symbolBrush=(195,46,212),  symbol='t2', symbolSize=14,name="\\      恢复打印")
        self.analyse.plot([0],pen=(217,83,25),symbolBrush=(217,83,25),  symbol='h', symbolSize=14,name="\\      停止打印")
        self.analyse.clear()
        self.current_temp = self.addPlot(row=2, col=0)
        self.current_temp.setLabel("left","Temperature","℃")
        self.current_temp.setLabel("bottom","Time","s")
        self.data_analyse=[]#初始化绘图数据
        self.drawLine()
        self.analyse.scene().sigMouseMoved.connect(self.mouseMoved)
        self.starttime=time
        self.stopLength=0#图1绘制时x的最大值
        self.start_point=[]
        self.pause_point=[]
        self.resume_point=[]
        self.stop_point=[]
    def addPoint(self,command,tick):
        if command=="start":
            self.start_point.append([tick-1,self.data_analyse[tick-1]])
        elif command=='pause':
            self.pause_point.append([tick-1,self.data_analyse[tick-1]])
        elif command=='resume':
            self.resume_point.append([tick-1,self.data_analyse[tick-1]])
        elif command=='stop':
            self.stop_point.append([tick-1,self.data_analyse[tick-1]])
    def drawLine(self):
        self.vline = pg.InfiniteLine(angle=90, movable=False)
        self.hline = pg.InfiniteLine(angle=0, movable=False)
        self.analyse.addItem(self.vline, ignoreBounds=True)
        self.analyse.addItem(self.hline, ignoreBounds=True)
        
    def mouseMoved(self,evt):
        if self.analyse.sceneBoundingRect().contains(evt):
            mousePoint = self.analyse.vb.mapSceneToView(evt)
            index = int(mousePoint.x()+0.5)
            if index >= 0 and index < self.stopLength:
                time=self.starttime+datetime.timedelta(seconds=index)
                strtime=time.strftime('%Y.%m.%d %H:%M:%S')
                self.label.setText("<span style='color: green'>x=%s<span style='color: red'>      y=%0.1f°C</span>" % (strtime,self.data_analyse[index]))
                self.vline.setPos(index)
                self.hline.setPos(self.data_analyse[index])
            else:
                self.vline.setPos(mousePoint.x())
                self.hline.setPos(mousePoint.y())
            
                
    def analyse_plot(self):
        self.stopLength=len(self.data_analyse)
        self.analyse.clear()
        self.drawLine()
        self.analyse.plot(self.data_analyse,pen='r')
        for point in self.start_point:
            self.analyse.plot(x=[point[0]],y=[point[1]],pen=(0,128,0),symbolBrush=(0,128,0), symbol='t', symbolSize=14)
        for point in self.pause_point:
            self.analyse.plot(x=[point[0]],y=[point[1]],pen=(237,177,32),symbolBrush=(237,177,32), symbol='star', symbolSize=14)
        for point in self.resume_point:
            self.analyse.plot(x=[point[0]],y=[point[1]],pen=(195,46,212),symbolBrush=(195,46,212),  symbol='t2', symbolSize=14)
        for point in self.stop_point:
            self.analyse.plot(x=[point[0]],y=[point[1]],pen=(217,83,25),symbolBrush=(217,83,25), symbol='h', symbolSize=14)
        
        #self.analyse.plot(x=[1],y=[10],pen=(0,200,200),symbolBrush=(0,200,200), symbolPen='w', symbol='h', symbolSize=14, name="symbol='h'")
    def current_temp_plot(self):
        self.current_temp.clear()
        self.current_temp.plot(self.data_analyse,pen='w')


if __name__=='__main__':
    app=QApplication(sys.argv)
    myform=Drawing()
    myform.show()
    app.exec_()
    sys.exit()
