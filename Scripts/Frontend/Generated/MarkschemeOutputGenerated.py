# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'markschemeoutputmainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TextDialog(object):
    def setupUi(self, TextDialog):
        TextDialog.setObjectName("TextDialog")
        TextDialog.resize(558, 500)
        font = QtGui.QFont()
        font.setPointSize(11)
        TextDialog.setFont(font)
        self.centralwidget = QtWidgets.QWidget(TextDialog)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lMarkschemeNotice = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lMarkschemeNotice.sizePolicy().hasHeightForWidth())
        self.lMarkschemeNotice.setSizePolicy(sizePolicy)
        self.lMarkschemeNotice.setObjectName("lMarkschemeNotice")
        self.verticalLayout.addWidget(self.lMarkschemeNotice)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.pbShowImages = QtWidgets.QPushButton(self.centralwidget)
        self.pbShowImages.setObjectName("pbShowImages")
        self.verticalLayout.addWidget(self.pbShowImages)
        TextDialog.setCentralWidget(self.centralwidget)

        self.retranslateUi(TextDialog)
        QtCore.QMetaObject.connectSlotsByName(TextDialog)

    def retranslateUi(self, TextDialog):
        _translate = QtCore.QCoreApplication.translate
        TextDialog.setWindowTitle(_translate("TextDialog", "Markscheme"))
        self.lMarkschemeNotice.setText(_translate("TextDialog", "TextLabel"))
        self.pbShowImages.setText(_translate("TextDialog", "Show markscheme images"))
