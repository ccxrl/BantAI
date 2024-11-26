from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(347, 442)
        Dialog.setStyleSheet("\n"
"background-color: rgb(151, 227, 227);")
        self.biometric_1 = QtWidgets.QWidget(Dialog)
        self.biometric_1.setGeometry(QtCore.QRect(30, 130, 281, 181))
        self.biometric_1.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.biometric_1.setObjectName("biometric_1")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 50, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(240, 240, 0)")
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(110, 350, 121, 71))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:\\Users\\yeiru\\Documents\\College\\Third Year\\Software Engineering\\bantai_project\\SoftEng_BantAI\\image_2024-11-18_134334864-removebg-preview.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", " You Are Happy"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) 
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())