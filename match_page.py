import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def open_match_management(root):
    # Prevent duplicate windows
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel) and widget.title() == "Match Management":
            widget.lift()
            return

    match_window = tk.Toplevel(root)
    match_window.title("Match Management")
    match_window.state("zoomed")  # Fullscreen

    conn = sqlite3.connect("soccer.db")
    cursor = conn.cursor()

    # ---------------- Back Button ----------------
    def go_back():
        match_window.destroy()

    back_btn = tk.Button(match_window, text="⬅ Back to Dashboard", command=go_back, bg="#95a5a6", fg="white")
    back_btn.pack(side="top", anchor="nw", padx=10, pady=10)

    # ---------------- Database Table ----------------
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

    # ---------------- Schedule Frame ----------------
    schedule_frame = tk.LabelFrame(match_window, text="Schedule / Update Matches", padx=10, pady=10)
    schedule_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(schedule_frame, text="Opponent:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    opponent_entry = tk.Entry(schedule_frame)
    opponent_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(schedule_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    date_entry = tk.Entry(schedule_frame)
    date_entry.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(schedule_frame, text="Venue:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
    venue_entry = tk.Entry(schedule_frame)
    venue_entry.grid(row=0, column=5, padx=5, pady=5)

    schedule_btn = tk.Button(schedule_frame, text="Schedule Match", bg="#27ae60", fg="white",
                             command=lambda: schedule_match())
    schedule_btn.grid(row=0, column=6, padx=10)

    # ---------------- Score / Remove Section ----------------
    tk.Label(schedule_frame, text="Team Score:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    team_score_entry = tk.Entry(schedule_frame, width=5)
    team_score_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(schedule_frame, text="Opponent Score:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    opponent_score_entry = tk.Entry(schedule_frame, width=5)
    opponent_score_entry.grid(row=1, column=3, padx=5, pady=5)

    update_btn = tk.Button(schedule_frame, text="Update Scores", bg="#2980b9", fg="white",
                           command=lambda: update_scores())
    update_btn.grid(row=1, column=4, padx=10)

    remove_btn = tk.Button(schedule_frame, text="Remove Match", bg="#c0392b", fg="white",
                           command=lambda: remove_match())
    remove_btn.grid(row=1, column=5, padx=10)

    # ---------------- Win Rate Label ----------------
    win_rate_label = tk.Label(match_window, text="Season Win Rate: 0%", font=("Arial", 14, "bold"))
    win_rate_label.pack(pady=5)

    # ---------------- Table ----------------
    columns = ("ID", "Opponent", "Date", "Venue", "Team Score", "Opponent Score", "Result")
    match_table = ttk.Treeview(match_window, columns=columns, show="headings")
    for col in columns:
        match_table.heading(col, text=col)
        match_table.column(col, anchor="center", width=120)
    match_table.pack(fill="both", expand=True, padx=20, pady=10)

    # ---------------- Core Functions ----------------
    def get_match_result(t1, t2):
        t1 = t1 or 0
        t2 = t2 or 0
        if t1 > t2: return "WIN"
        if t1 < t2: return "LOSS"
        return "DRAW"

    def calculate_win_rate():
        cursor.execute("SELECT team_score, opponent_score FROM matches")
        rows = cursor.fetchall()
        total = len(rows)
        if total == 0:
            return "0%"
        
        wins = 0
        for t_score, o_score in rows:
            t_score = t_score or 0   # convert None to 0
            o_score = o_score or 0
            if t_score > o_score:
                wins += 1
        return f"{wins / total * 100:.2f}%"

    def load_matches():
        for row in match_table.get_children():
            match_table.delete(row)
        cursor.execute("SELECT * FROM matches")
        rows = cursor.fetchall()
        for row in rows:
            res = get_match_result(row[4], row[5])
            display_data = list(row) + [res]
            match_table.insert("", tk.END, values=display_data)
        win_rate_label.config(text=f"Season Win Rate: {calculate_win_rate()}")

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

    def update_scores():
        selected = match_table.selection()
        if not selected:
            messagebox.showerror("Error", "Select a match to update")
            return
        try:
            team_score = int(team_score_entry.get())
            opponent_score = int(opponent_score_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Scores must be integers")
            return
        match_id = match_table.item(selected[0])["values"][0]
        cursor.execute("UPDATE matches SET team_score=?, opponent_score=? WHERE id=?",
                       (team_score, opponent_score, match_id))
        conn.commit()
        team_score_entry.delete(0, tk.END)
        opponent_score_entry.delete(0, tk.END)
        load_matches()
        messagebox.showinfo("Success", "Scores Updated")

    def remove_match():
        selected = match_table.selection()
        if not selected:
            messagebox.showerror("Error", "Select a match to remove")
            return
        match_id = match_table.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this match?"):
            cursor.execute("DELETE FROM matches WHERE id=?", (match_id,))
            conn.commit()
            load_matches()

    # Initial load
    load_matches()