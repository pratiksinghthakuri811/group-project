import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

DB_NAME = "soccer.db"

# ---------------- DATABASE SETUP ----------------
def create_player_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Fixed: Primary Key should usually be a single unique value like Jersey 
    # unless you specifically want a composite key.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            jersey INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            position TEXT,
            fitness TEXT,
            goals INTEGER,
            injury TEXT,
            suspension TEXT
        )
    """)
    conn.commit()
    conn.close()

# ---------------- PLAYER PAGE ----------------
def open_player_page(root):
    create_player_table()

    # If calling from a main menu, use Toplevel; if standalone, this handles it.
    window = tk.Toplevel(root) if root else tk.Tk()
    window.title("Player Management")
    window.geometry("900x700")
    window.config(bg="#f0f4f7")

    # ---------------- TITLE ----------------
    tk.Label(window, text="⚽ Player Management", font=("Helvetica", 22, "bold"), 
             bg="#f0f4f7", fg="#2C3E50").pack(pady=15)

    # ---------------- ENTRY FRAME ----------------
    entry_frame = tk.Frame(window, bg="#ffffff", bd=1, relief="solid")
    entry_frame.pack(pady=10, padx=15, fill="x")

    labels = ["Jersey Number", "Name", "Age", "Position", "Fitness", "Goals", "Injury", "Suspension"]
    entries = {}

    for i, label in enumerate(labels):
        row, col = divmod(i, 4)
        lbl = tk.Label(entry_frame, text=label, font=("Arial", 10), bg="#ffffff", fg="#34495E")
        lbl.grid(row=row, column=col*2, padx=5, pady=8, sticky="w")
        
        ent = tk.Entry(entry_frame, font=("Arial", 10), bd=1, relief="solid")
        ent.grid(row=row, column=col*2 + 1, padx=5, pady=8, sticky="ew")
        entries[label] = ent

    # ---------------- DATABASE FUNCTIONS ----------------
    def refresh_table():
        for row in player_table.get_children():
            player_table.delete(row)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM players")
        rows = cursor.fetchall()
        for idx, player in enumerate(rows):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            player_table.insert("", tk.END, values=player, tags=(tag,))
        conn.close()

    def clear_entries():
        for entry in entries.values():
            entry.delete(0, tk.END)

    def add_player():
        data = {k: v.get().strip() for k, v in entries.items()}
        
        if not data["Jersey Number"] or not data["Name"]:
            messagebox.showerror("Error", "Jersey and Name are required!", parent=window)
            return

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(data["Jersey Number"]), data["Name"], int(data["Age"] or 0),
                data["Position"], data["Fitness"], int(data["Goals"] or 0),
                data["Injury"], data["Suspension"]
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Player Added!", parent=window)
            clear_entries()
            refresh_table()
        except sqlite3.IntegrityError:
            messagebox.showwarning("Duplicate", "Jersey number already exists!", parent=window)
        except ValueError:
            messagebox.showerror("Error", "Jersey, Age, and Goals must be numbers!", parent=window)

    def delete_player():
        selected = player_table.focus()
        if not selected:
            messagebox.showerror("Error", "Select a player from the table to delete", parent=window)
            return

        # Get the Jersey Number (Column 0) which is our Primary Key
        values = player_table.item(selected, "values")
        jersey_val = values[0] 

        # Confirmation popup
        confirm = messagebox.askyesno("Confirm", f"Permanent delete Jersey #{jersey_val}?", parent=window)
        
        if confirm:
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                
                # Execute the delete
                cursor.execute("DELETE FROM players WHERE jersey=?", (jersey_val,))
                
                # CRITICAL: This saves the change to the .db file forever
                conn.commit() 
                
                # Check if any row was actually deleted in the file
                if cursor.rowcount > 0:
                    conn.close()
                    player_table.delete(selected) # Remove from UI
                    messagebox.showinfo("Success", "Player deleted forever!", parent=window)
                else:
                    conn.close()
                    messagebox.showwarning("Warning", "Player not found in database file.", parent=window)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Database error: {e}", parent=window)

    def search_player():
        val = entries["Name"].get().strip()
        jersey_search = entries["Jersey Number"].get().strip()
        
        for row in player_table.get_children():
            player_table.delete(row)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Searches by name (partial match) or exact jersey number
        cursor.execute("SELECT * FROM players WHERE name LIKE ? OR jersey = ?",(f'%{val}%', jersey_search))
        rows = cursor.fetchall()
        conn.close()

        for idx, player in enumerate(rows):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            player_table.insert("", tk.END, values=player, tags=(tag,))

    # ---------------- BUTTONS ----------------
    button_frame = tk.Frame(window, bg="#f0f4f7")
    button_frame.pack(pady=10)

    btns = [
        ("Add Player", "#27AE60", add_player),
        ("Search", "#F39C12", search_player),
        ("Refresh", "#2980B9", refresh_table),
        ("Delete", "#E74C3C", delete_player),
        ("Clear Fields", "#7F8C8D", clear_entries)
    ]

    for i, (text, color, cmd) in enumerate(btns):
        tk.Button(button_frame, text=text, bg=color, fg="white", font=("Arial", 10, "bold"),width=12, command=cmd).grid(row=0, column=i, padx=5)

    # ---------------- PLAYER TABLE ----------------
    table_frame = tk.Frame(window)
    table_frame.pack(pady=10, padx=15, fill="both", expand=True)

    columns = ("Jersey", "Name", "Age", "Position", "Fitness", "Goals", "Injury", "Suspension")
    player_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

    for col in columns:
        player_table.heading(col, text=col)
        player_table.column(col, width=80 if col != "Name" else 150, anchor="center")

    player_table.tag_configure('evenrow', background='#ecf0f1')
    player_table.tag_configure('oddrow', background='#ffffff')

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=player_table.yview)
    player_table.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    player_table.pack(side="left", fill="both", expand=True)

    refresh_table()
    
    if not root:
        window.mainloop()

# ---------------- APP START ----------------
if __name__ == "__main__":
    # You can pass None if running this file directly
    open_player_page(None)