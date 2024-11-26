from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(778, 502)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet("background-color: lightblue;")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(330, 270, 131, 20))
        self.lineEdit.setStyleSheet("background-color: white;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(330, 330, 131, 20))
        self.lineEdit_2.setStyleSheet("background-color: white;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(330, 380, 131, 20))
        self.lineEdit_3.setStyleSheet("background-color: white;")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(320, 40, 161, 91))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:\\Users\\jayce\\.designer\\templates\\../../Downloads/image-removebg-preview.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(360, 130, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_4.setAutoFillBackground(False)
        self.lineEdit_4.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"}\n"
"")
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(Form)
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
        self.lineEdit_6 = QtWidgets.QLineEdit(Form)
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
        self.lineEdit_7 = QtWidgets.QLineEdit(Form)
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
        self.lineEdit_8 = QtWidgets.QLineEdit(Form)
        self.lineEdit_8.setGeometry(QtCore.QRect(350, 240, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_8.setAutoFillBackground(False)
        self.lineEdit_8.setStyleSheet("QLineEdit {\n"
"    border: none;\n"
"}\n"
"")
        self.lineEdit_8.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_8.setObjectName("lineEdit_8")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lineEdit_4.setText(_translate("Form", "BantAI"))
        self.lineEdit_5.setText(_translate("Form", "username"))
        self.lineEdit_6.setText(_translate("Form", "email"))
        self.lineEdit_7.setText(_translate("Form", "password"))
        self.lineEdit_8.setText(_translate("Form", "Sign Up"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
