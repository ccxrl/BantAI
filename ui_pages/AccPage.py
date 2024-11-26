from PyQt5 import QtCore, QtGui, QtWidgets
from db_manager import db_manager
import sys

class Ui_AccountInformation(object):
    def __init__(self, username):
        self.username = username
        self.user_id = None
        self.input_fields = {}
        self.labels = {}

    def setupUi(self, AccountInformation):
        
        # Set window icon
        icon = QtGui.QIcon("../ui_files/logo_only.png")
        AccountInformation.setWindowIcon(icon)
        
        # List of input fields and their corresponding keys
        self.input_fields_config = {
            "first_name": "First Name",
            "last_name": "Last Name", 
            "email": "Email Address",
            "age": "Age",
            "weight": "Weight (kg)",
            "height": "Height (cm)",
            "bpm": "Current BPM"
        }

        # Initialize UI components
        self.init_ui_components(AccountInformation)
        
        # Load user data after initializing UI components
        self.load_user_data()

    def init_ui_components(self, AccountInformation):
        """Initialize UI components before loading data"""
        AccountInformation.setObjectName("AccountInformation")
        AccountInformation.resize(800, 800)
        
        
        AccountInformation.setStyleSheet("""
            background-color: rgb(151, 227, 227);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
        """)

        self.centralwidget = QtWidgets.QWidget(AccountInformation)
        self.centralwidget.setObjectName("centralwidget")

        # Main Vertical Layout
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(50, 20, 50, 20)

        # Profile Picture Frame with Centered Layout
        profile_layout = QtWidgets.QHBoxLayout()
        
        # Profile Picture Frame
        self.frame_2 = QtWidgets.QFrame()
        self.frame_2.setFixedSize(200, 200)
        self.frame_2.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
        """)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)

        # Placeholder Image/Icon
        self.profile_image = QtWidgets.QLabel(self.frame_2)
        self.profile_image.setAlignment(QtCore.Qt.AlignCenter)
        self.profile_image.setGeometry(QtCore.QRect(10, 10, 180, 180))
        
        default_icon = QtGui.QIcon.fromTheme("user-identity", QtGui.QIcon(":/icons/user-placeholder.png"))
        pixmap = default_icon.pixmap(180, 180)
        
        if pixmap.isNull():
            pixmap = QtGui.QPixmap(180, 180)
            pixmap.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(pixmap)
            painter.setPen(QtGui.QPen(QtCore.Qt.gray, 2, QtCore.Qt.DashLine))
            painter.drawRect(0, 0, 179, 179)
            painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, "Upload\nPhoto")
            painter.end()
        
        self.profile_image.setPixmap(pixmap)
        self.profile_image.setScaledContents(True)

        # Apply shadow effect to the frame
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(5, 5)
        shadow.setColor(QtCore.Qt.black)
        self.frame_2.setGraphicsEffect(shadow)

        # Center the profile frame
        profile_layout.addStretch()
        profile_layout.addWidget(self.frame_2)
        profile_layout.addStretch()

        main_layout.addLayout(profile_layout)
        main_layout.addSpacing(20)

        # Input Fields Layout
        input_layout = QtWidgets.QVBoxLayout()
        input_layout.setSpacing(10)

        # Create and add labels for user data
        for key, display_label in self.input_fields_config.items():
            label_widget = QtWidgets.QLabel()
            label_widget.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            """)
            self.labels[key] = label_widget
            input_layout.addWidget(label_widget)

        # Create input fields but keep them hidden initially
        for key in self.input_fields_config.keys():
            line_edit = self.create_input(key)
            line_edit.setVisible(False)
            self.input_fields[key] = line_edit
            input_layout.addWidget(line_edit)

        # Center the input layout
        input_container = QtWidgets.QHBoxLayout()
        input_container.addStretch()
        input_container.addLayout(input_layout)
        input_container.addStretch()

        main_layout.addLayout(input_container)
        main_layout.addSpacing(20)

        # Buttons Layout
        buttons_layout = QtWidgets.QHBoxLayout()
        
        # Edit Account Button
        self.editaccountbutton = QtWidgets.QPushButton("Edit Account Info")
        self.editaccountbutton.setStyleSheet("""
            background-color: #2196F3;
            color: white;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        self.editaccountbutton.setFixedSize(160, 45)
        self.editaccountbutton.clicked.connect(self.toggle_edit_mode)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.editaccountbutton)
        buttons_layout.addStretch()

        main_layout.addLayout(buttons_layout)

        AccountInformation.setCentralWidget(self.centralwidget)

        self.retranslateUi(AccountInformation)
        QtCore.QMetaObject.connectSlotsByName(AccountInformation)

    def create_input(self, key):
        """Helper function to create input fields"""
        line_edit = QtWidgets.QLineEdit()
        line_edit.setFixedWidth(300)
        line_edit.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 10px;
            font-size: 14px;
        """)
        line_edit.setPlaceholderText(self.input_fields_config[key])
        return line_edit
 
    def toggle_edit_mode(self):
        """Toggle between displaying labels and input fields, and update the database."""
        if self.input_fields["first_name"].isVisible():  # If inputs are visible, save the data
            # Collect data to update
            user_profile_data = {
                "first_name": self.input_fields["first_name"].text(),
                "last_name": self.input_fields["last_name"].text(),
                "email": self.input_fields["email"].text()
            }
            user_data_table_data = {
                "age": self.input_fields["age"].text(),
                "weight": self.input_fields["weight"].text(),
                "height": self.input_fields["height"].text(),
                "bpm": self.input_fields["bpm"].text()
            }

            # Update `users` table
            db_manager.update_user_profile(
                user_id=self.user_id,
                first_name=user_profile_data["first_name"],
                last_name=user_profile_data["last_name"],
                email=user_profile_data["email"]
            )

            # Update `user_data` table
            db_manager.update_user_data(
                user_id=self.user_id,
                age=user_data_table_data["age"],
                weight=user_data_table_data["weight"],
                height=user_data_table_data["height"],
                bpm=user_data_table_data["bpm"]
            )

            # Update labels and hide inputs
            for key in self.input_fields_config.keys():
                self.input_fields[key].setVisible(False)
                self.labels[key].setVisible(True)
                current_value = self.input_fields[key].text()
                display_label = self.input_fields_config[key]
                self.labels[key].setText(f"{display_label}: {current_value}")

            # Display success message with custom icon
            msg_box = QtWidgets.QMessageBox(self.centralwidget)  # Use self as the parent to ensure it stays on top
            msg_box.setWindowTitle("Success")
            msg_box.setText("Account information updated successfully!")
            msg_box.setIcon(QtWidgets.QMessageBox.Information)

            # Set custom window icon
            icon = QtGui.QIcon("../ui_files/logo_only.png")  # Update the path to your logo file
            msg_box.setWindowIcon(icon)
            
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
            
        else:  # If inputs are hidden, switch to edit mode
            for key in self.input_fields_config.keys():
                self.input_fields[key].setVisible(True)
                self.labels[key].setVisible(False)
                current_value = self.labels[key].text().split(": ")[1] if ": " in self.labels[key].text() else ""
                self.input_fields[key].setText(current_value)



    def retranslateUi(self, AccountInformation):
        _translate = QtCore.QCoreApplication.translate
        AccountInformation.setWindowTitle(_translate("AccountInformation", "BantAI - Account Management"))

    def load_user_data(self):
        """Load user data from the database and populate labels."""
        user_data = db_manager.get_user_by_username(self.username)
        if user_data:
            for key in self.input_fields_config.keys():
                value = user_data.get(key, '')
                value_str = str(value) if value is not None else ''
                display_label = self.input_fields_config[key]
                self.labels[key].setText(f"{display_label}: {value_str}")
            self.user_id = user_data.get('user_id')  # Store user ID for updates
        else:
            print("No user data found for username:", self.username)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AccountInformation = QtWidgets.QMainWindow()
    ui = Ui_AccountInformation(username='example_username')  # Pass a username for testing
    AccountInformation.setWindowIcon(QtGui.QIcon("../ui_files/logo_only.png"))
    ui.setupUi(AccountInformation)
    AccountInformation.show()
    sys.exit(app.exec_())
