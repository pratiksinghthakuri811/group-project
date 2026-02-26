import tkinter as tk
from PIL import Image, ImageTk
from login_page import open_login_page

# --- THEME COLORS ---
WHITE = "#FFFFFF"
BTN_COLOR = "#333333"

def open_window(parent, title="New Window"):
    """
    Opens a Toplevel window and inherits fullscreen/zoomed state from parent.
    """
    new_win = tk.Toplevel(parent)
    new_win.title(title)

    # Inherit fullscreen/zoomed state
    if str(parent.state()) == "zoomed":
        new_win.state("zoomed")
    else:
        # inherit size if parent is normal
        new_win.geometry(parent.winfo_geometry())

    # Hide parent
    parent.withdraw()

    # Show parent again when closing this window
    def on_close():
        parent.deiconify()
        new_win.destroy()
    new_win.protocol("WM_DELETE_WINDOW", on_close)

    return new_win

root = tk.Tk()
root.title("Soccer Management System")
root.geometry("1100x750")

# 1. Setup the Canvas
canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# 2. Global variable for the background image to prevent garbage collection
bg_photo = None
original_image = None

try:
    original_image = Image.open("football.png")
except Exception as e:
    print(f"Error loading image: {e}")
    canvas.config(bg="#2C3E50")

# 3. Create Objects once (placeholders)
title_text = canvas.create_text(0, 0, text="Soccer Management System",
                                font=("Times New Roman", 28, "bold"), fill=WHITE, anchor="nw")

welcome_text = canvas.create_text(0, 0, text="WELCOME", 
                                  font=("Times New Roman", 60, "bold"), fill=WHITE, anchor="center")

footer_text = canvas.create_text(0, 0, text="PLEASE LOG IN TO MANAGE PLAYERS, TEAMS, AND MATCHES", 
                                 font=("Arial", 14, "bold"), fill="#BDC3C7", anchor="center")

# 4. Button Logic
def open_login():
    print("Redirecting...")

btn_login = tk.Button(root, text="Login", bg=BTN_COLOR, fg=WHITE, 
                       font=("Arial", 11, "bold"), relief="flat", padx=25, pady=8, command=lambda:  open_login_page(open_window(root, title="Login")))
login_btn_window = canvas.create_window(0, 0, anchor="ne", window=btn_login)

# 5. The Magic Function: Resize and Realignment
def resize_content(event):
    global bg_photo
    
    # Get new dimensions
    w, h = event.width, event.height
    
    # Resize background image to fill screen
    if original_image:
        resized = original_image.resize((w, h))
        bg_photo = ImageTk.PhotoImage(resized)
        canvas.delete("bg") # Remove old background
        canvas.create_image(0, 0, anchor="nw", image=bg_photo, tags="bg")
        canvas.tag_lower("bg") # Keep it behind everything

    # RE-ALIGN EVERYTHING
    # Title: Keep in top-left
    canvas.coords(title_text, 30, 30)
    
    # Welcome: Always at center
    canvas.coords(welcome_text, w // 2, h // 2 - 50)
    
    # Footer: Always near the bottom
    canvas.coords(footer_text, w // 2, h - 100)
    
    # Login Button: Always at top-right
    canvas.coords(login_btn_window, w - 30, 30)

# Bind the resize event
canvas.bind("<Configure>", resize_content)
root.mainloop()