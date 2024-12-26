from picamera2 import Picamera2
from time import sleep

def verify_camera_access():
    try:
        # Initialize the Pi Camera
        picam2 = Picamera2()
        print("Camera initialized successfully.")
        
        # Configure the camera for preview
        preview_config = picam2.create_preview_configuration()
        picam2.configure(preview_config)
        
        print("Testing camera preview...")
        picam2.start()
        sleep(3)  # Show the preview for 3 seconds
        picam2.stop()
        
        print("Camera preview works. Camera access verified.")
        return True
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    if verify_camera_access():
        print("Camera is accessible.")
    else:
        print("Failed to access the camera. Please check connections and configurations.")
