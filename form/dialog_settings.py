# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_settings.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_settings(object):
    def setupUi(self, Dialog_settings):
        Dialog_settings.setObjectName("Dialog_settings")
        Dialog_settings.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_settings)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog_settings)
        self.buttonBox.accepted.connect(Dialog_settings.accept)
        self.buttonBox.rejected.connect(Dialog_settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_settings)

    def retranslateUi(self, Dialog_settings):
        _translate = QtCore.QCoreApplication.translate
        Dialog_settings.setWindowTitle(_translate("Dialog_settings", "Dialog"))
