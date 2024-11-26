from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LogIn(object):
    def setupUi(self, LogIn):
        LogIn.setObjectName("LogIn")
        LogIn.resize(778, 502)
        LogIn.setAutoFillBackground(False)
        LogIn.setStyleSheet("background-color: lightblue;")
        self.lineEdit_2 = QtWidgets.QLineEdit(LogIn)
        self.lineEdit_2.setGeometry(QtCore.QRect(340, 280, 131, 20))       
        self.lineEdit_2.setStyleSheet("background-color: white;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(LogIn)
        self.label.setGeometry(QtCore.QRect(260, 20, 281, 221))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:\\Users\\yeiru\\Documents\\College\\Third Year\\Software Engineering\\bantai_project\\SoftEng_BantAI\\../../Downloads/462560496_1136575027891776_4415080471714850003_n.png"))      
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.lineEdit_6 = QtWidgets.QLineEdit(LogIn)
        self.lineEdit_6.setGeometry(QtCore.QRect(340, 300, 31, 21))        
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_6.setAutoFillBackground(False)
        self.lineEdit_6.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"}\n"
"")
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(LogIn)
        self.lineEdit_7.setGeometry(QtCore.QRect(340, 350, 61, 21))        
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_7.setAutoFillBackground(False)
        self.lineEdit_7.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"}\n"
"")
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.pushButton = QtWidgets.QPushButton(LogIn)
        self.pushButton.setGeometry(QtCore.QRect(360, 460, 75, 23))        
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_4 = QtWidgets.QLineEdit(LogIn)
        self.lineEdit_4.setGeometry(QtCore.QRect(340, 330, 131, 20))       
        self.lineEdit_4.setStyleSheet("background-color: white;")
        self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.retranslateUi(LogIn)
        QtCore.QMetaObject.connectSlotsByName(LogIn)

    def retranslateUi(self, LogIn):
        _translate = QtCore.QCoreApplication.translate
        LogIn.setWindowTitle(_translate("LogIn", "Login Form"))
        self.lineEdit_6.setText(_translate("LogIn", "email"))
        self.lineEdit_7.setText(_translate("LogIn", "password"))
        self.pushButton.setText(_translate("LogIn", "Login"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LogIn = QtWidgets.QWidget()
    ui = Ui_LogIn()
    ui.setupUi(LogIn)
    LogIn.show()
    sys.exit(app.exec_())