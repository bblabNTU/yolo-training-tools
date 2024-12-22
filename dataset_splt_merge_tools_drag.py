import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import os
import shutil
from datetime import datetime
import random
from tkinterdnd2 import TkinterDnD, DND_FILES

def update_status(message):
    status_text.insert(tk.END, message + "\n")
    status_text.see(tk.END)  # Auto-scroll to the bottom
    root.update_idletasks()

def drop_folder(event, label):
    file_path = event.data.replace('{', '').replace('}', '').replace('"', '')
    if os.path.isfile(file_path):
        file_path = os.path.dirname(file_path)
    label.config(text=file_path)
    label.config(bg="white")
    update_status(f"📂 Selected folder: {file_path}")

def on_drag_enter(event, label):
    label.config(bg="lightblue")

def on_drag_leave(event, label):
    label.config(bg="white")

def select_folder(label):
    folder_path = filedialog.askdirectory()
    if folder_path:
        label.config(text=folder_path)
        update_status(f"📂 Selected folder: {folder_path}")

def split_dataset():
    try:
        source_folder = source_label.cget("text")
        output_folder = output_label.cget("text")
        
        if source_folder == "Drag source folder here or click Select":
            messagebox.showerror("Error", "No source folder selected.")
            return
        if output_folder == "Drag output folder here or click Select":
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

        # Clear status and start new processing
        status_text.delete(1.0, tk.END)
        update_status(f"🚀 Starting dataset split...")
        update_status(f"📊 Split ratios - Train: {train_ratio:.1%}, Valid: {valid_ratio:.1%}, Test: {test_ratio:.1%}")

        all_images = os.listdir(images_folder)
        update_status(f"📄 Found {len(all_images)} images")
        
        random.shuffle(all_images)

        # Check for missing images or labels
        missing_count = 0
        for label_file in os.listdir(labels_folder):
            base_name = os.path.splitext(label_file)[0]
            # Check for both .jpg and .png extensions
            image_path_jpg = os.path.join(images_folder, base_name + ".jpg")
            image_path_png = os.path.join(images_folder, base_name + ".png")
            label_path = os.path.join(labels_folder, label_file)
            
            # Only remove if neither jpg nor png exists
            if not os.path.exists(image_path_jpg) and not os.path.exists(image_path_png):
                os.remove(label_path)
                missing_count += 1
                update_status(f"⚠️ Removed orphaned label file: {label_file}")

        train_count = int(len(all_images) * train_ratio)
        valid_count = int(len(all_images) * valid_ratio)

        subsets = {
            "train": all_images[:train_count],
            "valid": all_images[train_count:train_count + valid_count],
            "test": all_images[train_count + valid_count:]
        }

        total_files = len(all_images) * 2  # Images and labels
        processed_files = 0

        for subset, images in subsets.items():
            subset_images_folder = os.path.join(output_folder, subset, "images")
            subset_labels_folder = os.path.join(output_folder, subset, "labels")
            os.makedirs(subset_images_folder, exist_ok=True)
            os.makedirs(subset_labels_folder, exist_ok=True)

            update_status(f"\n📁 Processing {subset} set ({len(images)} images)...")

            for image in images:
                image_path = os.path.join(images_folder, image)
                base_name = os.path.splitext(image)[0]
                label_path = os.path.join(labels_folder, base_name + ".txt")
                
                shutil.copy(image_path, subset_images_folder)
                processed_files += 1
                
                if os.path.exists(label_path):
                    shutil.copy(label_path, subset_labels_folder)
                    processed_files += 1
                else:
                    update_status(f"⚠️ Missing label for {image}")

                # Update progress
                progress = (processed_files / total_files) * 100
                progress_bar['value'] = progress
                progress_label.config(text=f"{progress:.1f}%")
                root.update_idletasks()

        # Final summary
        update_status("\n📊 Split Summary:")
        update_status(f"Train set: {len(subsets['train'])} images")
        update_status(f"Valid set: {len(subsets['valid'])} images")
        update_status(f"Test set: {len(subsets['test'])} images")
        update_status("\n✨ Dataset split completed successfully!")

    except Exception as e:
        update_status(f"❌ Error: {str(e)}")

def merge_dataset():
    try:
        train_folder = train_label.cget("text")
        valid_folder = valid_label.cget("text")
        test_folder = test_label.cget("text")
        merged_output = merged_output_label.cget("text")

        if any(folder == "Drag folder here or click Select" for folder in 
              [train_folder, valid_folder, test_folder, merged_output]):
            messagebox.showerror("Error", "Please select all required folders.")
            return

        # Clear status and start new processing
        status_text.delete(1.0, tk.END)
        update_status("🚀 Starting dataset merge...")

        # Generate merged folder name
        merged_folder_name = f"merged_{datetime.now().strftime('%Y-%m-%d')}"
        merged_folder = os.path.join(merged_output, merged_folder_name)
        images_output = os.path.join(merged_folder, "images")
        labels_output = os.path.join(merged_folder, "labels")
        os.makedirs(images_output, exist_ok=True)
        os.makedirs(labels_output, exist_ok=True)

        total_files = 0
        processed_files = 0

        # Count total files first
        for folder in [train_folder, valid_folder, test_folder]:
            for subset in ["images", "labels"]:
                subset_folder = os.path.join(folder, subset)
                if os.path.exists(subset_folder):
                    total_files += len(os.listdir(subset_folder))

        update_status(f"📄 Found {total_files} total files to merge")

        # Process each folder
        for folder, name in [(train_folder, "train"), (valid_folder, "valid"), (test_folder, "test")]:
            update_status(f"\n📁 Processing {name} folder...")
            
            for subset in ["images", "labels"]:
                subset_folder = os.path.join(folder, subset)
                if not os.path.exists(subset_folder):
                    update_status(f"⚠️ Missing {subset} folder in {name}")
                    continue
                    
                for item in os.listdir(subset_folder):
                    source_path = os.path.join(subset_folder, item)
                    target_path = os.path.join(images_output if subset == "images" else labels_output, item)
                    shutil.copy(source_path, target_path)
                    processed_files += 1
                    
                    # Update progress
                    progress = (processed_files / total_files) * 100
                    progress_bar['value'] = progress
                    progress_label.config(text=f"{progress:.1f}%")
                    root.update_idletasks()

        # Final summary
        update_status("\n📊 Merge Summary:")
        update_status(f"Total files processed: {processed_files}")
        update_status(f"Merged dataset location: {merged_folder}")
        update_status("\n✨ Dataset merge completed successfully!")

    except Exception as e:
        update_status(f"❌ Error: {str(e)}")

# GUI Setup
root = TkinterDnD.Tk()
root.title("Dataset Split and Merge Tool")
root.geometry("800x900")
root.configure(padx=20, pady=20)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, pady=5)

# Split Tab
split_tab = ttk.Frame(notebook)
notebook.add(split_tab, text="Split Dataset")

# Instructions frame for split tab
instructions_frame = tk.LabelFrame(split_tab, text="Instructions", padx=10, pady=5)
instructions_frame.pack(fill="x", pady=5)

instructions_text = """Requirements:
- Source folder must contain two subfolders: 'images' and 'labels'
- Images: Supported formats are PNG and JPG
- Labels: Must be YOLO format TXT files
- Filenames: Label files must match image names (e.g., image1.png → image1.txt)

Process:
1. Select source folder (with 'images' and 'labels' subfolders)
2. Choose output folder for the split dataset
3. Set train/validation ratios (test = remaining %)
4. Click 'Split Dataset' to process"""

tk.Label(instructions_frame, text=instructions_text, justify=tk.LEFT,
        anchor="w", padx=5, pady=5).pack(fill="x")

# Source folder frame
source_frame = tk.LabelFrame(split_tab, text="Source Folder (must contain 'images' and 'labels' subfolders)", padx=10, pady=5)
source_frame.pack(fill="x", pady=5)

source_label = tk.Label(source_frame, text="Drag source folder here or click Select",
                       bg="white", relief="solid", padx=5)
source_label.pack(fill="x", ipady=10, pady=5)
source_label.drop_target_register(DND_FILES)
source_label.dnd_bind('<<Drop>>', lambda e: drop_folder(e, source_label))
source_label.dnd_bind('<<DragEnter>>', lambda e: on_drag_enter(e, source_label))
source_label.dnd_bind('<<DragLeave>>', lambda e: on_drag_leave(e, source_label))

source_button = tk.Button(source_frame, text="Select Source",
                         command=lambda: select_folder(source_label))
source_button.pack(pady=5)

# Output folder frame
output_frame = tk.LabelFrame(split_tab, text="Output Folder", padx=10, pady=5)
output_frame.pack(fill="x", pady=5)

output_label = tk.Label(output_frame, text="Drag output folder here or click Select",
                       bg="white", relief="solid", padx=5)
output_label.pack(fill="x", ipady=10, pady=5)
output_label.drop_target_register(DND_FILES)
output_label.dnd_bind('<<Drop>>', lambda e: drop_folder(e, output_label))
output_label.dnd_bind('<<DragEnter>>', lambda e: on_drag_enter(e, output_label))
output_label.dnd_bind('<<DragLeave>>', lambda e: on_drag_leave(e, output_label))

output_button = tk.Button(output_frame, text="Select Output",
                         command=lambda: select_folder(output_label))
output_button.pack(pady=5)

# Ratio frame
ratio_frame = tk.LabelFrame(split_tab, text="Split Ratios", padx=10, pady=5)
ratio_frame.pack(fill="x", pady=5)

tk.Label(ratio_frame, text="Train Ratio:").grid(row=0, column=0, sticky="w", pady=2)
train_ratio_entry = tk.Entry(ratio_frame)
train_ratio_entry.grid(row=0, column=1, pady=2)
train_ratio_entry.insert(0, "0.7")

tk.Label(ratio_frame, text="Validation Ratio:").grid(row=1, column=0, sticky="w", pady=2)
valid_ratio_entry = tk.Entry(ratio_frame)
valid_ratio_entry.grid(row=1, column=1, pady=2)
valid_ratio_entry.insert(0, "0.2")

tk.Label(ratio_frame, text="Test Ratio: (auto-calculated)").grid(row=2, column=0, columnspan=2, sticky="w", pady=2)

split_button = tk.Button(split_tab, text="Split Dataset", command=split_dataset)
split_button.pack(pady=10)

# Merge Tab
merge_tab = ttk.Frame(notebook)
notebook.add(merge_tab, text="Merge Dataset")

# Train folder frame
train_frame = tk.LabelFrame(merge_tab, text="Train Folder", padx=10, pady=5)
train_frame.pack(fill="x", pady=5)

train_label = tk.Label(train_frame, text="Drag folder here or click Select",
                      bg="white", relief="solid", padx=5)
train_label.pack(fill="x", ipady=10, pady=5)
train_label.drop_target_register(DND_FILES)
train_label.dnd_bind('<<Drop>>', lambda e: drop_folder(e, train_label))
train_label.dnd_bind('<<DragEnter>>', lambda e: on_drag_enter(e, train_label))
train_label.dnd_bind('<<DragLeave>>', lambda e: on_drag_leave(e, train_label))

train_button = tk.Button(train_frame, text="Select Train Folder",
                        command=lambda: select_folder(train_label))
train_button.pack(pady=5)

# Valid folder frame
valid_frame = tk.LabelFrame(merge_tab, text="Validation Folder", padx=10, pady=5)
valid_frame.pack(fill="x", pady=5)

valid_label = tk.Label(valid_frame, text="Drag folder here or click Select",
                      bg="white", relief="solid", padx=5)
valid_label.pack(fill="x", ipady=10, pady=5)
valid_label.drop_target_register(DND_FILES)
valid_label.dnd_bind('<<Drop>>', lambda e: drop_folder(e, valid_label))
valid_label.dnd_bind('<<DragEnter>>', lambda e: on_drag_enter(e, valid_label))
valid_label.dnd_bind('<<DragLeave>>', lambda e: on_drag_leave(e, valid_label))

valid_button = tk.Button(valid_frame, text="Select Validation Folder",
                        command=lambda: select_folder(valid_label))
valid_button.pack(pady=5)

# Test folder frame
test_frame = tk.LabelFrame(merge_tab, text="Test Folder", padx=10, pady=5)
test_frame.pack(fill="x", pady=5)

test_label = tk.Label(test_frame, text="Drag folder here or click Select",
                     bg="white", relief="solid", padx=5)
test_label.pack(fill="x", ipady=10, pady=5)
test_label.drop_target_register(DND_FILES)
test_label.dnd_bind('<<Drop>>', lambda e: drop_folder(e, test_label))
test_label.test_label = tk.Label(test_frame, text="Drag folder here or click Select",
                     bg="white", relief="solid", padx=5)
test_label.pack(fill="x", ipady=10, pady=5)
test_label.drop_target_register(DND_FILES)
test_label.dnd_bind('<<Drop>>', lambda e: drop_folder(e, test_label))
test_label.dnd_bind('<<DragEnter>>', lambda e: on_drag_enter(e, test_label))
test_label.dnd_bind('<<DragLeave>>', lambda e: on_drag_leave(e, test_label))

test_button = tk.Button(test_frame, text="Select Test Folder",
                       command=lambda: select_folder(test_label))
test_button.pack(pady=5)

# Output folder for merged dataset
merged_output_frame = tk.LabelFrame(merge_tab, text="Output Folder", padx=10, pady=5)
merged_output_frame.pack(fill="x", pady=5)

merged_output_label = tk.Label(merged_output_frame, text="Drag folder here or click Select",
                             bg="white", relief="solid", padx=5)
merged_output_label.pack(fill="x", ipady=10, pady=5)
merged_output_label.drop_target_register(DND_FILES)
merged_output_label.dnd_bind('<<Drop>>', lambda e: drop_folder(e, merged_output_label))
merged_output_label.dnd_bind('<<DragEnter>>', lambda e: on_drag_enter(e, merged_output_label))
merged_output_label.dnd_bind('<<DragLeave>>', lambda e: on_drag_leave(e, merged_output_label))

merged_output_button = tk.Button(merged_output_frame, text="Select Output Folder",
                               command=lambda: select_folder(merged_output_label))
merged_output_button.pack(pady=5)

merge_button = tk.Button(merge_tab, text="Merge Dataset", command=merge_dataset)
merge_button.pack(pady=10)

# Progress bar (shared between tabs)
progress_frame = tk.Frame(root)
progress_frame.pack(fill="x", pady=5)

progress_bar = ttk.Progressbar(
    progress_frame,
    orient="horizontal",
    length=300,
    mode="determinate"
)
progress_bar.pack(side=tk.LEFT, fill="x", expand=True)

progress_label = tk.Label(progress_frame, text="0%", width=6)
progress_label.pack(side=tk.LEFT, padx=5)

# Status text area (shared between tabs)
status_text = scrolledtext.ScrolledText(root, height=15, width=80)
status_text.pack(fill="both", expand=True, pady=10)
status_text.insert(tk.END, "Ready to process dataset...\n")

root.mainloop()