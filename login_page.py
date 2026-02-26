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
    # Open login window via our helper (inherits fullscreen)
    root.withdraw()  # Hide the main root window
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("1100x750")

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
        signup_window.geometry("400x300")

        tk.Label(signup_window, text="Username").pack(pady=5)
        new_user = tk.Entry(signup_window)
        new_user.pack()

        tk.Label(signup_window, text="Password").pack(pady=5)
        new_pass = tk.Entry(signup_window, show="*")
        new_pass.pack()

        def register():
            conn = sqlite3.connect("soccer.db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_user.get(), new_pass.get()))
                conn.commit()
                signup_window.destroy()
            except sqlite3.IntegrityError:
                print("Username already exists!")
            conn.close()

        tk.Button(signup_window, text="Register", command=register).pack(pady=20)

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