import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from login_page import open_login_page

# ── Colour Palette ──────────────────────────────────────────
WHITE        = "#FFFFFF"
GOLD         = "#F0C040"
LIGHT_BLUE   = "#56CCF2"
BTN_BG       = "#3498DB"
BTN_HOVER    = "#2980B9"
OVERLAY_TOP  = (10, 10, 30, 210)   # deep navy, heavy top
OVERLAY_BOT  = (0, 0, 0, 160)      # softer black bottom strip

# ── Main Window ─────────────────────────────────────────────
root = tk.Tk()
root.title("Soccer Management System")
root.state("zoomed")

canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

bg_photo       = None
original_image = None
try:
    original_image = Image.open("football.png")
except Exception as e:
    print(f"Error loading image: {e}")
    canvas.config(bg="#0d1b2a")

# ── Static Canvas Elements ───────────────────────────────────
# Top navbar bar (drawn as a rectangle tag)
navbar_rect  = canvas.create_rectangle(0, 0, 0, 70, fill="#0d1b2a", outline="", tags="navbar")

# Brand / logo text  (top-left)
brand_text   = canvas.create_text(0, 0, anchor="w",
    text="⚽  SOCCER MANAGEMENT SYSTEM",
    font=("Arial", 15, "bold"), fill=GOLD, tags="ui")

# Divider line under navbar
divider_line = canvas.create_line(0, 70, 0, 70, fill=LIGHT_BLUE, width=2, tags="ui")

# Big WELCOME heading
welcome_main = canvas.create_text(0, 0, anchor="center",
    text="WELCOME", font=("Arial", 72, "bold"), fill=WHITE, tags="ui")

# Glowing subtitle line (coloured)
welcome_sub  = canvas.create_text(0, 0, anchor="center",
    text="Your All-In-One Soccer Management Platform",
    font=("Arial", 18, "italic"), fill=LIGHT_BLUE, tags="ui")

# Small description
desc_text    = canvas.create_text(0, 0, anchor="center",
    text="Manage Players  •  Build Teams  •  Track Matches",
    font=("Arial", 13), fill="#d0e8ff", tags="ui")

# Bottom footer bar
footer_rect  = canvas.create_rectangle(0, 0, 0, 0, fill="#0d1b2a", outline="", tags="footer")
footer_text  = canvas.create_text(0, 0, anchor="center",
    text="© 2025 Soccer Management System  |  Please log in to continue",
    font=("Arial", 10), fill="#7f8c8d", tags="ui")

# ── Login Button ─────────────────────────────────────────────
def safe_open_login():
    root.withdraw()
    open_login_page(root)

btn_login = tk.Button(
    root, text="  🔑  LOG IN  ", bg=BTN_BG, fg=WHITE,
    font=("Arial", 13, "bold"), relief="flat",
    padx=22, pady=10, cursor="hand2",
    activebackground=BTN_HOVER, activeforeground=WHITE,
    command=safe_open_login
)
btn_login_win = canvas.create_window(0, 0, anchor="ne", window=btn_login, tags="ui")

# Hover effects
btn_login.bind("<Enter>", lambda e: btn_login.config(bg=BTN_HOVER))
btn_login.bind("<Leave>", lambda e: btn_login.config(bg=BTN_BG))

# ── Resize / Redraw ──────────────────────────────────────────
def resize_content(event):
    global bg_photo
    w, h = event.width, event.height
    if w < 10 or h < 10:
        return

    # --- Background with gradient-style dark overlay ---
    if original_image:
        resized = original_image.resize((w, h), Image.LANCZOS).convert("RGBA")

        # Top dark band (navbar area)
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw    = ImageDraw.Draw(overlay)
        draw.rectangle([(0, 0), (w, 75)], fill=(13, 27, 42, 220))

        # Centre vignette to make text pop
        draw.rectangle([(w//2 - 520, h//2 - 160), (w//2 + 520, h//2 + 140)],
                        fill=(0, 0, 0, 90))

        # Bottom footer strip
        draw.rectangle([(0, h - 45), (w, h)], fill=(13, 27, 42, 210))

        combined = Image.alpha_composite(resized, overlay)
        bg_photo = ImageTk.PhotoImage(combined)
        canvas.delete("bg")
        canvas.create_image(0, 0, anchor="nw", image=bg_photo, tags="bg")
        canvas.tag_lower("bg")
    else:
        canvas.config(bg="#0d1b2a")

    # --- Reposition all elements ---
    cx = w // 2
    cy = h // 2

    # Navbar bar
    canvas.coords(navbar_rect, 0, 0, w, 70)

    # Brand text (left-aligned, vertically centred in navbar)
    canvas.coords(brand_text, 28, 35)

    # Divider
    canvas.coords(divider_line, 0, 70, w, 70)

    # Main heading — centre of screen, slightly above middle
    canvas.coords(welcome_main, cx, cy - 60)

    # Subtitle just below
    canvas.coords(welcome_sub, cx, cy + 30)

    # Description below subtitle
    canvas.coords(desc_text, cx, cy + 75)

    # Login button — top-right inside navbar
    canvas.coords(btn_login_win, w - 28, 35)

    # Footer bar + text
    canvas.coords(footer_rect, 0, h - 45, w, h)
    canvas.coords(footer_text, cx, h - 22)

    # Keep UI elements on top
    canvas.tag_raise("ui")
    canvas.tag_raise("navbar")
    canvas.tag_raise("footer")

canvas.bind("<Configure>", resize_content)
root.mainloop()
