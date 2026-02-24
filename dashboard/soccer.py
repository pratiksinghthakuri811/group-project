
import tkinter as tk

# Create main window
root = tk.Tk()
root.title("Soccer Management System")
root.geometry("500x450")
root.config(bg="#f0f0f0")

# Title Label
title = tk.Label(root, text="Wellcome",font=("Arial", 22, "bold"),bg="#f0f0f0")
title.pack(pady=30)

# Buttons (No Command Added)
btn_player = tk.Button(root, text="Player Management",width=25, height=2,font=("Arial", 12))
btn_player.pack(pady=10)
btn_team = tk.Button(root, text="Team Management",width=25, height=2,font=("Arial", 12))
btn_team.pack(pady=10)

btn_match = tk.Button(root, text="Match Management",width=25, height=2,font=("Arial", 12))
btn_match.pack(pady=10)

btn_tournament = tk.Button(root, text="Tournament Management",width=25, height=2,font=("Arial", 12))
btn_tournament.pack(pady=10)

root.mainloop()