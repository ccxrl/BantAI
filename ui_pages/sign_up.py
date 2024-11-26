import sys
import mysql.connector
from mysql.connector import Error
from PyQt5 import QtCore, QtGui, QtWidgets
import bcrypt

class DatabaseManager:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bantai"
            )
            if self.connection.is_connected():
                print("Successfully connected to database")
                self.cursor = self.connection.cursor()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def add_user(self, first_name, last_name, username, email, password):
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            query = """
            INSERT INTO users (first_name, last_name, username, email, password)
            VALUES (%s, %s, %s, %s, %s)
            """
            data = (first_name, last_name, username, email, hashed_password)
            self.cursor.execute(query, data)
            self.connection.commit()
            print("User registered successfully")
        except Error as e:
            print(f"Error adding user: {e}")

    def check_user_exists(self, username, email):
        try:
            query = """
            SELECT COUNT(*) FROM users WHERE username = %s OR email = %s
            """
            self.cursor.execute(query, (username, email))
            result = self.cursor.fetchone()
            return result[0] > 0  # Returns True if user exists, False otherwise
        except Error as e:
            print(f"Error checking user existence: {e}")
            return False

    def close(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed")


class Ui_SignUp(object):
    def setupUi(self, SignUp):
        SignUp.setObjectName("SignUp")
        SignUp.resize(800, 800)
        SignUp.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QLabel {
                font: 14px 'Arial';
            }
            QLineEdit {
                background-color: white;
                border: 2px solid #ccc;
                border-radius: 10px;
                padding: 8px;
                font: 14px 'Arial';
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                font: bold 14px 'Arial';
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            #loginButton {
                background-color: transparent;
                border: 2px solid #007BFF;  /* Blue border */
                color: #007BFF;  /* Blue text */
                font: bold 14px 'Arial';
                border-radius: 10px;
                padding: 10px;
            }
            #loginButton:hover {
                background-color: #007BFF;
                color: white;
            }
        """)

        # Title
        self.title = QtWidgets.QLabel(SignUp)
        self.title.setGeometry(QtCore.QRect(300, 50, 200, 50))
        self.title.setStyleSheet("font: bold 24px 'Arial'; color: #333;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setText("Sign Up")

        # First Name
        self.label_first_name = QtWidgets.QLabel(SignUp)
        self.label_first_name.setGeometry(QtCore.QRect(300, 120, 200, 20))
        self.label_first_name.setText("First Name:")
        self.lineEdit_first_name = QtWidgets.QLineEdit(SignUp)
        self.lineEdit_first_name.setGeometry(QtCore.QRect(300, 150, 200, 40))

        # Last Name
        self.label_last_name = QtWidgets.QLabel(SignUp)
        self.label_last_name.setGeometry(QtCore.QRect(300, 200, 200, 20))
        self.label_last_name.setText("Last Name:")
        self.lineEdit_last_name = QtWidgets.QLineEdit(SignUp)
        self.lineEdit_last_name.setGeometry(QtCore.QRect(300, 230, 200, 40))

        # Username
        self.label_username = QtWidgets.QLabel(SignUp)
        self.label_username.setGeometry(QtCore.QRect(300, 280, 200, 20))
        self.label_username.setText("Username:")
        self.lineEdit_username = QtWidgets.QLineEdit(SignUp)
        self.lineEdit_username.setGeometry(QtCore.QRect(300, 310, 200, 40))

        # Email
        self.label_email = QtWidgets.QLabel(SignUp)
        self.label_email.setGeometry(QtCore.QRect(300, 360, 200, 20))
        self.label_email.setText("Email:")
        self.lineEdit_email = QtWidgets.QLineEdit(SignUp)
        self.lineEdit_email.setGeometry(QtCore.QRect(300, 390, 200, 40))

        # Password
        self.label_password = QtWidgets.QLabel(SignUp)
        self.label_password.setGeometry(QtCore.QRect(300, 440, 200, 20))
        self.label_password.setText("Password:")
        self.lineEdit_password = QtWidgets.QLineEdit(SignUp)
        self.lineEdit_password.setGeometry(QtCore.QRect(300, 470, 200, 40))
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)

        # Confirm Password
        self.label_confirm_password = QtWidgets.QLabel(SignUp)
        self.label_confirm_password.setGeometry(QtCore.QRect(300, 520, 200, 20))
        self.label_confirm_password.setText("Confirm Password:")
        self.lineEdit_confirm_password = QtWidgets.QLineEdit(SignUp)
        self.lineEdit_confirm_password.setGeometry(QtCore.QRect(300, 550, 200, 40))
        self.lineEdit_confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)

        # Submit Button
        self.pushButton = QtWidgets.QPushButton(SignUp)
        self.pushButton.setGeometry(QtCore.QRect(300, 620, 200, 40))
        self.pushButton.setText("Sign Up")
        self.pushButton.clicked.connect(self.handle_signup)

        # Go to Login Button
        self.button_go_to_login = QtWidgets.QPushButton(SignUp)
        self.button_go_to_login.setObjectName("loginButton")
        self.button_go_to_login.setGeometry(QtCore.QRect(300, 670, 200, 40))
        self.button_go_to_login.setText("Go to Login")
        self.button_go_to_login.clicked.connect(self.open_login_page)

        self.retranslateUi(SignUp)
        QtCore.QMetaObject.connectSlotsByName(SignUp)

    def retranslateUi(self, SignUp):
        _translate = QtCore.QCoreApplication.translate
        SignUp.setWindowTitle(_translate("SignUp", "Sign Up Form"))

    def handle_signup(self):
        first_name = self.lineEdit_first_name.text()
        last_name = self.lineEdit_last_name.text()
        username = self.lineEdit_username.text()
        email = self.lineEdit_email.text()
        password = self.lineEdit_password.text()
        confirm_password = self.lineEdit_confirm_password.text()

        # Check if all fields are filled
        if not first_name or not last_name or not username or not email or not password or not confirm_password:
            QtWidgets.QMessageBox.warning(None, "Input Error", "All fields are required!")
            return

        # Check if passwords match
        if password != confirm_password:
            QtWidgets.QMessageBox.warning(None, "Input Error", "Passwords do not match!")
            return

        db = DatabaseManager()

        # Check if the email or username already exists
        if db.check_user_exists(username, email):
            QtWidgets.QMessageBox.warning(None, "Input Error", "Username or Email already exists!")
            return

        try:
            db.add_user(first_name, last_name, username, email, password)
            QtWidgets.QMessageBox.information(None, "Success", "User registered successfully!")
        finally:
            db.close()

    def open_login_page(self):
        from login import Ui_LogIn
        self.window = QtWidgets.QWidget()
        self.ui = Ui_LogIn()
        self.ui.setupUi(self.window)
        self.window.show()
        QtWidgets.QApplication.instance().activeWindow().close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    SignUp = QtWidgets.QWidget()
    ui = Ui_SignUp()
    ui.setupUi(SignUp)
    SignUp.show()
    sys.exit(app.exec_())
