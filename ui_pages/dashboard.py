from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from db_manager import db_manager  # Assuming you have a db_manager class

class Ui_Dashboard(object):
    def __init__(self, username):
        # Initialize with an empty username, to be filled after login
        self.username = username
        print("Username being passed to dashboard:", username)
        self.AccPage_window = None  # Track the Account Page window

    def setupUi(self, Dashboard):
        self.Dashboard = Dashboard  # Store reference to the main dashboard window
        Dashboard.setObjectName("Dashboard")
        Dashboard.resize(1076, 747)
        Dashboard.setStyleSheet("""
            background-color: #f5f5f5;
            font-family: 'Segoe UI', sans-serif;
        """)
        
        icon = QtGui.QIcon("../ui_files/logo_only.png")
        Dashboard.setWindowIcon(icon)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(Dashboard)
        self.centralwidget.setObjectName("centralwidget")

        # User Frame
        self.User_Frame = QtWidgets.QFrame(self.centralwidget)
        self.User_Frame.setGeometry(QtCore.QRect(70, 110, 591, 321))
        self.User_Frame.setStyleSheet("""
            background-color: white;
            border-radius: 12px;
            border: 1px solid #4f9f9c;
        """)
        self.User_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.User_Frame.setFrameShadow(QtWidgets.QFrame.Raised)

        # Biometrics scroll area
        self.Biometrics = QtWidgets.QScrollArea(self.centralwidget)
        self.Biometrics.setGeometry(QtCore.QRect(750, 110, 231, 491))
        self.Biometrics.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 12px;
        """)
        self.Biometrics.setWidgetResizable(True)
        self.Biometrics.setObjectName("Biometrics")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 229, 489))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        # Scrollbar
        self.verticalScrollBar = QtWidgets.QScrollBar(self.scrollAreaWidgetContents)
        self.verticalScrollBar.setGeometry(QtCore.QRect(210, 0, 21, 491))
        self.verticalScrollBar.setStyleSheet("""
            background-color: #4faaaa;
            border-radius: 5px;
        """)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.Biometrics.setWidget(self.scrollAreaWidgetContents)

        # Action Button (Account with username from DB)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 60, 181, 40))
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: #5db8b0;
                font: bold 14pt 'Segoe UI';
                color: white;
                border-radius: 12px;
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #4f9f9c;
            }
        """)

        # Set username on push button after successful login
        self.set_username_button()

        # Connect the button click to navigate to AccPage
        self.pushButton.clicked.connect(self.go_to_acc_page)

        Dashboard.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Dashboard)
        self.statusbar.setObjectName("statusbar")
        Dashboard.setStatusBar(self.statusbar)

        self.retranslateUi(Dashboard)
        QtCore.QMetaObject.connectSlotsByName(Dashboard)

    def retranslateUi(self, Dashboard):
        _translate = QtCore.QCoreApplication.translate
        Dashboard.setWindowTitle(_translate("Dashboard", "BantAI - HomePage"))

    def set_username_button(self):
        # Set the username on the push button
        self.pushButton.setText(self.username)

    def go_to_acc_page(self):
        # Disable the main dashboard window
        self.Dashboard.setEnabled(False)

        # Create and display the Account Page as a modal-like window
        from AccPage import Ui_AccountInformation
        self.AccPage_window = QtWidgets.QMainWindow()
        self.ui_AccPage = Ui_AccountInformation(self.username)
        self.ui_AccPage.setupUi(self.AccPage_window)
        
        # Set the Account Page as modal and always on top
        self.AccPage_window.setWindowModality(QtCore.Qt.ApplicationModal)
        self.AccPage_window.setWindowFlags(self.AccPage_window.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        # Connect the Account Page close event to re-enable the dashboard
        self.AccPage_window.closeEvent = self.on_accpage_closed
        
        self.AccPage_window.show()


    def on_accpage_closed(self, event):
        # Re-enable the main dashboard window when Account Page is closed
        self.Dashboard.setEnabled(True)
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dashboard = QtWidgets.QMainWindow()
    ui = Ui_Dashboard('example_username')
    ui.setupUi(Dashboard)
    Dashboard.show()
    sys.exit(app.exec_())