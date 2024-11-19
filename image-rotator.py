import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_label.config(text=file_path)

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_label.config(text=folder_path)

def rotate_image(image_path, rotation):
    img = Image.open(image_path)
    
    if rotation == "Left 90°":
        img = img.rotate(90, expand=True)
    elif rotation == "Right 90°":
        img = img.rotate(-90, expand=True)
    elif rotation == "Flip Vertical":
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    
    return img

def process_images(image_paths, rotation, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for image_path in image_paths:
        img = rotate_image(image_path, rotation)
        base_name = os.path.basename(image_path)
        output_path = os.path.join(output_folder, base_name)
        img.save(output_path)

def process_file():
    file_path = file_label.cget("text")
    rotation = rotation_var.get()

    if not rotation:
        status_label.config(text="Please select a rotation option.")
        return
    
    output_folder = os.path.join(os.path.dirname(file_path), "rotated")
    process_images([file_path], rotation, output_folder)
    
    status_label.config(text=f"Image saved to {output_folder}")

def batch_process():
    folder_path = folder_label.cget("text")
    rotation = rotation_var.get()

    if not rotation:
        status_label.config(text="Please select a rotation option.")
        return
    
    image_files = [f for f in os.listdir(folder_path) if f.endswith((".jpg", ".jpeg", ".png"))]
    image_paths = [os.path.join(folder_path, f) for f in image_files]
    output_folder = os.path.join(folder_path, "rotated")
    
    process_images(image_paths, rotation, output_folder)
    
    status_label.config(text=f"Images saved to {output_folder}")

root = tk.Tk()
root.title("Image Rotator")

file_label = tk.Label(root, text="No file selected")
file_label.pack()

file_button = tk.Button(root, text="Select Image File", command=select_file)
file_button.pack()

folder_label = tk.Label(root, text="No folder selected")
folder_label.pack()

folder_button = tk.Button(root, text="Select Folder for Batch Processing", command=select_folder)
folder_button.pack()

rotation_var = tk.StringVar()

rotation_label = tk.Label(root, text="Select Rotation:")
rotation_label.pack()

rotation_options = ["Left 90°", "Right 90°", "Flip Vertical"]
for option in rotation_options:
    tk.Radiobutton(root, text=option, variable=rotation_var, value=option).pack()

process_button = tk.Button(root, text="Process Image", command=process_file)
process_button.pack()

batch_button = tk.Button(root, text="Batch Process Folder", command=batch_process)
batch_button.pack()

status_label = tk.Label(root, text="Status: Idle")
status_label.pack()

root.mainloop()
