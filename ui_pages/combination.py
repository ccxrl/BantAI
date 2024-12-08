from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import mediapipe as mp
from PyQt5.QtGui import QImage, QPixmap
from datetime import datetime
from db_manager import db_manager
from advice_system import EmotionAdviceSystem, AdviceDialog
import sys
import serial
import serial.tools.list_ports
import threading
from PyQt5.QtWidgets import (QComboBox, QPushButton, QTextEdit, QHBoxLayout,
                             QVBoxLayout, QLabel, QWidget)
from PyQt5.QtCore import pyqtSignal, QObject


class SerialSignals(QObject):
    """Signals for thread-safe communication with GUI"""
    data_received = pyqtSignal(str)
    ports_updated = pyqtSignal(list)


class Ui_Dashboard(object):
    def __init__(self, username):
        # Existing initialization code remains the same
        self.username = username
        print("Username being passed to dashboard:", username)
        self.AccPage_window = None
        self.is_detecting = True
        self.last_emotion = None
        self.db = db_manager
        self.emotion_advice_system = EmotionAdviceSystem("API_KEY_HERE")
        self.last_advice_time = None
        user_data = self.db.get_user_by_username(username)
        if user_data:
            self.user_id = user_data['user_id']
            print(f"User ID retrieved: {self.user_id}")
        else:
            self.user_id = None
            print("Failed to get user ID")

        # Serial connection variables
        self.serial_thread = None
        self.stop_event = threading.Event()
        self.signals = SerialSignals()
        self.is_autoscroll = True

    def setupUi(self, Dashboard):
        # Existing setup code remains mostly the same, with modifications for serial monitor
        self.Dashboard = Dashboard
        Dashboard.setObjectName("Dashboard")
        Dashboard.resize(1200, 900)  # Increased size to accommodate serial monitor
        Dashboard.setStyleSheet("""
            background-color: #f5f5f5;
            font-family: 'Segoe UI', sans-serif;
        """)

        icon = QtGui.QIcon("../ui_files/logo_only.png")
        Dashboard.setWindowIcon(icon)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(Dashboard)
        self.centralwidget.setObjectName("centralwidget")

        # Main layout to organize emotion detection and serial monitor
        main_layout = QVBoxLayout(self.centralwidget)

        # Top section for emotion detection
        emotion_section = QWidget()
        emotion_layout = QVBoxLayout(emotion_section)

        # Emotion Display Frame
        self.Emotion_Frame = QtWidgets.QLabel()
        self.Emotion_Frame.setMinimumSize(800, 450)
        self.Emotion_Frame.setStyleSheet("""
            background-color: black;
            border-radius: 15px;
        """)
        self.Emotion_Frame.setAlignment(QtCore.Qt.AlignCenter)

        # Add control buttons container
        self.controlsContainer = QtWidgets.QWidget()
        self.controlsContainer.setStyleSheet("""
            background-color: transparent;
        """)

        # Create horizontal layout for buttons
        self.controlsLayout = QtWidgets.QHBoxLayout(self.controlsContainer)
        self.controlsLayout.setContentsMargins(200, 0, 200, 0)
        self.controlsLayout.setSpacing(40)

        # Start button (existing code)
        self.startButton = QtWidgets.QPushButton("Start")
        self.startButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 25px;
                padding: 10px 20px;
                font: bold 13pt 'Segoe UI';
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #777777;
            }
        """)
        self.startButton.clicked.connect(self.start_detection)
        self.startButton.setEnabled(False)

        # Stop button (existing code)
        self.stopButton = QtWidgets.QPushButton("Stop")
        self.stopButton.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 25px;
                padding: 10px 20px;
                font: bold 13pt 'Segoe UI';
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #777777;
            }
        """)
        self.stopButton.clicked.connect(self.stop_detection)

        # Add buttons to layout
        self.controlsLayout.addWidget(self.startButton)
        self.controlsLayout.addSpacing(40)
        self.controlsLayout.addWidget(self.stopButton)

        # Add emotion section widgets to layout
        emotion_layout.addWidget(self.Emotion_Frame)
        emotion_layout.addWidget(self.controlsContainer)

        # Serial Monitor Section
        serial_section = QWidget()
        serial_layout = QVBoxLayout(serial_section)

        # Serial Port Selection Widgets
        serial_controls_layout = QHBoxLayout()

        # Ports Dropdown
        self.ports_combo = QComboBox()
        self.ports_combo.addItem("Select Device to Connect")
        self.ports_combo.setCurrentIndex(0)

        # Baud Rate Dropdown
        self.baud_combo = QComboBox()
        self.baud_combo.addItems([
            "9600", "115200", "57600", "38400",
            "19200", "14400", "4800", "2400"
        ])
        self.baud_combo.setCurrentText("9600")

        # Buttons
        self.refresh_ports_btn = QPushButton("Refresh Ports")
        self.refresh_ports_btn.clicked.connect(self.update_available_ports)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.start_serial_connection)

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_serial)

        self.autoscroll_btn = QPushButton("Auto Scroll: ON")
        self.autoscroll_btn.clicked.connect(self.toggle_autoscroll)

        # Text area for serial data
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setMinimumHeight(200)

        # Clear Button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_text_area)

        # Add serial controls to layout
        serial_controls_layout.addWidget(self.ports_combo)
        serial_controls_layout.addWidget(self.baud_combo)
        serial_controls_layout.addWidget(self.refresh_ports_btn)
        serial_controls_layout.addWidget(self.connect_btn)
        serial_controls_layout.addWidget(self.disconnect_btn)
        serial_controls_layout.addWidget(self.autoscroll_btn)

        serial_layout.addLayout(serial_controls_layout)
        serial_layout.addWidget(self.text_area)
        serial_layout.addWidget(self.clear_btn)

        # Add both sections to main layout
        main_layout.addWidget(emotion_section)
        main_layout.addWidget(serial_section)

        # Rest of the existing setup code...
        # Action Button (Account with username from DB)
        self.pushButton = QtWidgets.QPushButton()
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

        # Connect signals for serial data
        self.signals.data_received.connect(self.update_text_area)

        # Initialize webcam and other existing initializations...
        self.cap = cv2.VideoCapture(0)
        self.face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5)
        self.model = load_model('model_file_30epochs.h5')

        self.labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy',
                            4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

        # Set up a timer for updating the frame
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30 ms

        # Initial port update
        self.update_available_ports()

    # Add serial monitor methods
    def toggle_autoscroll(self):
        """Toggle auto-scroll functionality"""
        self.is_autoscroll = not self.is_autoscroll
        if self.is_autoscroll:
            self.autoscroll_btn.setText("Auto Scroll: ON")
        else:
            self.autoscroll_btn.setText("Auto Scroll: OFF")

    def disconnect_serial(self):
        """Disconnect the serial connection"""
        if self.serial_thread and self.serial_thread.is_alive():
            self.stop_event.set()
            self.serial_thread.join()
            self.update_text_area("Disconnected from serial port")

    def update_available_ports(self):
        """Fetch and display available serial ports"""
        ports = serial.tools.list_ports.comports()
        port_list = []

        for port in ports:
            # Format: COM Port - Device Description
            port_description = f"{port.device} - {port.description}"
            port_list.append(port_description)

        # Clear existing items
        self.ports_combo.clear()
        self.ports_combo.addItem("Select Device to Connect")

        # Add new ports
        if port_list:
            self.ports_combo.addItems(port_list)
        else:
            self.ports_combo.addItem("No ports found")

    def start_serial_connection(self):
        # Stop any existing connection
        if self.serial_thread and self.serial_thread.is_alive():
            self.stop_event.set()
            self.serial_thread.join()

        # Reset stop event
        self.stop_event.clear()

        # Get selected port and baud rate
        selected_port = self.ports_combo.currentText()

        # Check if a valid port is selected
        if selected_port == "Select Device to Connect":
            self.update_text_area("Please select a valid port")
            return

        # Extract just the COM port (before the dash)
        port = selected_port.split(' - ')[0]
        baud = int(self.baud_combo.currentText())

        try:
            # Start new serial thread
            self.serial_thread = threading.Thread(
                target=self.read_serial,
                args=(port, baud)
            )
            self.serial_thread.start()
        except Exception as e:
            self.update_text_area(f"Error: {str(e)}")

    def read_serial(self, port, baud):
        try:
            with serial.Serial(port, baud, timeout=1) as ser:
                self.signals.data_received.emit(f"Connected to {port} at {baud} baud.")

                while not self.stop_event.is_set():
                    if ser.in_waiting > 0:
                        data = ser.readline().decode().strip()
                        self.signals.data_received.emit(data)
        except Exception as e:
            self.signals.data_received.emit(f"Error: {str(e)}")

    def update_text_area(self, text):
        """Update text area with new data"""
        self.text_area.append(text)

        # Auto-scroll only if enabled
        if self.is_autoscroll:
            self.text_area.verticalScrollBar().setValue(
                self.text_area.verticalScrollBar().maximum()
            )

    def clear_text_area(self):
        """Clear the text area"""
        self.text_area.clear()

    # Existing methods from the emotion detection dashboard remain unchanged
    # (set_username_button, start_detection, stop_detection, etc.)

    def closeEvent(self, event):
        """Handle application close"""
        if self.serial_thread and self.serial_thread.is_alive():
            self.stop_event.set()
            self.serial_thread.join()
        event.accept()

    # Rest of the existing methods remain the same...

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dashboard = QtWidgets.QMainWindow()
    ui = Ui_Dashboard('example_username')
    ui.setupUi(Dashboard)
    Dashboard.show()
    sys.exit(app.exec_())