import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import face_recognition
import threading
import cv2
import random
import time
import numpy as np
from edge_filter import apply_edge_filter, filterer

is_update_frame_running = False

font_size = 1
font_face = cv2.FONT_HERSHEY_SIMPLEX
font_color = (255,255,255)
line_type = 4

def load_image(image_label, window, model):
    file_path = filedialog.askopenfilename()
     
    if file_path:
        face_image=None
        #image = Image.open(file_path)  # Open the selected image file
        #image = ImageTk.PhotoImage(image)  # Convert the image to Tkinter PhotoImage format
        elo = face_recognition.load_image_file(file_path)
        face_locations = face_recognition.face_locations(elo)
        if face_locations:
            for face_location in face_locations:
                top, right, bottom, left = face_location 
                face_image = elo[:, :]
                
                cropped_and_resized = reize_to_required_size(elo[top:bottom,left:right].copy())

                drawBoundingBoxWithAgeEstimate(face_image, left, top, bottom, right, predict_age(model, cropped_and_resized))
           
        max_width = window.winfo_width()
        max_height = window.winfo_height()
        if face_image is None:
            face_image=elo
       
        pil_image = Image.fromarray(face_image)
        pil_image = pil_image.resize((max_width, max_height), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(pil_image)

        image_label.config(image=tk_image)
        image_label.image = tk_image
       
    return 

def load_folder(model, window):
    folder_path = filedialog.askdirectory()  # Open a directory dialog to choose a folder
    if folder_path:
        folder_thread = threading.Thread(target=process_folder_thread, args=(model, window, folder_path))
        folder_thread.start()

def process_folder_thread(model, window, folder_path):
    result_folder = os.path.join(folder_path, 'result')
    image_files = [file for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    images_count = len(image_files)  
    processed_images = 0
    progress_label = tk.Label(window, text="Processing folder", font=('Helvetica', 12))
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(window, length=300, mode='indeterminate')
    progress_bar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the progress bar
    progress_bar.start()
    window.update()

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        # original_image = Image.open(image_path)
        # image = ImageTk.PhotoImage(original_image)

        face_rec_image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(face_rec_image)
        if face_locations:
            for face_location in face_locations:
                top, right, bottom, left = face_location 
                face_image = face_rec_image[:, :]

                cropped_and_resized = reize_to_required_size(face_rec_image[top:bottom,left:right].copy())

                drawBoundingBoxWithAgeEstimate(face_image, left, top, bottom, right, predict_age(model, cropped_and_resized))

        os.makedirs(result_folder, exist_ok=True)
        pil_image = Image.fromarray(face_rec_image)
        result_image_path = os.path.join(result_folder, f"result_{image_file}")
        pil_image.save(result_image_path, quality=95)

    progress_bar.stop()
    progress_bar.destroy()
    progress_label.destroy()

# pierwsza 


def toggle_camera(image_label, vid, window, model):
    global is_update_frame_running

   
    if is_update_frame_running:
        is_update_frame_running = False
        if vid.isOpened():
            vid.release()
       
        image_label.photo_image = None
    else:
        
        if not vid.isOpened():
            vid = cv2.VideoCapture(0) 
            width, height = 700, 400
  

            vid.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
            vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 

        
        is_update_frame_running = True
        open_camera2(image_label, vid, window,model)


def open_camera2(image_label, vid, window, model):
    # Initialize some variables
    global is_update_frame_running
    face_locations = []
    process_this_frame = True
    frame_count = 0  # Counter for the frames saved
    save_folder = "results"  # Folder to save frames
    frame = None

    # Create the results folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    def on_key(event):
        nonlocal frame_count, frame, save_folder
        if event.char == 's':
            print(f"Will try to save")
            frame_count += 1
            save_path = os.path.join(save_folder, f"frame{frame_count}.jpg")
            cv2.imwrite(save_path, frame)
            print(f"Frame saved as {save_path}")

    window.bind('<KeyPress>', on_key)

    # Function to update the frame in the Tkinter label
    def update_frame():
        nonlocal process_this_frame, face_locations, frame
        # Grab a single frame of video

        if not is_update_frame_running:
            return 
        
        ret, frame = vid.read()
       
        
        if not ret:
            print("Failed to grab frame")
            image_label.after(10, update_frame)
            return
        frame = cv2.flip(frame, 1)
        if process_this_frame:
           small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
           rgb_small_frame = small_frame[:, :, ::-1]
           face_locations = face_recognition.face_locations(rgb_small_frame)
            
        process_this_frame = not process_this_frame
        # Display the results
        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cropped_and_resized = reize_to_required_size(frame[top:bottom,left:right].copy())
            drawBoundingBoxWithAgeEstimate(frame, left, top, bottom, right, predict_age(model, cropped_and_resized))
        
        max_height = window.winfo_height()
        max_width = window.winfo_width()
       

        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        pil_image = pil_image.resize((max_width, max_height), Image.LANCZOS)
        photo_image = ImageTk.PhotoImage(pil_image)

        image_label.photo_image = photo_image
        image_label.configure(image=photo_image)

        image_label.after(10, update_frame)

    update_frame()


def load_video(image_label, window, window_width, window_height, model):
    video_thread = threading.Thread(target=process_video_thread, args=(image_label, window, window_width, window_height, model))
    video_thread.start()

def display_processed_video(image_label, video_path, window_width, window_height, window, total_frames):

    progress_label = tk.Label(window, text="Loading your video...", font=('Helvetica', 12))
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(window, length=300, mode='indeterminate')
    progress_bar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the progress bar
    progress_bar.start()
    window.update()

    vid = cv2.VideoCapture(video_path)
    frames = []

    while True:
        ret, frame = vid.read()

        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (window_width, window_height))
        frames.append(frame)

    vid.release()
    progress_bar.stop()
    progress_bar.destroy()
    progress_label.destroy()

    tk_images = [ImageTk.PhotoImage(Image.fromarray(frame)) for frame in frames]

    # Display the processed frames in the Tkinter window
    for tk_image in tk_images:
        image_label.config(image=tk_image)
        image_label.image = tk_image
        image_label.update_idletasks()
        time.sleep(1 / 20)  # Adjust the sleep time according to the video's frame rate

    # Clear the displayed video after processing
    image_label.config(image=None)
    image_label.image = None

def drawBoundingBoxWithAgeEstimate(image, left, top, bottom, right, ageEstimate):
    padding = 2
    cv2.rectangle(image, (left - padding , top - padding ), (right + padding , bottom+ padding), (36,255,12), 5)
    label = str(ageEstimate)
    (w, h), _ = cv2.getTextSize(label, font_face,  font_size, line_type)

    cv2.rectangle(image, (left , top - h - padding ), (left + w + padding, top), (36,255,12), 5)
    cv2.rectangle(image, (left , top - h - padding ), (left + w + padding, top), (36,255,12), -1)
    cv2.putText(image, label ,(left, top), font_face, font_size ,font_color ,line_type)
    
def process_video_thread(image_label, window, window_width, window_height, model):
    if hasattr(image_label, 'image'):
        image_label.image = None
        image_label.config(image=None)

    video_path = filedialog.askopenfilename()
    if not video_path.lower().endswith(('.mp4')):
        print("wrong file format")
        return

    progress_label = tk.Label(window, text="Processing video...", font=('Helvetica', 12))
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(window, length=300, mode='determinate')
    progress_bar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the progress bar
    progress_bar.start()
    window.update()

    vid = cv2.VideoCapture(video_path)

    # Get video information
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    result_folder = os.path.join(os.path.dirname(video_path), 'result')
    os.makedirs(result_folder, exist_ok=True)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change the codec as needed
    result_video_path = os.path.join(result_folder, "result_video.mp4")
    out = cv2.VideoWriter(result_video_path, fourcc, fps, (width, height))
    total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

    while True:
        ret, frame = vid.read()
        if not ret:
            print("Video processing completed.")
            break

        frame = cv2.flip(frame, 1)

        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
           # Convert BGR to RGB
        rgb_small_frame = small_frame[:, :, ::-1]
        # Find all the faces and face encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)

        # Display the results
        for (top, right, bottom, left) in face_locations:
            top *=2
            right *=2
            bottom *=2
            left *=2

            cropped_and_resized = reize_to_required_size(frame[top:bottom,left:right].copy())
            drawBoundingBoxWithAgeEstimate(frame, left, top, bottom, right, predict_age(model, cropped_and_resized))
        
        # Write the modified frame to the output video file
        out.write(frame)

        current_frame = int(vid.get(cv2.CAP_PROP_POS_FRAMES))
        progress_value = int((current_frame / total_frames) * 100)
        progress_bar['value'] = progress_value
        # window.update_idletasks()

    progress_bar.stop()
    progress_bar.destroy()
    progress_label.destroy()
    # Release the VideoCapture and VideoWriter objects
    vid.release()
    out.release()

    display_processed_video(image_label, result_video_path, window_width, window_height, window, total_frames)
    return


def predict_age(model, face_image):
    face_image = filterer.filter_data(face_image)
    prediction = model.predict(np.expand_dims(face_image,axis=0), verbose = 0)
    return prediction[0]


def reize_to_required_size(face_image):
    resized = cv2.resize(face_image, dsize=(200, 200), interpolation=cv2.INTER_CUBIC)
    array = np.array(resized)
    return array