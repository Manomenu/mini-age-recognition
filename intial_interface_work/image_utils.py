import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def load_image(image_label):
    file_path = filedialog.askopenfilename()

    if file_path:
        image = Image.open(file_path)  # Open the selected image file
        image = ImageTk.PhotoImage(image)  # Convert the image to Tkinter PhotoImage format
        image_label.config(image=image)  # Set the image to the label
        image_label.image = image  # Keep a reference to the image to prevent it from being garbage collected
    return 


def load_folder(canvas_frame):
    folder_path = filedialog.askdirectory()  # Open a directory dialog to choose a folder
    if folder_path:
        image_files = [file for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        images = []
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            original_image = Image.open(image_path)
            resized_image = original_image.resize((100, 300))  # Resize the image to specific width and height
            image = ImageTk.PhotoImage(resized_image)
            images.append(image)

        if images:
            #canvas_frame.delete("all")  # Clear the canvas
            canvas = tk.Canvas(canvas_frame)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            canvas.config(yscrollcommand=scrollbar.set)
            canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window=frame, anchor='nw')

            for image in images:
                image_label = tk.Label(frame, image=image)
                image_label.image = image  # Keep a reference to the image to prevent it from being garbage collected
                image_label.pack()

            frame.update_idletasks()  # Update the frame to calculate the proper scroll region

            canvas.config(scrollregion=canvas.bbox("all"))