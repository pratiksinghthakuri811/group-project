import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
from player_page import open_player_page

# Create main window
root = tk.Tk()
root.title("Manager Dashboard")
root.geometry("500x450")
root.config(bg="#f0f0f0")

image = Image.open("image.png")
image = image.resize((500, 450))
bg_image = ImageTk.PhotoImage(image)

# Create a label for the background
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

title = tk.Label(root, text="Dashboard",font=("Arial", 22, "bold"),bg="#f0f0f0")
title.pack(pady=30)

btn_player =  tk.Button(root,text="Player Management",width=25,height=2,font=("Arial", 12),bg="#39268B",fg="white",command=lambda: open_player_page(root))
btn_player.pack(pady=10)
btn_team = tk.Button(root, text="Team Management",width=25, height=2,font=("Arial", 12), bg="#39268B", fg="white")
btn_team.pack(pady=10)

btn_match = tk.Button(root, text="Match Management",width=25, height=2,font=("Arial", 12), bg="#39268B", fg="white")
btn_match.pack(pady=10)

btn_tournament = tk.Button(root, text="Tournament Management",width=25, height=2,font=("Arial", 12), bg="#39268B", fg="white")
btn_tournament.pack(pady=10)

root.mainloop()