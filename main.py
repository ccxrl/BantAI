import sys
from PyQt5 import QtWidgets
from login import Ui_LogIn 

class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_LogIn()
        self.ui.setupUi(self)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())