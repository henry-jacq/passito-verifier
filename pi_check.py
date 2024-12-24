import picamera
from time import sleep

def verify_camera_access():
    try:
        # Attempt to initialize the Pi Camera
        with picamera.PiCamera() as camera:
            print("Camera initialized successfully.")
            print("Testing camera preview...")
            
            # Start the camera preview for a few seconds
            camera.start_preview()
            sleep(3)
            camera.stop_preview()
            
            print("Camera preview works. Camera access verified.")
            return True
    except picamera.PiCameraError as e:
        print(f"Pi Camera Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    if verify_camera_access():
        print("Camera is accessible.")
    else:
        print("Failed to access the camera. Please check connections and configurations.")
