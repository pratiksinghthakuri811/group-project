import tkinter as tk
from PIL import Image, ImageTk
from player_page import open_player_page
from team_page import team_management_page


root = tk.Tk()
root.title("Soccer Manager Pro")
root.geometry("1100x700")
root.configure(bg="#2C3E50")

# --- HEADER SECTION ---
header_frame = tk.Frame(root, bg="#34495E", height=150)
header_frame.pack(fill="x", side="top")

title_label = tk.Label(header_frame,text="⚽ SOCCER MANAGER PRO",font=("Helvetica", 32, "bold"),fg="#ECF0F1",bg="#3498DB")
title_label.pack(pady=40)


# --- BUTTON LIST ---
btn_player = tk.Button(root, text="Player Management",width=25, height=2, font=("Arial", 12),bg="#3498DB", fg="white",command=lambda: open_player_page(root))
btn_player.pack(pady=20)

btn_team = tk.Button(root, text="Team Management", width=25, height=2,font=("Arial", 12), bg="#3498DB", fg="white", command=lambda: team_management_page())
btn_team.pack(pady=20)

btn_match = tk.Button(root, text="Match Management", width=25, height=2,font=("Arial", 12), bg="#3498DB", fg="white")
btn_match.pack(pady=20)

btn_tournament = tk.Button(root, text="Tournament Management", width=25, height=2,font=("Arial", 12), bg="#3498DB", fg="white")
btn_tournament.pack(pady=20)

root.mainloop()