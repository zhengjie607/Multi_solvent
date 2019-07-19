from form import Ui_MultiPrint
from PyQt5 import QtWidgets,QtGui,QtCore
import sys
from opengl.gl_widget import GLWidget
from widget.Axis import Drawing
from widget.Inject import Inject
from widget.ToolBar import ToolBar
from widget.Graph import graph
from dialog.parasettings import Ui_Parasettings
from dialog.encrypt import Ui_encrypt
from numpy import array
import numpy as np
import pronsole
import datetime
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget
from encrypt.Bulid_SecretKey import deauthorization,getSerialNum,authorization
import uuid
from binascii import b2a_hex, a2b_hex,a2b_base64,b2a_base64
import os
class ParaDialog(QtWidgets.QDialog,Ui_Parasettings):
    def __init__(self):
        super(ParaDialog,self).__init__()
        self.setupUi(self)
class encryptDialog(QtWidgets.QDialog,Ui_encrypt):
    def __init__(self):
        super(encryptDialog,self).__init__()
        self.setupUi(self)
class myform(Ui_MultiPrint,QtWidgets.QWidget):
    def __init__(self):
        super(myform,self).__init__()
        self.setupUi(self)
        
        #初始化注册状态
        self.initRegister()


        self.firstImport=True#第一次导入文件
        self.timesecond=0#加工时间
        self.tick=0#温度曲线x点
        self.chan_1=True#选择通道1
        self.chan_2=False#选择通道2
        self.chan_both=False#选择混合通道
        self.start_time=datetime.datetime.now()#软件启动的时间点
        self.finish=False
        #self.data_temperature=[2,1,5,4,5,6,4,3,4,4,7,12,14,2,152,1,21,5,1,0,2,1,21,1,2,12,1,2,1,21,2,1,54,2,1]
        #初始化工具栏
        self.initToolBar()
        
        #初始化显示区
        self.initshow()
        
        
        #初始化左侧显示区
        self.initInject()
        
        #监控环境状态
        self.enviroment_monitor=QtCore.QTimer()
        self.enviroment_monitor.timeout.connect(self.EnviromentMonitor)
        self.enviroment_monitor.start(1000)
        
        #打印状态
        self.printing_status_monitor=QtCore.QTimer()
        self.printing_status_monitor.timeout.connect(self.printint_status)
        self.printing_status_monitor.start(50)
        
        #初始化打印机
        self.initPrinter()
        
        #初始化手动控制栏
        self.init_right()
        
        #绑定信号槽
        self.bindEvent()
    #窗口自适应  
    def resizeEvent(self,event):
        self.setToolbar()
    def initPrinter(self):
        self.printer=pronsole.pronsole()
        #self.printer.connect_to_printer('/dev/cu.usbserial-14140',250000,dtr=None)
    def initshow(self):
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setObjectName("tabWidget")
        self.opengl = GLWidget()
        self.opengl.setObjectName("opengl")
        self.tabWidget.addTab(self.opengl, "")
        #self.temperature = GraphicsLayoutWidget()
        self.temperature=graph(self.start_time)
        self.temperature.setObjectName("temperature")
        self.tabWidget.addTab(self.temperature, "")
        self.tabWidget.setTabText(0, "显示")
        self.tabWidget.setTabText(1, "温度曲线")
        self.tabWidget.setCurrentIndex(0)
        self.verticalLayout_3.addWidget(self.tabWidget)
    #初始化注册状态
    def initRegister(self):
        self.mechinaNum=getSerialNum()
        self.register=False#判定是否注册
        self.register_time=False#判定是否在注册日期之内
        self.using_day=0#剩余使用天数
        self.code=''
        
        if os.path.exists('keycode.kc'):
            f=open('keycode.kc','r')
            self.code=f.read()
            f.close()
            self.code=self.code.strip()
            code_len=len(self.code)
            code=self.code[2:code_len-3]
            serialnum,dead_day,now_day=deauthorization(bytes(code,encoding='utf-8'),"djjwiw38dn43wx1q")
            if now_day<datetime.datetime.now():
                now_day=datetime.datetime.now()
            else:
                QtWidgets.QMessageBox.critical(self,"错误","系统时间错误，软件即将退出",QtWidgets.QMessageBox.Ok)
                os._exit(5)
            if self.mechinaNum==serialnum:
                self.register=True
                if dead_day-now_day>datetime.timedelta(days=0):
                    self.register_time=True
                    self.using_day=(dead_day-now_day).days+1
            f=open('keycode.kc','w')

            newser=authorization(self.mechinaNum,self.using_day,"djjwiw38dn43wx1q")
            
            f.write(str(newser))
            f.close()
    def initInject(self):
        #绘制坐标轴
        self.widget_2=Drawing(self)
        self.verticalLayout_10.addWidget(self.widget_2)
        #1号注射器
        self.inject_1=Inject(self)
        self.gridLayout.addWidget(self.inject_1, 0, 1, 1, 1)
        #2号注射器
        self.inject_2=Inject(self)
        self.gridLayout.addWidget(self.inject_2, 0, 2, 1, 1)
        #1号打印头按钮
        self.btn_inject_1=QtWidgets.QPushButton(self.widget_inject_1)
        self.btn_inject_1.setStyleSheet(r"QPushButton{background-image:url(resource/Inject/channel_1.png)}")
        #2号打印头按钮
        self.btn_inject_2=QtWidgets.QPushButton(self.widget_inject_2)
        self.btn_inject_2.setStyleSheet(r"QPushButton{background-image:url(resource/Inject/channel_2.png)}")
        #混合打印头按钮
        self.btn_inject_both=QtWidgets.QPushButton(self.widget_hunhe)
        self.btn_inject_both.setStyleSheet(r"QPushButton{background-image:url(resource/Inject/channel_both.png)}")
        self.setChannel()#软件启动后，默认选择通道1
    #初始化右侧手动工具栏
    def init_right(self):
        self.btn_inject1_takeout.setEnabled(False)
        self.btn_inject1_enject.setEnabled(False)
        self.tb_inject1_volume.setEnabled(False)
        self.btn_inject2_takeout.setEnabled(False)
        self.btn_inject2_enject.setEnabled(False)
        self.tb_inject2_volume.setEnabled(False)
        self.btn_peristaltic_1.setEnabled(False)
        self.btn_peristaltic_both.setEnabled(False)
        self.btn_peristaltic_2.setEnabled(False)
        self.rb_x.setEnabled(False)
        self.rb_y.setEnabled(False)
        self.rb_z.setEnabled(False)
        self.Move_relative_add.setEnabled(False)
        self.btn_zero.setEnabled(False)
        self.Move_relative_positive.setEnabled(False)
        self.btn_move_positive.setEnabled(False)
        self.btn_move_nagative.setEnabled(False)
        self.tb_move.setEnabled(False)
    def setChannel(self):
        if self.chan_1:
            self.btn_inject_1.setStyleSheet(r"QPushButton{background-image:url(resource/Inject/channel_1_choose.png)}")
            self.btn_inject_2.setStyleSheet(r"QPushButton{background-image:url(resource/Inject/channel_2.png)}")
            self.btn_inject_both.setStyleSheet(r"QPushButton{background-image:url(resource/Inject/channel_both.png)}")
            self.inject_1.drawpixmap=self.inject_1.image_inject_enabled
            self.inject_1.update()
            self.inject_2.drawpixmap=self.inject_2.image_inject_disabled
            self.inject_2.update()
        elif self.chan_2:
            self.btn_inject_1.setStyleSheet(r"QPushButton{background-image:url(resource/Inject/channel_1.png)}")
            self.btn_inject_2.setStyleSheet(r"QPushButton{background-image:url(resource/Inject/channel_2_choose.png)}")
            self.btn_inject_both.setStyleSheet(r"QPushButton{background-image:url(resource/Inject/channel_both.png)}")
            self.inject_1.drawpixmap=self.inject_1.image_inject_disabled
            self.inject_1.update()
            self.inject_2.drawpixmap=self.inject_2.image_inject_enabled
            self.inject_2.update()
        elif self.chan_both:
            self.btn_inject_1.setStyleSheet(r"QPushButton{background-image:url(resource/Inject/channel_1.png)}")
            self.btn_inject_2.setStyleSheet(r"QPushButton{background-image:url(resource/Inject/channel_2.png)}")
            self.btn_inject_both.setStyleSheet(r"QPushButton{background-image:url(resource/Inject/channel_both_choose.png)}")
            self.inject_1.drawpixmap=self.inject_1.image_inject_enabled
            self.inject_1.update()
            self.inject_2.drawpixmap=self.inject_2.image_inject_enabled
            self.inject_2.update()
    def setToolbar(self):
        #设置工具栏自适应
        width=self.widget_22.rect().width()
        height=self.widget_22.rect().height()
        h=height/2-20
        w=width/14
        self.tool_1.setGeometry(QtCore.QRect(w*2, h, 40, 40))
        self.tool_2.setGeometry(QtCore.QRect(w*5, h, 40, 40))
        self.tool_3.setGeometry(QtCore.QRect(w*6, h, 40, 40))
        self.tool_4.setGeometry(QtCore.QRect(w*10, h, 40, 40))
        self.tool_5.setGeometry(QtCore.QRect(w*11, h, 40, 40))
        self.tool_6.setGeometry(QtCore.QRect(w*12, h, 40, 40))
        self.tool_7.setGeometry(QtCore.QRect(w*13, h, 40, 40))
        self.tool_8.setGeometry(QtCore.QRect(w/2, h, 40, 40))
        #设置左侧btn_1自适应
        width_btn_inject_1=self.widget_inject_1.rect().width()
        height_btn_inject_1=self.widget_inject_1.rect().height()
        h_btn_inject_1=height_btn_inject_1/2-20
        w_btn_inject_1=width_btn_inject_1/2-20
        self.btn_inject_1.setGeometry(QtCore.QRect(w_btn_inject_1, h_btn_inject_1, 40, 40))
         #设置左侧btn_2自适应
        width_btn_inject_2=self.widget_inject_2.rect().width()
        height_btn_inject_2=self.widget_inject_2.rect().height()
        h_btn_inject_2=height_btn_inject_2/2-20
        w_btn_inject_2=width_btn_inject_2/2-20
        self.btn_inject_2.setGeometry(QtCore.QRect(w_btn_inject_2, h_btn_inject_2, 40, 40))
         #设置左侧btn_both自适应
        width_btn_inject_both=self.widget_hunhe.rect().width()
        height_btn_inject_both=self.widget_hunhe.rect().height()
        h_btn_inject_both=height_btn_inject_both/2-20
        w_btn_inject_both=width_btn_inject_both/2-20
        self.btn_inject_both.setGeometry(QtCore.QRect(w_btn_inject_both, h_btn_inject_both, 40, 40))
    def initToolBar(self):
        #导入G代码
        self.tool_1=QtWidgets.QPushButton(self.widget_22)
        self.tool_1.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/gcode_enabled.png)}")
        self.tool_1.setToolTip(QtCore.QCoreApplication.translate('self.widget_22','导入G代码'))
        #打开灯光
        self.tool_2=QtWidgets.QPushButton(self.widget_22)
        self.tool_2.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/light_disabled.png)}")
        self.tool_2.setToolTip(QtCore.QCoreApplication.translate('self.widget_22','打开灯光'))
        #参数设置
        self.tool_3=QtWidgets.QPushButton(self.widget_22)
        self.tool_3.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/settins_enabled.png)}")
        self.tool_3.setToolTip(QtCore.QCoreApplication.translate('self.widget_22','参数设置'))
        #开始加工
        self.tool_4=QtWidgets.QPushButton(self.widget_22)
        self.tool_4.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/begin_disabled.png)}")
        self.tool_4.setToolTip(QtCore.QCoreApplication.translate('self.widget_22','开始加工'))
        self.tool_4.setEnabled(False)
        #暂停加工
        self.tool_5=QtWidgets.QPushButton(self.widget_22)
        self.tool_5.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/pause_disabled.png)}")
        self.tool_5.setToolTip(QtCore.QCoreApplication.translate('self.widget_22','暂停加工'))
        self.tool_5.setEnabled(False)
        #恢复加工
        self.tool_6=QtWidgets.QPushButton(self.widget_22)
        self.tool_6.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/resume_disabled.png)}")
        self.tool_6.setToolTip(QtCore.QCoreApplication.translate('self.widget_22','恢复加工'))
        self.tool_6.setEnabled(False)
        #停止加工
        self.tool_7=QtWidgets.QPushButton(self.widget_22)
        self.tool_7.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/stop_disabled.png)}")
        self.tool_7.setToolTip(QtCore.QCoreApplication.translate('self.widget_22','停止加工'))
        self.tool_7.setEnabled(False)
        #注册
        self.tool_8=QtWidgets.QPushButton(self.widget_22)
        self.tool_8.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/register.png)}")
        self.tool_8.setToolTip(QtCore.QCoreApplication.translate('self.widget_22','注册'))
    def EnviromentMonitor(self):#循环，时间间隔为1s
        
        #设置加工时间
        self.label_process_time_hour.setText(str(datetime.timedelta(seconds=self.timesecond)))
        #设置一次开始加工图标
        if self.register and self.printer.fgcode and self.firstImport and self.register_time:
            self.tool_4.setEnabled(True)
            self.tool_4.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/begin_enabled.png)}")
            self.firstImport=False
        #打印时间计算
        if self.printer.p.printing:
            self.timesecond=self.timesecond+1
        
            #设置x显示位置
        if self.printer.p.analyzer.current_x:
            self.widget_2.x=self.printer.p.analyzer.current_x
            #设置y显示位置
        if self.printer.p.analyzer.current_y:
            self.widget_2.y=self.printer.p.analyzer.current_y
            #设置z显示位置
        if self.printer.p.analyzer.current_z:
            self.widget_2.z=self.printer.p.analyzer.current_z
        self.widget_2.update()
            #设置总高度
        if self.printer.fgcode:
            if self.printer.fgcode.zmax:
                self.label_process_totallayer.setText("%.2f mm"%self.printer.fgcode.zmax)
            #设置总时间
            if self.printer.fgcode.duration:
                self.label_process_totaltime_hour.setText(str(self.printer.fgcode.duration))
        
        #设置基板温度
        if self.printer.status.bed_temp:
            self.label_temperature.setText("%d"%self.printer.status.bed_temp)
            self.temperature.data_analyse.append(self.printer.status.bed_temp)
            self.tick+=1
        else:
            self.label_temperature.setText('--')
        self.tick+=1
        self.temperature.data_analyse.append(np.random.normal())#测试用
        self.temperature.current_temp_plot()
        
        #设置注册状态
        if self.register and self.register_time:
            self.label_register.setText("已注册")
        elif self.register and not self.register_time:
            self.label_register.setText("已过期")
        else:
            self.label_register.setText("未注册")
        #设置完成百分比
        if self.printer.process:
            self.label_complete.setText("%.1f"%self.printer.process)
        #print(self.printer.p.mainqueue)
    def bindEvent(self):
        self.tool_1.clicked.connect(self.importGcode)
        self.slider_layer.valueChanged.connect(self.sliderValueChange)
        self.tb_layer.editingFinished.connect(self.tbChange)
        self.tool_4.clicked.connect(self.startPrint)
        self.tool_5.clicked.connect(self.pausePrint)
        self.tool_6.clicked.connect(self.resumePrint)
        self.tool_7.clicked.connect(self.stopPrint)
        self.cb_munnal.clicked.connect(self.munnal)
        self.btn_inject_1.clicked.connect(self.channel_1_clicked)
        self.btn_inject_2.clicked.connect(self.channel_2_clicked)
        self.btn_inject_both.clicked.connect(self.channel_both_clicked)
        self.btn_move_positive.clicked.connect(self.move_positive)
        self.btn_move_nagative.clicked.connect(self.move_nagative)
        self.Move_relative_add.pressed.connect(self.startmove_positive)
        self.Move_relative_add.released.connect(self.stopmove_positive)
        self.Move_relative_positive.pressed.connect(self.startmove_nagative)
        self.Move_relative_positive.released.connect(self.stopmove_nagative)
        self.btn_zero.clicked.connect(self.zero)
        self.tool_3.clicked.connect(self.paraSetting)
        self.tool_8.clicked.connect(self.registerform)
    def registerform(self):
        ui=encryptDialog()
        ui.tb_mechine.setText(self.mechinaNum)
        ui.tb_serialnum.setText(self.code) 
        if self.register and self.register_time:
            ui.label_register.setText("已注册")
            ui.label_date.setText('剩余天数：%d'%self.using_day)
        elif self.register:
            ui.label_register.setText("已过期")
            ui.label_date.setText('剩余天数：%d'%self.using_day)
        else:
            ui.label_register.setText("未注册")
            ui.label_date.setText('剩余天数：%d'%self.using_day)
        
        if ui.exec_():
            try:
                code=ui.tb_serialnum.text()
                code=code.strip()
                code_len=len(code)
                self.code=code[2:code_len-3]
                serialnum,dead_day,now_day=deauthorization(bytes(code,encoding='utf-8'),"djjwiw38dn43wx1q")
                if now_day<datetime.datetime.now():
                    now_day=datetime.datetime.now()
                else:
                    QtWidgets.QMessageBox.critical(self,"错误","系统时间错误，软件即将退出",QtWidgets.QMessageBox.Ok)
                    os._exit(5)
                if self.mechinaNum==serialnum:
                    self.register=True
                    if dead_day-now_day>datetime.timedelta(days=0):
                        self.register_time=True
                        self.using_day=(dead_day-now_day).days+1
                f=open('keycode.kc','w')

                newser=authorization(self.mechinaNum,self.using_day,"djjwiw38dn43wx1q")
            
                f.write(str(newser))
                f.close()
            except:
                pass
    
    def paraSetting(self):
        bed_temperature=str(self.printer.p.bed_temp_target)
        speed_xy=str(self.printer.settings.xy_feedrate)
        speed_z=str(self.printer.settings.z_feedrate)
        speed_inject=str(0.5)
        self.wid=ParaDialog()
        self.wid.bed_temperature.setText(bed_temperature)
        self.wid.speed_xy.setText(speed_xy)
        self.wid.speed_z.setText(speed_z)
        self.wid.speed_inject.setText(speed_inject)
        if self.wid.exec_():
            if self.wid.tb_bedtemp.text():
                try:
                    tmp=float(self.wid.tb_bedtemp.text())
                except:
                    tmp=float(bed_temperature)
                if tmp<0:
                    tmp=0
                if tmp>300:
                    tmp=300
                self.printer.p.bed_temp_target=tmp
            if self.wid.tb_xyspeed.text():
                try:
                    tmp=float(self.wid.tb_xyspeed.text())
                except:
                    tmp=float(speed_xy)
                if tmp<0:
                    tmp=0
                if tmp>5000:
                    tmp=5000
                self.printer.settings._set('xy_feedrate',tmp)
            if self.wid.tb_zspeed.text():
                try:
                    tmp=float(self.wid.tb_zspeed.text())
                except:
                    tmp=float(speed_z)
                if tmp<0:
                    tmp=0
                if tmp>5000:
                    tmp=5000
                self.printer.settings._set('z_feedrate',tmp)
            if self.wid.tb_injectspeed.text():
                pass
    def zero(self):
        if self.rb_x.isChecked():
            axis='x'
        elif self.rb_y.isChecked():
            axis='y'
        elif self.rb_z.isChecked():
            axis='z'
        self.printer.do_home(axis)
        self.widget_2.x=0
        self.widget_2.y=0
        self.widget_2.z=0
    def startmove_positive(self):
        self.startTimer=QtCore.QTimer()
        self.startTimer.timeout.connect(self.move_positive_no_wait)
        if self.rb_x.isChecked() or self.rb_y.isChecked():
            self.startTimer.start(12)
        elif self.rb_z.isChecked():
            self.startTimer.start(163)
        
    def stopmove_positive(self):
        self.startTimer.stop()
    def move_positive_no_wait(self):
        self.moveAxis(True,False)
    def startmove_nagative(self):
        self.startTimer=QtCore.QTimer()
        self.startTimer.timeout.connect(self.move_nagative_no_wait)
        if self.rb_x.isChecked() or self.rb_y.isChecked():
            self.startTimer.start(12)
        elif self.rb_z.isChecked():
            self.startTimer.start(163)
    def stopmove_nagative(self):
        self.startTimer.stop()
    def move_nagative_no_wait(self):
        self.moveAxis(False,False)
    def move_positive(self):
        self.moveAxis(True)
    def move_nagative(self):
        self.moveAxis(False)
    def moveAxis(self,positive,length=True):
        if self.rb_x.isChecked():
            axis='x'
        elif self.rb_y.isChecked():
            axis='y'
        elif self.rb_z.isChecked():
            axis='z'
        if length:
            try:
                print(self.tb_move.text())
                step=float(self.tb_move.text())
            except:
                step=0
        else:
            step=0.3
        if positive:
            step=abs(step)
        else:
            step=-abs(step)    
        command=axis+" "+str(step)
        self.printer.do_move(command)  
    def channel_1_clicked(self):
        if self.chan_1:
            self.chan_1=False
        else:
            self.chan_1=True
            self.chan_2=False
            self.chan_both=False
        self.setChannel()
    def channel_2_clicked(self):
        if self.chan_2:
            self.chan_2=False
        else:
            self.chan_2=True
            self.chan_1=False
            self.chan_both=False
        self.setChannel()
    def channel_both_clicked(self):
        if self.chan_both:
            self.chan_both=False
        else:
            self.chan_1=False
            self.chan_2=False
            self.chan_both=True
        self.setChannel()
    def munnal(self):
        if self.cb_munnal.isChecked():
            self.btn_inject1_takeout.setEnabled(True)
            self.btn_inject1_enject.setEnabled(True)
            self.tb_inject1_volume.setEnabled(True)
            self.btn_inject2_takeout.setEnabled(True)
            self.btn_inject2_enject.setEnabled(True)
            self.tb_inject2_volume.setEnabled(True)
            self.btn_peristaltic_1.setEnabled(True)
            self.btn_peristaltic_both.setEnabled(True)
            self.btn_peristaltic_2.setEnabled(True)
            self.rb_x.setEnabled(True)
            self.rb_y.setEnabled(True)
            self.rb_z.setEnabled(True)
            self.Move_relative_add.setEnabled(True)
            self.btn_zero.setEnabled(True)
            self.Move_relative_positive.setEnabled(True)
            self.btn_move_positive.setEnabled(True)
            self.btn_move_nagative.setEnabled(True)
            self.tb_move.setEnabled(True)
        else:
            self.btn_inject1_takeout.setEnabled(False)
            self.btn_inject1_enject.setEnabled(False)
            self.tb_inject1_volume.setEnabled(False)
            self.btn_inject2_takeout.setEnabled(False)
            self.btn_inject2_enject.setEnabled(False)
            self.tb_inject2_volume.setEnabled(False)
            self.btn_peristaltic_1.setEnabled(False)
            self.btn_peristaltic_both.setEnabled(False)
            self.btn_peristaltic_2.setEnabled(False)
            self.rb_x.setEnabled(False)
            self.rb_y.setEnabled(False)
            self.rb_z.setEnabled(False)
            self.Move_relative_add.setEnabled(False)
            self.btn_zero.setEnabled(False)
            self.Move_relative_positive.setEnabled(False)
            self.btn_move_positive.setEnabled(False)
            self.btn_move_nagative.setEnabled(False)
            self.tb_move.setEnabled(False)
    def printint_status(self):
        #设置当前状态
        if self.printer.p.printing:
            self.label_status.setText("正在打印")
            if self.printer.fgcode.has_index(self.printer.p.queueindex):
                layer,line=self.printer.fgcode.idxs(self.printer.p.queueindex)
                self.slider_layer.setValue(layer-1)
            #设置加工高度
            self.label_process_layer.setText("%.2f mm"%self.printer.layer_height[layer-2])
            self.tool_4.setEnabled(False)
            self.tool_4.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/begin_disabled.png)}")
            self.tool_5.setEnabled(True)
            self.tool_5.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/pause_enabled.png)}")
            self.tool_6.setEnabled(False)
            self.tool_6.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/resume_disabled.png)}")
            self.tool_7.setEnabled(True)
            self.tool_7.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/stop_enabled.png)}")
            self.tool_1.setEnabled(False)
            self.tool_1.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/gcode_disabled.png)}")
            self.tool_3.setEnabled(False)
            self.tool_3.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/settins_disabled.png)}")
            self.btn_inject_1.setEnabled(False)
            self.btn_inject_2.setEnabled(False)
            self.btn_inject_both.setEnabled(False)
            self.cb_munnal.setChecked(False)
            self.munnal()
            self.cb_munnal.setEnabled(False)
            if self.printer.p.queueindex==len(self.printer.p.mainqueue):
                self.temperature.addPoint('stop',self.tick)
                self.temperature.analyse_plot()
        elif self.printer.paused:
            self.label_status.setText("已暂停")
            self.tool_4.setEnabled(False)
            self.tool_4.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/begin_disabled.png)}")
            self.tool_5.setEnabled(False)
            self.tool_5.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/pause_disabled.png)}")
            self.tool_6.setEnabled(True)
            self.tool_6.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/resume_enabled.png)}")
            self.tool_7.setEnabled(True)
            self.tool_7.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/stop_enabled.png)}")
            self.tool_3.setEnabled(True)
            self.tool_3.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/settins_enabled.png)}")
            self.cb_munnal.setEnabled(True)
            
            
        else:
            if self.register and self.printer.fgcode and self.register_time:
                self.tool_4.setEnabled(True)
                self.tool_4.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/begin_enabled.png)}")
            else:
                self.tool_4.setEnabled(False)
                self.tool_4.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/begin_disabled.png)}")
            self.label_status.setText("已停止")
            self.tool_5.setEnabled(False)
            self.tool_5.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/pause_disabled.png)}")
            self.tool_6.setEnabled(False)
            self.tool_6.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/resume_disabled.png)}")
            self.tool_7.setEnabled(False)
            self.tool_7.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/stop_disabled.png)}")
            self.cb_munnal.setEnabled(True)
            self.tool_1.setEnabled(True)
            self.tool_1.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/gcode_enabled.png)}")
            self.tool_3.setEnabled(True)
            self.tool_3.setStyleSheet(r"QPushButton{background-image:url(resource/ToolBar/settins_enabled.png)}")
            self.btn_inject_1.setEnabled(True)
            self.btn_inject_2.setEnabled(True)
            self.btn_inject_both.setEnabled(True)
    def startPrint(self):
        if self.slider_layer.value()!=1:
            attention=QtWidgets.QMessageBox()
            reply=attention.question(self,"请注意","当前显示不是第一层，点击“Yes”后从当前层开始打印，点击“No”后从第一层开始打印",
                                             QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.Yes)
            if reply==QtWidgets.QMessageBox.Yes:
                self.printer.p.skip_layer=int(self.slider_layer.value())
        self.temperature.addPoint('start',self.tick)
        self.temperature.analyse_plot()
        self.timesecond=0
        self.printer.do_print(1)
        
    def pausePrint(self):
        self.temperature.addPoint('pause',self.tick)
        self.temperature.analyse_plot()
        self.printer.pause()
        self.printer.do_move('z 5')
        self.printer.do_home("xy")
    def resumePrint(self):
        self.printer.do_resume(1)
        self.temperature.addPoint('resume',self.tick)
        self.temperature.analyse_plot()
    def stopPrint(self):
        attention=QtWidgets.QMessageBox()
        reply=attention.question(self,"是否取消打印？","取消打印后无法恢复，请确认是否取消打印！",
                                             QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.Yes)
        if reply==QtWidgets.QMessageBox.Yes:
            self.printer.p.cancelprint()
            self.temperature.addPoint('stop',self.tick)
            self.temperature.analyse_plot()
    def tbChange(self):
        slider_value=self.slider_layer.value()
        slider_max=self.slider_layer.maximum()
        try:
            value=int(self.tb_layer.text())
        except:
            value=slider_value
        if value<1:
            value=1
        if value>slider_max:
            value=slider_max
        self.slider_layer.setValue(value)
        self.tb_layer.setText(str(value))
    def sliderValueChange(self):
        self.tb_layer.setText(str(self.slider_layer.value()))
        self.opengl.showlayer=self.slider_layer.value()-1
        self.opengl.update()
    
    def importGcode(self):
        dlg=QtWidgets.QFileDialog()
        f=dlg.getOpenFileName(self,'Open File','.','GCode file (*.gcode)')
        if f[0]:
            self.printer.do_load(f[0])
            self.slider_layer.setMaximum(len(self.printer.all_layers_for_opengl))
            self.opengl.initdata(self.printer.all_layers_for_opengl)
            self.opengl.update()
            for line in self.printer.fgcode.all_layers[1]:
                if line.command=='M190':
                    s=line.raw.split()[-1]
                    s=s.replace('S','')
                    self.printer.p.bed_temp_target=float(s)
if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    window=myform()
    window.show()
    app.exec_()
    sys.exit()