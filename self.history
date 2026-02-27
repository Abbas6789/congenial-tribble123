import numpy as np

class ProbabilisticBrain:
    def __init__(self):
        self.history = []

    def update_history(self, new_data):
        self.history = new_data

    def calculate_logic(self):
        if not self.history:
            return 0.5, "ڈیٹا کا انتظار ہے..."
        
        # پچھلے 10 راؤنڈز کی اوسط نکالنا
        avg = np.mean(self.history[-10:])
        
        # جیتنے کا امکان (Probability) نکالنا
        prob = 0.85 if avg < 1.8 else 0.45
        status = "بہتر موقع (Safe)" if prob > 0.7 else "خطرہ (High Risk)"
        
        return prob, status
