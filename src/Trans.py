
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, ConfusionMatrixDisplay
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------------------
# Global variables
# ---------------------------
vectorizer = None
svm_model = None
dataset_df = None
X_test_global, y_test_global, y_pred_global = None, None, None  # for visualization

# ---------------------------
# Generate synthetic dataset
# ---------------------------
def generate_dataset(rows=100):
    global dataset_df
    python_correct = ["print('Hello World')", "x = 5\ny = x + 2", "for i in range(5): print(i)"]
    python_buggy = ["print('Hello World'", "x = 5\ny = x +", "for i in range(5) print(i)"]

    java_correct = ["int x = 10;", "System.out.println('Hello');", "for(int i=0;i<5;i++){System.out.println(i);}"]
    java_buggy = ["int x = ;", "System.out.println('Hello'", "for(int i=0;i<5;i++) System.out.println(i"]

    js_correct = ["console.log('Hello')", "let x = 5; let y = x + 2;", "for(let i=0;i<5;i++){console.log(i);}"]
    js_buggy = ["console.log('Hello'", "let x = 5; let y = x + ;", "for(let i=0;i<5;i++) console.log(i"]

    dataset = []
    for _ in range(rows):
        lang = random.choice(["Python", "Java", "JavaScript"])
        if lang == "Python":
            label = random.choice([0,1])
            code = random.choice(python_correct if label==0 else python_buggy)
        elif lang == "Java":
            label = random.choice([0,1])
            code = random.choice(java_correct if label==0 else java_buggy)
        else:
            label = random.choice([0,1])
            code = random.choice(js_correct if label==0 else js_buggy)
        dataset.append({"code": code, "language": lang, "label": label})

    dataset_df = pd.DataFrame(dataset)
    return dataset_df

# ---------------------------
# Preprocess dataset
# ---------------------------
def preprocess_dataset():
    global dataset_df
    if dataset_df is None:
        messagebox.showwarning("Warning", "Generate dataset first!")
        return
    dataset_df['code'] = dataset_df['code'].str.strip()
    dataset_df['code'] = dataset_df['code'].str.replace('\n',' ', regex=True)
    messagebox.showinfo("Preprocessing Done", "Dataset preprocessing completed successfully.")

# ---------------------------
# Display dataset table
# ---------------------------
def display_dataset_table():
    global dataset_df
    if dataset_df is None:
        dataset_df = generate_dataset(100)

    display_window = tk.Toplevel(root)
    display_window.title("Generated Dataset")

    frame = tk.Frame(display_window)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    tree_scroll_y = tk.Scrollbar(frame)
    tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree_scroll_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

    tree = ttk.Treeview(frame, columns=("Code", "Language", "Label"), show="headings",
                        yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
    tree.pack(fill=tk.BOTH, expand=True)

    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    tree.heading("Code", text="Code")
    tree.heading("Language", text="Language")
    tree.heading("Label", text="Label")

    tree.column("Code", width=500)
    tree.column("Language", width=100)
    tree.column("Label", width=50, anchor="center")

    for _, row in dataset_df.iterrows():
        tree.insert("", tk.END, values=(row['code'], row['language'], row['label']))

    def on_row_double_click(event):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item, "values")
            code_text = values[0]
            test_code_box.delete("1.0", tk.END)
            test_code_box.insert(tk.END, code_text)

    tree.bind("<Double-1>", on_row_double_click)

# ---------------------------
# Train SVM
# ---------------------------
def train_svm():
    global vectorizer, svm_model, dataset_df, X_test_global, y_test_global, y_pred_global
    if dataset_df is None:
        messagebox.showwarning("Warning", "Generate dataset first!")
        return
    try:
        expanded_df = pd.concat([dataset_df]*100, ignore_index=True)
        vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1,6))
        X = vectorizer.fit_transform(expanded_df['code'])
        y = expanded_df['label']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_test_global, y_test_global = X_test, y_test

        svm_model = SVC(kernel='rbf', C=10, gamma='scale')
        svm_model.fit(X_train, y_train)
        y_pred = svm_model.predict(X_test)
        y_pred_global = y_pred

        acc = accuracy_score(y_test, y_pred)
        acc_percent = acc * 100
        report = classification_report(y_test, y_pred)

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Dataset training.\n")
        result_text.insert(tk.END, f"Accuracy: {acc_percent:.2f}%\n\n")
        result_text.insert(tk.END, f"Classification Report:\n{report}\n")
        result_text.insert(tk.END, "SVM training completed.")

    except Exception as e:
        messagebox.showerror("Error", f"Training failed: {e}")

# ---------------------------
# Test new code snippet
# ---------------------------
def test_code():
    global vectorizer, svm_model
    if svm_model is None or vectorizer is None:
        messagebox.showwarning("Warning", "Train the SVM model first!")
        return
    code = test_code_box.get("1.0", tk.END).strip()
    if not code:
        messagebox.showwarning("Warning", "Enter code to test!")
        return
    X_new = vectorizer.transform([code])
    pred = svm_model.predict(X_new)[0]
    result = "✅ Correct" if pred==0 else "❌ Buggy"
    messagebox.showinfo("Prediction Result", f"The code is predicted as: {result}")

# ---------------------------
# Clear All
# ---------------------------
def clear_all():
    test_code_box.delete("1.0", tk.END)
    result_text.delete("1.0", tk.END)
    messagebox.showinfo("Cleared", "All input and results have been cleared.")

# ---------------------------
# Visualization Functions
# ---------------------------
def show_label_distribution():
    if dataset_df is None:
        messagebox.showwarning("Warning", "Generate dataset first!")
        return
    window = tk.Toplevel(root)
    window.title("Label Distribution")
    fig, ax = plt.subplots(figsize=(5,4))
    dataset_df['label'].value_counts().plot(kind='bar', color=['green','red'], ax=ax)
    ax.set_title("Label Distribution (0=Correct, 1=Buggy)")
    ax.set_xlabel("Label")
    ax.set_ylabel("Count")
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()

def show_confusion_matrix():
    if y_test_global is None or y_pred_global is None:
        messagebox.showwarning("Warning", "Train the model first!")
        return
    window = tk.Toplevel(root)
    window.title("Confusion Matrix")
    fig, ax = plt.subplots(figsize=(5,4))
    from sklearn.metrics import ConfusionMatrixDisplay
    ConfusionMatrixDisplay.from_predictions(y_test_global, y_pred_global, ax=ax, cmap="Blues")
    ax.set_title("Confusion Matrix")
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()

# ---------------------------
# Tkinter GUI
# ---------------------------
root = tk.Tk()
root.title("AI Code Debugger - SVM Trainer & Tester")
root.geometry("1600x950")

title_label = tk.Label(root, text="AI Code Debugger - SVM Trainer & Tester", font=("Segoe UI", 20, "bold"))
title_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

display_btn = tk.Button(button_frame, text="Display Dataset", command=display_dataset_table, bg="#17a2b8", fg="white", font=("Segoe UI", 12))
display_btn.pack(side="left", padx=5)

preprocess_btn = tk.Button(button_frame, text="Preprocess Dataset", command=preprocess_dataset, bg="#ffc107", fg="black", font=("Segoe UI", 12))
preprocess_btn.pack(side="left", padx=5)

train_btn = tk.Button(button_frame, text="Train SVM", command=train_svm, bg="#28a745", fg="white", font=("Segoe UI", 12))
train_btn.pack(side="left", padx=5)

label_graph_btn = tk.Button(button_frame, text="Label Distribution", command=show_label_distribution, bg="#6f42c1", fg="white", font=("Segoe UI", 12))
label_graph_btn.pack(side="left", padx=5)

conf_matrix_btn = tk.Button(button_frame, text="Confusion Matrix", command=show_confusion_matrix, bg="#fd7e14", fg="white", font=("Segoe UI", 12))
conf_matrix_btn.pack(side="left", padx=5)

nav_frame = tk.Frame(root)  # Standard Tkinter Frame
nav_frame.pack(pady=10, fill="x")
# Back Button
back_btn = tk.Button(
    nav_frame, 
    text="⬅ Back", 
    width=150, 
    command=lambda: __import__("subprocess").call(["python", "main.py"])
)
back_btn.pack(side="left", padx=20, pady=10)

# Next Button
next_btn = tk.Button(
    nav_frame, 
    text="Next ➡", 
    width=150, 
    command=lambda: __import__("subprocess").call(["python", "Test.py"])
)
next_btn.pack(side="right", padx=20, pady=10)
clear_btn = tk.Button(button_frame, text="Clear All", command=clear_all, bg="#dc3545", fg="white", font=("Segoe UI", 12))
clear_btn.pack(side="left", padx=5)

result_text = tk.Text(root, height=10, width=100, font=("Segoe UI", 12))
result_text.pack(pady=10)

test_label = tk.Label(root, text="Enter Code to Test:", font=("Segoe UI", 14))
test_label.pack(pady=5)

test_code_box = tk.Text(root, height=5, width=80, font=("Segoe UI", 12))
test_code_box.pack(pady=5)

test_btn = tk.Button(root, text="Test Code Snippet", command=test_code, bg="#17a2b8", fg="white", font=("Segoe UI", 14))
test_btn.pack(pady=10)

root.mainloop()
