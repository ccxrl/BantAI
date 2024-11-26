from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SignUp(object):
    def setupUi(self, SignUp):
        SignUp.setObjectName("SignUp")
        SignUp.resize(778, 502)
        SignUp.setAutoFillBackground(False)
        SignUp.setStyleSheet("background-color: lightblue;")
        self.lineEdit = QtWidgets.QLineEdit(SignUp)
        self.lineEdit.setGeometry(QtCore.QRect(330, 270, 131, 20))
        self.lineEdit.setStyleSheet("background-color: white;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(SignUp)
        self.lineEdit_2.setGeometry(QtCore.QRect(330, 330, 131, 20))       
        self.lineEdit_2.setStyleSheet("background-color: white;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(SignUp)
        self.label.setGeometry(QtCore.QRect(260, 20, 281, 221))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:\\Users\\yeiru\\Documents\\College\\Third Year\\Software Engineering\\bantai_project\\SoftEng_BantAI\\../../Downloads/462560496_1136575027891776_4415080471714850003_n.png"))      
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.lineEdit_5 = QtWidgets.QLineEdit(SignUp)
        self.lineEdit_5.setGeometry(QtCore.QRect(330, 290, 61, 21))        
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_5.setAutoFillBackground(False)
        self.lineEdit_5.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"}\n"
"")
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(SignUp)
        self.lineEdit_6.setGeometry(QtCore.QRect(330, 350, 31, 21))        
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
        self.lineEdit_7 = QtWidgets.QLineEdit(SignUp)
        self.lineEdit_7.setGeometry(QtCore.QRect(330, 400, 61, 21))        
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
        self.pushButton = QtWidgets.QPushButton(SignUp)
        self.pushButton.setGeometry(QtCore.QRect(360, 460, 75, 23))        
        self.pushButton.setObjectName("pushButton")
        self.lineEdit_4 = QtWidgets.QLineEdit(SignUp)
        self.lineEdit_4.setGeometry(QtCore.QRect(330, 380, 131, 20))       
        self.lineEdit_4.setStyleSheet("background-color: white;")
        self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.retranslateUi(SignUp)
        QtCore.QMetaObject.connectSlotsByName(SignUp)

    def retranslateUi(self, SignUp):
        _translate = QtCore.QCoreApplication.translate
        SignUp.setWindowTitle(_translate("SignUp", "Sign Up Form"))        
        self.lineEdit_5.setText(_translate("SignUp", "username"))
        self.lineEdit_6.setText(_translate("SignUp", "email"))
        self.lineEdit_7.setText(_translate("SignUp", "password"))
        self.pushButton.setText(_translate("SignUp", "Sign Up"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SignUp = QtWidgets.QWidget()
    ui = Ui_SignUp()
    ui.setupUi(SignUp)
    SignUp.show()
    sys.exit(app.exec_())