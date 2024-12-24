import cv2
from pyzbar.pyzbar import decode

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
            print(f"QR Code Detected: {qr_data}")
            camera.release()
            return qr_data

        # Display the video frame
        cv2.imshow("QR Scanner", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    return None
