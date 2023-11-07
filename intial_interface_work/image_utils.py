import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import face_recognition
import cv2

def load_image(image_label):
    file_path = filedialog.askopenfilename()

    if file_path:
        #image = Image.open(file_path)  # Open the selected image file
        #image = ImageTk.PhotoImage(image)  # Convert the image to Tkinter PhotoImage format

        elo = face_recognition.load_image_file(file_path)
        face_locations = face_recognition.face_locations(elo)

        if face_locations:
            for face_location in face_locations:
                top, right, bottom, left = face_location 
                face_image = elo[:, :]
                padding = 0
                cv2.rectangle(face_image, (left - padding , top - padding ), (right + padding , bottom+ padding), (255,0,0), 2)

            #padding = 0
            #cv2.rectangle(face_image, (left - padding , top - padding ), (right + padding , bottom+ padding), (255,0,0), 2)

            pil_image = Image.fromarray(face_image) # Convert NumPy array to PIL Image
            tk_image = ImageTk.PhotoImage(pil_image)  # Convert PIL Image to Tkinter PhotoImage

            image_label.config(image=tk_image)  # Set the image to the label
            image_label.image = tk_image 
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