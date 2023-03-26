# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUIdesigns/Confirmwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConfirmWindow(object):
    def setupUi(self, ConfirmWindow):
        ConfirmWindow.setObjectName("ConfirmWindow")
        ConfirmWindow.resize(400, 233)
        ConfirmWindow.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(ConfirmWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lAlertMessage = QtWidgets.QLabel(ConfirmWindow)
        font = QtGui.QFont()
        font.setFamily("Dubai")
        font.setPointSize(10)
        self.lAlertMessage.setFont(font)
        self.lAlertMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lAlertMessage.setObjectName("lAlertMessage")
        self.verticalLayout.addWidget(self.lAlertMessage)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbConfirm = QtWidgets.QPushButton(ConfirmWindow)
        font = QtGui.QFont()
        font.setFamily("Dubai")
        font.setPointSize(12)
        self.pbConfirm.setFont(font)
        self.pbConfirm.setStyleSheet("background-color: rgb(0, 255, 127);\n"
"")
        self.pbConfirm.setObjectName("pbConfirm")
        self.horizontalLayout.addWidget(self.pbConfirm)
        self.pbCancel = QtWidgets.QPushButton(ConfirmWindow)
        font = QtGui.QFont()
        font.setFamily("Dubai")
        font.setPointSize(12)
        self.pbCancel.setFont(font)
        self.pbCancel.setStyleSheet("border-style: solid;\n"
"border-width: 3px;\n"
"background-color: rgb(180, 0, 0);\n"
"border-color: rgb(255, 102, 0);\n"
"color: rgb(255,255,255);\n"
"")
        self.pbCancel.setObjectName("pbCancel")
        self.horizontalLayout.addWidget(self.pbCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(ConfirmWindow)
        QtCore.QMetaObject.connectSlotsByName(ConfirmWindow)

    def retranslateUi(self, ConfirmWindow):
        _translate = QtCore.QCoreApplication.translate
        ConfirmWindow.setWindowTitle(_translate("ConfirmWindow", "Confirmation Required"))
        self.lAlertMessage.setText(_translate("ConfirmWindow", "placeholder alert message"))
        self.pbConfirm.setText(_translate("ConfirmWindow", "Confirm"))
        self.pbCancel.setText(_translate("ConfirmWindow", "Cancel"))
