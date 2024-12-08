import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from db_manager import db_manager  # Import the database manager


class Ui_UserDataForm(object):
    def __init__(self, user_id):
        self.user_id = user_id  # Store the user ID passed from the signup form

    def setupUi(self, UserDataForm):
        UserDataForm.setObjectName("User DataForm")
        UserDataForm.resize(800, 800)

        # Set window icon
        icon = QtGui.QIcon("../ui_files/logo_only.png")
        UserDataForm.setWindowIcon(icon)

        UserDataForm.setStyleSheet("""
            background-color: rgb(151, 227, 227);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
        """)

        # Main widget
        self.centralwidget = QtWidgets.QWidget(UserDataForm)
        UserDataForm.setCentralWidget(self.centralwidget)

        # Title
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(300, 50, 200, 50))
        self.title.setStyleSheet("font: bold 24px 'Arial'; color: #333;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setText("User Data Form")

        # Age
        self.label_age = QtWidgets.QLabel(self.centralwidget)
        self.label_age.setGeometry(QtCore.QRect(300, 120, 200, 20))
        self.label_age.setText("Age:")
        self.lineEdit_age = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_age.setGeometry(QtCore.QRect(300, 150, 200, 40))
        self.lineEdit_age.setStyleSheet("background-color: #ffffff; border: 1px solid #ccc;")

        # Height
        self.label_height = QtWidgets.QLabel(self.centralwidget)
        self.label_height.setGeometry(QtCore.QRect(300, 200, 200, 20))
        self.label_height.setText("Height (m):")
        self.lineEdit_height = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_height.setGeometry(QtCore.QRect(300, 230, 200, 40))
        self.lineEdit_height.setStyleSheet("background-color: #ffffff; border: 1px solid #ccc;")

        # Weight
        self.label_weight = QtWidgets.QLabel(self.centralwidget)
        self.label_weight.setGeometry(QtCore.QRect(300, 280, 200, 20))
        self.label_weight.setText("Weight (kg):")
        self.lineEdit_weight = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_weight.setGeometry(QtCore.QRect(300, 310, 200, 40))
        self.lineEdit_weight.setStyleSheet("background-color: #ffffff; border: 1px solid #ccc;")

        # BPM
        self.label_bpm = QtWidgets.QLabel(self.centralwidget)
        self.label_bpm.setGeometry(QtCore.QRect(300, 360, 200, 20))
        self.label_bpm.setText("BPM (Beats Per Minute):")
        self.lineEdit_bpm = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_bpm.setGeometry(QtCore.QRect(300, 390, 200, 40))
        self.lineEdit_bpm.setStyleSheet("background-color: #ffffff; border: 1px solid #ccc;")

        # BMI Display Panel
        self.label_bmi = QtWidgets.QLabel(self.centralwidget)
        self.label_bmi.setGeometry(QtCore.QRect(300, 450, 200, 20))
        self.label_bmi.setText("BMI & Category:")
        self.textEdit_bmi = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_bmi.setGeometry(QtCore.QRect(300, 480, 200, 80))
        self.textEdit_bmi.setStyleSheet("background-color: #e6e6e6; border: 1px solid #ccc;")
        self.textEdit_bmi.setReadOnly(True)

        # Submit Button
        self.pushButton_submit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_submit.setGeometry(QtCore.QRect(300, 580, 200, 40))
        self.pushButton_submit.setText("Submit")
        self.pushButton_submit.setStyleSheet("background-color: #4CAF50; color: white; border: none; border-radius: 5px;")
        self.pushButton_submit.clicked.connect(self.submit_data)

        # Retranslate UI
        self.retranslateUi(UserDataForm)

    def calculate_bmi(self):
        try:
            height = float(self.lineEdit_height.text())
            weight = float(self.lineEdit_weight.text())
            bmi = weight / (height ** 2)

            # BMI Category
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 24.9:
                category = "Normal weight"
            elif 25 <= bmi < 29.9:
                category = "Overweight"
            else:
                category = "Obesity"

            return f"{bmi:.2f}", category
        except ValueError:
            return None, "Invalid Input"

    def submit_data(self):
        try:
            age = int(self.lineEdit_age.text())
            height = float(self.lineEdit_height.text())
            weight = float(self.lineEdit_weight.text())
            bpm = int(self.lineEdit_bpm.text())
            bmi, category = self.calculate_bmi()

            if bmi and category:
                self.textEdit_bmi.setText(f"BMI: {bmi}\nCategory: {category}")

                # Insert data into the database, associating it with the user ID
                query = """
                INSERT INTO user_data (user_id, age, height, weight, bpm, bmi, bmi_category)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                db_manager.cursor.execute(query, (self.user_id, age, height, weight, bpm, bmi, category))
                db_manager.connection.commit()
                QtWidgets.QMessageBox.information(None, "Success", "Data submitted successfully!")
                self.open_login_page()
            else:
                self.textEdit_bmi.setText("Please enter valid height and weight.")
        except ValueError:
            QtWidgets.QMessageBox.warning(None, "Error", "Please fill in all fields correctly.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"An error occurred: {e}")

    def open_login_page(self):
        """Opens the login page (you can implement the logic)."""
        from main import Ui_LogIn
        self.logIn_window = QtWidgets.QMainWindow()
        self.ui_login = Ui_LogIn()
        self.ui_login.setupUi(self.logIn_window)
        self.logIn_window.show()
        
        self.centralwidget.parent().close()
        print("Opening login page...")
        
    def retranslateUi(self, UserDataForm):
        _translate = QtCore.QCoreApplication.translate
        UserDataForm.setWindowTitle(_translate("UserDataForm", "BantAI - User Data Form"))


# Main execution
if __name__ == "__main__":
    # Simulate user ID passing from signup form (for example)
    user_id = 1  # Replace with the actual user ID from your signup process
    app = QtWidgets.QApplication(sys.argv)
    UserDataForm = QtWidgets.QMainWindow()
    ui = Ui_UserDataForm(user_id)  # Pass the user ID
    ui.setupUi(UserDataForm)
    UserDataForm.show()
    sys.exit(app.exec_())
