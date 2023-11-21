import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from image_utils import load_image, load_folder, open_camera2,toggle_camera
import cv2

def exit_program():
    window.destroy()


 #Define a video capture object 
vid = cv2.VideoCapture(0) 
  
# Declare the width and height in variables 
width, height = 700, 400
  
# Set the width and height 
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 

window = tk.Tk()
window.title("Simple Window")
window.geometry("600x400")

menu_bar = tk.Menu(window)

canvas_frame = tk.Frame(window)
canvas_frame.pack(fill=tk.BOTH, expand=True)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Image", command=lambda: load_image(image_label, window))
file_menu.add_command(label="Folder", command=lambda: load_folder(canvas_frame))
file_menu.add_command(label="Camera", command=lambda:toggle_camera(image_label,vid))
menu_bar.add_cascade(label="Menu", menu=file_menu)

menu_bar.add_command(label="Exit", command=exit_program)

window.config(menu=menu_bar)

image_label = tk.Label(window)
image_label.pack()

window.geometry("1000x600")
window.title("Age recognition")
window.mainloop()



