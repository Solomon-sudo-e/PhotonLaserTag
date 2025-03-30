
import tkinter as tk
from PIL import Image, ImageTk
import os


def display_intro_screen(root: tk.Tk, image_path: str, delay: int, on_complete) -> None:
    try:
        image = Image.open(image_path)
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        image = image.resize((width, height))
        image_obj = ImageTk.PhotoImage(image)

        label = tk.Label(root, image=image_obj, bg="black")
        label.place(x=0, y=0, relwidth=1, relheight=1)
        label.image = image_obj

        root.after(delay, lambda: [label.destroy(), on_complete()])
    except Exception as e:
        print(f"[UI] Splash screen error: {e}")
        on_complete()
