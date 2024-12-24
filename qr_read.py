from pyzbar.pyzbar import decode
from PIL import Image

# Test decoding a static QR code image
image_path = "qrcode_plain.png"  # Replace with the path to your QR code image
image = Image.open(image_path)
decoded_objects = decode(image)

if decoded_objects:
    for obj in decoded_objects:
        print("Decoded Data:", obj.data.decode('utf-8'))
else:
    print("[ERROR] No QR code detected in the image.")
