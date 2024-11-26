from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(340, 709)
        Dialog.setStyleSheet("background-color: rgb(151, 227, 227);")      
        self.biometric_3 = QtWidgets.QWidget(Dialog)
        self.biometric_3.setGeometry(QtCore.QRect(30, 320, 271, 181))      
        self.biometric_3.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.biometric_3.setObjectName("biometric_3")
        self.Frame_Angry = QtWidgets.QFrame(Dialog)
        self.Frame_Angry.setGeometry(QtCore.QRect(10, 70, 321, 221))       
        self.Frame_Angry.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Frame_Angry.setFrameShape(QtWidgets.QFrame.StyledPanel)       
        self.Frame_Angry.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Frame_Angry.setObjectName("Frame_Angry")
        self.label_2 = QtWidgets.QLabel(self.Frame_Angry)
        self.label_2.setGeometry(QtCore.QRect(60, 170, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(214, 0, 0)")     
        self.label_2.setObjectName("label_2")
        self.opencam3 = QtWidgets.QLabel(Dialog)
        self.opencam3.setGeometry(QtCore.QRect(90, 530, 151, 141))
        self.opencam3.setText("")
        self.opencam3.setPixmap(QtGui.QPixmap("C:\\Users\\yeiru\\Documents\\College\\Third Year\\Software Engineering\\bantai_project\\SoftEng_BantAI\\image_2024-11-18_134353450-removebg-preview.png"))
        self.opencam3.setScaledContents(True)
        self.opencam3.setObjectName("opencam3")

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