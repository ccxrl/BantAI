from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

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
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
        self.model = GPT2LMHeadModel.from_pretrained("distilgpt2")
        
    def generate_advice(self, emotion):
        prompts = {
            "Sad": "Here's some supportive advice for someone feeling sad: ",
            "Angry": "Here's some calming advice for someone feeling angry: "
        }
        
        prompt = prompts.get(emotion, "Here's some advice: ")
        
        # Encode the prompt
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        
        # Generate response
        outputs = self.model.generate(
            inputs,
            max_length=100,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # Decode and return the generated text
        advice = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return advice