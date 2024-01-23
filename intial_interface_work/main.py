import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from image_utils import load_image, load_folder, toggle_camera, load_video
import cv2

import tensorflow as tf
from tensorflow import keras


def exit_program():
    window.destroy()

def load_model():
    new_model = tf.keras.models.load_model("my_model.h5")
    return new_model

age_prediction_model = load_model()

 #Define a video capture object 
vid = cv2.VideoCapture(0) 
  
# Declare the width and height in variables 
width, height = 700, 400
  
# Set the width and height 
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 

window = tk.Tk()
# window.title("Simple Window")
# window.geometry("600x400")

menu_bar = tk.Menu(window)

canvas_frame = tk.Frame(window)
canvas_frame.pack(fill=tk.BOTH, expand=True)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Image file", command=lambda: load_image(image_label, window, age_prediction_model))
file_menu.add_command(label="Folder", command=lambda: load_folder(age_prediction_model))
file_menu.add_command(label="Camera", command=lambda:toggle_camera(image_label,vid, window, age_prediction_model))
file_menu.add_command(label="Video", command=lambda:load_video(image_label, window, 1000, 600, age_prediction_model))
menu_bar.add_cascade(label="Menu", menu=file_menu)

menu_bar.add_command(label="Exit", command=exit_program)

window.config(menu=menu_bar)

image_label = tk.Label(window)
image_label.pack()

window.geometry("1000x600")
window.title("Age recognition")
window.mainloop()






