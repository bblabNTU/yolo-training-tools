# yolo-training-tools

# Image-extractor-drag.py

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
