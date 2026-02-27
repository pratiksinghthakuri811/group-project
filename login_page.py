import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from soccer import open_dashboard
import sqlite3

# ----------------- DATABASE SETUP -----------------
def create_user_table():
    conn = sqlite3.connect("soccer.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()


# ----------------- THEME COLORS -----------------
WHITE = "#FFFFFF"
TEXT_DIM = "#E0E0E0"
BTN_COLOR = "#2C3E50"
ACCENT_COLOR = "#3498DB"  # Blue for "Create Account"

# ----------------- LOGIN PAGE -----------------
def open_login_page(root):
    # Only withdraw root if it's currently visible (first launch, not after logout)
    try:
        if root.state() != "withdrawn":
            root.withdraw()
    except:
        pass
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.state("zoomed")  # Fullscreen

    # --- Canvas Setup ---
    canvas = tk.Canvas(login_window, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    bg_photo = None
    original_image = None

    try:
        original_image = Image.open("football.png")
    except:
        canvas.config(bg="#1a1a1a")

    # ----------------- LOGIC FUNCTIONS -----------------
    def handle_login():
        username = e1.get()
        password = e2.get()

        conn = sqlite3.connect("soccer.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            login_window.destroy()
            open_dashboard(root)
        else:
            canvas.itemconfig(status_text, text="Invalid credentials", fill="#FF6B6B")

    def open_signup():
        signup_window = tk.Toplevel(login_window)
        signup_window.title("Create Account")
        signup_window.geometry("480x560")
        signup_window.resizable(False, False)
        signup_window.configure(bg="#1a1a2e")

        # Center the window on screen
        signup_window.update_idletasks()
        x = (signup_window.winfo_screenwidth() // 2) - 240
        y = (signup_window.winfo_screenheight() // 2) - 280
        signup_window.geometry(f"480x560+{x}+{y}")

        # ── Header banner ──
        header = tk.Frame(signup_window, bg="#3498DB", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="⚽", font=("Arial", 28), bg="#3498DB", fg="white").pack(pady=(12, 0))
        tk.Label(header, text="Create Your Account", font=("Arial", 15, "bold"),
                 bg="#3498DB", fg="white").pack()

        # ── Card body ──
        card = tk.Frame(signup_window, bg="#16213e", padx=40, pady=30)
        card.pack(fill="both", expand=True, padx=25, pady=20)

        tk.Label(card, text="Join the Soccer Management System",
                 font=("Arial", 10), bg="#16213e", fg="#a0aec0").pack(pady=(0, 20))

        # Error/success message label
        msg_var = tk.StringVar()
        msg_label = tk.Label(card, textvariable=msg_var, font=("Arial", 9, "italic"),
                             bg="#16213e", fg="#FF6B6B", wraplength=360)
        msg_label.pack()

        # ── Username field ──
        tk.Label(card, text="USERNAME", font=("Arial", 9, "bold"),
                 bg="#16213e", fg="#a0aec0", anchor="w").pack(fill="x", pady=(10, 3))
        user_frame = tk.Frame(card, bg="#2d3748", pady=2)
        user_frame.pack(fill="x")
        tk.Label(user_frame, text="👤", font=("Arial", 12), bg="#2d3748", fg="#a0aec0").pack(side="left", padx=8)
        new_user = tk.Entry(user_frame, font=("Arial", 13), bg="#2d3748", fg="white",
                            insertbackground="white", relief="flat", bd=0)
        new_user.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))

        # ── Password field ──
        tk.Label(card, text="PASSWORD", font=("Arial", 9, "bold"),
                 bg="#16213e", fg="#a0aec0", anchor="w").pack(fill="x", pady=(15, 3))
        pass_frame = tk.Frame(card, bg="#2d3748", pady=2)
        pass_frame.pack(fill="x")
        tk.Label(pass_frame, text="🔒", font=("Arial", 12), bg="#2d3748", fg="#a0aec0").pack(side="left", padx=8)
        new_pass = tk.Entry(pass_frame, font=("Arial", 13), bg="#2d3748", fg="white",
                            insertbackground="white", relief="flat", bd=0, show="●")
        new_pass.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))

        # ── Confirm Password field ──
        tk.Label(card, text="CONFIRM PASSWORD", font=("Arial", 9, "bold"),
                 bg="#16213e", fg="#a0aec0", anchor="w").pack(fill="x", pady=(15, 3))
        conf_frame = tk.Frame(card, bg="#2d3748", pady=2)
        conf_frame.pack(fill="x")
        tk.Label(conf_frame, text="🔒", font=("Arial", 12), bg="#2d3748", fg="#a0aec0").pack(side="left", padx=8)
        conf_pass = tk.Entry(conf_frame, font=("Arial", 13), bg="#2d3748", fg="white",
                             insertbackground="white", relief="flat", bd=0, show="●")
        conf_pass.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))

        def register():
            uname = new_user.get().strip()
            pwd   = new_pass.get()
            cpwd  = conf_pass.get()

            if not uname or not pwd:
                msg_var.set("⚠ Username and password cannot be empty.")
                msg_label.config(fg="#FF6B6B")
                return
            if pwd != cpwd:
                msg_var.set("⚠ Passwords do not match.")
                msg_label.config(fg="#FF6B6B")
                return
            if len(pwd) < 4:
                msg_var.set("⚠ Password must be at least 4 characters.")
                msg_label.config(fg="#FF6B6B")
                return

            conn = sqlite3.connect("soccer.db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (uname, pwd))
                conn.commit()
                msg_var.set("✅ Account created! You can now log in.")
                msg_label.config(fg="#48BB78")
                signup_window.after(1500, signup_window.destroy)
            except sqlite3.IntegrityError:
                msg_var.set("⚠ Username already taken. Try another.")
                msg_label.config(fg="#FF6B6B")
            finally:
                conn.close()

        # ── Register Button ──
        reg_btn = tk.Button(card, text="CREATE ACCOUNT", bg="#3498DB", fg="white",
                            font=("Arial", 12, "bold"), relief="flat", pady=12,
                            activebackground="#2980b9", activeforeground="white",
                            cursor="hand2", command=register)
        reg_btn.pack(fill="x", pady=(25, 0))

        # ── Cancel link ──
        tk.Button(card, text="Cancel", bg="#16213e", fg="#a0aec0",
                  font=("Arial", 9), relief="flat", cursor="hand2",
                  activebackground="#16213e", activeforeground="white",
                  command=signup_window.destroy).pack(pady=(10, 0))

        new_user.focus_set()

    # ----------------- UI RESIZE & POSITIONING -----------------
    def resize_content(event):
        nonlocal bg_photo
        w, h = event.width, event.height

        # Background
        if original_image:
            resized = original_image.resize((w, h))
            overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Semi-transparent box
            box_w, box_h = 450, 550
            shape = [(w//2 - box_w//2, h//2 - box_h//2), (w//2 + box_w//2, h//2 + box_h//2)]
            draw.rounded_rectangle(shape, radius=20, fill=(0, 0, 0, 140))
            
            combined = Image.alpha_composite(resized.convert('RGBA'), overlay)
            bg_photo = ImageTk.PhotoImage(combined)
            
            canvas.delete("bg")
            canvas.create_image(0, 0, anchor="nw", image=bg_photo, tags="bg")
            canvas.tag_lower("bg")

        update_form_positions(w, h)

    def update_form_positions(w, h):
        global e1, e2, status_text
        canvas.delete("form")
        cx, cy = w // 2, h // 2

        # Title & Subtitle
        canvas.create_text(cx, cy - 220, text="Welcome", font=("Arial", 28, "bold"), fill=WHITE, tags="form")
        canvas.create_text(cx, cy - 180, text="Sign in to your account to continue", font=("Arial", 10), fill=TEXT_DIM, tags="form")

        # Status/Error Message
        status_text = canvas.create_text(cx, cy - 150, text="", font=("Arial", 10, "italic"), fill=WHITE, tags="form")

        # Labels
        canvas.create_text(cx - 155, cy - 120, text="Username", font=("Arial", 11, "bold"), fill=WHITE, anchor="w", tags="form")
        canvas.create_text(cx - 155, cy - 20, text="Password", font=("Arial", 11, "bold"), fill=WHITE, anchor="w", tags="form")

        # Entry Fields
        e1 = tk.Entry(login_window, font=("Arial", 14), width=28, bg="#333333", fg=WHITE, insertbackground=WHITE, relief="flat")
        canvas.create_window(cx, cy - 80, window=e1, tags="form")

        e2 = tk.Entry(login_window, font=("Arial", 14), width=28, bg="#333333", fg=WHITE, insertbackground=WHITE, relief="flat", show="*")
        canvas.create_window(cx, cy + 20, window=e2, tags="form")

        # Login Button
        btn_login = tk.Button(login_window, text="LOG IN", bg=BTN_COLOR, fg=WHITE, font=("Arial", 12, "bold"), width=22, pady=8, relief="flat", command=handle_login)
        canvas.create_window(cx, cy + 110, window=btn_login, tags="form")

        # Create Account Section
        canvas.create_text(cx - 5, cy + 180, text="Don't have an account?", font=("Arial", 10), fill=WHITE, tags="form")
        btn_create = tk.Button(login_window, text="CREATE NEW ACCOUNT", bg="#1e272e", fg=ACCENT_COLOR, font=("Arial", 10, "bold"), width=25, relief="flat", command=open_signup)
        canvas.create_window(cx, cy + 230, window=btn_create, tags="form")

    canvas.bind("<Configure>", resize_content)

    # Make sure table exists
    create_user_table()