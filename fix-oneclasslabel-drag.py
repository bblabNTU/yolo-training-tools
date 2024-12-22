import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
import os
from pathlib import Path

# First try to import tkinterdnd2
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    using_dnd = True
except ImportError:
    print("tkinterdnd2 not found. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "tkinterdnd2"])
    from tkinterdnd2 import TkinterDnD, DND_FILES
    using_dnd = True

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_label.config(text=folder_path)
        status_text.delete(1.0, tk.END)
        status_text.insert(tk.END, f"Selected folder: {folder_path}\n")

def drop_folder(event):
    # Clean the file path (remove curly braces and quotes if present)
    file_path = event.data.replace('{', '').replace('}', '').replace('"', '')
    
    # If it's a file, get its directory
    if os.path.isfile(file_path):
        file_path = os.path.dirname(file_path)
    
    folder_label.config(text=file_path)
    folder_label.config(bg="white")
    status_text.delete(1.0, tk.END)
    status_text.insert(tk.END, f"Dropped folder: {file_path}\n")

def on_drag_enter(event):
    folder_label.config(bg="lightblue")

def on_drag_leave(event):
    folder_label.config(bg="white")

def update_status(message):
    status_text.insert(tk.END, message + "\n")
    status_text.see(tk.END)  # Auto-scroll to the bottom
    root.update_idletasks()

def fix_labels():
    labels_dir = folder_label.cget("text")
    if labels_dir == "Drag a labels folder here or click 'Select Folder'":
        update_status("⚠️ Please select a folder first!")
        return
        
    try:
        labels_path = Path(labels_dir)
        if not labels_path.is_dir():
            update_status("❌ Error: Not a valid directory")
            return

        # Clear status text and start new processing
        status_text.delete(1.0, tk.END)
        update_status(f"📂 Processing folder: {labels_dir}")
        
        # Count total files first
        txt_files = list(labels_path.glob('*.txt'))
        total_files = len(txt_files)
        
        if total_files == 0:
            update_status("❌ No .txt files found in the selected folder!")
            return
        
        update_status(f"📄 Found {total_files} .txt files")
        modified_count = 0
        processed_count = 0
        
        for label_file in txt_files:
            modified = False
            new_lines = []
            modified_lines = 0
            
            with open(label_file, 'r') as f:
                lines = f.readlines()
                
                for line in lines:
                    parts = line.strip().split()
                    
                    if parts and parts[0] == '1':
                        new_line = '0 ' + ' '.join(parts[1:]) + '\n'
                        modified = True
                        modified_lines += 1
                    else:
                        new_line = line
                        
                    new_lines.append(new_line)
            
            if modified:
                with open(label_file, 'w') as f:
                    f.writelines(new_lines)
                modified_count += 1
                update_status(f"✅ Modified {label_file.name} ({modified_lines} lines changed)")
            else:
                update_status(f"ℹ️ Skipped {label_file.name} (no changes needed)")
            
            processed_count += 1
            
            # Update progress
            progress = (processed_count / total_files) * 100
            progress_bar['value'] = progress
            progress_label.config(text=f"{progress:.1f}%")
            root.update_idletasks()
        
        # Final summary
        update_status("\n📊 Summary:")
        update_status(f"Total files processed: {total_files}")
        update_status(f"Files modified: {modified_count}")
        update_status(f"Files unchanged: {total_files - modified_count}")
        update_status("\n✨ Processing completed successfully!")
        
    except Exception as e:
        update_status(f"❌ Error: {str(e)}")

# Create main window with DnD support
root = TkinterDnD.Tk()
root.title("YOLO Label Class Fixer")
root.geometry("600x600")
root.configure(padx=20, pady=20)

# Create and pack widgets
title_label = tk.Label(root, text="YOLO Label Class Fixer", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Instructions
usage_text = """
Instructions:
1. Drag and drop your labels folder into the box below OR use the 'Select Folder' button
2. Click 'Fix Labels' to convert all class 1 to class 0
3. Watch the progress and status below
"""
usage_label = tk.Label(root, text=usage_text, justify=tk.LEFT, anchor="w")
usage_label.pack(fill="x", pady=5)

# Folder Selection Frame
folder_frame = tk.Frame(root)
folder_frame.pack(fill="x", pady=5)

folder_label = tk.Label(
    folder_frame, 
    text="Drag a labels folder here or click 'Select Folder'",
    anchor="w",
    bg="white",
    relief="solid",
    padx=5
)
folder_label.pack(fill="x", ipady=20)

# Configure drag and drop
folder_label.drop_target_register(DND_FILES)
folder_label.dnd_bind('<<Drop>>', drop_folder)
folder_label.dnd_bind('<<DragEnter>>', lambda e: on_drag_enter(e))
folder_label.dnd_bind('<<DragLeave>>', lambda e: on_drag_leave(e))

# Buttons Frame
button_frame = tk.Frame(root)
button_frame.pack(fill="x", pady=10)

folder_button = tk.Button(button_frame, text="Select Folder", command=select_folder)
folder_button.pack(side=tk.LEFT, padx=5)

process_button = tk.Button(button_frame, text="Fix Labels", command=fix_labels)
process_button.pack(side=tk.LEFT, padx=5)

# Progress Bar Frame
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

# Status Text Area
status_text = scrolledtext.ScrolledText(root, height=15, width=60)
status_text.pack(fill="both", expand=True, pady=10)
status_text.insert(tk.END, "Ready to process files...\n")

root.mainloop()