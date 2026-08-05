import tkinter as tk
from subprocess import call
from tkvideo import tkvideo

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Online Spread Terrorism Using Web Data Mining")

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"{w}x{h}+0+0")
root.resizable(False, False)

# ================= VIDEO BACKGROUND =================
video_label = tk.Label(root)
video_label.place(x=0, y=0, relwidth=1, relheight=1)

player = tkvideo("w.mp4", video_label, loop=1, size=(w, h))
player.play()

# ================= GRADIENT OVERLAY =================
overlay = tk.Canvas(root, width=w, height=h, highlightthickness=0)
overlay.place(x=0, y=0)

# Create vertical gradient
for i in range(h):
    r = int(10 + (30 - 10) * (i / h))
    g = int(10 + (30 - 10) * (i / h))
    b = int(20 + (60 - 20) * (i / h))
    color = f"#{r:02x}{g:02x}{b:02x}"
    overlay.create_line(0, i, w, i, fill=color)

# ================= GLASS CARD =================
card = tk.Frame(root, bg="#111827")
card.place(relx=0.5, rely=0.5, anchor="center", width=700, height=400)

# Slight transparency illusion
card.config(highlightbackground="#374151", highlightthickness=1)

# ================= TITLE =================
title = tk.Label(
    card,
    text="ONLINE SPREAD TERRORISM\nUSING WEB DATA MINING",
    font=("Segoe UI", 28, "bold"),
    fg="white",
    bg="#111827",
    justify="center"
)
title.pack(pady=40)

subtitle = tk.Label(
    card,
    text="AI Powered Monitoring & Threat Detection System",
    font=("Segoe UI", 14),
    fg="#9ca3af",
    bg="#111827"
)
subtitle.pack(pady=10)

# ================= BUTTON FUNCTION =================
def start_app():
    call(["python", "GUI_main.py"])

# ================= MODERN BUTTON =================
def on_enter(e):
    start_btn.config(bg="#2563eb")

def on_leave(e):
    start_btn.config(bg="#3b82f6")

start_btn = tk.Button(
    card,
    text="GET STARTED",
    command=start_app,
    font=("Segoe UI", 14, "bold"),
    bg="#3b82f6",
    fg="white",
    activebackground="#1e40af",
    activeforeground="white",
    bd=0,
    padx=40,
    pady=12,
    cursor="hand2"
)
start_btn.pack(pady=40)

start_btn.bind("<Enter>", on_enter)
start_btn.bind("<Leave>", on_leave)

# ================= FOOTER =================
footer = tk.Label(
    root,
    text="© 2026 Web Data Mining Security System",
    font=("Segoe UI", 11),
    fg="#d1d5db",
    bg="#0f172a"
)
footer.place(relx=0.5, rely=0.96, anchor="center")

root.mainloop()
