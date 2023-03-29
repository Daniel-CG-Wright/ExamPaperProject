# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'questionbankmainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ViewAllQuestions(object):
    def setupUi(self, ViewAllQuestions):
        ViewAllQuestions.setObjectName("ViewAllQuestions")
        ViewAllQuestions.resize(715, 537)
        font = QtGui.QFont()
        font.setPointSize(11)
        ViewAllQuestions.setFont(font)
        ViewAllQuestions.setDocumentMode(False)
        ViewAllQuestions.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(ViewAllQuestions)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 678, 854))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lMin = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lMin.setObjectName("lMin")
        self.horizontalLayout_2.addWidget(self.lMin)
        self.sbMin = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.sbMin.setObjectName("sbMin")
        self.horizontalLayout_2.addWidget(self.sbMin)
        self.lMax = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lMax.setObjectName("lMax")
        self.horizontalLayout_2.addWidget(self.lMax)
        self.sbMax = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        self.sbMax.setObjectName("sbMax")
        self.horizontalLayout_2.addWidget(self.sbMax)
        self.checkBoxForSingleParts = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBoxForSingleParts.setObjectName("checkBoxForSingleParts")
        self.horizontalLayout_2.addWidget(self.checkBoxForSingleParts)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cbSelectTopic = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbSelectTopic.sizePolicy().hasHeightForWidth())
        self.cbSelectTopic.setSizePolicy(sizePolicy)
        self.cbSelectTopic.setObjectName("cbSelectTopic")
        self.horizontalLayout.addWidget(self.cbSelectTopic)
        self.cbComponent = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbComponent.sizePolicy().hasHeightForWidth())
        self.cbComponent.setSizePolicy(sizePolicy)
        self.cbComponent.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.cbComponent.setObjectName("cbComponent")
        self.horizontalLayout.addWidget(self.cbComponent)
        self.cbLevel = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbLevel.sizePolicy().hasHeightForWidth())
        self.cbLevel.setSizePolicy(sizePolicy)
        self.cbLevel.setObjectName("cbLevel")
        self.horizontalLayout.addWidget(self.cbLevel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.lTip = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lTip.setObjectName("lTip")
        self.verticalLayout_2.addWidget(self.lTip)
        self.lWjec = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lWjec.setObjectName("lWjec")
        self.verticalLayout_2.addWidget(self.lWjec)
        self.twQuestionBank = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.twQuestionBank.sizePolicy().hasHeightForWidth())
        self.twQuestionBank.setSizePolicy(sizePolicy)
        self.twQuestionBank.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twQuestionBank.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.twQuestionBank.setObjectName("twQuestionBank")
        self.twQuestionBank.setColumnCount(0)
        self.twQuestionBank.setRowCount(0)
        self.twQuestionBank.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.twQuestionBank)
        self.twParts = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.twParts.sizePolicy().hasHeightForWidth())
        self.twParts.setSizePolicy(sizePolicy)
        self.twParts.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twParts.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.twParts.setObjectName("twParts")
        self.twParts.setColumnCount(0)
        self.twParts.setRowCount(0)
        self.twParts.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.twParts)
        self.teQuestionPreview = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.teQuestionPreview.sizePolicy().hasHeightForWidth())
        self.teQuestionPreview.setSizePolicy(sizePolicy)
        self.teQuestionPreview.setUndoRedoEnabled(False)
        self.teQuestionPreview.setReadOnly(True)
        self.teQuestionPreview.setObjectName("teQuestionPreview")
        self.verticalLayout_2.addWidget(self.teQuestionPreview)
        self.pbShowMarkscheme = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pbShowMarkscheme.setObjectName("pbShowMarkscheme")
        self.verticalLayout_2.addWidget(self.pbShowMarkscheme)
        self.pbViewImages = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pbViewImages.setObjectName("pbViewImages")
        self.verticalLayout_2.addWidget(self.pbViewImages)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pbAddQuestion = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pbAddQuestion.setObjectName("pbAddQuestion")
        self.horizontalLayout_3.addWidget(self.pbAddQuestion)
        self.pbEditQuestion = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pbEditQuestion.setObjectName("pbEditQuestion")
        self.horizontalLayout_3.addWidget(self.pbEditQuestion)
        self.pbDeleteQuestion = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pbDeleteQuestion.setObjectName("pbDeleteQuestion")
        self.horizontalLayout_3.addWidget(self.pbDeleteQuestion)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        ViewAllQuestions.setCentralWidget(self.centralwidget)

        self.retranslateUi(ViewAllQuestions)
        QtCore.QMetaObject.connectSlotsByName(ViewAllQuestions)

    def retranslateUi(self, ViewAllQuestions):
        _translate = QtCore.QCoreApplication.translate
        ViewAllQuestions.setWindowTitle(_translate("ViewAllQuestions", "Question Bank"))
        self.lineEdit.setPlaceholderText(_translate("ViewAllQuestions", "Search question contents..."))
        self.lMin.setText(_translate("ViewAllQuestions", "Min marks:"))
        self.lMax.setText(_translate("ViewAllQuestions", "Max marks:"))
        self.checkBoxForSingleParts.setText(_translate("ViewAllQuestions", "0 parts"))
        self.lTip.setText(_translate("ViewAllQuestions", "Click on a question to view all parts. 0 parts - return single part questions (good for long answer Qs)"))
        self.lWjec.setText(_translate("ViewAllQuestions", "WJEC units 1 and 3 = component 1. WJEC unit 4 = component 2"))
        self.pbShowMarkscheme.setText(_translate("ViewAllQuestions", "Show Markscheme"))
        self.pbViewImages.setText(_translate("ViewAllQuestions", "View images for this question"))
        self.pbAddQuestion.setText(_translate("ViewAllQuestions", "Add Question"))
        self.pbEditQuestion.setText(_translate("ViewAllQuestions", "Edit Question"))
        self.pbDeleteQuestion.setText(_translate("ViewAllQuestions", "Delete question"))
