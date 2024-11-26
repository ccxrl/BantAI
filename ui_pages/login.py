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
                self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def check_user(self, email, password):
        try:
            query = """
            SELECT * FROM users 
            WHERE email = %s
            """
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()
            
            if result:
                stored_password = result['password'].encode('utf-8')
                return bcrypt.checkpw(password.encode('utf-8'), stored_password)
            return False
        except Error as e:
            print(f"Error checking user: {e}")
            return False

    def close(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed")


class Ui_LogIn(object):
    def setupUi(self, LogIn):
        self.window = LogIn
        LogIn.setObjectName("LogIn")
        LogIn.resize(800, 600)
        LogIn.setStyleSheet("""
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
            QLabel#signupLink {
                font: italic 14px 'Arial';
                color: #007BFF;
            }
            QLabel#signupLink:hover {
                text-decoration: underline;
            }
        """)

        # Title
        self.title = QtWidgets.QLabel(LogIn)
        self.title.setGeometry(QtCore.QRect(300, 100, 200, 50))
        self.title.setStyleSheet("font: bold 24px 'Arial'; color: #333;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setText("Log In")

        # Email
        self.label_email = QtWidgets.QLabel(LogIn)
        self.label_email.setGeometry(QtCore.QRect(300, 200, 200, 20))
        self.label_email.setText("Email:")
        self.lineEdit_email = QtWidgets.QLineEdit(LogIn)
        self.lineEdit_email.setGeometry(QtCore.QRect(300, 230, 200, 40))

        # Password
        self.label_password = QtWidgets.QLabel(LogIn)
        self.label_password.setGeometry(QtCore.QRect(300, 280, 200, 20))
        self.label_password.setText("Password:")
        self.lineEdit_password = QtWidgets.QLineEdit(LogIn)
        self.lineEdit_password.setGeometry(QtCore.QRect(300, 310, 200, 40))
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)

        # Login Button
        self.pushButton_login = QtWidgets.QPushButton(LogIn)
        self.pushButton_login.setGeometry(QtCore.QRect(300, 380, 200, 40))
        self.pushButton_login.setText("Log In")
        self.pushButton_login.clicked.connect(self.handle_login)

        # Don't have an account yet? Text Link
        self.signup_link = QtWidgets.QLabel(LogIn)
        self.signup_link.setObjectName("signupLink")
        self.signup_link.setGeometry(QtCore.QRect(300, 440, 300, 20))
        self.signup_link.setText("No account yet? Sign up here")
        self.signup_link.mousePressEvent = self.open_sign_up_page

        self.signup_link.setCursor(QtCore.Qt.PointingHandCursor)

        self.retranslateUi(LogIn)
        QtCore.QMetaObject.connectSlotsByName(LogIn)

    def retranslateUi(self, LogIn):
        _translate = QtCore.QCoreApplication.translate
        LogIn.setWindowTitle(_translate("LogIn", "Login Form"))

    def handle_login(self):
        try:
            email = self.lineEdit_email.text()
            password = self.lineEdit_password.text()

            if not email or not password:
                QtWidgets.QMessageBox.warning(None, "Input Error", "Email and password are required!")
                return

            db = DatabaseManager()
            try:
                if db.check_user(email, password):
                    QtWidgets.QMessageBox.information(None, "Login Successful", "You have successfully logged in!")
                else:
                    QtWidgets.QMessageBox.warning(None, "Login Failed", "Invalid email or password.")
            except Exception as db_error:
                print(f"Database error: {db_error}")
                QtWidgets.QMessageBox.critical(None, "Database Error", str(db_error))
            finally:
                db.close()
        except Exception as e:
            print(f"Unexpected error in handle_login: {e}")
            QtWidgets.QMessageBox.critical(None, "Unexpected Error", str(e))

    def open_sign_up_page(self, event):
        from sign_up import Ui_SignUp

        sign_up_window = QtWidgets.QDialog()
        sign_up_ui = Ui_SignUp()
        sign_up_ui.setupUi(sign_up_window)

        if hasattr(self, 'window') and self.window is not None:
            self.window.close()

        sign_up_window.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LogIn = QtWidgets.QWidget()
    ui = Ui_LogIn()
    ui.setupUi(LogIn)
    LogIn.show()
    sys.exit(app.exec_())
