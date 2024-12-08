# db_manager.py
import mysql.connector
from mysql.connector import Error
import hashlib
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class DatabaseManager:
    _instance = None
    logged_in_user = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            try:
                self.connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='bantai'  # Make sure to use the correct database name
                )
                self.cursor = self.connection.cursor(dictionary=True)
                self.initialized = True
                print("MySQL Database connection established successfully!")
            except Error as e:
                print(f"Error connecting to MySQL Database: {e}")
                self.show_error_message(f"Error connecting to MySQL Database: {e}")

    def show_error_message(self, message):
        """Displays a simple error message box using tkinter."""
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Database Connection Error", message)
        root.destroy()

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def record_emotion(self, user_id, emotion_type, heart_rate_id=None):
        """
        Record emotion data for a user
        :param user_id: User's unique identifier
        :param emotion_type: Type of emotion detected
        """
        try:
            query = """
                INSERT INTO user_emotion 
                (user_id, emotion_type, timestamp, heart_rate_id) 
                VALUES (%s, %s, NOW(), %s)
                """
            self.cursor.execute(query, (user_id, emotion_type, heart_rate_id))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error recording emotion: {e}")
            return None

    def register_user(self, first_name, last_name, username, email, password):
        """Register a new user"""
        try:
            # Check if username or email already exists
            check_query = "SELECT * FROM users WHERE username = %s OR email = %s"
            self.cursor.execute(check_query, (username, email))
            if self.cursor.fetchone():
                print("Username or email already exists")
                return None

            hashed_password = self.hash_password(password)
            query = """
            INSERT INTO users 
            (first_name, last_name, username, email, password) 
            VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (first_name, last_name, username, email, hashed_password))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error registering user: {e}")
            return None

    def get_user_by_username(self, username):
        """Retrieve user details by username"""
        try:
            query = """
            SELECT 
                u.user_id, 
                u.first_name, 
                u.last_name, 
                u.username, 
                u.email, 
                u.password,
                ud.age, 
                ud.weight, 
                ud.height, 
                ud.bpm
            FROM 
                users u
            LEFT JOIN 
                user_data ud ON u.user_id = ud.user_id
            WHERE 
                u.username = %s
            """
            self.cursor.execute(query, (username,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching user: {e}")
            return None

    def login_user(self, username, password):
        """Authenticate user"""
        try:
            hashed_password = self.hash_password(password)
            query = """
            SELECT * FROM users 
            WHERE (username = %s OR email = %s) AND password = %s
            """
            self.cursor.execute(query, (username, username, hashed_password))
            user = self.cursor.fetchone()

            if user:
                actual_username = user['username']
                DatabaseManager.logged_in_user = actual_username
                return {
                    'username': actual_username,
                    'email': user['email']
                }
            return None
        except Error as e:
            print(f"Login error: {e}")
            return None

    def get_logged_in_username(self):
        """Get the username of the currently logged-in user"""
        return DatabaseManager.logged_in_user

    def get_user_by_id(self, user_id):
        """Retrieve user details by user_id"""
        try:
            query = "SELECT * FROM users WHERE user_id = %s"
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching user: {e}")
            return None

    def update_user_profile(self, user_id, first_name=None, last_name=None, username=None, email=None):
        """Update user profile details"""
        try:
            update_fields = []
            params = []

            if first_name:
                update_fields.append("first_name = %s")
                params.append(first_name)
            if last_name:
                update_fields.append("last_name = %s")
                params.append(last_name)
            if username:
                update_fields.append("username = %s")
                params.append(username)
            if email:
                update_fields.append("email = %s")
                params.append(email)

            if not update_fields:
                return False

            params.append(user_id)
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = %s"
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error updating user profile: {e}")
            return False

    def update_user_data(self, user_id, age=None, weight=None, height=None, bpm=None):
        """Update user data"""
        try:
            update_fields = []
            params = []

            if age:
                update_fields.append("age = %s")
                params.append(age)
            if weight:
                update_fields.append("weight = %s")
                params.append(weight)
            if height:
                update_fields.append("height = %s")
                params.append(height)
            if bpm:
                update_fields.append("bpm = %s")
                params.append(bpm)

            if not update_fields:
                return False

            params.append(user_id)
            query = f"UPDATE user_data SET {', '.join(update_fields)} WHERE user_id = %s"
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error updating user data: {e}")
            return False

    def add_emotion_record(self, user_id, emotion_type):
        """Add emotion record for a user"""
        try:
            query = """
            INSERT INTO user_emotion 
            (user_id, emotion_type, timestamp) 
            VALUES (%s, %s, NOW())
            """
            self.cursor.execute(query, (user_id, emotion_type))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error adding emotion record: {e}")
            return None

    def add_heart_rate_record(self, user_id, heart_rate, spo2):
        """Add heart rate and SpO2 record for a user"""
        try:
            query = """
            INSERT INTO user_heart_rate 
            (user_id, heart_rate, spo2, timestamp) 
            VALUES (%s, %s, %s, NOW())
            """
            self.cursor.execute(query, (user_id, heart_rate, spo2))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error adding heart rate and SpO2 record: {e}")
            return None

    def check_if_user_exists(self, username, email):
        """Check if username or email already exists"""
        cursor = self.connection.cursor()
        query = "SELECT COUNT(*) FROM users WHERE username = %s OR email = %s"
        cursor.execute(query, (username, email))
        result = cursor.fetchone()
        cursor.close()
        return result[0] > 0

    def close(self):
        """Close database connection"""
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed")

# Create a singleton instance
db_manager = DatabaseManager()