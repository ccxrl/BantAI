# db_manager.py
import mysql.connector
from mysql.connector import Error
import hashlib
import tkinter as tk
from tkinter import messagebox

class DatabaseManager:
    _instance = None
    logged_in_user = None  # To store the logged-in user's username

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            try:
                self.connection = mysql.connector.connect(
                    host='localhost',
                    user='root',  # Replace with your MySQL username
                    password='',  # Replace with your MySQL password
                    database='bantai'
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
        root.withdraw()  # Hide the root window
        messagebox.showerror("Database Connection Error", message)  # Show the error message
        root.destroy()  # Destroy the root window after the message box is closed

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, first_name, last_name, username, email, password):
        """
        Register a new user
        :param first_name: User's first name
        :param last_name: User's last name
        :param username: Unique username
        :param email: User's email
        :param password: User's password (will be hashed)
        :return: user_id if successful, None otherwise
        """
        try:
            # Check if username or email already exists
            check_query = "SELECT * FROM users WHERE username = %s OR email = %s"
            self.cursor.execute(check_query, (username, email))
            if self.cursor.fetchone():
                print("Username or email already exists")
                return None

            # Hash the password
            hashed_password = self.hash_password(password)

            # Insert new user
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
        """
        Retrieve user details by username, joining users and user_data tables
        :param username: User's unique username
        :return: User data or None
        """
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
        """
        Authenticate user
        :param username: Username or email
        :param password: User's password
        :return: User data if successful, None otherwise
        """
        try:
            # Hash the input password
            hashed_password = self.hash_password(password)

            # Check credentials
            query = """
            SELECT * FROM users 
            WHERE (username = %s OR email = %s) AND password = %s
            """
            self.cursor.execute(query, (username, username, hashed_password))
            user = self.cursor.fetchone()

            # If login is successful, set the logged-in user
            if user:
                # Explicitly get the username, even if login was with email
                actual_username = user['username']
                DatabaseManager.logged_in_user = actual_username
                return {
                    'username': actual_username,  # Always return the actual username
                    'email': user['email'],
                    # Add more fields as needed
                }
            else:
                return None
        except Error as e:
            print(f"Login error: {e}")
            return None

    def get_logged_in_username(self):
        """
        Get the username of the currently logged-in user
        :return: Username if logged in, None otherwise
        """
        if DatabaseManager.logged_in_user:
            return DatabaseManager.logged_in_user
        else:
            return None

    def get_user_by_id(self, user_id):
        """
        Retrieve user details by user_id
        :param user_id: User's unique identifier
        :return: User data or None
        """
        try:
            query = "SELECT * FROM users WHERE user_id = %s"
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching user: {e}")
            return None

    def update_user_profile(self, user_id, first_name=None, last_name=None, username=None, email=None):
        """
        Update user profile details
        :param user_id: User's unique identifier
        :param first_name: New first name (optional)
        :param last_name: New last name (optional)
        :param username: New username (optional)
        :param email: New email (optional)
        :return: True if successful, False otherwise
        """
        try:
            # Prepare update query dynamically
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

            # Add user_id to params
            params.append(user_id)

            # Construct full query
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = %s"
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error updating user profile: {e}")
            return False
    
    def update_user_data(self, user_id, age=None, weight=None, height=None, bpm=None):
        """
        Update user data table.
        :param user_id: User's unique identifier
        :param age: New age (optional)
        :param weight: New weight (optional)
        :param height: New height (optional)
        :param bpm: New BPM (optional)
        :return: True if successful, False otherwise
        """
        try:
            # Prepare update query dynamically
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

            # Add user_id to params
            params.append(user_id)

            # Construct full query
            query = f"UPDATE user_data SET {', '.join(update_fields)} WHERE user_id = %s"
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error updating user data: {e}")
            return False


    def add_emotion_record(self, user_id, emotion_type):
        """
        Add emotion record for a user
        :param user_id: User's unique identifier
        :param emotion_type: Type of emotion
        :return: Record ID if successful, None otherwise
        """
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

    def add_heart_rate_record(self, user_id, heart_rate):
        """
        Add heart rate record for a user
        :param user_id: User's unique identifier
        :param heart_rate: Heart rate value
        :return: Record ID if successful, None otherwise
        """
        try:
            query = """
            INSERT INTO user_heart_rate 
            (user_id, heart_rate, timestamp) 
            VALUES (%s, %s, NOW())
            """
            self.cursor.execute(query, (user_id, heart_rate))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error adding heart rate record: {e}")
            return None
        
    def check_if_user_exists(self, username, email):
        """Checks if the username or email already exists in the database."""
        cursor = self.connection.cursor()
        query = "SELECT COUNT(*) FROM users WHERE username = %s OR email = %s"
        cursor.execute(query, (username, email))
        result = cursor.fetchone()
        cursor.close()

        # If the count is greater than 0, it means the username or email exists
        return result[0] > 0

    def close_connection(self):
        """Close database connection"""
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL Database connection closed.")

db_manager = DatabaseManager()