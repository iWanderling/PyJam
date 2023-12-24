from PyQt5 import QtCore, QtGui, QtWidgets


# pyuic5 name.ui -o name.py


class UI_PyJam(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(412, 572)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet("QWidget { background-color: #0d6efd; font-style: Yu Gothic UI Semibold;}\n"
"\n"
"QLabel { color: white }\n"
"\n"
"QPushButton {\n"
"  background-color: white;\n"
"  color: #0d6efd;\n"
"  font-weight: 700;\n"
"  border-radius: 8px;\n"
"  border: 1px solid #0d6efd;\n"
"  padding: 5px 15px;\n"
"  margin-top: 10px;\n"
"  outline: 0px;\n"
"}\n"
"\n"
"QPushButton:hover,\n"
"QPushButton:focus {\n"
"  background-color: #eceeee;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(50, 20, 311, 310))
        self.imageLabel.setStyleSheet("background-color: white;\n"
"border-radius: 10px;")
        self.imageLabel.setText("")
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setObjectName("imageLabel")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 420, 391, 62))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.recognizeSong_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.recognizeSong_Button.setStyleSheet("")
        self.recognizeSong_Button.setObjectName("recognizeSong_Button")
        self.horizontalLayout.addWidget(self.recognizeSong_Button)
        self.recognizeFile_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.recognizeFile_Button.setStyleSheet("")
        self.recognizeFile_Button.setObjectName("recognizeFile_Button")
        self.horizontalLayout.addWidget(self.recognizeFile_Button)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 470, 391, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.search_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.search_Button.setObjectName("search_Button")
        self.horizontalLayout_2.addWidget(self.search_Button)
        self.copyLink_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.copyLink_Button.setObjectName("copyLink_Button")
        self.horizontalLayout_2.addWidget(self.copyLink_Button)
        self.recognized_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.recognized_Button.setObjectName("recognized_Button")
        self.horizontalLayout_2.addWidget(self.recognized_Button)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 340, 391, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.showTrackLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.showTrackLabel.setFont(font)
        self.showTrackLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.showTrackLabel.setObjectName("showTrackLabel")
        self.verticalLayout.addWidget(self.showTrackLabel)
        self.showBandLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.showBandLabel.setFont(font)
        self.showBandLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.showBandLabel.setObjectName("showBandLabel")
        self.verticalLayout.addWidget(self.showBandLabel)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 412, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.recognizeSong_Button.setText(_translate("MainWindow", "Распознать музыку"))
        self.recognizeFile_Button.setText(_translate("MainWindow", "Распознать аудиофайл"))
        self.search_Button.setText(_translate("MainWindow", "Поиск"))
        self.copyLink_Button.setText(_translate("MainWindow", "Скопировать ссылку"))
        self.recognized_Button.setText(_translate("MainWindow", "Распознанное"))
        self.showTrackLabel.setText(_translate("MainWindow", "Нажмите кнопку, чтобы начать"))
        self.showBandLabel.setText(_translate("MainWindow", ":)"))


class UI_Charts(object):
    def setupUi(self, Charts):
        Charts.setObjectName("Charts")
        Charts.resize(412, 572)
        Charts.setStyleSheet("QWidget { background-color: #0d6efd; font-style: Yu Gothic UI Semibold;}\n"
"\n"
"QLabel { color: white }\n"
"\n"
"QPushButton {\n"
"  background-color: white;\n"
"  color: #0d6efd;\n"
"  font-weight: 700;\n"
"  border-radius: 8px;\n"
"  border: 1px solid #0d6efd;\n"
"  padding: 5px 15px;\n"
"  margin-top: 10px;\n"
"  outline: 0px;\n"
"}\n"
"\n"
"QPushButton:hover,\n"
"QPushButton:focus {\n"
"  background-color: #eceeee;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(Charts)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 420, 331, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.worldTop_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.worldTop_Button.setObjectName("worldTop_Button")
        self.horizontalLayout.addWidget(self.worldTop_Button)
        self.countryTop_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(87)
        self.countryTop_Button.setFont(font)
        self.countryTop_Button.setObjectName("countryTop_Button")
        self.horizontalLayout.addWidget(self.countryTop_Button)
        self.cityTop_Button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cityTop_Button.setObjectName("cityTop_Button")
        self.horizontalLayout.addWidget(self.cityTop_Button)
        self.copyLink_Button = QtWidgets.QPushButton(self.centralwidget)
        self.copyLink_Button.setGeometry(QtCore.QRect(40, 460, 331, 41))
        self.copyLink_Button.setObjectName("copyLink_Button")
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(50, 20, 311, 310))
        self.imageLabel.setStyleSheet("background-color: white;\n"
"border-radius: 10px;")
        self.imageLabel.setText("")
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setObjectName("imageLabel")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 340, 391, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.showTrackLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.showTrackLabel.setFont(font)
        self.showTrackLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.showTrackLabel.setObjectName("showTrackLabel")
        self.verticalLayout.addWidget(self.showTrackLabel)
        self.showBandLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.showBandLabel.setFont(font)
        self.showBandLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.showBandLabel.setObjectName("showBandLabel")
        self.verticalLayout.addWidget(self.showBandLabel)
        Charts.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Charts)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 412, 26))
        self.menubar.setObjectName("menubar")
        Charts.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Charts)
        self.statusbar.setObjectName("statusbar")
        Charts.setStatusBar(self.statusbar)

        self.retranslateUi(Charts)
        QtCore.QMetaObject.connectSlotsByName(Charts)

    def retranslateUi(self, Charts):
        _translate = QtCore.QCoreApplication.translate
        Charts.setWindowTitle(_translate("Charts", "MainWindow"))
        self.worldTop_Button.setText(_translate("Charts", "Топ мира"))
        self.countryTop_Button.setText(_translate("Charts", "Топ страны"))
        self.cityTop_Button.setText(_translate("Charts", "Топ города"))
        self.copyLink_Button.setText(_translate("Charts", "Скопировать ссылку"))
        self.showTrackLabel.setText(_translate("Charts", "Нажмите кнопку, чтобы начать"))
        self.showBandLabel.setText(_translate("Charts", ":)"))


class UI_DataBaseWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("QWidget { background-color: #0d6efd; font-style: Yu Gothic UI Semibold;}\n"
"\n"
"QLabel { color: white; font-style: Yu Gothic UI Semibold;}\n"
"\n"
"QPushButton {\n"
"  background-color: white;\n"
"  color: #0d6efd;\n"
"  font-weight: 700;\n"
"  border-radius: 8px;\n"
"  border: 1px solid #0d6efd;\n"
"  padding: 5px 15px;\n"
"  margin-top: 10px;\n"
"  outline: 0px;\n"
"}\n"
"\n"
"QPushButton:hover,\n"
"QPushButton:focus {\n"
"  background-color: #eceeee;\n"
"}")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


class UI_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setStyleSheet("QWidget { background-color: #0d6efd; font-style: Yu Gothic UI Semibold;}\n"
"\n"
"QLabel { color: white }\n"
"\n"
"QPushButton {\n"
"  background-color: white;\n"
"  color: #0d6efd;\n"
"  font-weight: 700;\n"
"  border-radius: 8px;\n"
"  border: 1px solid #0d6efd;\n"
"  padding: 5px 15px;\n"
"  margin-top: 10px;\n"
"  outline: 0px;\n"
"}\n"
"\n"
"QPushButton:hover,\n"
"QPushButton:focus {\n"
"  background-color: #eceeee;\n"
"}")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))