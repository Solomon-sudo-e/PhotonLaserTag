
import tkinter as tk
from data.database import PlayerDatabase
from networking.udp_connection import UDPConnection
from ui.splash import display_intro_screen

def on_splash_complete(root, db, net):
    from ui.entry_screen import launch_entry_screen
    launch_entry_screen(root, db, net)

def start_app():
    db = PlayerDatabase(use_mock=True)
    db.connect()
    db.initialize()

    net = UDPConnection()
    net.initialize()

    root = tk.Tk()
    root.title("Photon Refactored")
    root.configure(background="white")
    root.attributes('-fullscreen', True)
    root.resizable(False, False)

    root.bind("<Escape>", lambda e: shutdown(root, db, net))
    root.protocol("WM_DELETE_WINDOW", lambda: shutdown(root, db, net))

    display_intro_screen(root, "assets/logo.jpg", 3000, lambda: on_splash_complete(root, db, net))
    root.mainloop()

def shutdown(root, db, net):
    db.close()
    net.shutdown()
    root.destroy()

if __name__ == "__main__":
    start_app()
