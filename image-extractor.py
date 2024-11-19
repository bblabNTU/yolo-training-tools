import tkinter as tk
from tkinter import filedialog
import cv2
import os

# Default directory
default_dir = "/home/chucklab/Data/"

def select_file():
    file_path = filedialog.askopenfilename(initialdir=default_dir)
    if file_path:
        file_label.config(text=file_path)

def select_folder():
    folder_path = filedialog.askdirectory(initialdir=default_dir)
    if folder_path:
        folder_label.config(text=folder_path)

def extract_frames(video_path, sample_rate, output_folder,rotation):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        status_label.config(text=f"Error: Cannot open video {video_path}")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    interval = int(fps / sample_rate)

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    os.makedirs(output_folder, exist_ok=True)

    count = 0                                                                                            
    while True:                       
        ret, frame = cap.read()                                                                          
        if not ret:                                                                                      
            break                                                                                        
        if count % interval == 0:                                                                        
            if rotation == "Rotate Left 90°":
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)                                
            elif rotation == "Rotate Right 90°":                                                         
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)                                       
            frame_name = f"{base_name}_frame_{count // interval}.jpg"                                    
            frame_path = os.path.join(output_folder, frame_name)                                         
            cv2.imwrite(frame_path, frame)                                                               
        count += 1 
    cap.release()

def batch_process():
    folder_path = folder_label.cget("text")
    sample_rate = sample_rate_entry.get()
    rotation = rotation_var.get()

    if not sample_rate.isdigit() or int(sample_rate) <= 0:
        status_label.config(text="Please enter a valid positive integer for the sample rate.")
        return

    sample_rate = int(sample_rate)
    output_folder = os.path.join(folder_path, "output")
    video_files = [f for f in os.listdir(folder_path) if f.endswith((".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".mpeg", ".mpg", ".3gp"))]

    for i, video_file in enumerate(video_files):
        status_label.config(text=f"Processing {video_file} ({i+1}/{len(video_files)})...")
        root.update_idletasks()  # Update the GUI to reflect changes
        video_path = os.path.join(folder_path, video_file)
        extract_frames(video_path, sample_rate, output_folder, rotation)    
    status_label.config(text="Batch processing completed.")

def process_video():
    file_path = file_label.cget("text")
    sample_rate = sample_rate_entry.get()
    rotation = rotation_var.get()

    if not sample_rate.isdigit() or int(sample_rate) <= 0:
        status_label.config(text="Please enter a valid positive integer for the sample rate.")
        return

    sample_rate = int(sample_rate)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_folder = os.path.join(os.path.dirname(file_path), f"{base_name}_frames")
    status_label.config(text="Processing video...")
    root.update_idletasks()  # Update the GUI to reflect changes
    extract_frames(file_path, sample_rate, output_folder, rotation)
    status_label.config(text="Video processing completed.")

root = tk.Tk()
root.title("Video Frame Extractor")

file_label = tk.Label(root, text="No file selected")
file_label.pack()

file_button = tk.Button(root, text="Select Video File", command=select_file)
file_button.pack()

folder_label = tk.Label(root, text="No folder selected")
folder_label.pack()

folder_button = tk.Button(root, text="Select Folder for Batch Processing", command=select_folder)
folder_button.pack()

sample_rate_label = tk.Label(root, text="Enter Sample Rate (fps):")
sample_rate_label.pack()

sample_rate_entry = tk.Entry(root)
sample_rate_entry.pack()

rotation_label = tk.Label(root, text="Select Rotation:")
rotation_label.pack()

rotation_var = tk.StringVar(value="No Rotation")
rotation_options = ["No Rotation", "Rotate Left 90°", "Rotate Right 90°"]
rotation_menu = tk.OptionMenu(root, rotation_var, *rotation_options)
rotation_menu.pack()

process_button = tk.Button(root, text="Process Video", command=process_video)
process_button.pack()

batch_button = tk.Button(root, text="Batch Process Folder", command=batch_process)
batch_button.pack()

status_label = tk.Label(root, text="Status: Idle")
status_label.pack()

root.mainloop()
