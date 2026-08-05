import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from subprocess import call
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Admin Login")
root.geometry("900x600")
#root.resizable(False, False)

# ================= LEFT PANEL =================
left_frame = ctk.CTkFrame(root, width=400, fg_color="#1E3A8A")
left_frame.pack(side="left", fill="both")

ctk.CTkLabel(
    left_frame,
    text="Welcome Back!",
    font=("Arial", 32, "bold"),
    text_color="white"
).place(relx=0.5, rely=0.4, anchor="center")

ctk.CTkLabel(
    left_frame,
    text="Login to continue\nAdmin Evaluation System",
    font=("Arial", 16),
    text_color="white"
).place(relx=0.5, rely=0.5, anchor="center")

# ================= RIGHT PANEL =================
right_frame = ctk.CTkFrame(root, fg_color="#F8FAFC")
right_frame.pack(side="right", fill="both", expand=True)

login_card = ctk.CTkFrame(right_frame, width=380, height=420, corner_radius=20)
login_card.place(relx=0.5, rely=0.5, anchor="center")

ctk.CTkLabel(
    login_card,
    text="Login",
    font=("Arial", 26, "bold")
).pack(pady=20)

# ================= Variables =================
username = ctk.StringVar()
password = ctk.StringVar()

# ================= Username Field =================
user_frame = ctk.CTkFrame(login_card, fg_color="transparent")
user_frame.pack(pady=10, padx=40, fill="x")

ctk.CTkLabel(
    user_frame,
    text="Username",
    font=("Arial", 14, "bold"),
    anchor="w"
).pack(fill="x")

ctk.CTkEntry(
    user_frame,
    textvariable=username,
    width=280,
    height=40,
    corner_radius=10
).pack(pady=5)

# ================= Password Field =================
pass_frame = ctk.CTkFrame(login_card, fg_color="transparent")
pass_frame.pack(pady=10, padx=40, fill="x")

ctk.CTkLabel(
    pass_frame,
    text="Password",
    font=("Arial", 14, "bold"),
    anchor="w"
).pack(fill="x")

ctk.CTkEntry(
    pass_frame,
    textvariable=password,
    show="*",
    width=280,
    height=40,
    corner_radius=10
).pack(pady=5)

# ================= LOGIN FUNCTION =================
def login():
    with sqlite3.connect('evaluation.db') as db:
        c = db.cursor()
        c.execute("SELECT * FROM admin_registration WHERE username=? AND password=?",
                  (username.get(), password.get()))
        result = c.fetchone()

        if result:
            messagebox.showinfo("Success", "Login Successful!")
            root.destroy()
            call(["python", "main (1).py"])
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

ctk.CTkButton(
    login_card,
    text="Login",
    command=login,
    width=280,
    height=45,
    corner_radius=12,
    fg_color="#2563EB",
    hover_color="#1D4ED8"
).pack(pady=15)

# ================= Forgot Password =================
def forgot_password():
    forgot_win = ctk.CTkToplevel(root)
    forgot_win.title("Reset Password")
    forgot_win.geometry("400x400")
    forgot_win.grab_set()  # Focus on this window

    ctk.CTkLabel(
        forgot_win,
        text="Reset Password",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    # Variables
    user_var = ctk.StringVar()
    new_pass = ctk.StringVar()
    confirm_pass = ctk.StringVar()

    # Username
    ctk.CTkLabel(forgot_win, text="Username", anchor="w").pack(padx=50, fill="x")
    ctk.CTkEntry(forgot_win, textvariable=user_var, width=280, height=40).pack(pady=5)

    # New Password
    ctk.CTkLabel(forgot_win, text="New Password", anchor="w").pack(padx=50, fill="x")
    ctk.CTkEntry(forgot_win, textvariable=new_pass, show="*", width=280, height=40).pack(pady=5)

    # Confirm Password
    ctk.CTkLabel(forgot_win, text="Confirm Password", anchor="w").pack(padx=50, fill="x")
    ctk.CTkEntry(forgot_win, textvariable=confirm_pass, show="*", width=280, height=40).pack(pady=5)

    # Update Function
    def update_password():
        if not user_var.get() or not new_pass.get() or not confirm_pass.get():
            messagebox.showerror("Error", "All fields are required!")
            return

        if new_pass.get() != confirm_pass.get():
            messagebox.showerror("Error", "Passwords do not match!")
            return

        with sqlite3.connect('evaluation.db') as db:
            c = db.cursor()
            c.execute("UPDATE admin_registration SET password=? WHERE username=?",
                      (new_pass.get(), user_var.get()))
            db.commit()

            if c.rowcount > 0:
                messagebox.showinfo("Success", "Password Updated Successfully!")
                forgot_win.destroy()
            else:
                messagebox.showerror("Error", "Username not found!")

    ctk.CTkButton(
        forgot_win,
        text="Update Password",
        command=update_password,
        width=280,
        height=40
    ).pack(pady=20)


ctk.CTkButton(
    login_card,
    text="Forgot Password?",
    fg_color="transparent",
    text_color="#2563EB",
    hover=False,
    command=forgot_password
).pack()

# ================= Signup =================
def go_register():
    root.destroy()
    import registration

ctk.CTkButton(
    login_card,
    text="Create New Account",
    width=280,
    height=40,
    corner_radius=12,
    fg_color="#10B981",
    hover_color="#059669",
    command=go_register
).pack(pady=15)

root.mainloop()
