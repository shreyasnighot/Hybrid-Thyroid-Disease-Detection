import customtkinter as ctk
from tkinter import messagebox
import sqlite3

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Create Account")
root.geometry("1000x650")
#root.resizable(False, False)

# ================= LEFT PANEL =================
left_frame = ctk.CTkFrame(root, width=450, height=650, fg_color="#1E3A8A")
left_frame.pack(side="left", fill="both")

ctk.CTkLabel(
    left_frame,
    text="Join Us Today!",
    font=("Arial", 32, "bold"),
    text_color="white"
).place(relx=0.5, rely=0.4, anchor="center")

ctk.CTkLabel(
    left_frame,
    text="Create your admin account\nAdmin Evaluation System",
    font=("Arial", 16),
    text_color="white"
).place(relx=0.5, rely=0.5, anchor="center")

# ================= RIGHT PANEL =================
right_frame = ctk.CTkFrame(root, width=550, height=650, fg_color="#F8FAFC")
right_frame.pack(side="right", fill="both", expand=True)

card = ctk.CTkFrame(right_frame, width=450, height=580, corner_radius=20)
card.place(relx=0.5, rely=0.5, anchor="center")

ctk.CTkLabel(
    card,
    text="Create Account",
    font=("Arial", 26, "bold")
).pack(pady=20)

# ================= Variables =================
fullname = ctk.StringVar()
username = ctk.StringVar()
email = ctk.StringVar()
phone = ctk.StringVar()
age = ctk.StringVar()
password = ctk.StringVar()
confirm_password = ctk.StringVar()

# ================= Modern Field Function =================
def create_field(parent, label_text, variable, show=""):
    field_frame = ctk.CTkFrame(parent, fg_color="transparent")
    field_frame.pack(pady=6, padx=40, fill="x")

    label = ctk.CTkLabel(
        field_frame,
        text=label_text,
        font=("Arial", 14, "bold"),
        anchor="w"
    )
    label.pack(fill="x")

    entry = ctk.CTkEntry(
        field_frame,
        textvariable=variable,
        width=350,
        height=40,
        corner_radius=10,
        show=show
    )
    entry.pack(pady=5, fill="x")

# ================= Fields =================
create_field(card, "Full Name", fullname)
create_field(card, "Username", username)
create_field(card, "Email Address", email)
create_field(card, "Phone Number", phone)
create_field(card, "Age", age)
create_field(card, "Password", password, show="*")
create_field(card, "Confirm Password", confirm_password, show="*")

# ================= Register Function =================
def register():
    if (not fullname.get() or not username.get() or not email.get()
        or not phone.get() or not age.get()
        or not password.get() or not confirm_password.get()):
        messagebox.showerror("Error", "All fields are required!")
        return

    if password.get() != confirm_password.get():
        messagebox.showerror("Error", "Passwords do not match!")
        return

    with sqlite3.connect('evaluation.db') as db:
        c = db.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS admin_registration (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT,
                username TEXT UNIQUE,
                email TEXT,
                phoneno TEXT,
                age INTEGER,
                password TEXT
            )
        """)

        try:
            c.execute("""
                INSERT INTO admin_registration
                (fullname, username, email, phoneno, age, password)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                fullname.get(),
                username.get(),
                email.get(),
                phone.get(),
                age.get(),
                password.get()
            ))
            db.commit()
            messagebox.showinfo("Success", "Registration Successful!")
            root.destroy()
            import login

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")

# ================= Buttons =================
ctk.CTkButton(
    card,
    text="Create Account",
    command=register,
    width=350,
    height=45,
    corner_radius=12,
    fg_color="#2563EB",
    hover_color="#1D4ED8"
).pack(pady=15)

def back_to_login():
    root.destroy()
    import login

ctk.CTkButton(
    card,
    text="Back to Login",
    command=back_to_login,
    width=350,
    height=40,
    corner_radius=12,
    fg_color="#10B981",
    hover_color="#059669"
).pack(pady=5)

root.mainloop()
