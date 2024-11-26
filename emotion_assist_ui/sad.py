from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(341, 441)
        Dialog.setStyleSheet("background-color:  rgb(151, 227, 227);")     
        self.biometric_2 = QtWidgets.QWidget(Dialog)
        self.biometric_2.setGeometry(QtCore.QRect(30, 140, 281, 181))      
        self.biometric_2.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.biometric_2.setObjectName("biometric_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 50, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(0, 145, 218)")     
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(110, 350, 121, 71))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("C:\\Users\\yeiru\\Documents\\College\\Third Year\\Software Engineering\\bantai_project\\SoftEng_BantAI\\image_2024-11-18_134334864-removebg-preview.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "  You Are Sad"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())