import sqlite3
import tkinter as tk
from tkinter import messagebox
import os

# Try to import Pillow for background image support
try:
    from PIL import Image, ImageTk, ImageFilter
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

# ================================================================
#  DATABASE
# ================================================================
def get_conn():
    return sqlite3.connect("football.db")

def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role     TEXT NOT NULL DEFAULT 'manager'
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ================================================================
#  COLORS & FONTS  (all valid 6-digit hex)
# ================================================================
ACCENT       = "#00c853"
ACCENT_DARK  = "#009624"
WHITE        = "#ffffff"
BLACK        = "#000000"
TEXT_DIM     = "#bbbbbb"
CARD_BG      = "#111111"
INPUT_BG     = "#222222"
INPUT_BORDER = "#333333"
PAGE_BG      = "#0d1a0d"

FONT_SUB   = ("Segoe UI", 11)
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_BTN   = ("Segoe UI", 11, "bold")
FONT_SMALL = ("Segoe UI", 9)

# ================================================================
#  LOGIN APP
# ================================================================
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Soccer Management System")
        self.root.geometry("900x580")
        self.root.resizable(False, False)
        self._center()
        self._load_background()
        self._build_ui()

    def _center(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 900) // 2
        y = (self.root.winfo_screenheight() - 580) // 2
        self.root.geometry(f"900x580+{x}+{y}")

    # ── Background ──────────────────────────────────────────────
    def _load_background(self):
        self.canvas = tk.Canvas(self.root, width=900, height=580,
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        img_loaded = False

        if PILLOW_AVAILABLE:
            for name in ["background.jpg", "background.png", "bg.jpg", "bg.png"]:
                if os.path.exists(name):
                    try:
                        img = Image.open(name).resize((900, 580), Image.LANCZOS)
                        # blur slightly so text is readable
                        img = img.filter(ImageFilter.GaussianBlur(radius=2))
                        # dark overlay using Pillow (valid, no tkinter transparency needed)
                        overlay = Image.new("RGBA", (900, 580), (0, 0, 0, 140))
                        img = img.convert("RGBA")
                        img = Image.alpha_composite(img, overlay).convert("RGB")
                        self.bg_photo = ImageTk.PhotoImage(img)
                        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
                        img_loaded = True
                        print(f"✅ Background image loaded: {name}")
                        break
                    except Exception as e:
                        print(f"Could not load {name}: {e}")

        if not img_loaded:
            self._draw_gradient()

    def _draw_gradient(self):
        """Dark green gradient fallback — no image needed."""
        for i in range(580):
            ratio = i / 580
            r = int(8  + ratio * 5)
            g = int(20 + ratio * 35)
            b = int(8  + ratio * 5)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, 900, i, fill=color)

        # Subtle football field circle & lines
        self.canvas.create_oval(355, 195, 545, 385, outline="#1a3a1a", width=2)
        self.canvas.create_line(450, 80, 450, 500,  fill="#1a2a1a", width=1)
        self.canvas.create_rectangle(310, 160, 590, 420, outline="#152515", width=1)

    # ── Build UI ────────────────────────────────────────────────
    def _build_ui(self):
        # Left — Branding
        self.canvas.create_text(215, 190, text="⚽",
                                font=("Segoe UI", 68), fill=ACCENT, anchor="center")
        self.canvas.create_text(215, 285, text="Soccer",
                                font=("Segoe UI", 26, "bold"), fill=WHITE, anchor="center")
        self.canvas.create_text(215, 318, text="Management System",
                                font=("Segoe UI", 13), fill=TEXT_DIM, anchor="center")
        self.canvas.create_text(215, 348, text="🏆 Tournament & League Edition",
                                font=("Segoe UI", 10), fill=ACCENT, anchor="center")
        self.canvas.create_text(215, 400, text="Track · Manage · Win",
                                font=("Segoe UI", 9), fill="#555555", anchor="center")

        # Vertical divider
        self.canvas.create_line(420, 50, 420, 530, fill="#1e3a1e", width=1)

        # Right — Login Card
        card = tk.Frame(self.root, bg=CARD_BG, bd=0)
        card.place(x=445, y=55, width=430, height=470)

        tk.Label(card, text="Welcome Back 👋",
                 font=("Segoe UI", 17, "bold"), bg=CARD_BG, fg=WHITE).pack(pady=(22, 3))
        tk.Label(card, text="Sign in to continue",
                 font=FONT_SMALL, bg=CARD_BG, fg=TEXT_DIM).pack()

        # Green underline accent
        tk.Frame(card, bg=ACCENT, height=2, width=55).pack(pady=10)

        form = tk.Frame(card, bg=CARD_BG)
        form.pack(padx=28, fill="x")

        # ── Username ──
        self._field_label(form, "USERNAME")
        self.uf = tk.Frame(form, bg=INPUT_BG, highlightthickness=1,
                           highlightbackground=INPUT_BORDER)
        self.uf.pack(fill="x")
        tk.Label(self.uf, text="👤", bg=INPUT_BG,
                 font=("Segoe UI", 11)).pack(side="left", padx=8)
        self.e_user = tk.Entry(self.uf, bg=INPUT_BG, fg=WHITE, font=FONT_SUB,
                               relief="flat", insertbackground=WHITE, width=24)
        self.e_user.pack(side="left", ipady=9, fill="x", expand=True, padx=(0, 8))
        self.e_user.bind("<FocusIn>",  lambda e: self.uf.config(highlightbackground=ACCENT))
        self.e_user.bind("<FocusOut>", lambda e: self.uf.config(highlightbackground=INPUT_BORDER))

        # ── Password ──
        self._field_label(form, "PASSWORD", top=12)
        self.pf = tk.Frame(form, bg=INPUT_BG, highlightthickness=1,
                           highlightbackground=INPUT_BORDER)
        self.pf.pack(fill="x")
        tk.Label(self.pf, text="🔒", bg=INPUT_BG,
                 font=("Segoe UI", 11)).pack(side="left", padx=8)
        self.e_pass = tk.Entry(self.pf, bg=INPUT_BG, fg=WHITE, font=FONT_SUB,
                               relief="flat", insertbackground=WHITE,
                               show="*", width=22)
        self.e_pass.pack(side="left", ipady=9, fill="x", expand=True)
        self.e_pass.bind("<FocusIn>",  lambda e: self.pf.config(highlightbackground=ACCENT))
        self.e_pass.bind("<FocusOut>", lambda e: self.pf.config(highlightbackground=INPUT_BORDER))

        # Show/hide toggle
        self.show_pass = False
        def toggle():
            self.show_pass = not self.show_pass
            self.e_pass.config(show="" if self.show_pass else "*")
            eye.config(text="🙈" if self.show_pass else "👁")
        eye = tk.Button(self.pf, text="👁", bg=INPUT_BG, fg=TEXT_DIM,
                        relief="flat", cursor="hand2", command=toggle,
                        activebackground=INPUT_BG, activeforeground=WHITE,
                        font=("Segoe UI", 11), bd=0)
        eye.pack(side="right", padx=6)

        # ── Login Button ──
        lb = tk.Button(form, text="🔑   LOGIN", command=self._login,
                       bg=ACCENT, fg=BLACK, font=FONT_BTN,
                       relief="flat", cursor="hand2",
                       activebackground=ACCENT_DARK, activeforeground=WHITE)
        lb.pack(fill="x", ipady=10, pady=(18, 0))
        lb.bind("<Enter>", lambda e: lb.config(bg=ACCENT_DARK, fg=WHITE))
        lb.bind("<Leave>", lambda e: lb.config(bg=ACCENT, fg=BLACK))

        tk.Label(form, text="— OR —", bg=CARD_BG,
                 fg=INPUT_BORDER, font=FONT_SMALL).pack(pady=6)

        # ── Register Button ──
        rb = tk.Button(form, text="📝   CREATE ACCOUNT",
                       command=self._show_register,
                       bg=INPUT_BG, fg=WHITE, font=FONT_BTN,
                       relief="flat", cursor="hand2",
                       activebackground=INPUT_BORDER, activeforeground=WHITE,
                       highlightthickness=1, highlightbackground=INPUT_BORDER)
        rb.pack(fill="x", ipady=8)
        rb.bind("<Enter>", lambda e: rb.config(bg=INPUT_BORDER))
        rb.bind("<Leave>", lambda e: rb.config(bg=INPUT_BG))

        tk.Label(card, text="© 2025 Soccer Management System",
                 bg=CARD_BG, fg="#444444", font=("Segoe UI", 8)).pack(side="bottom", pady=8)

        self.root.bind("<Return>", lambda e: self._login())

    def _field_label(self, parent, text, top=6):
        tk.Label(parent, text=text, bg=CARD_BG, fg=TEXT_DIM,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(top, 2))

    # ── Register Popup ──────────────────────────────────────────
    def _show_register(self):
        win = tk.Toplevel(self.root)
        win.title("Create Account")
        win.geometry("400x370")
        win.configure(bg=CARD_BG)
        win.resizable(False, False)
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth()  - 400) // 2
        y = (win.winfo_screenheight() - 370) // 2
        win.geometry(f"400x370+{x}+{y}")

        tk.Label(win, text="⚽ Create Account",
                 font=("Segoe UI", 16, "bold"), bg=CARD_BG, fg=WHITE).pack(pady=(22, 4))
        tk.Label(win, text="Register as a Manager",
                 font=FONT_SMALL, bg=CARD_BG, fg=TEXT_DIM).pack()
        tk.Frame(win, bg=ACCENT, height=2, width=50).pack(pady=10)

        form = tk.Frame(win, bg=CARD_BG)
        form.pack(padx=30, fill="x")

        def make_field(label, show=None):
            tk.Label(form, text=label, bg=CARD_BG, fg=TEXT_DIM,
                     font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(8, 2))
            f = tk.Frame(form, bg=INPUT_BG, highlightthickness=1,
                         highlightbackground=INPUT_BORDER)
            f.pack(fill="x")
            e = tk.Entry(f, bg=INPUT_BG, fg=WHITE, font=FONT_SUB,
                         relief="flat", insertbackground=WHITE,
                         width=28, show=show or "")
            e.pack(ipady=9, fill="x", padx=10)
            e.bind("<FocusIn>",  lambda ev: f.config(highlightbackground=ACCENT))
            e.bind("<FocusOut>", lambda ev: f.config(highlightbackground=INPUT_BORDER))
            return e

        e_u = make_field("USERNAME")
        e_p = make_field("PASSWORD",         show="*")
        e_c = make_field("CONFIRM PASSWORD", show="*")

        def do_register():
            u = e_u.get().strip()
            p = e_p.get().strip()
            c = e_c.get().strip()
            r = "manager"
            if not u or not p or not c:
                messagebox.showwarning("Missing", "All fields are required.", parent=win)
                return
            if p != c:
                messagebox.showerror("Mismatch", "Passwords do not match!", parent=win)
                return
            try:
                conn = get_conn()
                conn.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (u, p, r)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Success",
                    f"Account '{u}' created!\nYou can now login.", parent=win)
                win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!", parent=win)
            except Exception as ex:
                messagebox.showerror("Database Error", f"Something went wrong:\n{ex}", parent=win)

        btn = tk.Button(form, text="✅   REGISTER", command=do_register,
                        bg=ACCENT, fg=BLACK, font=FONT_BTN, relief="flat",
                        cursor="hand2", activebackground=ACCENT_DARK, activeforeground=WHITE)
        btn.pack(fill="x", ipady=10, pady=(16, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_DARK, fg=WHITE))
        btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT,      fg=BLACK))

    # ── Login Logic ─────────────────────────────────────────────
    def _login(self):
        u = self.e_user.get().strip()
        p = self.e_pass.get().strip()
        if not u or not p:
            messagebox.showwarning("Missing", "Please enter username and password.")
            return
        conn = get_conn()
        row = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (u, p)
        ).fetchone()
        conn.close()
        if row:
            messagebox.showinfo("Welcome!", f"Welcome, {u}! 🎉\nRole: Manager")
            # TODO: open main dashboard here
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            self.e_pass.delete(0, "end")
            self.e_pass.focus()

# ================================================================
#  RUN
# ================================================================
if __name__ == "__main__":
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()