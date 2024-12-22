import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from datetime import datetime
import random

def split_dataset():
    try:
        source_folder = filedialog.askdirectory(title="Select Source Folder")
        if not source_folder:
            messagebox.showerror("Error", "No folder selected for splitting.")
            return

        output_folder = filedialog.askdirectory(title="Select Output Folder")
        if not output_folder:
            messagebox.showerror("Error", "No output folder selected.")
            return

        train_ratio = float(train_ratio_entry.get())
        valid_ratio = float(valid_ratio_entry.get())
        test_ratio = 1 - train_ratio - valid_ratio

        if train_ratio + valid_ratio >= 1 or train_ratio < 0 or valid_ratio < 0:
            messagebox.showerror("Error", "Invalid train/valid/test ratio.")
            return

        images_folder = os.path.join(source_folder, "images")
        labels_folder = os.path.join(source_folder, "labels")

        if not os.path.exists(images_folder) or not os.path.exists(labels_folder):
            messagebox.showerror("Error", "Source folder must contain 'images' and 'labels'.")
            return

        all_images = os.listdir(images_folder)
        random.shuffle(all_images)

        # Check for missing images or labels
        for label_file in os.listdir(labels_folder):
            image_name = os.path.splitext(label_file)[0] + ".jpg"  # Assuming .jpg images
            image_path = os.path.join(images_folder, image_name)
            label_path = os.path.join(labels_folder, label_file)
            if not os.path.exists(image_path):
                os.remove(label_path)
                print(f"Removed missing label file: {label_file}")

        train_count = int(len(all_images) * train_ratio)
        valid_count = int(len(all_images) * valid_ratio)

        subsets = {
            "train": all_images[:train_count],
            "valid": all_images[train_count:train_count + valid_count],
            "test": all_images[train_count + valid_count:]
        }

        for subset, images in subsets.items():
            subset_images_folder = os.path.join(output_folder, subset, "images")
            subset_labels_folder = os.path.join(output_folder, subset, "labels")
            os.makedirs(subset_images_folder, exist_ok=True)
            os.makedirs(subset_labels_folder, exist_ok=True)

            for image in images:
                image_path = os.path.join(images_folder, image)
                label_path = os.path.join(labels_folder, os.path.splitext(image)[0] + ".txt")
                shutil.copy(image_path, subset_images_folder)
                # Copy label file only if it exists
                if os.path.exists(label_path):
                    shutil.copy(label_path, subset_labels_folder)

        messagebox.showinfo("Success", "Dataset split completed.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        
# Function to merge dataset
def merge_dataset():
    try:
        folders = []
        for subset in ["train", "valid", "test"]:
            folder = filedialog.askdirectory(title=f"Select {subset} Folder")
            if not folder:
                messagebox.showerror("Error", f"No folder selected for {subset}.")
                return
            folders.append(folder)

        root_directory = filedialog.askdirectory(title="Select Root Directory for Merged Dataset")
        if not root_directory:
            messagebox.showerror("Error", "No root directory selected.")
            return

        # Generate a folder name with the current date
        merged_folder_name = f"merged_{datetime.now().strftime('%Y-%m-%d')}"
        merged_folder = os.path.join(root_directory, merged_folder_name)
        images_output = os.path.join(merged_folder, "images")
        labels_output = os.path.join(merged_folder, "labels")
        os.makedirs(images_output, exist_ok=True)
        os.makedirs(labels_output, exist_ok=True)

        for folder in folders:
            for subset in ["images", "labels"]:
                subset_folder = os.path.join(folder, subset)
                for item in os.listdir(subset_folder):
                    source_path = os.path.join(subset_folder, item)
                    target_path = os.path.join(images_output if subset == "images" else labels_output, item)
                    shutil.copy(source_path, target_path)

        messagebox.showinfo("Success", f"Merged dataset created at: {merged_folder}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Dataset Split and Merge Tool")
root.geometry("400x300")
root.configure(padx=10, pady=10)

# Split Frame
split_frame = tk.LabelFrame(root, text="Split Dataset", padx=10, pady=10)
split_frame.pack(fill="x", pady=10)

tk.Label(split_frame, text="Train Ratio:").grid(row=0, column=0, sticky="w")
train_ratio_entry = tk.Entry(split_frame)
train_ratio_entry.grid(row=0, column=1)
train_ratio_entry.insert(0, "0.7")

tk.Label(split_frame, text="Validation Ratio:").grid(row=1, column=0, sticky="w")
valid_ratio_entry = tk.Entry(split_frame)
valid_ratio_entry.grid(row=1, column=1)
valid_ratio_entry.insert(0, "0.2")

split_button = tk.Button(split_frame, text="Split Dataset", command=split_dataset)
split_button.grid(row=2, column=0, columnspan=2, pady=5)

# Merge Frame
merge_frame = tk.LabelFrame(root, text="Merge Dataset", padx=10, pady=10)
merge_frame.pack(fill="x", pady=10)

merge_button = tk.Button(merge_frame, text="Merge Dataset", command=merge_dataset)
merge_button.pack(pady=5)

# Status Label
status_label = tk.Label(root, text="Status: Idle", relief="sunken", anchor="w")
status_label.pack(fill="x", pady=10)

root.mainloop()
