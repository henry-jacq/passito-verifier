import cv2
from pyzbar.pyzbar import decode
import json

# Function to scan QR code in real-time
def scan_qr():
    camera = cv2.VideoCapture(0)  # Use the first available camera
    print("Scanning for QR Code...")

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        decoded_objects = decode(frame)
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print(f"[SUCCESS] QR Code Detected: {qr_data}")
            camera.release()
            cv2.destroyAllWindows()
            return qr_data

        # Display the video frame
        cv2.imshow("QR Scanner", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    return None

# Main script
if __name__ == "__main__":
    # Step 1: Scan QR code in real-time
    qr_data = scan_qr()
    if not qr_data:
        print("[ERROR] No valid QR code data found!")
        exit()

    print("[INFO] QR Code Data:", qr_data)

    # Step 2: Parse the QR code data (assume it's plain JSON)
    try:
        parsed_data = json.loads(qr_data)
        print("[SUCCESS] QR Code Data Parsed Successfully!")
        print("[INFO] Outpass Data:", json.dumps(parsed_data, indent=4))
    except json.JSONDecodeError:
        print("[ERROR] QR Code does not contain valid JSON data.")
