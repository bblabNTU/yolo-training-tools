# yolo-training-tools

# 1.Image-extractor-drag.py

A simple GUI tool for extracting frames from video files using OpenCV and Tkinter.

## Features

- Drag and drop video files or folders for easy selection.
- Supports custom sample rates for frame extraction (frames per second).
- Option to rotate frames (90° clockwise or counterclockwise).
- Adjustable JPEG compression for output frames.
- Batch processing for multiple videos in a folder.

## Requirements

- Python 3.6+
- Libraries: `tkinter`, `cv2` (OpenCV), `tkinterdnd2`

## Installation

1. Install required libraries:
   ```bash
   pip install opencv-python tkinterdnd2
   ```
2. Place the script in your desired directory.

## Usage

1. Run the script:
   ```bash
   python video_frame_extractor.py
   ```
2. Use the GUI to:
   - **Select a Video File:** Click the "Select Video File" button or drag a video file to the designated area.
   - **Select a Folder for Batch Processing:** Click "Select Folder for Batch Processing" or drag a folder to the designated area.
   - **Set Parameters:**
     - Enter the desired **sample rate** (frames per second).
     - Choose a rotation option (No Rotation, Rotate Left 90°, or Rotate Right 90°).
     - Adjust the **compression level** using the slider.
   - Click **Process Video** to process a single file or **Batch Process Folder** to process all videos in the selected folder.

## Output

- Extracted frames are saved in an `output` folder within the selected folder (for batch processing) or in a new folder named `<video_name>_frames` next to the video file.

## Notes

- Supported video formats include `.mp4`, `.avi`, `.mkv`, `.mov`, `.flv`, `.wmv`, `.mpeg`, `.mpg`, and `.3gp`.
- Compression level ranges from 0 (lowest quality) to 100 (highest quality). The default value is 90.
- The default directory for file dialogs can be changed by modifying the `default_dir` variable in the script.

# 2. dataset-split-unsplit.py

This tool provides an easy-to-use graphical interface to manage annotated datasets. It includes two main functionalities:

1. **Split Dataset**: Splits a dataset into training, validation, and test sets.
2. **Merge Dataset**: Merges training, validation, and test datasets into a single dataset.

---

## Features

### Split Dataset

- Splits a dataset into `train`, `valid`, and `test` subsets based on user-defined ratios.
- Handles missing labels:
  - If an image exists without a corresponding label file, it is still included (assumes no objects are annotated in the image).
  - If a label file exists without a corresponding image, the label file is removed, and a notification is printed in the console.
- Organizes the output into a structured format:
  ```
  ├── train
  │   ├── images
  │   └── labels
  ├── valid
  │   ├── images
  │   └── labels
  └── test
      ├── images
      └── labels
  ```

### Merge Dataset

- Merges separate `train`, `valid`, and `test` datasets into a unified dataset containing `images` and `labels`.
- Names the merged dataset folder as `merged_<date>` (e.g., `merged_2024-11-19`).

---

## Requirements

- **Python 3.6+**
- Libraries:
  - `tkinter`
  - `os`
  - `shutil`
  - `random`
  - `datetime`

---

## Installation

1. Install Python 3.6+ if not already installed.
2. Save the script as `dataset_tool.py`.

---

## Usage

### Running the Tool

Run the script:

```bash
python dataset_tool.py
```

### Split Dataset

1. **Select Source Folder**:
   - Choose a folder containing two subfolders: `images` and `labels`.
2. **Select Output Folder**:
   - Choose where the split dataset will be saved.
3. **Set Ratios**:
   - Define the `train` and `valid` ratios (e.g., 0.7 and 0.2). The `test` ratio is calculated automatically.
4. Click **Split Dataset**.

**Output Structure**:

- The tool creates three folders: `train`, `valid`, and `test`.
- Each folder contains `images` and `labels`.

**Handling Missing Data**:

- Images without labels are included.
- Labels without corresponding images are removed, and their filenames are logged in the console.

---

### Merge Dataset

1. **Select `train`, `valid`, and `test` Folders**:
   - Choose the folders containing the datasets to merge.
2. **Select Root Directory**:
   - Choose a root directory to save the merged dataset.
3. The merged dataset is saved in a folder named `merged_<date>` inside the selected root directory.

**Output Structure**:

```
merged_<date>
├── images
└── labels
```

## Notes

- The tool assumes `.jpg` images for label matching. Modify the script if other formats (e.g., `.png`) are used.
- The `labels` should be `.txt` files with the same names as their corresponding images.
