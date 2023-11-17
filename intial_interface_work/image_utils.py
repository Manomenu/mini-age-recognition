import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import face_recognition
import cv2
is_update_frame_running = False

def load_image(image_label, window):
    file_path = filedialog.askopenfilename()

    if file_path:
        #image = Image.open(file_path)  # Open the selected image file
        

        elo = face_recognition.load_image_file(file_path)
        face_locations = face_recognition.face_locations(elo)

        if face_locations:
            for face_location in face_locations:
                top, right, bottom, left = face_location 
                face_image = elo[:, :]
                padding = 0
                cv2.rectangle(face_image, (left - padding , top - padding ), (right + padding , bottom+ padding), (255,0,0), 2)
       
            padding = 0
            cv2.rectangle(face_image, (left - padding , top - padding ), (right + padding , bottom+ padding), (255,0,0), 2)

        max_width = window.winfo_width()
        max_height = window.winfo_height()
       # face_image=face_recognition(elo);
        pil_image = Image.fromarray(face_image) # Convert NumPy array to PIL Image

        pil_image.thumbnail((max_width, max_height), Image.LANCZOS)
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


# pierwsza 

#https://www.geeksforgeeks.org/how-to-show-webcam-in-tkinter-window-python/

def toggle_camera(image_label, vid):
    global is_update_frame_running

   
    if is_update_frame_running:
        is_update_frame_running = False
        if vid.isOpened():
            vid.release()
       
        image_label.photo_image = None
    else:
        
        if not vid.isOpened():
            vid.open(0)


        
        is_update_frame_running = True
        open_camera2(image_label, vid)


def open_camera2(image_label, vid):
    # Initialize some variables
    global is_update_frame_running
    face_locations = []
    process_this_frame = True
    
    # Function to update the frame in the Tkinter label
    def update_frame():
        nonlocal process_this_frame, face_locations;
        # Grab a single frame of video

        if not is_update_frame_running:
            return 
        
        ret, frame = vid.read()
       
        
        if not ret:
            print("Failed to grab frame")
            image_label.after(10, update_frame)
            return

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert BGR to RGB
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings
            face_locations = face_recognition.face_locations(rgb_small_frame)
            

            
            

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
           # font = cv2.FONT_HERSHEY_DUPLEX
           # name="HANDSOME GAY"
            #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
           # cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
            

       
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        photo_image = ImageTk.PhotoImage(pil_image)

        # Update the image_label with the new image
        image_label.photo_image = photo_image
        image_label.configure(image=photo_image)

        # Repeat after an interval to capture the next frame
        image_label.after(10, update_frame)

    update_frame()