import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

def open_match_management(root):
    # Check if window already exists to prevent duplicates
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel) and widget.title() == "Match Management":
            widget.lift()
            return

    # HIDE the dashboard
    root.withdraw()

    match_window = tk.Toplevel(root)
    match_window.title("Match Management")
    match_window.geometry("1100x700")
    
    conn = sqlite3.connect("soccer.db")
    cursor = conn.cursor()


    def go_back():
        match_window.destroy()
        root.deiconify() # Shows the dashboard again

    # Back Button
    back_btn = tk.Button(match_window, text="⬅ Back to Dashboard", command=go_back, bg="#95a5a6", fg="white")
    back_btn.pack(side="top", anchor="nw", padx=10, pady=10)


    # TABLES SETUP

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        opponent TEXT,
        match_date TEXT,
        venue TEXT,
        team_score INTEGER DEFAULT 0,
        opponent_score INTEGER DEFAULT 0
    )""")
    conn.commit()


    # CORE LOGIC FUNCTIONS

    def get_match_result(t1, t2):
        if t1 > t2: return "WIN"
        if t1 < t2: return "LOSS"
        return "DRAW"

    def load_matches():
        # 1. Clear the table
        for row in match_table.get_children():
            match_table.delete(row)

        # 2. Fetch data from DB
        cursor.execute("SELECT * FROM matches")
        rows = cursor.fetchall()

        # 3. Insert rows into the table
        for row in rows:
            res = get_match_result(row[4], row[5])
            display_data = list(row) + [res]
            match_table.insert("", tk.END, values=display_data)
            
        # 4. UPDATE THE WIN RATE LABEL (The Fix)
        current_rate = calculate_win_rate()
        win_rate_label.config(text=f"Season Win Rate: {current_rate}")


    def schedule_match():
        opponent = opponent_entry.get()
        date = date_entry.get()
        venue = venue_entry.get()

        if not opponent or not date:
            messagebox.showerror("Error", "Opponent and Date required")
            return

        cursor.execute("INSERT INTO matches (opponent, match_date, venue, team_score, opponent_score) VALUES (?, ?, ?, 0, 0)",
                       (opponent, date, venue))
        conn.commit()
        
        opponent_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        venue_entry.delete(0, tk.END)
        
        load_matches() 
        messagebox.showinfo("Success", "Match Scheduled")

    def calculate_win_rate():
        cursor.execute("SELECT team_score, opponent_score FROM matches")
        rows = cursor.fetchall()
        
        total_matches = len(rows)
        if total_matches == 0:
            return "0%"
... (96 lines left)