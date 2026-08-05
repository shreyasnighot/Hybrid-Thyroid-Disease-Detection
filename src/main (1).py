import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import subprocess
import joblib
import threading
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ================= APP SETTINGS =================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Thyroid Disease Detection Dashboard - Enhanced")
root.geometry("1500x850")

# ================= MAIN LAYOUT =================
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True)

sidebar = ctk.CTkFrame(main_frame, width=260)
sidebar.pack(side="left", fill="y", padx=10, pady=10)

content = ctk.CTkFrame(main_frame)
content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

ctk.CTkLabel(sidebar, text="Thyroid Detection",
             font=("Segoe UI", 24, "bold")).pack(pady=20)

# ================= CLEAR FUNCTION =================
def clear_content():
    for widget in content.winfo_children():
        widget.destroy()

# ================= ENHANCED PATIENT ENTRY =================
def patient_entry():
    clear_content()

    scroll_frame = ctk.CTkScrollableFrame(content, width=1200, height=700)
    scroll_frame.pack(fill="both", expand=True, padx=30, pady=30)

    ctk.CTkLabel(
        scroll_frame,
        text="Patient Information Entry",
        font=("Segoe UI", 26, "bold")
    ).pack(pady=20)

    # Enhanced form with checkboxes
    entries = {}
    checkboxes = {}
    
    # Numeric fields
    numeric_fields = [
        ("Age", "age"),
        ("TSH Level", "tsh"),
        ("T3 Level", "t3"),
        ("T4 Level", "t4"),
        ("Heart Rate", "heart_rate"),
        ("Blood Pressure", "blood_pressure"),
        ("Cholesterol", "cholesterol"),
        ("BMI", "bmi")
    ]
    
    for label, key in numeric_fields:
        frame = ctk.CTkFrame(scroll_frame)
        frame.pack(pady=8, fill="x")
        
        ctk.CTkLabel(frame, text=label, width=200).pack(side="left", padx=20)
        entry = ctk.CTkEntry(frame, width=200)
        entry.pack(side="left", padx=20)
        entries[key] = entry
    
    # Gender selection with dropdown
    gender_frame = ctk.CTkFrame(scroll_frame)
    gender_frame.pack(pady=8, fill="x")
    ctk.CTkLabel(gender_frame, text="Gender", width=200).pack(side="left", padx=20)
    
    gender_var = ctk.StringVar(value="Male")
    gender_menu = ctk.CTkOptionMenu(gender_frame, variable=gender_var, 
                                   values=["Male", "Female"])
    gender_menu.pack(side="left", padx=20)
    
    # Checkbox fields (replacing 0/1 inputs)
    checkbox_fields = [
        ("Weight Change", "weight_change"),
        ("Fatigue", "fatigue"),
        ("Hair Loss", "hair_loss"),
        ("Cold Sensitivity", "cold_sensitivity"),
        ("Family History", "family_history")
    ]
    
    for label, key in checkbox_fields:
        frame = ctk.CTkFrame(scroll_frame)
        frame.pack(pady=8, fill="x")
        
        ctk.CTkLabel(frame, text=label, width=200).pack(side="left", padx=20)
        
        # Yes/No radio buttons
        radio_var = ctk.StringVar(value="No")
        yes_radio = ctk.CTkRadioButton(frame, text="Yes", variable=radio_var, value="Yes")
        yes_radio.pack(side="left", padx=10)
        no_radio = ctk.CTkRadioButton(frame, text="No", variable=radio_var, value="No")
        no_radio.pack(side="left", padx=10)
        
        checkboxes[key] = radio_var

    # Label selection dropdown
    label_frame = ctk.CTkFrame(scroll_frame)
    label_frame.pack(pady=8, fill="x")
    ctk.CTkLabel(label_frame, text="Label", width=200).pack(side="left", padx=20)
    
    label_var = ctk.StringVar(value="No")
    label_menu = ctk.CTkOptionMenu(label_frame, variable=label_var, 
                                  values=["No", "Yes"])
    label_menu.pack(side="left", padx=20)

    def save_data():
        try:
            # Collect data with enhanced inputs
            row_data = {
                "Age": int(entries["age"].get()),
                "Gender": 1 if gender_var.get() == "Female" else 0,
                "TSH": float(entries["tsh"].get()),
                "T3": float(entries["t3"].get()),
                "T4": float(entries["t4"].get()),
                "HeartRate": int(entries["heart_rate"].get()),
                "BloodPressure": int(entries["blood_pressure"].get()),
                "Cholesterol": int(entries["cholesterol"].get()),
                "BMI": float(entries["bmi"].get()),
                "WeightChange": 1 if checkboxes["weight_change"].get() == "Yes" else 0,
                "Fatigue": 1 if checkboxes["fatigue"].get() == "Yes" else 0,
                "HairLoss": 1 if checkboxes["hair_loss"].get() == "Yes" else 0,
                "ColdSensitivity": 1 if checkboxes["cold_sensitivity"].get() == "Yes" else 0,
                "FamilyHistory": 1 if checkboxes["family_history"].get() == "Yes" else 0,
                "Label": 1 if label_var.get() == "Yes" else 0
            }

            df_new = pd.DataFrame([row_data])

            file_path = "test.csv"

            # If file exists -> append
            if os.path.exists(file_path):
                df_old = pd.read_csv(file_path)
                df_final = pd.concat([df_old, df_new], ignore_index=True)
            else:
                df_final = df_new

            df_final.to_csv(file_path, index=False)

            messagebox.showinfo("Success", "Patient Data Saved Successfully!")

            # Clear fields after saving
            for entry in entries.values():
                entry.delete(0, "end")
            for radio_var in checkboxes.values():
                radio_var.set("No")
            gender_var.set("Male")
            label_var.set("No")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected Error:\n{str(e)}")

    # Test current patient button
    def test_current_patient():
        try:
            # Collect data from current form entries
            patient_data = {
                "Age": int(entries["age"].get()),
                "Gender": 1 if gender_var.get() == "Female" else 0,
                "TSH": float(entries["tsh"].get()),
                "T3": float(entries["t3"].get()),
                "T4": float(entries["t4"].get()),
                "HeartRate": int(entries["heart_rate"].get()),
                "BloodPressure": int(entries["blood_pressure"].get()),
                "Cholesterol": int(entries["cholesterol"].get()),
                "BMI": float(entries["bmi"].get()),
                "WeightChange": 1 if checkboxes["weight_change"].get() == "Yes" else 0,
                "Fatigue": 1 if checkboxes["fatigue"].get() == "Yes" else 0,
                "HairLoss": 1 if checkboxes["hair_loss"].get() == "Yes" else 0,
                "ColdSensitivity": 1 if checkboxes["cold_sensitivity"].get() == "Yes" else 0,
                "FamilyHistory": 1 if checkboxes["family_history"].get() == "Yes" else 0,
                "Label": 1 if label_var.get() == "Yes" else 0
            }
            
            # Check if model exists
            if not os.path.exists("thyroid_model.joblib"):
                messagebox.showerror("Error", "Please train the model first!")
                return
            
            if not os.path.exists("scaler.joblib"):
                messagebox.showerror("Error", "Please train the model first!")
                return
            
            # Load model and scaler
            model = joblib.load("thyroid_model.joblib")
            scaler = joblib.load("scaler.joblib")
            
            # Convert to DataFrame for prediction
            df_patient = pd.DataFrame([patient_data])
            
            # Prepare data for prediction (exclude Label)
            X_patient = df_patient.drop("Label", axis=1)
            X_scaled = scaler.transform(X_patient)
            
            # Make prediction
            prediction = model.predict(X_scaled)[0]
            
            # Analyze blood test and symptoms
            blood_test_result = analyze_blood_test(df_patient.iloc[0])
            symptom_result = analyze_symptoms(df_patient.iloc[0])
            
            # Get combined result
            final_result, disease_stage, precaution, doctor, treatment = get_combined_result(
                prediction, blood_test_result, symptom_result
            )
            
            # Show result in the form
            show_patient_test_result(final_result, disease_stage, precaution, doctor, treatment, 
                                    blood_test_result, symptom_result)
            
        except ValueError:
            messagebox.showerror("Error", "Please fill all required fields with valid values!")
        except Exception as e:
            messagebox.showerror("Error", f"Test failed: {str(e)}")
    
    def show_patient_test_result(final_result, disease_stage, precaution, doctor, treatment, 
                                 blood_test_result, symptom_result):
        """Display test result in the patient entry form"""
        # Create result frame
        result_frame = ctk.CTkFrame(scroll_frame)
        result_frame.pack(fill="x", pady=20, padx=20)
        
        # Result header with color
        header_color = "#10b981" if final_result == "Normal" else "#ef4444"
        result_header = ctk.CTkFrame(result_frame, fg_color=header_color)
        result_header.pack(fill="x", pady=(10, 5))
        
        header_text = f"Test Result: {final_result}"
        header_label = ctk.CTkLabel(result_header, text=header_text, 
                                  font=("Segoe UI", 18, "bold"), text_color="white")
        header_label.pack(pady=10)
        
        # Result details
        details_frame = ctk.CTkFrame(result_frame)
        details_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        details_text = f"""Blood Test: {blood_test_result} | Symptoms: {symptom_result}
Stage: {disease_stage} | Doctor: {doctor}
Precautions: {precaution}
Treatment: {treatment}"""
        
        details_label = ctk.CTkLabel(details_frame, text=details_text, justify="left")
        details_label.pack(pady=10, padx=20)
        
        # Download report button for this patient
        def download_current_report():
            patient_data = {
                'patient_id': 'Current',
                'blood_test': blood_test_result,
                'symptoms': symptom_result,
                'final_result': final_result,
                'disease_stage': disease_stage,
                'precaution': precaution,
                'doctor': doctor,
                'treatment': treatment
            }
            generate_individual_pdf_report(patient_data)
        
        ctk.CTkButton(details_frame, text="Download Report", command=download_current_report,
                     height=35, width=150, fg_color="#3b82f6").pack(pady=10)

    # Buttons frame
    button_frame = ctk.CTkFrame(scroll_frame)
    button_frame.pack(pady=20)
    
    ctk.CTkButton(
        button_frame,
        text="Test Patient",
        command=test_current_patient,
        height=45,
        width=150,
        fg_color="#f59e0b"
    ).pack(side="left", padx=10)
    
    ctk.CTkButton(
        button_frame,
        text="Save Patient",
        command=save_data,
        height=45,
        width=150,
        fg_color="#10b981"
    ).pack(side="left", padx=10)

# ================= DISPLAY DATA =================
def display_data():
    clear_content()

    if not os.path.exists("test.csv"):
        messagebox.showerror("Error", "No dataset found!")
        return

    df = pd.read_csv("test.csv")

    table_frame = ctk.CTkFrame(content)
    table_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tree = ttk.Treeview(table_frame, show="headings")
    tree.pack(fill="both", expand=True)

    tree["columns"] = list(df.columns)

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

# ================= PREPROCESS =================
def preprocess_data():
    if not os.path.exists("test.csv"):
        messagebox.showerror("Error", "No dataset found!")
        return

    df = pd.read_csv("test.csv")
    df = df.dropna()

    df.to_csv("test_clean.csv", index=False)

    messagebox.showinfo("Success",
                        f"Preprocessing Complete!\nRows remaining: {len(df)}")

# ================= TRAIN SVM =================
def train_svm():
    if not os.path.exists("test_clean.csv"):
        messagebox.showerror("Error", "Run preprocessing first!")
        return

    def task():
        df = pd.read_csv("test_clean.csv")

        X = df.drop("Label", axis=1)
        y = df["Label"]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.3, random_state=42)

        model = SVC(kernel="rbf")
        model.fit(X_train, y_train)

        pred = model.predict(X_test)
        acc = accuracy_score(y_test, pred) * 100

        joblib.dump(model, "thyroid_model.joblib")
        joblib.dump(scaler, "scaler.joblib")

        clear_content()

        frame = ctk.CTkFrame(content)
        frame.pack(pady=40)

        ctk.CTkLabel(frame,
                     text=f"Model Accuracy: {acc:.2f}%",
                     font=("Segoe UI", 26, "bold")).pack(pady=20)

        textbox = ctk.CTkTextbox(frame, width=900, height=300)
        textbox.insert("0.0", classification_report(y_test, pred))
        textbox.configure(state="disabled")
        textbox.pack()

    threading.Thread(target=task).start()

# ================= ENHANCED TEST MODEL WITH COMBINED RESULTS =================
def test_model():
    if not os.path.exists("thyroid_model.joblib"):
        messagebox.showerror("Error", "Train model first!")
        return

    model = joblib.load("thyroid_model.joblib")
    scaler = joblib.load("scaler.joblib")

    df = pd.read_csv("test_clean.csv")

    X = df.drop("Label", axis=1)
    X_scaled = scaler.transform(X)

    predictions = model.predict(X_scaled)

    df["Predicted"] = predictions

    # Enhanced combined analysis
    combined_results = []
    
    for i, row in df.iterrows():
        # Blood test analysis
        blood_test_result = analyze_blood_test(row)
        
        # Symptom analysis
        symptom_result = analyze_symptoms(row)
        
        # Combined final result
        final_result, disease_stage, precaution, doctor, treatment = get_combined_result(
            row["Predicted"], blood_test_result, symptom_result
        )
        
        combined_results.append({
            "patient_id": i+1,
            "blood_test": blood_test_result,
            "symptoms": symptom_result,
            "final_result": final_result,
            "disease_stage": disease_stage,
            "precaution": precaution,
            "doctor": doctor,
            "treatment": treatment
        })

    show_enhanced_report(combined_results)

def analyze_blood_test(row):
    """Analyze blood test results"""
    tsh = row["TSH"]
    t3 = row["T3"]
    t4 = row["T4"]
    
    score = 0
    
    # TSH analysis
    if tsh < 0.4 or tsh > 4.0:
        score += 2
    
    # T3/T4 analysis
    if t3 < 80 or t3 > 200:
        score += 1
    if t4 < 4.5 or t4 > 12.0:
        score += 1
    
    if score >= 3:
        return "Abnormal"
    elif score >= 1:
        return "Borderline"
    else:
        return "Normal"

def analyze_symptoms(row):
    """Analyze symptom patterns"""
    symptoms = [
        row["WeightChange"],
        row["Fatigue"], 
        row["HairLoss"],
        row["ColdSensitivity"],
        row["FamilyHistory"]
    ]
    
    score = sum(symptoms)
    
    if score >= 3:
        return "High Risk"
    elif score >= 1:
        return "Moderate Risk"
    else:
        return "Low Risk"

def get_combined_result(ml_prediction, blood_test, symptoms):
    """Combine all analyses for final result"""
    
    # Weight the different analyses
    ml_weight = 0.4
    blood_weight = 0.35
    symptom_weight = 0.25
    
    # Calculate combined score
    ml_score = 1 if ml_prediction == 1 else 0
    blood_score = 2 if blood_test == "Abnormal" else 1 if blood_test == "Borderline" else 0
    symptom_score = 2 if symptoms == "High Risk" else 1 if symptoms == "Moderate Risk" else 0
    
    combined_score = (ml_score * ml_weight) + (blood_score * blood_weight) + (symptom_score * symptom_weight)
    
    # Determine final result
    if combined_score >= 1.2:
        final_result = "Disease Detected"
        disease_stage = "Thyroid Stage II"
        precaution = "Avoid stress, balanced iodine intake, regular monitoring"
        doctor = "Endocrinologist"
        treatment = "Hormone therapy / Thyroxine medication"
    else:
        final_result = "Normal"
        disease_stage = "Thyroid Stage I"
        precaution = "Maintain healthy diet and regular checkup"
        doctor = "General Physician"
        treatment = "Routine monitoring and lifestyle management"
    
    return final_result, disease_stage, precaution, doctor, treatment

def show_enhanced_report(results):
    """Show results one patient at a time"""
    if not results:
        messagebox.showerror("Error", "No results to display!")
        return
    
    # Store results globally for navigation
    global current_patient_index, all_results
    current_patient_index = 0
    all_results = results
    
    show_single_patient_result()

def show_single_patient_result():
    """Show single patient result with navigation"""
    clear_content()
    
    result = all_results[current_patient_index]
    
    frame = ctk.CTkFrame(content)
    frame.pack(fill="both", expand=True, padx=40, pady=40)

    # Header with patient info and navigation
    header_frame = ctk.CTkFrame(frame)
    header_frame.pack(fill="x", pady=20)
    
    # Navigation buttons
    nav_frame = ctk.CTkFrame(header_frame)
    nav_frame.pack(side="left", padx=20)
    
    def previous_patient():
        global current_patient_index
        if current_patient_index > 0:
            current_patient_index -= 1
            show_single_patient_result()
    
    def next_patient():
        global current_patient_index
        if current_patient_index < len(all_results) - 1:
            current_patient_index += 1
            show_single_patient_result()
    
    # Previous button
    prev_btn = ctk.CTkButton(nav_frame, text="Previous", command=previous_patient,
                           height=35, width=100)
    prev_btn.pack(side="left", padx=5)
    
    # Patient counter
    counter_label = ctk.CTkLabel(nav_frame, 
                                 text=f"Patient {current_patient_index + 1} of {len(all_results)}",
                                 font=("Segoe UI", 14, "bold"))
    counter_label.pack(side="left", padx=20)
    
    # Next button
    next_btn = ctk.CTkButton(nav_frame, text="Next", command=next_patient,
                           height=35, width=100)
    next_btn.pack(side="left", padx=5)
    
    # Disable buttons at boundaries
    if current_patient_index == 0:
        prev_btn.configure(state="disabled")
    if current_patient_index == len(all_results) - 1:
        next_btn.configure(state="disabled")

    # Patient result card
    patient_card = ctk.CTkFrame(frame)
    patient_card.pack(fill="both", expand=True, pady=20)
    
    # Patient header with result color
    header_color = "#10b981" if result['final_result'] == "Normal" else "#ef4444"
    result_header = ctk.CTkFrame(patient_card, fg_color=header_color)
    result_header.pack(fill="x", pady=(10, 5))
    
    header_text = f"Patient {result['patient_id']} - {result['final_result']}"
    header_label = ctk.CTkLabel(result_header, text=header_text, 
                              font=("Segoe UI", 20, "bold"), text_color="white")
    header_label.pack(pady=15)
    
    # Patient details
    details_frame = ctk.CTkFrame(patient_card)
    details_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
    
    # Blood test section
    blood_frame = ctk.CTkFrame(details_frame)
    blood_frame.pack(fill="x", pady=10)
    
    ctk.CTkLabel(blood_frame, text="Blood Test Analysis", 
                font=("Segoe UI", 16, "bold")).pack(pady=5)
    ctk.CTkLabel(blood_frame, text=f"Result: {result['blood_test']}", 
                font=("Segoe UI", 14)).pack(pady=5)
    
    # Symptoms section
    symptom_frame = ctk.CTkFrame(details_frame)
    symptom_frame.pack(fill="x", pady=10)
    
    ctk.CTkLabel(symptom_frame, text="Symptom Analysis", 
                font=("Segoe UI", 16, "bold")).pack(pady=5)
    ctk.CTkLabel(symptom_frame, text=f"Risk Level: {result['symptoms']}", 
                font=("Segoe UI", 14)).pack(pady=5)
    
    # Medical recommendations section
    medical_frame = ctk.CTkFrame(details_frame)
    medical_frame.pack(fill="x", pady=10)
    
    ctk.CTkLabel(medical_frame, text="Medical Recommendations", 
                font=("Segoe UI", 16, "bold")).pack(pady=5)
    
    recommendations = f"""Disease Stage: {result['disease_stage']}
Suggested Doctor: {result['doctor']}
Precautions: {result['precaution']}
Treatment: {result['treatment']}"""
    
    ctk.CTkLabel(medical_frame, text=recommendations, 
                font=("Segoe UI", 12), justify="left").pack(pady=10, padx=20)
    
    # Action buttons
    button_frame = ctk.CTkFrame(frame)
    button_frame.pack(fill="x", pady=20)
    
    # Download individual report button
    def download_individual():
        generate_individual_pdf_report(result)
    
    ctk.CTkButton(button_frame, text="Download Patient Report", command=download_individual,
                 height=45, width=200, fg_color="#3b82f6").pack(side="left", padx=10)
    
    # Download all reports button
    def download_all():
        generate_pdf_report(all_results)
    
    ctk.CTkButton(button_frame, text="Download All Reports", command=download_all,
                 height=45, width=200, fg_color="#8b5cf6").pack(side="left", padx=10)
    
    
def show_patient_details(patient_data):
    """Show detailed view for a single patient"""
    clear_content()
    
    frame = ctk.CTkFrame(content)
    frame.pack(fill="both", expand=True, padx=40, pady=40)
    
    # Back button
    def go_back():
        test_model()
    
    ctk.CTkButton(frame, text="Back to All Patients", command=go_back,
                 height=35, width=150).pack(pady=10, anchor="w")
    
    # Patient header
    header_color = "#10b981" if patient_data['final_result'] == "Normal" else "#ef4444"
    header_frame = ctk.CTkFrame(frame, fg_color=header_color)
    header_frame.pack(fill="x", pady=20)
    
    header_text = f"Patient {patient_data['patient_id']} - {patient_data['final_result']}"
    header_label = ctk.CTkLabel(header_frame, text=header_text, 
                                  font=("Segoe UI", 20, "bold"), text_color="white")
    header_label.pack(pady=15)
    
    # Detailed information cards
    info_frame = ctk.CTkFrame(frame)
    info_frame.pack(fill="both", expand=True, pady=20)
    
    # Blood test card
    blood_card = ctk.CTkFrame(info_frame)
    blood_card.pack(fill="x", pady=10, padx=20)
    
    ctk.CTkLabel(blood_card, text="Blood Test Analysis", 
                font=("Segoe UI", 16, "bold")).pack(pady=10)
    ctk.CTkLabel(blood_card, text=f"Result: {patient_data['blood_test']}", 
                font=("Segoe UI", 14)).pack(pady=5)
    
    # Symptoms card
    symptom_card = ctk.CTkFrame(info_frame)
    symptom_card.pack(fill="x", pady=10, padx=20)
    
    ctk.CTkLabel(symptom_card, text="Symptom Analysis", 
                font=("Segoe UI", 16, "bold")).pack(pady=10)
    ctk.CTkLabel(symptom_card, text=f"Risk Level: {patient_data['symptoms']}", 
                font=("Segoe UI", 14)).pack(pady=5)
    
    # Medical recommendations card
    medical_card = ctk.CTkFrame(info_frame)
    medical_card.pack(fill="x", pady=10, padx=20)
    
    ctk.CTkLabel(medical_card, text="Medical Recommendations", 
                font=("Segoe UI", 16, "bold")).pack(pady=10)
    
    recommendations = f"""Disease Stage: {patient_data['disease_stage']}
Suggested Doctor: {patient_data['doctor']}
Precautions: {patient_data['precaution']}
Treatment: {patient_data['treatment']}"""
    
    ctk.CTkLabel(medical_card, text=recommendations, 
                font=("Segoe UI", 12), justify="left").pack(pady=10, padx=20)
    
    # Download button
    def download_report():
        generate_individual_pdf_report(patient_data)
    
    ctk.CTkButton(frame, text="Download Patient Report", command=download_report,
                 height=45, width=200, fg_color="#3b82f6").pack(pady=20)

# ================= PDF REPORT GENERATION =================
def generate_pdf_report(results):
    try:
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"thyroid_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        if not filename:
            return
        
        # Create PDF with basic settings
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        story.append(Paragraph("Thyroid Disease Detection Report", styles['Title']))
        story.append(Spacer(1, 20))
        
        # Report date
        story.append(Paragraph(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Summary
        normal_count = len([r for r in results if r["final_result"] == "Normal"])
        disease_count = len([r for r in results if r["final_result"] == "Disease Detected"])
        
        story.append(Paragraph("Summary", styles['Heading2']))
        story.append(Paragraph(f"Total Patients: {len(results)}", styles['Normal']))
        story.append(Paragraph(f"Normal Cases: {normal_count}", styles['Normal']))
        story.append(Paragraph(f"Disease Cases: {disease_count}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Detailed results
        story.append(Paragraph("Detailed Analysis Results", styles['Heading2']))
        
        # Create table
        table_data = [["Patient ID", "Blood Test", "Symptoms", "Final Result", "Stage", "Doctor", "Treatment"]]
        
        for result in results:
            table_data.append([
                str(result['patient_id']),
                result['blood_test'],
                result['symptoms'],
                result['final_result'],
                result['disease_stage'],
                result['doctor'],
                result['treatment']
            ])
        
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Footer
        story.append(Paragraph("This report was generated by the Thyroid Disease Detection System.", styles['Normal']))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Please consult with a healthcare professional for medical advice.", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        messagebox.showinfo("Success", f"PDF report saved to: {filename}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")

def generate_individual_pdf_report(patient_data):
    """Generate PDF report for a single patient"""
    try:
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"patient_{patient_data['patient_id']}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        if not filename:
            return
        
        # Create PDF with basic settings
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        story.append(Paragraph(f"Patient {patient_data['patient_id']} - Thyroid Analysis Report", styles['Title']))
        story.append(Spacer(1, 20))
        
        # Report date
        story.append(Paragraph(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Final Result
        story.append(Paragraph("Final Result", styles['Heading2']))
        story.append(Paragraph(f"{patient_data['final_result']}", styles['Heading3']))
        story.append(Spacer(1, 20))
        
        # Analysis Details
        story.append(Paragraph("Analysis Details", styles['Heading2']))
        
        # Create table for analysis results
        table_data = [
            ["Analysis Type", "Result", "Details"],
            ["Blood Test", patient_data['blood_test'], "TSH, T3, T4 levels analysis"],
            ["Symptom Analysis", patient_data['symptoms'], "Risk assessment based on symptoms"],
            ["Disease Stage", patient_data['disease_stage'], "Classification based on combined analysis"]
        ]
        
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Medical Recommendations
        story.append(Paragraph("Medical Recommendations", styles['Heading2']))
        
        recommendations = f"""Suggested Doctor: {patient_data['doctor']}
Precautions: {patient_data['precaution']}
Treatment: {patient_data['treatment']}"""
        
        story.append(Paragraph(recommendations, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Footer
        story.append(Paragraph("This report was generated by the Thyroid Disease Detection System.", styles['Normal']))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Please consult with a healthcare professional for medical advice.", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        messagebox.showinfo("Success", f"Patient report saved to: {filename}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")

# ================= ENHANCED DATA VISUALIZATION =================
def show_data_visualization_matplotlib():
    if not os.path.exists("test_clean.csv"):
        messagebox.showerror("Error", "No dataset found! Preprocess data first.")
        return

    clear_content()

    df = pd.read_csv("test_clean.csv")

    # Make predictions if model exists
    if os.path.exists("thyroid_model.joblib") and os.path.exists("scaler.joblib"):
        model = joblib.load("thyroid_model.joblib")
        scaler = joblib.load("scaler.joblib")
        X = df.drop("Label", axis=1)
        X_scaled = scaler.transform(X)
        df["Predicted"] = model.predict(X_scaled)
        df["ThyroidStage"] = df["Predicted"].apply(lambda x: "Stage I" if x==0 else "Stage II")
    else:
        df["Predicted"] = df["Label"]
        df["ThyroidStage"] = df["Predicted"].apply(lambda x: "Stage I" if x==0 else "Stage II")

    # Create enhanced visualization
    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    fig.tight_layout(pad=5.0)

    # 1. Thyroid Stage Count with better colors
    df["ThyroidStage"].value_counts().plot(kind="bar", ax=axes[0,0], 
                                          color=['#10b981', '#ef4444'], title="Thyroid Stage Count")

    # 2. Age distribution by Stage with better styling
    df[df["ThyroidStage"]=="Stage I"]["Age"].plot(kind="hist", bins=15, alpha=0.7, 
                                                  ax=axes[0,1], label="Stage I", color='#10b981')
    df[df["ThyroidStage"]=="Stage II"]["Age"].plot(kind="hist", bins=15, alpha=0.7, 
                                                   ax=axes[0,1], label="Stage II", color='#ef4444')
    axes[0,1].set_title("Age Distribution by Stage")
    axes[0,1].legend()

    # 3. TSH Levels with enhanced styling
    df.boxplot(column="TSH", by="ThyroidStage", ax=axes[1,0])
    axes[1,0].set_title("TSH Levels by Stage")
    axes[1,0].set_xlabel("")

    # 4. T3 Levels
    df.boxplot(column="T3", by="ThyroidStage", ax=axes[1,1])
    axes[1,1].set_title("T3 Levels by Stage")
    axes[1,1].set_xlabel("")

    # 5. T4 Levels
    df.boxplot(column="T4", by="ThyroidStage", ax=axes[2,0])
    axes[2,0].set_title("T4 Levels by Stage")
    axes[2,0].set_xlabel("")

    # 6. BMI vs Age with better colors
    colors_map = {0: '#10b981', 1: '#ef4444'}
    scatter_colors = [colors_map[p] for p in df["Predicted"]]
    axes[2,1].scatter(df["BMI"], df["Age"], c=scatter_colors, alpha=0.7)
    axes[2,1].set_title("BMI vs Age by Stage")
    axes[2,1].set_xlabel("BMI")
    axes[2,1].set_ylabel("Age")

    # Embed in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=content)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# ================= SIDEBAR WITH ENHANCED UI =================
def menu_button(text, command, icon="", color=None):
    button = ctk.CTkButton(sidebar, text=f"{icon} {text}", command=command, height=45)
    if color:
        button.configure(fg_color=color)
    return button

def load_next_model():
    subprocess.call(["python", "GUI_Master_old.py"])

# Enhanced sidebar buttons with better colors and icons
menu_button("Patient Entry", patient_entry, "patient_entry", "#10b981").pack(pady=10, fill="x", padx=20)
menu_button("Display Data", display_data, "display_data", "#3b82f6").pack(pady=10, fill="x", padx=20)
menu_button("Preprocess Data", preprocess_data, "preprocess", "#f59e0b").pack(pady=10, fill="x", padx=20)
menu_button("Train SVM", train_svm, "", "#8b5cf6").pack(pady=10, fill="x", padx=20)
menu_button("Test & Report", test_model, "", "#ef4444").pack(pady=10, fill="x", padx=20)
menu_button("Data Visualization", show_data_visualization_matplotlib, "visualization", "#06b6d4").pack(pady=10, fill="x", padx=20)
menu_button("Next Model", load_next_model, "next", "#64748b").pack(pady=10, fill="x", padx=20)
menu_button("Exit", root.destroy, "exit", "#dc2626").pack(pady=30, fill="x", padx=20)

root.mainloop()
