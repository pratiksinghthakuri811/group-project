import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# ================================================================
#  COLORS & FONTS  (change here to re-theme the whole app)
# ================================================================
BG_DARK   = "#0d1117"
BG_CARD   = "#161b22"
BG_INPUT  = "#21262d"
ACCENT    = "#238636"   # green
ACCENT2   = "#1f6feb"   # blue
RED       = "#da3633"
TEXT      = "#c9d1d9"
TEXT_DIM  = "#8b949e"
WHITE     = "#f0f6fc"
BORDER    = "#30363d"

FONT_TITLE  = ("Segoe UI", 22, "bold")
FONT_SUB    = ("Segoe UI", 11)
FONT_LABEL  = ("Segoe UI", 10)
FONT_BOLD   = ("Segoe UI", 10, "bold")
FONT_SMALL  = ("Segoe UI", 9)

# ================================================================
#  DATABASE SETUP
# ================================================================
def get_conn():
    return sqlite3.connect("football.db")

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role     TEXT NOT NULL DEFAULT 'user'
    );
    CREATE TABLE IF NOT EXISTS tournaments (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT NOT NULL,
        type       TEXT NOT NULL,
        start_date TEXT,
        end_date   TEXT,
        venue      TEXT,
        status     TEXT DEFAULT 'Upcoming'
    );
    CREATE TABLE IF NOT EXISTS teams_in_tournament (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        tournament_id INTEGER,
        team_name     TEXT NOT NULL,
        played        INTEGER DEFAULT 0,
        won           INTEGER DEFAULT 0,
        drawn         INTEGER DEFAULT 0,
        lost          INTEGER DEFAULT 0,
        goals_for     INTEGER DEFAULT 0,
        goals_against INTEGER DEFAULT 0,
        points        INTEGER DEFAULT 0,
        FOREIGN KEY(tournament_id) REFERENCES tournaments(id)
    );
    CREATE TABLE IF NOT EXISTS matches (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        tournament_id INTEGER,
        home_team     TEXT NOT NULL,
        away_team     TEXT NOT NULL,
        match_date    TEXT,
        venue         TEXT,
        home_score    INTEGER DEFAULT 0,
        away_score    INTEGER DEFAULT 0,
        status        TEXT DEFAULT 'Scheduled',
        FOREIGN KEY(tournament_id) REFERENCES tournaments(id)
    );
    """)
    conn.commit()
    conn.close()

init_db()

# ================================================================
#  HELPER WIDGETS
# ================================================================
def styled_entry(parent, show=None, width=28):
    e = tk.Entry(parent, bg=BG_INPUT, fg=WHITE, insertbackground=WHITE,
                 relief="flat", font=FONT_LABEL, width=width,
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT2)
    if show:
        e.config(show=show)
    return e

def styled_btn(parent, text, command, color=ACCENT, width=18):
    btn = tk.Button(parent, text=text, command=command,
                    bg=color, fg=WHITE, font=FONT_BOLD,
                    relief="flat", width=width, cursor="hand2",
                    activebackground=color, activeforeground=WHITE,
                    padx=6, pady=6)
    btn.bind("<Enter>", lambda e: btn.config(bg=_lighten(color)))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn

def _lighten(hex_color):
    """Very simple highlight: shift each channel up by 20."""
    h = hex_color.lstrip("#")
    rgb = [min(int(h[i:i+2], 16) + 20, 255) for i in (0, 2, 4)]
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def section_label(parent, text):
    tk.Label(parent, text=text, bg=BG_CARD, fg=TEXT_DIM,
             font=FONT_SMALL).pack(anchor="w")

def card_frame(parent, pady=10):
    f = tk.Frame(parent, bg=BG_CARD, padx=20, pady=15,
                 highlightthickness=1, highlightbackground=BORDER)
    f.pack(fill="x", padx=20, pady=pady)
    return f

# ================================================================
#  LOGIN / REGISTER SCREEN
# ================================================================
class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("⚽ Football Management System")
        self.root.geometry("480x560")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)
        self._center()
        self._build()

    def _center(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 480) // 2
        y = (self.root.winfo_screenheight() - 560) // 2
        self.root.geometry(f"480x560+{x}+{y}")

    def _build(self):
        # --- Header ---
        hdr = tk.Frame(self.root, bg=BG_DARK)
        hdr.pack(pady=30)
        tk.Label(hdr, text="⚽", font=("Segoe UI", 42),
                 bg=BG_DARK, fg=ACCENT).pack()
        tk.Label(hdr, text="Football Management System",
                 font=FONT_TITLE, bg=BG_DARK, fg=WHITE).pack()
        tk.Label(hdr, text="Tournament & League Edition",
                 font=FONT_SUB, bg=BG_DARK, fg=TEXT_DIM).pack()

        # --- Card ---
        card = tk.Frame(self.root, bg=BG_CARD, padx=30, pady=25,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(padx=40, fill="x")

        # Username
        section_label(card, "USERNAME")
        self.e_user = styled_entry(card, width=32)
        self.e_user.pack(fill="x", pady=(2, 12))

        # Password
        section_label(card, "PASSWORD")
        self.e_pass = styled_entry(card, show="●", width=32)
        self.e_pass.pack(fill="x", pady=(2, 12))

        # Role
        section_label(card, "ROLE")
        self.role_var = tk.StringVar(value="user")
        role_frame = tk.Frame(card, bg=BG_CARD)
        role_frame.pack(fill="x", pady=(2, 18))
        for val, label in [("user", "👤  User"), ("admin", "🛡️  Admin")]:
            tk.Radiobutton(role_frame, text=label, variable=self.role_var,
                           value=val, bg=BG_CARD, fg=TEXT, selectcolor=BG_INPUT,
                           activebackground=BG_CARD, activeforeground=WHITE,
                           font=FONT_LABEL).pack(side="left", padx=10)

        # Buttons
        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.pack(fill="x")
        styled_btn(btn_row, "🔑  Login",    self._login,    ACCENT2, 14).pack(side="left",  expand=True, fill="x", padx=(0,6))
        styled_btn(btn_row, "📝  Register", self._register, ACCENT,  14).pack(side="right", expand=True, fill="x", padx=(6,0))

        # Footer
        tk.Label(self.root, text="© 2025 Football Management System",
                 bg=BG_DARK, fg=TEXT_DIM, font=FONT_SMALL).pack(pady=20)

    # ---------- actions ----------
    def _login(self):
        u, p = self.e_user.get().strip(), self.e_pass.get().strip()
        if not u or not p:
            messagebox.showwarning("Missing", "Please enter username and password.")
            return
        conn = get_conn()
        row = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (u, p)
        ).fetchone()
        conn.close()
        if row:
            self.root.destroy()
            MainApp(row[1], row[3])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def _register(self):
        u, p, r = self.e_user.get().strip(), self.e_pass.get().strip(), self.role_var.get()
        if not u or not p:
            messagebox.showwarning("Missing", "Username and password are required.")
            return
        try:
            conn = get_conn()
            conn.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)", (u,p,r))
            conn.commit()
            conn.close()
            messagebox.showinfo("Registered", f"Account '{u}' created! You can now log in.")
            self.e_user.delete(0, "end")
            self.e_pass.delete(0, "end")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")

# ================================================================
#  MAIN APP  (after login)
# ================================================================
class MainApp:
    def __init__(self, username, role):
        self.username = username
        self.role     = role
        self.root = tk.Tk()
        self.root.title("⚽ Football Management System")
        self.root.geometry("1100x700")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)
        self._center()
        self._build()
        self.show_dashboard()
        self.root.mainloop()

    def _center(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 1100) // 2
        y = (self.root.winfo_screenheight() - 700)  // 2
        self.root.geometry(f"1100x700+{x}+{y}")

    def _build(self):
        # ---- Sidebar ----
        self.sidebar = tk.Frame(self.root, bg=BG_CARD, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="⚽ FMS", font=("Segoe UI", 18, "bold"),
                 bg=BG_CARD, fg=WHITE).pack(pady=(25,5))
        tk.Label(self.sidebar, text=f"👤 {self.username}  [{self.role}]",
                 bg=BG_CARD, fg=TEXT_DIM, font=FONT_SMALL).pack(pady=(0,25))

        separator = tk.Frame(self.sidebar, bg=BORDER, height=1)
        separator.pack(fill="x", padx=15, pady=5)

        # nav buttons
        self.nav_buttons = {}
        nav_items = [
            ("🏠  Dashboard",    "dashboard",    self.show_dashboard),
            ("🏆  Tournaments",  "tournaments",  self.show_tournaments),
            ("📋  Standings",    "standings",    self.show_standings),
            ("⚽  Matches",      "matches",      self.show_matches),
        ]
        for label, key, cmd in nav_items:
            btn = tk.Button(self.sidebar, text=label, command=cmd,
                            bg=BG_CARD, fg=TEXT, font=FONT_LABEL,
                            relief="flat", anchor="w", padx=20, pady=10,
                            cursor="hand2", activebackground=BG_INPUT,
                            activeforeground=WHITE)
            btn.pack(fill="x")
            self.nav_buttons[key] = btn

        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", padx=15, pady=10)
        tk.Button(self.sidebar, text="🚪  Logout", command=self._logout,
                  bg=BG_CARD, fg=RED, font=FONT_LABEL, relief="flat",
                  anchor="w", padx=20, pady=10, cursor="hand2",
                  activebackground=BG_INPUT, activeforeground=RED).pack(fill="x")

        # ---- Main content area ----
        self.content = tk.Frame(self.root, bg=BG_DARK)
        self.content.pack(side="left", fill="both", expand=True)

    def _set_active(self, key):
        for k, btn in self.nav_buttons.items():
            btn.config(bg=BG_CARD if k != key else BG_INPUT,
                       fg=WHITE   if k == key else TEXT)

    def _clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _page_header(self, title, subtitle=""):
        hdr = tk.Frame(self.content, bg=BG_DARK)
        hdr.pack(fill="x", padx=30, pady=(25, 5))
        tk.Label(hdr, text=title, font=("Segoe UI", 18, "bold"),
                 bg=BG_DARK, fg=WHITE).pack(anchor="w")
        if subtitle:
            tk.Label(hdr, text=subtitle, font=FONT_SMALL,
                     bg=BG_DARK, fg=TEXT_DIM).pack(anchor="w")
        tk.Frame(self.content, bg=BORDER, height=1).pack(fill="x", padx=30, pady=8)

    # ============================================================
    #  DASHBOARD
    # ============================================================
    def show_dashboard(self):
        self._clear()
        self._set_active("dashboard")
        self._page_header("🏠 Dashboard", f"Welcome back, {self.username}!")

        conn = get_conn()
        t_count = conn.execute("SELECT COUNT(*) FROM tournaments").fetchone()[0]
        m_count = conn.execute("SELECT COUNT(*) FROM matches").fetchone()[0]
        m_done  = conn.execute("SELECT COUNT(*) FROM matches WHERE status='Completed'").fetchone()[0]
        teams   = conn.execute("SELECT COUNT(DISTINCT team_name) FROM teams_in_tournament").fetchone()[0]
        conn.close()

        stats = [
            ("🏆", "Tournaments", t_count, ACCENT),
            ("👥", "Teams",        teams,   ACCENT2),
            ("⚽", "Matches",      m_count, "#e3b341"),
            ("✅", "Completed",    m_done,  "#3fb950"),
        ]
        row = tk.Frame(self.content, bg=BG_DARK)
        row.pack(fill="x", padx=30, pady=10)
        for icon, label, val, color in stats:
            card = tk.Frame(row, bg=BG_CARD, padx=20, pady=18,
                            highlightthickness=1, highlightbackground=color)
            card.pack(side="left", expand=True, fill="x", padx=8)
            tk.Label(card, text=icon, font=("Segoe UI", 28), bg=BG_CARD, fg=color).pack()
            tk.Label(card, text=str(val), font=("Segoe UI", 24, "bold"),
                     bg=BG_CARD, fg=WHITE).pack()
            tk.Label(card, text=label, font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM).pack()

        # Recent matches
        self._page_header("📅 Recent Matches")
        conn = get_conn()
        rows = conn.execute("""
            SELECT m.match_date, t.name, m.home_team, m.home_score,
                   m.away_score, m.away_team, m.status
            FROM matches m JOIN tournaments t ON m.tournament_id=t.id
            ORDER BY m.id DESC LIMIT 5
        """).fetchall()
        conn.close()

        if rows:
            for r in rows:
                f = tk.Frame(self.content, bg=BG_CARD, padx=15, pady=8,
                             highlightthickness=1, highlightbackground=BORDER)
                f.pack(fill="x", padx=30, pady=3)
                date_str = r[0] or "TBD"
                tk.Label(f, text=date_str, font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM, width=12, anchor="w").pack(side="left")
                tk.Label(f, text=f"[{r[1]}]", font=FONT_SMALL, bg=BG_CARD, fg=ACCENT2, width=18, anchor="w").pack(side="left")
                score = f"{r[2]}  {r[3]} – {r[4]}  {r[5]}"
                tk.Label(f, text=score, font=FONT_BOLD, bg=BG_CARD, fg=WHITE).pack(side="left", padx=10)
                color = ACCENT if r[6] == "Completed" else TEXT_DIM
                tk.Label(f, text=r[6], font=FONT_SMALL, bg=BG_CARD, fg=color).pack(side="right")
        else:
            tk.Label(self.content, text="No matches recorded yet.",
                     bg=BG_DARK, fg=TEXT_DIM, font=FONT_LABEL).pack(pady=10)

    # ============================================================
    #  TOURNAMENTS
    # ============================================================
    def show_tournaments(self):
        self._clear()
        self._set_active("tournaments")
        self._page_header("🏆 Tournament Management", "Create and manage tournaments")

        # -- Form card --
        form = card_frame(self.content)
        tk.Label(form, text="➕  Add New Tournament", font=FONT_BOLD,
                 bg=BG_CARD, fg=WHITE).grid(row=0, columnspan=4, sticky="w", pady=(0,10))

        labels = ["Tournament Name", "Type", "Start Date (YYYY-MM-DD)",
                  "End Date (YYYY-MM-DD)", "Venue"]
        self.t_entries = {}
        fields = ["name", "type", "start_date", "end_date", "venue"]
        for i, (lbl, key) in enumerate(zip(labels, fields)):
            col = (i % 3) * 2
            row = 1 + i // 3
            tk.Label(form, text=lbl, bg=BG_CARD, fg=TEXT_DIM,
                     font=FONT_SMALL).grid(row=row, column=col, sticky="w", padx=(0,5))
            if key == "type":
                var = tk.StringVar(value="League")
                opt = tk.OptionMenu(form, var, "League", "Knockout", "Group Stage")
                opt.config(bg=BG_INPUT, fg=WHITE, font=FONT_LABEL, relief="flat",
                           highlightthickness=0, activebackground=BG_INPUT)
                opt["menu"].config(bg=BG_INPUT, fg=WHITE)
                opt.grid(row=row, column=col+1, sticky="ew", padx=(0,15), pady=4)
                self.t_entries[key] = var
            else:
                e = styled_entry(form, width=20)
                e.grid(row=row, column=col+1, sticky="ew", padx=(0,15), pady=4)
                self.t_entries[key] = e

        styled_btn(form, "✅  Create Tournament", self._create_tournament).grid(
            row=3, column=0, columnspan=2, pady=10, sticky="w")

        # -- List --
        self._page_header("📋 All Tournaments")
        self._tournament_list()

    def _create_tournament(self):
        vals = {}
        for k, w in self.t_entries.items():
            vals[k] = w.get().strip() if hasattr(w, "get") else w.get()
        if not vals["name"]:
            messagebox.showwarning("Missing", "Tournament name is required.")
            return
        conn = get_conn()
        conn.execute("""
            INSERT INTO tournaments (name,type,start_date,end_date,venue)
            VALUES (?,?,?,?,?)
        """, (vals["name"], vals["type"], vals["start_date"], vals["end_date"], vals["venue"]))
        conn.commit()
        conn.close()
        messagebox.showinfo("Created", f"Tournament '{vals['name']}' created!")
        self.show_tournaments()

    def _tournament_list(self):
        conn = get_conn()
        rows = conn.execute("SELECT id,name,type,start_date,end_date,venue,status FROM tournaments ORDER BY id DESC").fetchall()
        conn.close()

        headers = ["ID","Name","Type","Start","End","Venue","Status","Actions"]
        tree_frame = tk.Frame(self.content, bg=BG_DARK)
        tree_frame.pack(fill="both", expand=True, padx=30, pady=5)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=BG_CARD, foreground=TEXT,
                        fieldbackground=BG_CARD, rowheight=30,
                        font=FONT_LABEL)
        style.configure("Custom.Treeview.Heading",
                        background=BG_INPUT, foreground=WHITE,
                        font=FONT_BOLD)
        style.map("Custom.Treeview", background=[("selected", ACCENT2)])

        cols = ("id","name","type","start","end","venue","status")
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                            style="Custom.Treeview", height=12)
        widths = [40,200,100,100,100,150,100]
        heads  = ["ID","Name","Type","Start","End","Venue","Status"]
        for col, head, w in zip(cols, heads, widths):
            tree.heading(col, text=head)
            tree.column(col, width=w, anchor="center")

        for r in rows:
            tree.insert("", "end", values=r)

        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        btn_row = tk.Frame(self.content, bg=BG_DARK)
        btn_row.pack(fill="x", padx=30, pady=5)

        def manage_teams():
            sel = tree.selection()
            if not sel:
                messagebox.showinfo("Select", "Please select a tournament first.")
                return
            tid, tname = tree.item(sel[0])["values"][0], tree.item(sel[0])["values"][1]
            self._open_team_manager(tid, tname)

        def delete_tournament():
            sel = tree.selection()
            if not sel:
                return
            tid  = tree.item(sel[0])["values"][0]
            name = tree.item(sel[0])["values"][1]
            if messagebox.askyesno("Delete", f"Delete tournament '{name}'?"):
                conn = get_conn()
                conn.execute("DELETE FROM tournaments WHERE id=?", (tid,))
                conn.execute("DELETE FROM teams_in_tournament WHERE tournament_id=?", (tid,))
                conn.execute("DELETE FROM matches WHERE tournament_id=?", (tid,))
                conn.commit()
                conn.close()
                self.show_tournaments()

        styled_btn(btn_row, "👥  Manage Teams",       manage_teams,       ACCENT2).pack(side="left", padx=5)
        styled_btn(btn_row, "🗑️  Delete Tournament",  delete_tournament,  RED, 20).pack(side="left", padx=5)

    def _open_team_manager(self, tid, tname):
        win = tk.Toplevel(self.root)
        win.title(f"Teams — {tname}")
        win.geometry("560x500")
        win.configure(bg=BG_DARK)
        win.resizable(False, False)

        tk.Label(win, text=f"👥 Teams in: {tname}", font=FONT_BOLD,
                 bg=BG_DARK, fg=WHITE).pack(pady=15)

        entry_frame = tk.Frame(win, bg=BG_DARK)
        entry_frame.pack()
        tk.Label(entry_frame, text="Team Name:", bg=BG_DARK, fg=TEXT,
                 font=FONT_LABEL).pack(side="left", padx=5)
        e_team = styled_entry(entry_frame, width=24)
        e_team.pack(side="left", padx=5)

        listbox = tk.Listbox(win, bg=BG_CARD, fg=TEXT, font=FONT_LABEL,
                             selectbackground=ACCENT2, height=14, width=50,
                             highlightthickness=0)
        listbox.pack(padx=20, pady=10, fill="both", expand=True)

        def refresh():
            listbox.delete(0, "end")
            conn = get_conn()
            for row in conn.execute(
                "SELECT id,team_name FROM teams_in_tournament WHERE tournament_id=?", (tid,)
            ).fetchall():
                listbox.insert("end", f"  {row[0]}. {row[1]}")
            conn.close()

        def add_team():
            name = e_team.get().strip()
            if not name:
                return
            conn = get_conn()
            conn.execute("INSERT INTO teams_in_tournament (tournament_id,team_name) VALUES (?,?)",
                         (tid, name))
            conn.commit()
            conn.close()
            e_team.delete(0, "end")
            refresh()

        def remove_team():
            sel = listbox.curselection()
            if not sel:
                return
            text = listbox.get(sel[0])
            team_id = int(text.strip().split(".")[0])
            conn = get_conn()
            conn.execute("DELETE FROM teams_in_tournament WHERE id=?", (team_id,))
            conn.commit()
            conn.close()
            refresh()

        refresh()
        btn_row = tk.Frame(win, bg=BG_DARK)
        btn_row.pack(pady=5)
        styled_btn(btn_row, "➕ Add Team",    add_team,    ACCENT,  12).pack(side="left", padx=5)
        styled_btn(btn_row, "❌ Remove Team", remove_team, RED,     12).pack(side="left", padx=5)

    # ============================================================
    #  STANDINGS
    # ============================================================
    def show_standings(self):
        self._clear()
        self._set_active("standings")
        self._page_header("📋 League Standings", "Points table for all tournaments")

        # Tournament selector
        conn = get_conn()
        tournaments = conn.execute("SELECT id,name FROM tournaments").fetchall()
        conn.close()

        if not tournaments:
            tk.Label(self.content, text="No tournaments found. Create one first!",
                     bg=BG_DARK, fg=TEXT_DIM, font=FONT_LABEL).pack(pady=20)
            return

        sel_frame = tk.Frame(self.content, bg=BG_DARK)
        sel_frame.pack(fill="x", padx=30, pady=5)
        tk.Label(sel_frame, text="Select Tournament:", bg=BG_DARK,
                 fg=TEXT, font=FONT_LABEL).pack(side="left", padx=(0,10))
        t_var = tk.StringVar()
        t_map = {t[1]: t[0] for t in tournaments}
        t_var.set(tournaments[0][1])
        opt = tk.OptionMenu(sel_frame, t_var, *[t[1] for t in tournaments])
        opt.config(bg=BG_INPUT, fg=WHITE, font=FONT_LABEL, relief="flat",
                   highlightthickness=0, activebackground=BG_INPUT)
        opt["menu"].config(bg=BG_INPUT, fg=WHITE)
        opt.pack(side="left")

        tree_holder = tk.Frame(self.content, bg=BG_DARK)
        tree_holder.pack(fill="both", expand=True, padx=30, pady=10)

        def load_standings(*_):
            for w in tree_holder.winfo_children():
                w.destroy()
            tid = t_map[t_var.get()]
            conn = get_conn()
            rows = conn.execute("""
                SELECT team_name,played,won,drawn,lost,goals_for,goals_against,
                       (goals_for - goals_against) as gd, points
                FROM teams_in_tournament WHERE tournament_id=?
                ORDER BY points DESC, gd DESC, goals_for DESC
            """, (tid,)).fetchall()
            conn.close()

            style = ttk.Style()
            style.configure("Stand.Treeview",
                            background=BG_CARD, foreground=TEXT,
                            fieldbackground=BG_CARD, rowheight=28, font=FONT_LABEL)
            style.configure("Stand.Treeview.Heading",
                            background=BG_INPUT, foreground=WHITE, font=FONT_BOLD)
            style.map("Stand.Treeview", background=[("selected", ACCENT2)])

            cols = ("pos","team","p","w","d","l","gf","ga","gd","pts")
            tree = ttk.Treeview(tree_holder, columns=cols, show="headings",
                                style="Stand.Treeview", height=14)
            heads = ["#","Team","P","W","D","L","GF","GA","GD","PTS"]
            widths= [40,200,50,50,50,50,50,50,50,60]
            for col,head,w in zip(cols,heads,widths):
                tree.heading(col,text=head)
                tree.column(col,width=w,anchor="center")

            for i, r in enumerate(rows, 1):
                tag = "top3" if i <= 3 else ""
                tree.insert("", "end", values=(i, *r), tags=(tag,))
            tree.tag_configure("top3", foreground="#e3b341")

            sb = ttk.Scrollbar(tree_holder, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=sb.set)
            tree.pack(side="left", fill="both", expand=True)
            sb.pack(side="right", fill="y")

            # Update points button
            def update_pts_popup():
                self._update_standings_popup(tid, t_var.get(), load_standings)

            btn_f = tk.Frame(self.content, bg=BG_DARK)
            btn_f.pack(fill="x", padx=30, pady=5)
            styled_btn(btn_f, "✏️  Update Team Stats", update_pts_popup, ACCENT2).pack(side="left")

        t_var.trace("w", load_standings)
        load_standings()

    def _update_standings_popup(self, tid, tname, refresh_cb):
        conn = get_conn()
        teams = conn.execute(
            "SELECT id,team_name,played,won,drawn,lost,goals_for,goals_against,points "
            "FROM teams_in_tournament WHERE tournament_id=?", (tid,)
        ).fetchall()
        conn.close()

        if not teams:
            messagebox.showinfo("No Teams", "Add teams to this tournament first.")
            return

        win = tk.Toplevel(self.root)
        win.title(f"Update Stats — {tname}")
        win.geometry("500x420")
        win.configure(bg=BG_DARK)
        win.resizable(False, False)

        tk.Label(win, text=f"✏️ Update Stats: {tname}", font=FONT_BOLD,
                 bg=BG_DARK, fg=WHITE).pack(pady=12)

        tk.Label(win, text="Select Team:", bg=BG_DARK, fg=TEXT, font=FONT_LABEL).pack()
        team_names = [t[1] for t in teams]
        team_var = tk.StringVar(value=team_names[0])
        opt = tk.OptionMenu(win, team_var, *team_names)
        opt.config(bg=BG_INPUT, fg=WHITE, font=FONT_LABEL, relief="flat",
                   highlightthickness=0, activebackground=BG_INPUT)
        opt["menu"].config(bg=BG_INPUT, fg=WHITE)
        opt.pack(pady=5)

        fields_frame = tk.Frame(win, bg=BG_DARK)
        fields_frame.pack(pady=10)
        field_keys  = ["played","won","drawn","lost","goals_for","goals_against"]
        field_labels= ["Played","Won","Drawn","Lost","Goals For","Goals Against"]
        entries = {}
        for i,(k,l) in enumerate(zip(field_keys, field_labels)):
            row = i // 2
            col = (i % 2) * 2
            tk.Label(fields_frame, text=l, bg=BG_DARK, fg=TEXT_DIM,
                     font=FONT_SMALL).grid(row=row, column=col, sticky="e", padx=8, pady=6)
            e = styled_entry(fields_frame, width=10)
            e.grid(row=row, column=col+1, padx=8, pady=6)
            entries[k] = e

        def load_team(*_):
            name = team_var.get()
            t = next(t for t in teams if t[1] == name)
            for i,k in enumerate(field_keys):
                entries[k].delete(0,"end")
                entries[k].insert(0, str(t[i+2]))

        team_var.trace("w", load_team)
        load_team()

        def save():
            name = team_var.get()
            t    = next(t for t in teams if t[1] == name)
            try:
                vals = {k: int(entries[k].get()) for k in field_keys}
            except ValueError:
                messagebox.showerror("Error", "All fields must be numbers.")
                return
            pts = vals["won"]*3 + vals["drawn"]
            conn = get_conn()
            conn.execute("""
                UPDATE teams_in_tournament
                SET played=?,won=?,drawn=?,lost=?,goals_for=?,goals_against=?,points=?
                WHERE id=?
            """, (vals["played"],vals["won"],vals["drawn"],vals["lost"],
                  vals["goals_for"],vals["goals_against"],pts, t[0]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Saved", f"Stats updated for {name}! Points: {pts}")
            win.destroy()
            refresh_cb()

        styled_btn(win, "💾  Save Stats", save, ACCENT).pack(pady=12)

    # ============================================================
    #  MATCHES
    # ============================================================
    def show_matches(self):
        self._clear()
        self._set_active("matches")
        self._page_header("⚽ Match Management", "Schedule and record match results")

        # -- form --
        form = card_frame(self.content)
        tk.Label(form, text="➕  Schedule a Match", font=FONT_BOLD,
                 bg=BG_CARD, fg=WHITE).grid(row=0, columnspan=6, sticky="w", pady=(0,10))

        conn = get_conn()
        tournaments = conn.execute("SELECT id,name FROM tournaments").fetchall()
        conn.close()

        if not tournaments:
            tk.Label(form, text="No tournaments found. Create one first!",
                     bg=BG_CARD, fg=TEXT_DIM, font=FONT_LABEL).grid(row=1, column=0)
        else:
            t_map = {t[1]: t[0] for t in tournaments}
            t_var = tk.StringVar(value=tournaments[0][1])

            def get_team_names(*_):
                tid = t_map[t_var.get()]
                conn = get_conn()
                names = [r[0] for r in conn.execute(
                    "SELECT team_name FROM teams_in_tournament WHERE tournament_id=?", (tid,)
                ).fetchall()]
                conn.close()
                return names or ["(no teams)"]

            m_entries = {}

            # Row 1
            def labeled(row, col, label, widget):
                tk.Label(form, text=label, bg=BG_CARD, fg=TEXT_DIM,
                         font=FONT_SMALL).grid(row=row, column=col, sticky="w", padx=5)
                widget.grid(row=row, column=col+1, padx=5, pady=4, sticky="ew")

            opt_t = tk.OptionMenu(form, t_var, *[t[1] for t in tournaments])
            opt_t.config(bg=BG_INPUT, fg=WHITE, font=FONT_LABEL, relief="flat",
                         highlightthickness=0, activebackground=BG_INPUT)
            opt_t["menu"].config(bg=BG_INPUT, fg=WHITE)
            labeled(1, 0, "Tournament", opt_t)

            home_var = tk.StringVar()
            away_var = tk.StringVar()

            def update_team_menus(*_):
                names = get_team_names()
                home_var.set(names[0])
                away_var.set(names[-1])
                for var, opt_widget in [(home_var, opt_home), (away_var, opt_away)]:
                    menu = opt_widget["menu"]
                    menu.delete(0, "end")
                    for n in names:
                        menu.add_command(label=n, command=lambda v=n, vr=var: vr.set(v))

            names0 = get_team_names()
            home_var.set(names0[0])
            away_var.set(names0[-1] if len(names0) > 1 else names0[0])

            opt_home = tk.OptionMenu(form, home_var, *names0)
            opt_away = tk.OptionMenu(form, away_var, *names0)
            for opt in [opt_home, opt_away]:
                opt.config(bg=BG_INPUT, fg=WHITE, font=FONT_LABEL, relief="flat",
                           highlightthickness=0, activebackground=BG_INPUT)
                opt["menu"].config(bg=BG_INPUT, fg=WHITE)

            t_var.trace("w", update_team_menus)
            labeled(1, 2, "Home Team", opt_home)
            labeled(1, 4, "Away Team", opt_away)

            e_date  = styled_entry(form, width=14); labeled(2, 0, "Date (YYYY-MM-DD)", e_date)
            e_venue = styled_entry(form, width=14); labeled(2, 2, "Venue",             e_venue)

            def schedule_match():
                tid = t_map[t_var.get()]
                h, a = home_var.get(), away_var.get()
                if h == a:
                    messagebox.showwarning("Error", "Home and Away teams must be different.")
                    return
                conn = get_conn()
                conn.execute("""
                    INSERT INTO matches (tournament_id,home_team,away_team,match_date,venue)
                    VALUES (?,?,?,?,?)
                """, (tid, h, a, e_date.get().strip(), e_venue.get().strip()))
                conn.commit()
                conn.close()
                messagebox.showinfo("Scheduled", f"Match {h} vs {a} scheduled!")
                self.show_matches()

            m_entries["schedule"] = schedule_match
            styled_btn(form, "📅  Schedule Match", schedule_match, ACCENT2).grid(
                row=3, column=0, columnspan=2, pady=10, sticky="w")

        # -- list --
        self._page_header("📋 All Matches")
        self._match_list()

    def _match_list(self):
        frame = tk.Frame(self.content, bg=BG_DARK)
        frame.pack(fill="both", expand=True, padx=30, pady=5)

        style = ttk.Style()
        style.configure("Match.Treeview",
                        background=BG_CARD, foreground=TEXT,
                        fieldbackground=BG_CARD, rowheight=28, font=FONT_LABEL)
        style.configure("Match.Treeview.Heading",
                        background=BG_INPUT, foreground=WHITE, font=FONT_BOLD)
        style.map("Match.Treeview", background=[("selected", ACCENT2)])

        cols = ("id","tournament","home","score","away","date","venue","status")
        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            style="Match.Treeview", height=10)
        heads  = ["ID","Tournament","Home","Score","Away","Date","Venue","Status"]
        widths = [40,150,120,70,120,100,120,90]
        for col,head,w in zip(cols,heads,widths):
            tree.heading(col, text=head)
            tree.column(col, width=w, anchor="center")

        conn = get_conn()
        rows = conn.execute("""
            SELECT m.id,t.name,m.home_team,
                   m.home_score||' - '||m.away_score,
                   m.away_team,m.match_date,m.venue,m.status
            FROM matches m JOIN tournaments t ON m.tournament_id=t.id
            ORDER BY m.id DESC
        """).fetchall()
        conn.close()

        for r in rows:
            tag = "done" if r[7] == "Completed" else ""
            tree.insert("", "end", values=r, tags=(tag,))
        tree.tag_configure("done", foreground="#3fb950")

        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        btn_row = tk.Frame(self.content, bg=BG_DARK)
        btn_row.pack(fill="x", padx=30, pady=5)

        def record_result():
            sel = tree.selection()
            if not sel:
                messagebox.showinfo("Select", "Please select a match.")
                return
            vals = tree.item(sel[0])["values"]
            mid  = vals[0]
            self._record_result_popup(mid, vals[2], vals[4], self.show_matches)

        def delete_match():
            sel = tree.selection()
            if not sel:
                return
            mid = tree.item(sel[0])["values"][0]
            if messagebox.askyesno("Delete", "Delete this match?"):
                conn = get_conn()
                conn.execute("DELETE FROM matches WHERE id=?", (mid,))
                conn.commit()
                conn.close()
                self.show_matches()

        styled_btn(btn_row, "⚽  Record Result", record_result, ACCENT).pack(side="left", padx=5)
        styled_btn(btn_row, "🗑️  Delete Match",  delete_match,  RED,    16).pack(side="left", padx=5)

    def _record_result_popup(self, mid, home, away, refresh_cb):
        win = tk.Toplevel(self.root)
        win.title("Record Result")
        win.geometry("380x260")
        win.configure(bg=BG_DARK)
        win.resizable(False, False)

        tk.Label(win, text=f"⚽ {home}  vs  {away}", font=FONT_BOLD,
                 bg=BG_DARK, fg=WHITE).pack(pady=18)

        row = tk.Frame(win, bg=BG_DARK)
        row.pack()
        tk.Label(row, text=f"{home} Score:", bg=BG_DARK, fg=TEXT, font=FONT_LABEL).grid(row=0,column=0,padx=10,pady=8)
        e_home = styled_entry(row, width=6); e_home.grid(row=0,column=1)
        e_home.insert(0,"0")

        tk.Label(row, text=f"{away} Score:", bg=BG_DARK, fg=TEXT, font=FONT_LABEL).grid(row=1,column=0,padx=10,pady=8)
        e_away = styled_entry(row, width=6); e_away.grid(row=1,column=1)
        e_away.insert(0,"0")

        def save():
            try:
                hs, as_ = int(e_home.get()), int(e_away.get())
            except ValueError:
                messagebox.showerror("Error", "Scores must be integers.")
                return
            conn = get_conn()
            conn.execute("""
                UPDATE matches SET home_score=?,away_score=?,status='Completed'
                WHERE id=?
            """, (hs, as_, mid))
            conn.commit()
            conn.close()
            messagebox.showinfo("Saved", "Result recorded!")
            win.destroy()
            refresh_cb()

        styled_btn(win, "💾  Save Result", save, ACCENT).pack(pady=18)

    # ============================================================
    #  LOGOUT
    # ============================================================
    def _logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            new_root = tk.Tk()
            LoginScreen(new_root)
            new_root.mainloop()

# ================================================================
#  ENTRY POINT
# ================================================================
if __name__ == "__main__":
    root = tk.Tk()
    LoginScreen(root)
    root.mainloop()