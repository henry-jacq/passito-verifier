from picamera2 import Picamera2
import time
import numpy as np
from PIL import Image

# Initialize the camera
picam2 = Picamera2()

# Configure the camera for still capture (photo mode)
picam2.configure(picam2.create_still_configuration())

# Start the camera preview (optional, for preview before taking a picture)
picam2.start()

# Give the camera some time to adjust (optional)
time.sleep(2)

# Capture the image as a numpy array
image_array = picam2.capture_array()

# Apply vertical flip (vflip) using numpy's flipud (flip up-down)
image_array_vflip = np.flipud(image_array)

# Convert the numpy array to a PIL Image
image = Image.fromarray(image_array_vflip)

# Save the flipped image
image.save("photo_vflip.jpg")

# Stop the camera preview
picam2.stop()

print("Vertical flip applied and picture saved as 'photo_vflip.jpg'")
