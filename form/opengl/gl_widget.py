from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GLU import *
from OpenGL.GLUT import *
from opengl.Camera import camera
from opengl.Vector3f import *
from opengl.Light import Light,Materials
from numpy import array
import numpy as np
class GLWidget(QOpenGLWidget):
    def __init__(self, *args, **kwargs):
        super(GLWidget, self).__init__(*args, **kwargs)
        self.setGeometry(QtCore.QRect(10, 10,700, 700))#窗口位置和大小
        self.isMove=False
        self.isRotate=False
        self.data=None#该列表需要存储一个一个的字典，字典形式为{'material':Materials,'data':numpy.array()}，每一个model[x]代表一个模型，包含材质和点的数据
        self.quad=gluNewQuadric()
        self.showlayer=0
    def changeGeometry(self,x,y,width,height):
        self.setGeometry(QtCore.QRect(x, y,width, height))
    def initdata(self,data):
        self.data=data
    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1,1,1,0)
        self.camera=camera()
        #self.light=Light(Materials[0])
    def paintGL(self):
        self.camera.Update()
        #绘制基板
        self.drawBase(200,200)
        glPushMatrix()
        #self.light.Update(Materials[0])
        if self.data:
            self.drawLine(self.showlayer)
        glPopMatrix()
    def drawLine(self,showline):
        for lines in self.data[showline]:
            glBegin(GL_LINE_LOOP)
            glColor(1,0,0)
            for line in lines:
                glVertex(line[0],line[1],line[2])
            glEnd()
    def drawBase(self,width,height):
        w_increment=width/8
        h_increment=height/8
        glColor(0,0,0)
        glBegin(GL_LINES)
        for i in range(9):
            glVertex(w_increment*i,0,-1)
            glVertex(w_increment*i,height,-1)
        for i in range(9):
            glVertex(0,h_increment*i,-1)
            glVertex(width,h_increment*i,-1)
        glEnd()
        
        glBegin(GL_POLYGON)
        glColor(0,1,0)
        #glPointSize(3.0) 
        x,y=self.circle(0,0,3,100)
        for x_,y_ in zip(x,y):
            glVertex(x_,y_,-1)
        glEnd()
    def circle(self,x, y, r, n):
        theta = np.linspace(0, 2*np.pi, n)
        x = x + r * np.cos(theta)
        y = y + r * np.sin(theta)
        return x, y    
    #该函数用来截屏并保存为png图像，glReadPixels的参数以窗体左下角为坐标原点。
    def geti(self):
        data = glReadPixels(10, 190, 700, 700, GL_RGBA, GL_UNSIGNED_BYTE)
        import png
        png.write(open("screen_shot.png", "wb"), 700, 700, 4, data)
   
    def mousePressEvent(self,event):
        self.myMousePosition=event.pos()
        if event.button()==QtCore.Qt.LeftButton:
            self.isMove=True
        #if event.button()==QtCore.Qt.RightButton:
            #self.isRotate=True
        #self.update()
    def wheelEvent(self,event):
        if event.angleDelta().y()>0:
            self.camera.right*=0.95
            self.camera.top*=0.95
        if event.angleDelta().y()<0:
            self.camera.right/=0.95
            self.camera.top/=0.95
        self.update()
    def mouseReleaseEvent(self,event):
        if event.button()==QtCore.Qt.LeftButton:
            self.isMove=False
        #if event.button()==QtCore.Qt.RightButton:
            #self.isRotate=False
    def mouseMoveEvent(self,event):
        if self.isMove:
            moveX=event.pos().x()-self.myMousePosition.x()
            moveY=event.pos().y()-self.myMousePosition.y()
            self.camera.Move(moveX*self.camera.right/250,moveY*self.camera.right/250)
            self.myMousePosition=event.pos()
        if self.isRotate:
            moveX=event.pos().x()-self.myMousePosition.x()
            moveY=event.pos().y()-self.myMousePosition.y()
            self.camera.Yaw(-moveX)
            self.camera.Pitch(-moveY)
            self.light.lightpos=[-self.camera.forwardDir.X,-self.camera.forwardDir.Y,-self.camera.forwardDir.Z,0]
            self.myMousePosition=event.pos()
        self.update()
