import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from db_manager import db_manager  # Import the database manager
from sign_up_final import Ui_SignUp  # Assuming the sign-up page is in sign_up_final.py

class Ui_LogIn(object):
    def setupUi(self, LogIn):
        LogIn.setObjectName("LogIn")
        LogIn.resize(800, 800)

        # Set window icon
        icon = QtGui.QIcon("../ui_files/logo_only.png")
        LogIn.setWindowIcon(icon)

        LogIn.setStyleSheet("""
            background-color: rgb(151, 227, 227);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
        """)

        # Main widget
        self.centralwidget = QtWidgets.QWidget(LogIn)
        LogIn.setCentralWidget(self.centralwidget)

        # Title
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(300, 50, 200, 50))
        self.title.setStyleSheet("font: bold 24px 'Arial'; color: #333;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setText("Log In")

        # Email/Username
        self.label_email_username = QtWidgets.QLabel(self.centralwidget)
        self.label_email_username.setGeometry(QtCore.QRect(300, 180, 200, 20))
        self.label_email_username.setText("Email or Username:")
        self.lineEdit_email_username = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_email_username.setGeometry(QtCore.QRect(300, 210, 200, 40))
        self.lineEdit_email_username.setStyleSheet("background-color: #ffffff; border: 1px solid #ccc; border-radius: 10px;")
        self.lineEdit_email_username.setPlaceholderText("Enter email or username")

        # Password
        self.label_password = QtWidgets.QLabel(self.centralwidget)
        self.label_password.setGeometry(QtCore.QRect(300, 270, 200, 20))
        self.label_password.setText("Password:")
        self.lineEdit_password = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_password.setGeometry(QtCore.QRect(300, 300, 200, 40))
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setStyleSheet("background-color: #ffffff; border: 1px solid #ccc; border-radius: 10px;")
        self.lineEdit_password.setPlaceholderText("Enter password")
        
        # Log In Button
        self.loginButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginButton.setGeometry(QtCore.QRect(300, 370, 200, 40))
        self.loginButton.setText("Log In")
        self.loginButton.setStyleSheet("background-color: #4CAF50; color: white; border: none; border-radius: 5px;")
        self.loginButton.clicked.connect(self.handle_login)

        # Sign Up Button
        self.signupButton = QtWidgets.QPushButton(self.centralwidget)
        self.signupButton.setGeometry(QtCore.QRect(300, 420, 200, 40))
        self.signupButton.setText("Go to Sign Up")
        self.signupButton.setStyleSheet("background-color: #2196F3; color: white; border: none; border-radius: 5px;")
        self.signupButton.clicked.connect(self.open_signup_page)

        # Add Enter key event handling for both input fields
        self.lineEdit_email_username.returnPressed.connect(self.handle_login)
        self.lineEdit_password.returnPressed.connect(self.handle_login)

        # Retranslate UI
        self.retranslateUi(LogIn)

    def handle_login(self):
        db = db_manager  # Singleton instance of DatabaseManager

        username_or_email = self.lineEdit_email_username.text()
        password = self.lineEdit_password.text()

        # Check if the input is an email or username
        user_data = db.login_user(username_or_email, password)
        
        if user_data:
            print("Login successful!")
            username = user_data['username']  # Get the username from the returned user data
            self.open_dashboard_page(username)  # Pass the username to the dashboard page
            print("Login successful!")
        
            # Debug prints
            print("Login input:", username_or_email)
            print("Authenticated user data:", user_data)
            
            username = user_data['username']  # Get the username from the returned user data
            print("Username being passed to dashboard:", username)
        else:
            print("Invalid credentials!")
            self.show_message("Error", "Invalid email/username or password.")

    def open_signup_page(self):
        """Opens the signup page."""
        self.signup_window = QtWidgets.QMainWindow()
        self.ui_signup = Ui_SignUp()  # Import and use the sign-up class
        self.ui_signup.setupUi(self.signup_window)
        self.signup_window.show()

        # Optionally close the login window
        self.centralwidget.parent().close()

    def open_dashboard_page(self, username):
        """Opens the dashboard page."""
        from dashboard import Ui_Dashboard
        self.dashboard_window = QtWidgets.QMainWindow()
        self.ui_dashboard = Ui_Dashboard(username)  # Pass user data to dashboard
        self.ui_dashboard.setupUi(self.dashboard_window)
        self.dashboard_window.show()

        # Optionally close the login window
        self.centralwidget.parent().close()

    def show_message(self, title, message):
        """Displays a message box with custom design."""
        msg_box = QtWidgets.QMessageBox(self.centralwidget)  # Use self as the parent to ensure it stays on top
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QtWidgets.QMessageBox.Information)  # Set the default information icon

        # Set custom window icon
        icon = QtGui.QIcon("../ui_files/logo_only.png")  # Update the path to your logo file
        msg_box.setWindowIcon(icon)

        # Apply custom styling to the message box
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: rgb(255, 255, 255);  /* White background */
                border: 1px solid #ccc;                 /* Border color */
                border-radius: 10px;                    /* Rounded corners */
            }
            QMessageBox QLabel {
                font-size: 14px;
                font-weight: bold;
                background-color: rgb(255, 255, 255);
                color: rgb(0, 0, 0);  /* Black text color */
            }
            QMessageBox QPushButton {
                background-color: #2196F3;  /* Button color */
                color: white;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
            QMessageBox QPushButton:hover {
                background-color: #1976D2;  /* Darker button color on hover */
            }
        """)

        # Show the message box
        msg_box.exec_()

    def retranslateUi(self, LogIn):
        _translate = QtCore.QCoreApplication.translate
        LogIn.setWindowTitle(_translate("LogIn", "BantAI - Log In"))

# Main execution
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    LogIn = QtWidgets.QMainWindow()  # Changed to QMainWindow to match the design
    ui = Ui_LogIn()
    ui.setupUi(LogIn)
    LogIn.show()
    sys.exit(app.exec_())