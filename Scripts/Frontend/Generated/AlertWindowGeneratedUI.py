# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUIdesigns/Alertwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AlertWindow(object):
    def setupUi(self, AlertWindow):
        AlertWindow.setObjectName("AlertWindow")
        AlertWindow.resize(400, 233)
        AlertWindow.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(AlertWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lAlertMessage = QtWidgets.QLabel(AlertWindow)
        font = QtGui.QFont()
        font.setFamily("Dubai")
        font.setPointSize(10)
        self.lAlertMessage.setFont(font)
        self.lAlertMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.lAlertMessage.setObjectName("lAlertMessage")
        self.verticalLayout.addWidget(self.lAlertMessage)
        self.pbAcceptAlert = QtWidgets.QPushButton(AlertWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbAcceptAlert.sizePolicy().hasHeightForWidth())
        self.pbAcceptAlert.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Dubai")
        font.setPointSize(10)
        self.pbAcceptAlert.setFont(font)
        self.pbAcceptAlert.setObjectName("pbAcceptAlert")
        self.verticalLayout.addWidget(self.pbAcceptAlert)
        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(AlertWindow)
        self.pbAcceptAlert.clicked.connect(AlertWindow.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(AlertWindow)

    def retranslateUi(self, AlertWindow):
        _translate = QtCore.QCoreApplication.translate
        AlertWindow.setWindowTitle(_translate("AlertWindow", "Dialog"))
        self.lAlertMessage.setText(_translate("AlertWindow", "placeholder alert message"))
        self.pbAcceptAlert.setText(_translate("AlertWindow", "OK"))
