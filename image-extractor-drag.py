import tkinter as tk
from tkinter import filedialog, ttk
import cv2
import os
from tkinterdnd2 import TkinterDnD, DND_FILES

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

def drop_file(event):
    file_label.config(text=event.data)
    file_label.config(bg="white")  # Revert background color after drop

def drop_folder(event):
    folder_label.config(text=event.data)
    folder_label.config(bg="white")  # Revert background color after drop

def on_drag_enter(event, label):
    label.config(bg="lightblue")  # Highlight drop area

def on_drag_leave(event, label):
    label.config(bg="white")  # Revert background color when dragging leaves the label

def extract_frames(video_path, sample_rate, output_folder, rotation, compression):
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
            cv2.imwrite(frame_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), compression])  # Apply compression
        count += 1
    cap.release()

def batch_process():
    folder_path = folder_label.cget("text")
    sample_rate = sample_rate_entry.get()
    rotation = rotation_var.get()
    compression = compression_slider.get()

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
        extract_frames(video_path, sample_rate, output_folder, rotation, compression)
    status_label.config(text="Batch processing completed.")

def process_video():
    file_path = file_label.cget("text")
    sample_rate = sample_rate_entry.get()
    rotation = rotation_var.get()
    compression = compression_slider.get()

    if not sample_rate.isdigit() or int(sample_rate) <= 0:
        status_label.config(text="Please enter a valid positive integer for the sample rate.")
        return

    sample_rate = int(sample_rate)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_folder = os.path.join(os.path.dirname(file_path), f"{base_name}_frames")
    status_label.config(text="Processing video...")
    root.update_idletasks()  # Update the GUI to reflect changes
    extract_frames(file_path, sample_rate, output_folder, rotation, compression)
    status_label.config(text="Video processing completed.")

root = TkinterDnD.Tk()
root.title("Video Frame Extractor")
root.geometry("400x700")
root.configure(padx=10, pady=10)

# File Selection Frame
file_frame = tk.Frame(root)
file_frame.pack(fill="x", pady=5)

file_label = tk.Label(file_frame, text="Drag a video file here or click to select", anchor="w", bg="white", relief="solid")
file_label.pack(fill="x", ipady=10)
file_label.drop_target_register(DND_FILES)
file_label.dnd_bind('<<Drop>>', drop_file)
file_label.dnd_bind('<<DragEnter>>', lambda event: on_drag_enter(event, file_label))
file_label.dnd_bind('<<DragLeave>>', lambda event: on_drag_leave(event, file_label))

file_button = tk.Button(file_frame, text="Select Video File", command=select_file)
file_button.pack(pady=5)

# Folder Selection Frame
folder_frame = tk.Frame(root)
folder_frame.pack(fill="x", pady=5)

folder_label = tk.Label(folder_frame, text="Drag a folder here or click to select", anchor="w", bg="white", relief="solid")
folder_label.pack(fill="x", ipady=10)
folder_label.drop_target_register(DND_FILES)
folder_label.dnd_bind('<<Drop>>', drop_folder)
folder_label.dnd_bind('<<DragEnter>>', lambda event: on_drag_enter(event, folder_label))
folder_label.dnd_bind('<<DragLeave>>', lambda event: on_drag_leave(event, folder_label))

folder_button = tk.Button(folder_frame, text="Select Folder for Batch Processing", command=select_folder)
folder_button.pack(pady=5)

# Sample Rate Frame
sample_rate_frame = tk.Frame(root)
sample_rate_frame.pack(fill="x", pady=5)

sample_rate_label = tk.Label(sample_rate_frame, text="Enter Sample Rate (fps):", anchor="w")
sample_rate_label.pack(fill="x")

sample_rate_entry = tk.Entry(sample_rate_frame)
sample_rate_entry.pack(fill="x", pady=5)

# Rotation Option Frame
rotation_frame = tk.Frame(root)
rotation_frame.pack(fill="x", pady=5)

rotation_label = tk.Label(rotation_frame, text="Select Rotation:", anchor="w")
rotation_label.pack(fill="x")

rotation_var = tk.StringVar(value="No Rotation")
rotation_options = ["No Rotation", "Rotate Left 90°", "Rotate Right 90°"]
rotation_menu = tk.OptionMenu(rotation_frame, rotation_var, *rotation_options)
rotation_menu.pack(fill="x", pady=5)

# Compression Slider Frame
compression_frame = tk.Frame(root)
compression_frame.pack(fill="x", pady=5)

compression_label = tk.Label(compression_frame, text="JPEG Compression Level (0-100):", anchor="w")
compression_label.pack(fill="x")

compression_slider = tk.Scale(compression_frame, from_=0, to=100, orient="horizontal", tickinterval=10)
compression_slider.set(90)  # Default value for high quality
compression_slider.pack(fill="x", pady=5)

# Process Buttons
process_frame = tk.Frame(root)
process_frame.pack(fill="x", pady=10)

process_button = tk.Button(process_frame, text="Process Video", command=process_video)
process_button.pack(fill="x", pady=5)

batch_button = tk.Button(process_frame, text="Batch Process Folder", command=batch_process)
batch_button.pack(fill="x", pady=5)

# Status Label
status_label = tk.Label(root, text="Status: Idle", anchor="w", relief="sunken")
status_label.pack(fill="x", pady=10)

root.mainloop()
