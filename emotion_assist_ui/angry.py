from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(331, 446)
        Dialog.setStyleSheet("background-color: rgb(151, 227, 227);")      
        self.biometric_3 = QtWidgets.QWidget(Dialog)
        self.biometric_3.setGeometry(QtCore.QRect(30, 140, 271, 181))      
        self.biometric_3.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.biometric_3.setObjectName("biometric_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 60, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(214, 0, 0)")     
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(110, 350, 121, 71))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("C:\\Users\\yeiru\\Documents\\College\\Third Year\\Software Engineering\\bantai_project\\SoftEng_BantAI\\image_2024-11-18_134334864-removebg-preview.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "  You Are Angry"))      


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())