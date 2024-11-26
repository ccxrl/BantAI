from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(341, 714)
        Dialog.setStyleSheet("background-color:  rgb(151, 227, 227);")     
        self.biometric_2 = QtWidgets.QWidget(Dialog)
        self.biometric_2.setGeometry(QtCore.QRect(30, 320, 281, 181))      
        self.biometric_2.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.biometric_2.setObjectName("biometric_2")
        self.Frame_Sad = QtWidgets.QFrame(Dialog)
        self.Frame_Sad.setGeometry(QtCore.QRect(10, 70, 321, 221))
        self.Frame_Sad.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Frame_Sad.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Frame_Sad.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Frame_Sad.setObjectName("Frame_Sad")
        self.label = QtWidgets.QLabel(self.Frame_Sad)
        self.label.setGeometry(QtCore.QRect(60, 170, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(0, 145, 218)")     
        self.label.setObjectName("label")
        self.opencam2 = QtWidgets.QLabel(Dialog)
        self.opencam2.setGeometry(QtCore.QRect(90, 530, 151, 141))
        self.opencam2.setText("")
        self.opencam2.setPixmap(QtGui.QPixmap("C:\\Users\\yeiru\\Documents\\College\\Third Year\\Software Engineering\\bantai_project\\SoftEng_BantAI\\image_2024-11-18_134353450-removebg-preview.png"))
        self.opencam2.setScaledContents(True)
        self.opencam2.setObjectName("opencam2")

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