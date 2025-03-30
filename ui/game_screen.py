import tkinter as tk

def render_game_screen(root, players, net, db):
    root.configure(bg="black")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    frame = tk.Frame(root, bg="black")
    frame.grid(row=0, column=0, sticky="nsew")

    title = tk.Label(frame, text="Match Overview", font=("Arial", 20, "bold"), bg="black", fg="white")
    title.grid(row=0, column=0, columnspan=3, pady=(20, 10))

    lead_label = tk.Label(frame, text="Leading Team: Tie", font=("Arial", 14), bg="black", fg="white")
    lead_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))

    left_panel = tk.Frame(frame, bg="#005500", padx=10, pady=10)
    right_panel = tk.Frame(frame, bg="#550000", padx=10, pady=10)
    left_panel.grid(row=2, column=0, padx=(30, 15), sticky="n")
    right_panel.grid(row=2, column=2, padx=(15, 30), sticky="n")

    spacer = tk.Frame(frame, bg="black", width=40)
    spacer.grid(row=2, column=1)

    def build_team_panel(panel, team_name, team_color, members):
        tk.Label(panel, text=f"{team_name} Team", font=("Arial", 16, "bold"), bg=team_color, fg="white").pack(pady=(0, 10), fill="x")
        total_score = 0
        for player in members:
            card = tk.Frame(panel, bg="black", bd=1, relief="ridge", padx=10, pady=5)
            card.pack(fill="x", pady=4)
            tk.Label(card, text=f"Codename: {player.codename}", font=("Arial", 12, "bold"), bg="black", fg="white").grid(row=0, column=0, sticky="w")
            tk.Label(card, text=f"User ID: {player.user_id}", font=("Arial", 10), bg="black", fg="gray").grid(row=1, column=0, sticky="w")
            tk.Label(card, text=f"Equip ID: {player.equipment_id}", font=("Arial", 10), bg="black", fg="gray").grid(row=1, column=1, sticky="e")
            tk.Label(card, text=f"Base Tagged: {'Yes' if player.tagged_base else 'No'}", font=("Arial", 10), bg="black", fg="gray").grid(row=2, column=0, sticky="w")
            tk.Label(card, text=f"Score: {player.score}", font=("Arial", 10), bg="black", fg="white").grid(row=2, column=1, sticky="e")
            total_score += player.score

        score_label = tk.Label(panel, text=f"{team_name} Team Score: {total_score}", font=("Arial", 12, "bold"), bg=team_color, fg="white")
        score_label.pack(pady=(10, 0), fill="x")
        return total_score

    green_score = build_team_panel(left_panel, "Green", "#007F00", players["green"])
    red_score = build_team_panel(right_panel, "Red", "#AA0000", players["red"])

    if green_score > red_score:
        lead_label.config(text="Leading Team: Green", fg="#00FF00")
    elif red_score > green_score:
        lead_label.config(text="Leading Team: Red", fg="#FF4444")
    else:
        lead_label.config(text="Leading Team: Tie", fg="white")

    countdown_label = tk.Label(frame, text="", font=("Arial", 36, "bold"), bg="black", fg="white")
    countdown_label.grid(row=3, column=0, columnspan=3, pady=20)

    def start_countdown(count=30):
        if count >= 0:
            countdown_label.config(text=f"Game Starts In: {count}")
            frame.after(1000, lambda: start_countdown(count - 1))
        else:
            countdown_label.config(text="Game Started!")
            net.transmit("202")

    control_frame = tk.Frame(frame, bg="black")
    control_frame.grid(row=4, column=0, columnspan=3, pady=30)

    def go_back():
        frame.destroy()
        from ui.entry_screen import launch_entry_screen
        launch_entry_screen(root, db, net, players)

    tk.Button(control_frame, text="Back to Entry", font=("Arial", 11), height=2, bd=2, relief="raised", highlightthickness=0, command=go_back).grid(row=0, column=0, padx=20)
    tk.Button(control_frame, text="Start Game", font=("Arial", 11), height=2, bd=2, relief="raised", highlightthickness=0, command=start_countdown).grid(row=0, column=1, padx=20)
