import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

DB_NAME = "soccer.db"

# DATABASE SETUP
def setup_team_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                team_name TEXT PRIMARY KEY,
                coach TEXT,
                staff_info TEXT,
                formation TEXT
            )
        """)
        try:
            cursor.execute("ALTER TABLE players ADD COLUMN team_assigned TEXT")
        except sqlite3.OperationalError:
            pass
        conn.commit()
    except Exception as e:
        print(f"Database Setup Error: {e}")
    finally:
        conn.close()

# UI & LOGIC
def team_management_page(dashboard_root=None):
    setup_team_db()
    
    # Use Toplevel if dashboard exists, otherwise create a new Tk instance
    if dashboard_root:
        root = tk.Toplevel(dashboard_root)
    else:
        root = tk.Tk()

    root.title("Soccer Pro - Team Management")
    root.state("zoomed")  # Fullscreen
    root.configure(bg="#f4f7f6")
    
    def go_back():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", go_back)

    #  HEADER
    header = tk.Frame(root, bg="#2C3E50", height=80)  # Unified header to prevent overlaps
    header.pack(fill="x")
    
    tk.Button(header, text="⬅ Back", bg="#7F8C8D", fg="white", font=("Arial", 10, "bold"), 
              command=go_back).pack(side="left", padx=20, pady=20)
    
    tk.Label(header, text="TEAM & LINEUP BUILDER", font=("Helvetica", 18, "bold"), 
             fg="white", bg="#2C3E50").pack(pady=20)

    # MAIN CONTAINER
    main_frame = tk.Frame(root, bg="#f4f7f6")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # DATABASE LOGIC FUNCTIONS 
    
    def refresh_teams_list():
        team_listbox.delete(0, tk.END)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT team_name FROM teams")
        for row in cursor.fetchall():
            team_listbox.insert(tk.END, row[0])
        conn.close()

    def load_squad(selected_team):
        for row in squad_table.get_children():
            squad_table.delete(row)
            
        if not selected_team:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT jersey, name, position FROM players WHERE team_assigned = ?", (selected_team,))
        for p in cursor.fetchall():
            squad_table.insert("", tk.END, values=p)
        conn.close()

    def save_team():
        name = team_entries["Team Name"].get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Team Name is required!")
            return
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO teams VALUES (?, ?, ?, ?)",
                       (name, team_entries["Head Coach"].get(),
                        team_entries["Staff Details"].get(), formation_combo.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Team '{name}' configured successfully.")
        refresh_teams_list()

    def assign_to_team():
        selection = team_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a team from the list first!")
            return
            
        selected_team = team_listbox.get(selection[0])
        jersey = assign_entry.get().strip()
        
        if not jersey:
            messagebox.showwarning("Input Error", "Enter a Player Jersey #")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE players SET team_assigned = ? WHERE jersey = ?", (selected_team, jersey))
        
        if cursor.rowcount == 0:
            messagebox.showerror("Error", f"Player #{jersey} not found in database.")
        else:
            conn.commit()
            messagebox.showinfo("Success", f"Player #{jersey} joined {selected_team}")
            load_squad(selected_team)
            assign_entry.delete(0, tk.END)
        conn.close()

    def remove_player_from_team():
        selected_item = squad_table.focus()
        if not selected_item:
            messagebox.showwarning("Selection", "Click on a player in the squad list to remove them.")
            return

        values = squad_table.item(selected_item, 'values')
        jersey_val, name_val = values[0], values[1]

        if messagebox.askyesno("Confirm", f"Remove {name_val} from the team?"):
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("UPDATE players SET team_assigned = NULL WHERE jersey = ?", (jersey_val,))
            conn.commit()
            conn.close()
            
            squad_table.delete(selected_item)
            messagebox.showinfo("Success", f"{name_val} removed from squad.")

    def on_team_select(event):
        selection = team_listbox.curselection()
        if selection:
            team_name = team_listbox.get(selection[0])
            load_squad(team_name)
    
    def delete_team():
        selection = team_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a team from the list to delete.")
            return
            
        team_name = team_listbox.get(selection[0])
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{team_name}'?\n\nPlayers will become Free Agents."):
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("UPDATE players SET team_assigned = NULL WHERE team_assigned = ?", (team_name,))
                cursor.execute("DELETE FROM teams WHERE team_name = ?", (team_name,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Deleted", f"Team '{team_name}' has been removed.")
                refresh_teams_list() 
                for row in squad_table.get_children():
                    squad_table.delete(row)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete team: {e}")

    # --- UI LAYOUT ---
    left_frame = tk.LabelFrame(main_frame, text=" Register/Edit Team ", bg="white", padx=15, pady=15)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10)

    labels = ["Team Name", "Head Coach", "Staff Details"]
    team_entries = {}
    for label in labels:
        tk.Label(left_frame, text=label, bg="white").pack(anchor="w", pady=(5, 0))
        ent = tk.Entry(left_frame, font=("Arial", 11), bd=1, relief="solid")
        ent.pack(fill="x", pady=5)
        team_entries[label] = ent

    tk.Label(left_frame, text="Tactical Formation", bg="white").pack(anchor="w", pady=(5, 0))
    formation_combo = ttk.Combobox(left_frame, values=["4-4-2", "4-3-3", "3-5-2", "4-2-3-1", "5-4-1"], state="readonly")
    formation_combo.pack(fill="x", pady=5)
    formation_combo.set("4-4-2")

    tk.Button(left_frame, text="💾 Save Team Info", bg="#27AE60", fg="white", 
              font=("Arial", 10, "bold"), command=save_team).pack(fill="x", pady=20)

    right_frame = tk.LabelFrame(main_frame, text=" Teams & Assignment ", bg="white", padx=15, pady=15)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10)

    tk.Label(right_frame, text="Select a Team:", bg="white", font=("Arial", 9, "bold")).pack(anchor="w")
    team_listbox = tk.Listbox(right_frame, height=6, font=("Arial", 10), bd=1, relief="solid")
    team_listbox.pack(fill="x", pady=5)
    team_listbox.bind("<<ListboxSelect>>", on_team_select)

    tk.Label(right_frame, text="Assign Jersey # to Team:", bg="white", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 0))
    assign_entry = tk.Entry(right_frame, font=("Arial", 11), bd=1, relief="solid")
    assign_entry.pack(fill="x", pady=5)

    tk.Button(right_frame, text="➕ Confirm Assignment", bg="#2980B9", fg="white", 
              font=("Arial", 10, "bold"), command=assign_to_team).pack(fill="x", pady=10)

    delete_team_btn = tk.Button(right_frame, text="🗑️ Delete Selected Team", bg="#e67e22", fg="white", 
                                font=("Arial", 10, "bold"), command=delete_team)
    delete_team_btn.pack(fill="x", pady=5)

    squad_frame = tk.LabelFrame(main_frame, text=" Current Team Squad ", bg="white", padx=10, pady=10)
    squad_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=15)

    cols = ("Jersey", "Name", "Position")
    squad_table = ttk.Treeview(squad_frame, columns=cols, show="headings", height=8)
    for col in cols:
        squad_table.heading(col, text=col)
        squad_table.column(col, width=150, anchor="center")

    scrolly = ttk.Scrollbar(squad_frame, orient="vertical", command=squad_table.yview)
    squad_table.configure(yscroll=scrolly.set)
    squad_table.pack(side="left", fill="both", expand=True)
    scrolly.pack(side="right", fill="y")

    remove_btn = tk.Button(squad_frame, text="Remove Selected Player from Team", bg="#c0392b", fg="white",
                           font=("Arial", 10, "bold"), command=remove_player_from_team)
    remove_btn.pack(side="bottom", fill="x", pady=(10, 0))

    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)

    refresh_teams_list()
    root.mainloop()

if __name__ == "__main__":
    team_management_page()