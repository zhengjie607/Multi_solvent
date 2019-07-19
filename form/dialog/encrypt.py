# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'encrypt.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_encrypt(object):
    def setupUi(self, encrypt):
        encrypt.setObjectName("encrypt")
        encrypt.resize(400, 204)
        self.buttonBox = QtWidgets.QDialogButtonBox(encrypt)
        self.buttonBox.setGeometry(QtCore.QRect(30, 160, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtWidgets.QWidget(encrypt)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 40, 301, 102))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_date = QtWidgets.QLabel(self.layoutWidget)
        self.label_date.setAlignment(QtCore.Qt.AlignCenter)
        self.label_date.setObjectName("label_date")
        self.gridLayout.addWidget(self.label_date, 3, 1, 1, 1)
        self.tb_serialnum = QtWidgets.QLineEdit(self.layoutWidget)
        self.tb_serialnum.setObjectName("tb_serialnum")
        self.gridLayout.addWidget(self.tb_serialnum, 1, 1, 1, 1)
        self.tb_mechine = QtWidgets.QLineEdit(self.layoutWidget)
        self.tb_mechine.setReadOnly(True)
        self.tb_mechine.setObjectName("tb_mechine")
        self.gridLayout.addWidget(self.tb_mechine, 0, 1, 1, 1)
        self.label_register = QtWidgets.QLabel(self.layoutWidget)
        self.label_register.setAlignment(QtCore.Qt.AlignCenter)
        self.label_register.setObjectName("label_register")
        self.gridLayout.addWidget(self.label_register, 2, 1, 1, 1)
        self.btn_clear = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_clear.sizePolicy().hasHeightForWidth())
        self.btn_clear.setSizePolicy(sizePolicy)
        self.btn_clear.setMinimumSize(QtCore.QSize(10, 10))
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayout.addWidget(self.btn_clear, 1, 2, 1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 10)
        self.gridLayout.setColumnStretch(2, 1)

        self.retranslateUi(encrypt)
        self.buttonBox.accepted.connect(encrypt.accept)
        self.buttonBox.rejected.connect(encrypt.reject)
        QtCore.QMetaObject.connectSlotsByName(encrypt)
        self.btn_clear.clicked.connect(self.clearText)
    def clearText(self):
        self.tb_serialnum.setText("")
    def retranslateUi(self, encrypt):
        _translate = QtCore.QCoreApplication.translate
        encrypt.setWindowTitle(_translate("encrypt", "注册"))
        self.label.setText(_translate("encrypt", "机器码："))
        self.label_2.setText(_translate("encrypt", "序列号："))
        self.label_date.setText(_translate("encrypt", "TextLabel"))
        self.label_register.setText(_translate("encrypt", "TextLabel"))
        self.btn_clear.setText(_translate("encrypt", "×"))
