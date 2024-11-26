from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(339, 688)
        Dialog.setStyleSheet("\n"
"background-color: rgb(151, 227, 227);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 190, 251, 71))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(170, 85, 255)")    
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(50, 320, 251, 161))
        self.frame.setStyleSheet("background-color:white")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(20, 40, 301, 251))
        self.frame_2.setStyleSheet("background-color:white")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.opencam2 = QtWidgets.QLabel(Dialog)
        self.opencam2.setGeometry(QtCore.QRect(100, 520, 151, 141))        
        self.opencam2.setText("")
        self.opencam2.setPixmap(QtGui.QPixmap("C:\\Users\\yeiru\\Documents\\College\\Third Year\\Software Engineering\\bantai_project\\SoftEng_BantAI\\image_2024-11-18_134353450-removebg-preview.png"))
        self.opencam2.setScaledContents(True)
        self.opencam2.setObjectName("opencam2")
        self.frame_2.raise_()
        self.label.raise_()
        self.frame.raise_()
        self.opencam2.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "You are in fear."))    
        self.label.setText(_translate("Dialog", "You Are In Fear"))        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())