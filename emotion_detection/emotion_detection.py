# FINAL ISH 11/20, 8:31 am
# no face mesh, better visualization

import cv2
import numpy as np
from tensorflow.keras.models import load_model
import mediapipe as mp
from datetime import datetime
import mysql.connector
from mysql.connector import Error

model = load_model('SoftEng_BantAI\emotion_detection\model_file_30epochs.h5')

labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

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

    def record_emotion(self, user_id, emotion_type):
        try:
            query = """
            INSERT INTO user_emotion 
            (user_id, emotion_type, timestamp) 
            VALUES (%s, %s, %s)
            """
            current_time = datetime.now()
            data = (user_id, emotion_type, current_time)
            self.cursor.execute(query, data)
            self.connection.commit()
            print(f"Recorded emotion: {emotion_type}")
        except Error as e:
            print(f"Error recording emotion: {e}")

    def close(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed")

def initialize_webcam(camera_index=0):
    """Initialize the webcam."""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise ValueError("Failed to open webcam")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return cap

def initialize_face_detection():
    """Initialize MediaPipe Face Detection."""
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5
    )
    return face_detection

def process_frame_with_model(frame, face_detection):
    """Detect faces and perform emotion recognition using the trained model."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

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
            result = model.predict(reshaped_face)
            label = np.argmax(result, axis=1)[0]

            faces.append((x, y, w, h))
            emotions.append(labels_dict[label])

    return faces, emotions

def draw_emotion_info(frame, faces, emotions):
    """Draw emotion information on the frame with purple bounding box and label background."""
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


def main():
    try:
        db = DatabaseManager()
        cap = initialize_webcam()
        face_detection = initialize_face_detection()

        print("Press 'q' to quit")
        print("Starting emotion detection...")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            faces, emotions = process_frame_with_model(frame, face_detection)

            for emotion in emotions:
                db.record_emotion(user_id=1, emotion_type=emotion)  # Example user_id = 1

            frame = draw_emotion_info(frame, faces, emotions)
            
            cv2.imshow('Emotion Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quitting...")
                break

    except Exception as e:
        print(f"Main loop error: {str(e)}")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        face_detection.close()
        db.close()
        print("Cleanup completed")

if __name__ == "__main__":
    main()