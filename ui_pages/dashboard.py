from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import mediapipe as mp
from PyQt5.QtGui import QImage, QPixmap
from datetime import datetime
from db_manager import db_manager
from advice_system import EmotionAdviceSystem, AdviceDialog
from datetime import datetime

class Ui_Dashboard(object):
    def __init__(self, username):
        self.username = username
        print("Username being passed to dashboard:", username)
        self.AccPage_window = None
        self.is_detecting = True
        self.last_emotion = None
        self.db = db_manager
        self.emotion_advice_system = EmotionAdviceSystem()  # Initialize the advice system
        self.last_advice_time = None
        user_data = self.db.get_user_by_username(username)
        if user_data:
            self.user_id = user_data['user_id']
            print(f"User ID retrieved: {self.user_id}")
        else:
            self.user_id = None
            print("Failed to get user ID")

    def setupUi(self, Dashboard):
        self.Dashboard = Dashboard
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

        # Biometrics scroll area
        self.Biometrics = QtWidgets.QScrollArea(self.centralwidget)
        self.Biometrics.setGeometry(QtCore.QRect(750, 110, 231, 491))
        self.Biometrics.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 15px;
        """)
        self.Biometrics.setWidgetResizable(True)
        self.Biometrics.setObjectName("Biometrics")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 229, 489))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        # Scrollbar
        self.verticalScrollBar = QtWidgets.QScrollBar(self.scrollAreaWidgetContents)
        self.verticalScrollBar.setGeometry(QtCore.QRect(210, 0, 21, 491))
        self.verticalScrollBar.setStyleSheet("background-color: #4faaaa;")
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.Biometrics.setWidget(self.scrollAreaWidgetContents)

        # Emotion Display Frame
        self.Emotion_Frame = QtWidgets.QLabel(self.centralwidget)
        self.Emotion_Frame.setGeometry(QtCore.QRect(70, 110, 591, 321))
        self.Emotion_Frame.setStyleSheet("""
            background-color: black;
            border-radius: 15px;
        """)
        self.Emotion_Frame.setAlignment(QtCore.Qt.AlignCenter)

        # Add control buttons container
        self.controlsContainer = QtWidgets.QWidget(self.centralwidget)
        self.controlsContainer.setGeometry(QtCore.QRect(70, 440, 591, 50))
        self.controlsContainer.setStyleSheet("""
            background-color: transparent;
        """)

        # Create horizontal layout for buttons
        self.controlsLayout = QtWidgets.QHBoxLayout(self.controlsContainer)
        self.controlsLayout.setContentsMargins(200, 0, 200, 0)  # Adjust margins as needed
        self.controlsLayout.setSpacing(40)  # Set spacing between buttons

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
        self.controlsLayout.addSpacing(40)  # Add spacing between buttons
        self.controlsLayout.addWidget(self.stopButton)

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

        # Initialize webcam and emotion detection
        self.cap = cv2.VideoCapture(0)
        self.face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5)
        self.model = load_model('model_file_30epochs.h5')

        self.labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy',
                           4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

        # Set up a timer for updating the frame
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30 ms
    
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
        # Re-enable the main dashboard window when Account Page is closed
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
                face_img = frame[max(0, y):y+h, max(0, x):x+w]
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
            if emotion != self.last_emotion:
                try:
                    self.db.record_emotion(user_id=self.user_id, emotion_type=emotion)
                    self.last_emotion = emotion
                    
                    # Check if the emotion is Sad or Angry and show advice
                    if emotion in ['Sad', 'Angry']:
                        if (self.last_advice_time is None or 
                            (current_time - self.last_advice_time).total_seconds() > 60):
                            try:
                                advice = self.emotion_advice_system.generate_advice(emotion)
                                dialog = AdviceDialog(advice, self.Dashboard)
                                dialog.show()
                                self.last_advice_time = current_time
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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dashboard = QtWidgets.QMainWindow()
    ui = Ui_Dashboard('example_username')
    ui.setupUi(Dashboard)
    Dashboard.show()
    sys.exit(app.exec_())