from form import Ui_MultiPrint
from PyQt5 import QtWidgets,QtGui,QtCore
import sys
from opengl.gl_widget import GLWidget
from widget.Axis import Drawing
from widget.Inject import Inject
from widget.ToolBar import ToolBar
from Optimizermaster.FileHandler import FileHandler
from numpy import array
class myform(Ui_MultiPrint,QtWidgets.QWidget):
    def __init__(self):
        super(myform,self).__init__()
        self.setupUi(self)
        #初始化工具栏
        self.initToolBar()
        #初始化OpelGL
        self.opengl=GLWidget(self)
        self.verticalLayout_3.addWidget(self.opengl)
        #初始化左侧显示区
        self.initInject()
        
        '''path=r"E:\模型\蝴蝶.stl"
        file=FileHandler().load_mesh(path)#f[0]是路径，f[1]是类型
        data=array(file['mesh'],'f')
        self.opengl.initdata(data)'''
        #self.widget_2.initdata(data)
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.add)
        self.Move_relative_add.pressed.connect(self.start)
        self.Move_relative_add.released.connect(self.end)
    def resizeEvent(self,event):
        print(self.widget_22.rect())
        self.setToolbar()
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
    def change(self):
        self.tools_1.setStyleSheet(r"QWidget{border-image:url(resource/GCode_disabled.png)}")
    def start(self):
        self.timer.start(50)
    def end(self):
        self.timer.stop()
    def add(self):
        self.inject_1.plunger=self.inject_1.plunger+0.1
        self.inject_1.update()
app=QtWidgets.QApplication(sys.argv)
window=myform()
window.show()
app.exec_()
sys.exit()
