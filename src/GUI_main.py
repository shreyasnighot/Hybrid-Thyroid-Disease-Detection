import customtkinter as ctk
from tkinter import messagebox
from subprocess import call

# ================= THEME =================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Thyroid Detection Using ML")

# Fullscreen
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")
#root.resizable(False, False)

# ================= BACKGROUND =================
main_bg = ctk.CTkFrame(root, fg_color="#0f172a")  # modern navy
main_bg.pack(fill="both", expand=True)

# ================= HERO SECTION (LEFT SIDE) =================
hero_frame = ctk.CTkFrame(main_bg, fg_color="transparent")
hero_frame.place(relx=0.25, rely=0.5, anchor="center")

title = ctk.CTkLabel(
    hero_frame,
    text="Thyroid Detection\nUsing Machine Learning",
    font=ctk.CTkFont("Segoe UI", 50, weight="bold"),
    text_color="white",
    justify="left"
)
title.pack(anchor="w")

subtitle = ctk.CTkLabel(
    hero_frame,
    text="AI-powered healthcare system for early\nthyroid disease diagnosis and prediction.",
    font=ctk.CTkFont("Segoe UI", 20),
    text_color="#94a3b8",
    justify="left"
)
subtitle.pack(pady=20, anchor="w")

# ================= BUTTON ACTIONS =================
def reg():
    call(["python", "registration.py"])

def log():
    call(["python", "Login.py"])

def next_page():
    call(["python", "main.py"])

def exit_app():
    root.destroy()

def show_info():
    messagebox.showinfo(
        "System Info",
        "Thyroid Disease Detection using ML\n\n"
        "Algorithms: SVM, Random Forest, Decision Tree\n"
        "Parameters: TSH, T3, T4 levels\n\n"
        "Designed for intelligent healthcare support."
    )

# ================= GLASS CARD (RIGHT SIDE) =================
card = ctk.CTkFrame(
    main_bg,
    width=500,
    height=520,
    corner_radius=30,
    fg_color="#1e293b",
    border_width=1,
    border_color="#334155"
)
card.place(relx=0.75, rely=0.5, anchor="center")

ctk.CTkLabel(
    card,
    text="Get Started",
    font=ctk.CTkFont("Segoe UI", 28, weight="bold"),
    text_color="white"
).pack(pady=30)

btn_style = {
    "corner_radius": 20,
    "height": 55,
    "width": 320,
    "font": ctk.CTkFont("Segoe UI", 18, weight="bold"),
    "text_color": "white"
}

ctk.CTkButton(
    card,
    text="🔐 Login",
    command=log,
    fg_color="#2563eb",
    hover_color="#1d4ed8",
    **btn_style
).pack(pady=15)

ctk.CTkButton(
    card,
    text="📝 Register",
    command=reg,
    fg_color="#10b981",
    hover_color="#059669",
    **btn_style
).pack(pady=15)

ctk.CTkButton(
    card,
    text="ℹ️ About System",
    command=show_info,
    fg_color="#8b5cf6",
    hover_color="#7c3aed",
    **btn_style
).pack(pady=15)

# ctk.CTkButton(
#     card,
#     text="➡️ Continue",
#     command=next_page,
#     fg_color="#06b6d4",
#     hover_color="#0891b2",
#     **btn_style
# ).pack(pady=15)

ctk.CTkButton(
    card,
    text="❌ Exit",
    command=exit_app,
    fg_color="#ef4444",
    hover_color="#dc2626",
    **btn_style
).pack(pady=15)

# ================= FOOTER =================
footer = ctk.CTkLabel(
    main_bg,
    text="2026 Thyroid ML System | Designed with Team",
    font=ctk.CTkFont("Segoe UI", 14),
    text_color="#64748b"
)
footer.place(relx=0.5, rely=0.96, anchor="center")

root.mainloop()
