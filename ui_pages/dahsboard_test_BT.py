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
        self.emotion_advice_system = EmotionAdviceSystem("AIzaSyClu8VwAUJqi15LUEd03MoqbY-X0IrgS0o")
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
        Dashboard.resize(400, 850)  # Increased size to accommodate serial monitor
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


        # Header section for account and username display
        self.header_layout = QtWidgets.QHBoxLayout()


        # Top section for emotion detection
        emotion_section = QWidget()
        emotion_layout = QVBoxLayout(emotion_section)

        # Emotion Display Frame
        self.Emotion_Frame = QtWidgets.QLabel()
        self.Emotion_Frame.setMinimumSize(800, 450)
        self.Emotion_Frame.setStyleSheet("""
            background-color: black;
            border-radius: 15px;
            margin-top: 20px;  # Adds space between header and frame
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

        # Start button
        self.startButton = QtWidgets.QPushButton("Start")
        self.startButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 25px;
                padding: 10px 20px;
                font: bold 13pt 'Segoe UI';
                min-width: 120px;
                min-height: 40px;  /* Add this for better proportion */
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

        # Stop button
        self.stopButton = QtWidgets.QPushButton("Stop")
        self.stopButton.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 25px;
                padding: 10px 20px;
                font: bold 13pt 'Segoe UI';
                min-width: 120px;
                min-height: 40px;  /* Add this for better proportion */
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
        serial_controls_layout = QVBoxLayout()

        # Ports Dropdown
        self.ports_combo = QComboBox()
        self.ports_combo.addItem("Select Device to Connect")
        self.ports_combo.setCurrentIndex(0)
        self.ports_combo.setStyleSheet("""
            QComboBox {
                background-color: #ECEFF1;
                border: 1px solid #CFD8DC;
                border-radius: 8px;
                padding: 4px 8px;
                font: 12pt 'Segoe UI';
                color: #37474F;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
            }
            QComboBox::down-arrow {
                image: url('path/to/arrow-icon.png'); /* Optional: Add custom arrow icon */
            }
            QComboBox:hover {
                border-color: #90A4AE;
            }
            QComboBox:focus {
                border-color: #2196F3;
            }
        """)

        # Baud Rate Dropdown
        self.baud_combo = QComboBox()
        self.baud_combo.addItems([
            "9600", "115200", "57600", "38400",
            "19200", "14400", "4800", "2400"
        ])
        self.baud_combo.setStyleSheet("""
            QComboBox {
                background-color: #ECEFF1;
                border: 1px solid #CFD8DC;
                border-radius: 8px;
                padding: 4px 8px;
                font: 12pt 'Segoe UI';
                color: #37474F;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
            }
            QComboBox::down-arrow {
                image: url('path/to/arrow-icon.png'); /* Optional: Add custom arrow icon */
            }
            QComboBox:hover {
                border-color: #90A4AE;
            }
            QComboBox:focus {
                border-color: #2196F3;
            }
        """)

        self.baud_combo.setCurrentText("9600")

        # Buttons
        self.refresh_ports_btn = QPushButton("Refresh Ports")
        self.refresh_ports_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font: bold 12pt 'Segoe UI';
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #B0BEC5;
                color: #CFD8DC;
            }
        """)
        self.refresh_ports_btn.clicked.connect(self.update_available_ports)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font: bold 12pt 'Segoe UI';
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            QPushButton:disabled {
                background-color: #B0BEC5;
                color: #CFD8DC;
            }
        """)
        self.connect_btn.clicked.connect(self.start_serial_connection)

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                font: bold 12pt 'Segoe UI';
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
            QPushButton:disabled {
                background-color: #B0BEC5;
                color: #CFD8DC;
            }
        """)
        self.disconnect_btn.clicked.connect(self.disconnect_serial)

        self.autoscroll_btn = QPushButton("Auto Scroll: ON")
        self.autoscroll_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: black;
                font: bold 12pt 'Segoe UI';
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #FFB300;
            }
            QPushButton:disabled {
                background-color: #FFE082;
                color: #B0BEC5;
            }
        """)
        self.autoscroll_btn.clicked.connect(self.toggle_autoscroll)

        # Text area for serial data
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: #ECEFF1;
                border: 1px solid #CFD8DC;
                border-radius: 8px;
                font: 11pt 'Segoe UI';
                color: #37474F;
                padding: 8px;
            }
        """)
        self.text_area.setMinimumHeight(200)

        # Clear Button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #9E9E9E;
                color: white;
                font: bold 12pt 'Segoe UI';
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #757575;
            }
            QPushButton:disabled {
                background-color: #B0BEC5;
                color: #CFD8DC;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_text_area)

        # Add serial controls to layout
        # Top row for dropdowns
        top_row = QHBoxLayout()
        top_row.addWidget(self.ports_combo)
        top_row.addWidget(self.baud_combo)
        serial_controls_layout.addLayout(top_row)

        # Bottom row for buttons
        bottom_row = QHBoxLayout()
        bottom_row.addWidget(self.refresh_ports_btn)
        bottom_row.addWidget(self.connect_btn)
        bottom_row.addWidget(self.disconnect_btn)
        bottom_row.addWidget(self.autoscroll_btn)
        serial_controls_layout.addLayout(bottom_row)

        serial_layout.addLayout(serial_controls_layout)
        serial_layout.addWidget(self.text_area)
        serial_layout.addWidget(self.clear_btn)

        header_section = QWidget()
        header_layout = QHBoxLayout(header_section)

        header_layout.addWidget(self.pushButton, alignment=QtCore.Qt.AlignLeft)
        header_layout.addStretch()  # Ensures button stays on the left

        # Optional: Add spacing or other widgets in the header layout
        header_layout.addStretch()

        # Add both sections to main layout
        # Add header section to the main layout
        main_layout.addWidget(header_section)
        main_layout.addWidget(emotion_section)
        main_layout.addWidget(serial_section)
        main_layout.addSpacing(5)  # Adjust value for desired spacing

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

    def retranslateUi(self, Dashboard):
        _translate = QtCore.QCoreApplication.translate
        Dashboard.setWindowTitle(_translate("Dashboard", "BantAI - HomePage"))

    def set_username_button(self):
        # Set the username on the push button
        self.pushButton.setText(self.username)

    def start_detection(self):
        """Start emotion detection"""
        self.is_detecting = True
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)

    def stop_detection(self):
        """Stop emotion detection"""
        self.is_detecting = False
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)

        # Display a paused message on the frame
        height = self.Emotion_Frame.height()
        width = self.Emotion_Frame.width()
        blank_image = np.zeros((height, width, 3), np.uint8)
        blank_image.fill(0)  # Black background

        # Add "Detection Paused" text
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = "Detection Paused"
        font_scale = 1
        thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]

        # Calculate text position to center it
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2

        cv2.putText(blank_image, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)

        # Convert to QImage and display
        bytes_per_line = 3 * width
        qImg = QImage(blank_image.data, width, height, bytes_per_line, QImage.Format_BGR888)
        self.Emotion_Frame.setPixmap(QPixmap.fromImage(qImg))

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
        self.Dashboard.setEnabled(True)
        event.accept()

    def process_frame_with_model(self, frame):
        """Detect faces and perform emotion recognition."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)

        faces = []
        emotions = []

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)

                # Crop and preprocess the face for the model
                face_img = frame[max(0, y):y + h, max(0, x):x + w]
                gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                resized_face = cv2.resize(gray_face, (48, 48))
                normalized_face = resized_face / 255.0
                reshaped_face = np.reshape(normalized_face, (1, 48, 48, 1))

                # Predict emotion
                result = self.model.predict(reshaped_face)
                label = np.argmax(result, axis=1)[0]

                faces.append((x, y, w, h))
                emotions.append(self.labels_dict[label])

        return faces, emotions

    def draw_emotion_info(self, frame, faces, emotions):
        """Draw emotion information on the frame."""
        for (x, y, w, h), emotion in zip(faces, emotions):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

            label_background = (255, 0, 255)
            label_font_color = (255, 255, 255)
            font_scale = 0.9
            font = cv2.FONT_HERSHEY_SIMPLEX
            thickness = 2

            (text_width, text_height), _ = cv2.getTextSize(emotion, font, font_scale, thickness)
            cv2.rectangle(frame, (x, y - 30), (x + text_width, y), label_background, thickness=cv2.FILLED)
            cv2.putText(frame, emotion, (x, y - 10), font, font_scale, label_font_color, thickness)

        return frame

    # GENERATE ADVICE ONLY EVERY 30 SECONDS
    def update_frame(self):
        """Capture frame from webcam and update the QLabel."""
        if not self.is_detecting:
            return

        if self.user_id is None:
            print("Cannot record emotions: No valid user_id")
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        # Ensure the frame maintains 16:9 aspect ratio
        height, width, _ = frame.shape
        target_width = 640
        target_height = int(target_width * 9 / 16)

        # Resize the frame to 16:9
        resized_frame = cv2.resize(frame, (target_width, target_height))

        faces, emotions = self.process_frame_with_model(resized_frame)

        # Check for emotions and generate advice if needed
        current_time = datetime.now()
        for emotion in emotions:
            # Only generate advice if the emotion has changed and cooldown has passed
            if emotion != self.last_emotion and (self.last_advice_time is None or
                                                 (current_time - self.last_advice_time).total_seconds() > 30):
                try:
                    self.db.record_emotion(user_id=self.user_id, emotion_type=emotion)
                    self.last_emotion = emotion

                    # Check if the emotion is Sad or Angry and show advice
                    if emotion in ['Sad', 'Angry']:
                        try:
                            advice = self.emotion_advice_system.generate_advice(emotion)
                            dialog = AdviceDialog(advice, self.Dashboard)
                            dialog.show()
                            self.last_advice_time = current_time  # Update last advice time

                        except Exception as e:
                            print(f"Error generating advice: {e}")

                except Exception as e:
                    print(f"Error recording emotion: {e}")

        final_frame = self.draw_emotion_info(resized_frame, faces, emotions)

        # Convert the frame to QImage for PyQt5 display
        bytes_per_line = 3 * target_width
        qImg = QImage(final_frame.data, target_width, target_height,
                      bytes_per_line, QImage.Format_BGR888)

        # Display the image on the QLabel
        self.Emotion_Frame.setPixmap(QPixmap.fromImage(qImg))

    def closeEvent(self, event):
        """Handle application close and ensure all connections are terminated"""
        # Stop emotion detection and release webcam
        self.is_detecting = False
        if hasattr(self, 'cap'):
            self.cap.release()

        # Disconnect Serial/Bluetooth if active
        if hasattr(self, 'serial_monitor'):
            serial_monitor = self.serial_monitor
            if serial_monitor.serial_thread and serial_monitor.serial_thread.is_alive():
                try:
                    serial_monitor.stop_event.set()
                    serial_monitor.serial_thread.join(timeout=2)  # Wait for thread to terminate
                    serial_monitor.update_text_area("Connection closed due to application exit")
                except Exception as e:
                    print(f"Error closing serial connection: {e}")

        # Close any open dialogs or child windows
        if hasattr(self, 'AccPage_window') and self.AccPage_window:
            self.AccPage_window.close()

        # Stop any running timers
        if hasattr(self, 'timer'):
            self.timer.stop()

        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dashboard = QtWidgets.QMainWindow()
    ui = Ui_Dashboard('example_username')
    ui.setupUi(Dashboard)
    Dashboard.show()
    sys.exit(app.exec_())