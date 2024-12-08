import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from db_manager import db_manager  # Import the database manager
from userdata_form import Ui_UserDataForm  # Import the UserDataForm class


class Ui_SignUp(object):
    def setupUi(self, SignUp):
        SignUp.setObjectName("SignUp")
        SignUp.resize(800, 800)
        
        # Set window icon
        icon = QtGui.QIcon("../ui_files/logo_only.png")
        SignUp.setWindowIcon(icon)
        
        SignUp.setStyleSheet("""
            background-color: rgb(151, 227, 227);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
        """)
        
        # Main widget
        self.centralwidget = QtWidgets.QWidget(SignUp)
        SignUp.setCentralWidget(self.centralwidget)

        # Title
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(300, 50, 200, 50))
        self.title.setStyleSheet("font: bold 24px 'Arial'; color: #333;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setText("Sign Up")

        # First Name
        self.label_first_name = QtWidgets.QLabel(self.centralwidget)
        self.label_first_name.setGeometry(QtCore.QRect(300, 120, 200, 20))
        self.label_first_name.setText("First Name:")
        self.lineEdit_first_name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_first_name.setGeometry(QtCore.QRect(300, 150, 200, 40))
        self.lineEdit_first_name.setStyleSheet("background-color: #ffffff; border: 1px solid #ccc; border-radius: 10px;")

        # Last Name
        self.label_last_name = QtWidgets.QLabel(self.centralwidget)
        self.label_last_name.setGeometry(QtCore.QRect(300, 200, 200, 20))
        self.label_last_name.setText("Last Name:")
        self.lineEdit_last_name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_last_name.setGeometry(QtCore.QRect(300, 230, 200, 40))
        self.lineEdit_last_name.setStyleSheet("background-color: #ffffff; border: 1px solid #ccc; border-radius: 10px;")

        # Username
        self.label_username = QtWidgets.QLabel(self.centralwidget)
        self.label_username.setGeometry(QtCore.QRect(300, 280, 200, 20))
        self.label_username.setText("Username:")
        self.lineEdit_username = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_username.setGeometry(QtCore.QRect(300, 310, 200, 40))
        self.lineEdit_username.setStyleSheet("background-color: #ffffff; border: 1px solid #ccc; border-radius: 10px;")

        # Email
        self.label_email = QtWidgets.QLabel(self.centralwidget)
        self.label_email.setGeometry(QtCore.QRect(300, 360, 200, 20))
        self.label_email.setText("Email:")
        self.lineEdit_email = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_email.setGeometry(QtCore.QRect(300, 390, 200, 40))
        self.lineEdit_email.setStyleSheet("background-color: #ffffff; border: 1px solid #ccc; border-radius: 10px;")

        # Password
        self.label_password = QtWidgets.QLabel(self.centralwidget)
        self.label_password.setGeometry(QtCore.QRect(300, 440, 200, 20))
        self.label_password.setText("Password:")
        self.lineEdit_password = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_password.setGeometry(QtCore.QRect(300, 470, 200, 40))
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setStyleSheet("background-color: #ffffff; border: 1px solid #ccc; border-radius: 10px;")

        # Confirm Password
        self.label_confirm_password = QtWidgets.QLabel(self.centralwidget)
        self.label_confirm_password.setGeometry(QtCore.QRect(300, 520, 200, 20))
        self.label_confirm_password.setText("Confirm Password:")
        self.lineEdit_confirm_password = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_confirm_password.setGeometry(QtCore.QRect(300, 550, 200, 40))
        self.lineEdit_confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_confirm_password.setStyleSheet("background-color: #ffffff; border: 1px solid #ccc; border-radius: 10px;")

        # Signup Button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 620, 200, 40))
        self.pushButton.setText("Sign Up")
        self.pushButton.setStyleSheet("background-color: #4CAF50; color: white; border: none; border-radius: 5px;")

        # Connect signup button to handle_signup method
        self.pushButton.clicked.connect(self.handle_signup)

        # Login Button
        self.loginButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginButton.setGeometry(QtCore.QRect(300, 670, 200, 40))
        self.loginButton.setText("Go to Login")
        self.loginButton.setStyleSheet("background-color: #2196F3; color: white; border: none; border-radius: 5px;")
        self.loginButton.clicked.connect(self.open_login_page)

        # Retranslate UI
        self.retranslateUi(SignUp)

    def handle_signup(self):
        """Handles the signup action."""
        first_name = self.lineEdit_first_name.text()
        last_name = self.lineEdit_last_name.text()
        username = self.lineEdit_username.text()
        email = self.lineEdit_email.text()
        password = self.lineEdit_password.text()
        confirm_password = self.lineEdit_confirm_password.text()

        # Check if passwords match
        if password != confirm_password:
            self.show_message("Error", "Passwords do not match!")
            return

        # Basic validation for empty fields
        if not first_name or not last_name or not username or not email or not password:
            self.show_message("Error", "All fields must be filled!")
            return

        # Email format validation
        if not self.is_valid_email(email):
            self.show_message("Error", "Invalid email format!")
            return

        # Check if username or email already exists
        if db_manager.check_if_user_exists(username, email):
            self.show_message("Error", "Username or email already exists!")
            return

        # Save user data to the database
        user_id = db_manager.register_user(first_name, last_name, username, email, password)
        if user_id:
            self.show_message("Success", "Account created successfully!")
            print(f"User registered with ID {user_id}")
            self.open_userdata_form(user_id)
        else:
            self.show_message("Error", "User registration failed.")
            print("User registration failed.")


    def open_userdata_form(self, user_id):
        """Opens the UserDataForm after successful signup."""
        # Create the UserDataForm and pass the user_id
        self.userdata_window = QtWidgets.QMainWindow()
        self.ui_userdata = Ui_UserDataForm(user_id)
        self.ui_userdata.setupUi(self.userdata_window)
        self.userdata_window.show()

        # Optionally close the current window
        self.centralwidget.parent().close()


    def show_message(self, title, message):
        """Displays a message box."""
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def is_valid_email(self, email):
        """Checks if the email format is valid."""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)

    def open_login_page(self):
        """Opens the login page (you can implement the logic)."""
        from main import Ui_LogIn
        self.logIn_window = QtWidgets.QMainWindow()
        self.ui_login = Ui_LogIn()
        self.ui_login.setupUi(self.logIn_window)
        self.logIn_window.show()
        
        self.centralwidget.parent().close()
        print("Opening login page...")

    def retranslateUi(self, SignUp):
        _translate = QtCore.QCoreApplication.translate
        SignUp.setWindowTitle(_translate("SignUp", "BantAI - Sign Up"))

# Main execution
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    SignUp = QtWidgets.QMainWindow()
    ui = Ui_SignUp()
    ui.setupUi(SignUp)
    SignUp.show()
    sys.exit(app.exec_())
