import cv2
import os
import shutil
import sys
from ultralytics import YOLO

# Configuration
MODEL_DIR = 'best'
MODEL_FILE = 'best.pt'
CAMERA_INDEX = 0  # 0 is usually the default for USB or CSI cameras on Pi
CONFIDENCE_THRESHOLD = 0.5

# Monkeypatch torch.load to set weights_only=False by default if running on very new PyTorch
# This is needed because ultralytics/yolo might not pass this flag yet
import torch
_original_load = torch.load
def safe_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)
torch.load = safe_load

def check_and_restore_model():
    """
    Checks if 'best.pt' exists. If not, but 'best' directory exists,
    it zips the directory to create 'best.pt' (PyTorch format).
    """
    if os.path.exists(MODEL_FILE):
        print(f"Items found: {MODEL_FILE}")
        return True
    
    if os.path.exists(MODEL_DIR) and os.path.isdir(MODEL_DIR):
        print(f"'{MODEL_FILE}' not found, but '{MODEL_DIR}' directory exists.")
        
        # ZIP does not support timestamps before 1980. We need to touch all files.
        print("Updating file timestamps for compatibility...")
        import time
        current_time = time.time()
        for root, dirs, files in os.walk(MODEL_DIR):
            for f in files:
                os.utime(os.path.join(root, f), (current_time, current_time))
            for d in dirs:
                os.utime(os.path.join(root, d), (current_time, current_time))
        os.utime(MODEL_DIR, (current_time, current_time))

        print(f"Compressing '{MODEL_DIR}' to '{MODEL_FILE}'...")
        
        # Create a zip archive of the 'best' directory with 'best/' prefix
        # This is critical for PyTorch to recognize the directory structure
        try:
            # root_dir='.' means zip relative to current directory
            # base_dir='best' means include best/ folder in the zip
            shutil.make_archive('temp_model', 'zip', root_dir='.', base_dir=MODEL_DIR)
            os.rename('temp_model.zip', MODEL_FILE)
            print(f"Successfully created {MODEL_FILE}")
            return True
        except Exception as e:
            print(f"Error creating model file: {e}")
            return False
            
    print(f"Error: Model file '{MODEL_FILE}' and directory '{MODEL_DIR}' not found.")
    return False

def main():
    # 1. Prepare Model
    if not check_and_restore_model():
        sys.exit(1)
        
    # 2. Load Model
    print("Loading YOLO model...")
    try:
        model = YOLO(MODEL_FILE)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Failed to load model: {e}")
        print("Ensure ultralytics is installed: pip install ultralytics")
        sys.exit(1)

import subprocess
import numpy as np
import threading
import time

class LibcameraVideoCapture:
    def __init__(self, width=640, height=480, fps=20):
        self.width = width
        self.height = height
        # rpicam-vid command to stream raw YUV420 to stdout
        # Reduced FPS to 20 to lower CPU load and match likely inference speed
        self.cmd = [
            "rpicam-vid",
            "-t", "0",
            "--inline",
            "--nopreview",
            "--width", str(width),
            "--height", str(height),
            "--framerate", str(fps),
            "--codec", "yuv420",
            "-o", "-"
        ]
        print(f"Starting camera with command: {' '.join(self.cmd)}")
        try:
            self.proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            print("Error: rpicam-vid not found. Please ensure rpicam-apps are installed.")
            self.proc = None
            
        self.frame_size = int(width * height * 1.5)
        self.latest_frame = None
        self.running = True
        self.lock = threading.Lock()
        
        # Start background thread to read frames
        if self.proc:
            self.thread = threading.Thread(target=self._update, daemon=True)
            self.thread.start()

    def _update(self):
        while self.running and self.proc:
            try:
                # Read one frame size
                raw_data = self.proc.stdout.read(self.frame_size)
                if len(raw_data) != self.frame_size:
                    print("Camera stream ended unexpectedly.")
                    self.running = False
                    break
                
                # Convert to BGR
                yuv = np.frombuffer(raw_data, dtype=np.uint8).reshape((self.height * 3 // 2, self.width))
                bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
                
                # Update latest frame
                with self.lock:
                    self.latest_frame = bgr
            except Exception as e:
                print(f"Error in camera thread: {e}")
                self.running = False
                break

    def isOpened(self):
        return self.running and self.proc is not None

    def read(self):
        with self.lock:
            if self.latest_frame is not None:
                return True, self.latest_frame.copy()
            return False, None

    def release(self):
        self.running = False
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.proc.kill()

    def set(self, propId, value):
        pass

def main():
    # 1. Prepare Model
    if not check_and_restore_model():
        sys.exit(1)
        
    # 2. Load Model
    print("Loading YOLO model...")
    try:
        model = YOLO(MODEL_FILE)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Failed to load model: {e}")
        print("Ensure ultralytics is installed: pip install ultralytics")
        sys.exit(1)

    # 3. Initialize Camera
    print(f"Opening camera using rpicam-vid (threaded)...")
    
    # Use our wrapper class instead of cv2.VideoCapture
    cap = LibcameraVideoCapture(width=640, height=480, fps=20)
    
    # Wait a moment for the camera to warm up
    time.sleep(1)

    if not cap.isOpened():
        print("Error: Could not open camera via rpicam-vid.")
        sys.exit(1)

    print("Starting inference. Press 'q' to quit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                # If no frame yet, just spin briefly
                time.sleep(0.01)
                continue

            # 4. Inference
            # stream=True is recommended for video sources
            results = model.predict(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)

            # 5. Visualize
            # Plot the results on the frame
            annotated_frame = results[0].plot()

            # Display the frame
            cv2.imshow("Road Damage Detection", annotated_frame)

            # Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
