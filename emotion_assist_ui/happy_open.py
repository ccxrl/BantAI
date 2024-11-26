from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(347, 720)
        Dialog.setStyleSheet("\n"
"background-color: rgb(151, 227, 227);")
        self.biometric_1 = QtWidgets.QWidget(Dialog)
        self.biometric_1.setGeometry(QtCore.QRect(30, 320, 281, 181))      
        self.biometric_1.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.biometric_1.setObjectName("biometric_1")
        self.Frame_Happy = QtWidgets.QFrame(Dialog)
        self.Frame_Happy.setGeometry(QtCore.QRect(10, 70, 321, 221))       
        self.Frame_Happy.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Frame_Happy.setFrameShape(QtWidgets.QFrame.StyledPanel)       
        self.Frame_Happy.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Frame_Happy.setObjectName("Frame_Happy")
        self.label_2 = QtWidgets.QLabel(self.Frame_Happy)
        self.label_2.setGeometry(QtCore.QRect(40, 170, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(240, 240, 0)")   
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(100, 530, 151, 141))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:\\Users\\yeiru\\Documents\\College\\Third Year\\Software Engineering\\bantai_project\\SoftEng_BantAI\\../../../Downloads/466841123_1226061185277283_6014974344434280784_n.png"))   
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.opencam1 = QtWidgets.QLabel(Dialog)
        self.opencam1.setGeometry(QtCore.QRect(80, 540, 151, 141))
        self.opencam1.setText("")
        self.opencam1.setPixmap(QtGui.QPixmap("C:\\Users\\yeiru\\Documents\\College\\Third Year\\Software Engineering\\bantai_project\\SoftEng_BantAI\\image_2024-11-18_134353450-removebg-preview.png"))
        self.opencam1.setScaledContents(True)
        self.opencam1.setObjectName("opencam1")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", " You Are Happy"))       


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())