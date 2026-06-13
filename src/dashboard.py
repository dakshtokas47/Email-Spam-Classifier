import os
import tkinter as tk
from tkinter import messagebox, ttk
import joblib

# Clear out any path confusion to find the trained model files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'spam_model.pkl')
vec_path = os.path.join(BASE_DIR, 'vectorizer.pkl')

# Global variables for our AI model components
model = None
vectorizer = None

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    model_status = "🤖 AI Engine: ONLINE"
except Exception as e:
    model_status = "🤖 AI Engine: OFFLINE (Run Notebook First)"

# --- FUNCTIONS FOR INTERACTION ---
def analyze_email():
    """Extracts text from the dashboard input and runs the AI classifier."""
    if not model or not vectorizer:
        messagebox.showerror("Error", "AI Model components are not loaded. Please ensure you ran all cells in your notebook successfully first!")
        return
        
    raw_text = text_input.get("1.0", tk.END).strip()
    
    if not raw_text:
        messagebox.showwarning("Input Empty", "Please paste or type an email phrase to scan.")
        return
        
    # Transform data and run predictions
    processed_input = [raw_text.lower()]
    vectorized_input = vectorizer.transform(processed_input)
    prediction = model.predict(vectorized_input)[0]
    
    # Update results UI interface based on verdict
    if prediction == 'spam':
        result_label.config(text="🚨 CRITICAL WARNING: SPAM DETECTED!", foreground="#d9534f")
        verdict_details.config(text="This email matches malicious phishing or vehicle spam patterns.", foreground="#d9534f")
    else:
        result_label.config(text="✅ SAFE VERDICT: CLEAN EMAIL (HAM)", foreground="#5cb85c")
        verdict_details.config(text="This communication is categorized as safe, legitimate correspondence.", foreground="#5cb85c")

# --- UI WINDOW SETUP ---
root = tk.Tk()
root.title("CODTECH: Vehicle Email Spam Classifier Dashboard")
root.geometry("600x500")
root.configure(bg="#f5f6fa")

# Main Header App Banner (Fixed padding bug here)
header_frame = tk.Frame(root, bg="#2c3e50")
header_frame.pack(fill=tk.X)
header_title = tk.Label(header_frame, text="🚗 VEHICLE EMAIL SPAM CLASSIFIER", font=("Helvetica", 16, "bold"), fg="white", bg="#2c3e50", pady=15)
header_title.pack()

status_strip = tk.Label(root, text=model_status, font=("Helvetica", 9, "italic"), fg="#7f8c8d", bg="#f5f6fa")
status_strip.pack(anchor=tk.W, padx=20, pady=5)

# Text Input Area Label
input_label = tk.Label(root, text="✍️ Paste Email Text Content Below:", font=("Helvetica", 11, "bold"), bg="#f5f6fa", fg="#34495e")
input_label.pack(anchor=tk.W, padx=20, pady=5)

# Text Box Scrollable Entry Space
text_input = tk.Text(root, height=8, width=65, font=("Helvetica", 10), relief=tk.SOLID, bd=1)
text_input.pack(padx=20, pady=5)

# Execution Scanner Button
scan_button = tk.Button(root, text="🚀 Run AI Analysis Scan", font=("Helvetica", 11, "bold"), fg="white", bg="#2980b9", activebackground="#3498db", relief=tk.FLAT, command=analyze_email, cursor="hand2", pady=8)
scan_button.pack(fill=tk.X, padx=20, pady=15)

# Divider line
divider = tk.Frame(root, height=2, bg="#dcdde1")
divider.pack(fill=tk.X, padx=20, pady=5)

# Results Panel Block
output_frame = tk.LabelFrame(root, text=" AI Analytical Results Output ", font=("Helvetica", 10, "bold"), bg="white", fg="#2c3e50", relief=tk.GROOVE, bd=2)
output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

result_label = tk.Label(output_frame, text="Awaiting Input Scanner...", font=("Helvetica", 13, "bold"), bg="white", fg="#7f8c8d")
result_label.pack(pady=10)

verdict_details = tk.Label(output_frame, text="Results summary parameters will display here.", font=("Helvetica", 10), bg="white", fg="#95a5a6")
verdict_details.pack(pady=5)

# Start desktop execution loop
root.mainloop()