import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from player_page import open_player_page
from team_page import team_management_page
from match_page import open_match_management

def open_dashboard(root):
    dashboard = tk.Toplevel(root)
    dashboard.state("zoomed")   # Fullscreen
    dashboard.title("Soccer Management System")
    dashboard.configure(bg="#2C3E50")

    bg_image_original = Image.open("football.png")

    bg_label = tk.Label(dashboard)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # --- Global reference for background photo ---
    dashboard.bg_photo = None

    def resize_background(event):
        w, h = event.width, event.height
        if w < 2 or h < 2:
            return  # skip tiny initial size

        resized = bg_image_original.resize((w, h))
        dashboard.bg_photo = ImageTk.PhotoImage(resized)  # keep reference
        bg_label.config(image=dashboard.bg_photo)

    dashboard.bind("<Configure>", resize_background)

    # --- Dashboard Title ---
    title_label = tk.Label(dashboard,
                           text="Soccer Management System",
                           font=("Helvetica", 32, "bold"),
                           fg="#ECF0F1",
                           bg="#3498DB")
    title_label.pack(pady=40)

    # --- Navigation Functions ---
    def navigate(func):
        func(dashboard)  # Open sub-page without hiding dashboard

    def logout():
        if messagebox.askyesno("Logout", "Are you sure?"):
            dashboard.destroy()
            from login_page import open_login_page
            open_login_page(root)

    # --- Buttons ---
    btn_logout = tk.Button(dashboard, text="Logout ⏻", bg="#E74C3C",
                           fg="white", font=("Arial", 10, "bold"), command=logout)
    btn_logout.place(relx=1.0, x=-20, y=20, anchor="ne")

    btn_player = tk.Button(dashboard, text="Player Management", width=25, height=2,
                           font=("Arial", 12), bg="#0B293D", fg="white",
                           command=lambda: navigate(open_player_page))
    btn_player.pack(pady=20)

    btn_team = tk.Button(dashboard, text="Team Management", width=25, height=2,
                         font=("Arial", 12), bg="#0B293D", fg="white",
                         command=lambda: navigate(lambda r: team_management_page(r)))
    btn_team.pack(pady=20)

    btn_match = tk.Button(dashboard, text="Match Management", width=25, height=2,
                          font=("Arial", 12), bg="#0B293D", fg="white",
                          command=lambda: navigate(open_match_management))
    btn_match.pack(pady=20)