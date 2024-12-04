from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import google.generativeai as genai

class AdviceDialog(QDialog):
    def __init__(self, advice_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("BantAI Advice")
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                border-radius: 15px;
            }
            QLabel {
                font: 12pt 'Segoe UI';
                color: #333333;
                padding: 10px;
            }
            QPushButton {
                background-color: #5db8b0;
                color: white;
                border-radius: 12px;
                padding: 8px 16px;
                font: bold 10pt 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #4f9f9c;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Add advice text
        advice_label = QLabel(advice_text)
        advice_label.setWordWrap(True)
        layout.addWidget(advice_label)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        self.resize(400, 200)

class EmotionAdviceSystem:
    def __init__(self, api_key):
        # Configure Gemini AI with the provided API key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
    def generate_advice(self, emotion):
        prompts = {
            "Sad": "Provide a short advice to someone who feels sad: ",
            "Angry": "Provide a short advice to someone who feels angry: "
        }
        
        prompt = prompts.get(emotion, "Provide advice: ")
        
        # Generate advice using Gemini AI
        response = self.model.generate_content(prompt)
        
        # Return the generated advice
        return response.text