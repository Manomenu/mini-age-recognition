import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from image_utils import load_image, load_folder

def exit_program():
    window.destroy()


def load_camera():
    return

window = tk.Tk()
window.title("Simple Window")
window.geometry("300x200")

menu_bar = tk.Menu(window)

canvas_frame = tk.Frame(window)
canvas_frame.pack(fill=tk.BOTH, expand=True)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Image", command=lambda: load_image(image_label))
file_menu.add_command(label="Folder", command=lambda: load_folder(canvas_frame))
file_menu.add_command(label="Camera", command=load_camera)
menu_bar.add_cascade(label="Menu", menu=file_menu)

menu_bar.add_command(label="Exit", command=exit_program)

window.config(menu=menu_bar)

image_label = tk.Label(window)
image_label.pack()

window.geometry("700x400")
window.title("Age recognition")
window.mainloop()
