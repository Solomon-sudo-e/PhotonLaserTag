import tkinter as tk
from tkinter import messagebox
from data.player_model import GameParticipant

def launch_entry_screen(root, db, net, preloaded_players=None):
    ui = EntryScreenUI(root, db, net, preloaded_players)
    ui.build()


class EntryScreenUI:
    def __init__(self, root, db, net, preloaded_players=None):
        self.root = root
        self.db = db
        self.net = net
        self.players = {"green": [], "red": []}
        self.entries = {"green": [], "red": []}
        self.preloaded = preloaded_players or {"green": [], "red": []}

    def build(self):
        self._setup_root()
        self._build_main_frame()
        self._build_team_ui("green", "Green", "#007F00")
        self._build_team_ui("red", "Red", "#AA0000")
        self._build_control_panel()
        self._handle_preload()
        self._bind_keys()

    def _setup_root(self):
        self.root.configure(bg="black")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.update_idletasks()

    def _build_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.team_frame = tk.Frame(self.main_frame, bg="black")
        self.team_frame.grid(row=0, column=0, pady=(30, 10), padx=30)

    def _build_team_ui(self, key, name, color):
        frame = tk.Frame(self.team_frame, bg=color, padx=10, pady=10, bd=2, relief="ridge")
        frame.grid(row=0, column=0 if key == "green" else 1, padx=20)
        tk.Label(frame, text=f"{name} Team", font=("Arial", 14, "bold"), bg=color, fg="white").grid(row=0, column=0, columnspan=3, pady=(0, 10))
        for i, header in enumerate(["Equipment ID", "User ID", "Codename"]):
            tk.Label(frame, text=header, font=("Arial", 10, "bold"), bg=color, fg="white").grid(row=1, column=i, padx=5, pady=2)
        rows = []
        for r in range(15):
            eq, uid, code = (tk.Entry(frame, width=16, bg="black", fg="white", insertbackground="white", relief="sunken", bd=2) for _ in range(3))
            eq.grid(row=r+2, column=0, padx=5, pady=2)
            uid.grid(row=r+2, column=1, padx=5, pady=2)
            code.grid(row=r+2, column=2, padx=5, pady=2)
            uid.bind("<FocusOut>", lambda e, u=uid, c=code: self._lookup_codename(u, c))
            rows.append((eq, uid, code))
        self.entries[key] = rows

    def _build_control_panel(self):
        control = tk.Frame(self.main_frame, bg="black")
        control.grid(row=1, column=0, pady=30)
        self.port_entry = tk.Entry(control, width=18, bg="black", fg="white", insertbackground="white", relief="sunken", bd=2)
        self.port_entry.grid(row=0, column=0, padx=10)
        tk.Button(control, text="Update Address", font=("Arial", 11), height=2, bd=2, relief="raised", highlightthickness=0, command=self._update_server).grid(row=0, column=1, padx=10)
        tk.Button(control, text="Clear All", font=("Arial", 11), height=2, bd=2, relief="raised", highlightthickness=0, command=self._clear_all).grid(row=0, column=2, padx=10)
        tk.Button(control, text="Continue", font=("Arial", 11), height=2, bd=2, relief="raised", highlightthickness=0, command=self._submit_all).grid(row=1, column=0, columnspan=3, pady=20)

    def _lookup_codename(self, uid_entry, codename_entry):
        try:
            uid = int(uid_entry.get().strip())
            record = self.db.get_by_id(uid)
            codename_entry.delete(0, tk.END)
            if record and record[1].lower() != "unknown":
                codename_entry.insert(0, record[1])
        except:
            codename_entry.delete(0, tk.END)

    def _clear_all(self):
        for team in self.entries:
            for row in self.entries[team]:
                for field in row:
                    field.delete(0, tk.END)
            self.players[team].clear()
        self.port_entry.delete(0, tk.END)

    def _update_server(self):
        try:
            port = int(self.port_entry.get())
            if self.net.update_send_port(port):
                messagebox.showinfo("Success", "Server port updated.")
            else:
                messagebox.showerror("Error", "Failed to update port.")
        except:
            messagebox.showerror("Error", "Invalid port number.")

    def _parse_row(self, team, i, eq_entry, uid_entry, code_entry, seen_user_ids, seen_eq_ids):
        eq_val, uid_val, codename = eq_entry.get().strip(), uid_entry.get().strip(), code_entry.get().strip()
        if not eq_val and not uid_val and not codename:
            return None
        if not eq_val.isdigit() or not uid_val.isdigit():
            raise ValueError(f"{team.capitalize()} Row {i+1}: Equipment ID and User ID must be numbers.")
        eq_id, user_id = int(eq_val), int(uid_val)
        if eq_id in seen_eq_ids:
            raise ValueError(f"Duplicate Equipment ID: {eq_id}")
        if user_id in seen_user_ids:
            raise ValueError(f"Duplicate User ID: {user_id}")
        if not codename:
            raise ValueError(f"{team.capitalize()} Row {i+1}: Codename required.")
        seen_eq_ids.add(eq_id)
        seen_user_ids.add(user_id)
        if self.db.get_by_id(user_id) is None:
            self.db.add_player(user_id, codename)
        self.net.transmit(str(eq_id))
        return GameParticipant(i + 1, eq_id, user_id, codename, team)

    def _submit_all(self):
        try:
            seen_user_ids = set()
            seen_eq_ids = set()
            for team in ["green", "red"]:
                self.players[team].clear()
                for i, (eq_entry, uid_entry, code_entry) in enumerate(self.entries[team]):
                    result = self._parse_row(team, i, eq_entry, uid_entry, code_entry, seen_user_ids, seen_eq_ids)
                    if result:
                        self.players[team].append(result)
            if not self.players["green"] or not self.players["red"]:
                raise ValueError("Each team must have at least one player.")
            self.main_frame.destroy()
            from ui.game_screen import render_game_screen
            render_game_screen(self.root, self.players, self.net, self.db)
        except Exception as e:
            messagebox.showerror("Input Error", str(e))

    def _handle_preload(self):
        for team in ["green", "red"]:
            for i, player in enumerate(self.preloaded[team]):
                eq, uid, code = self.entries[team][i]
                eq.insert(0, str(player.equipment_id))
                uid.insert(0, str(player.user_id))
                code.insert(0, player.codename)

    def _bind_keys(self):
        self.root.bind("<F5>", lambda e: self._submit_all())
        self.root.bind("<F12>", lambda e: self._clear_all())


