import cv2
from pyzbar.pyzbar import decode

def scan_qr():
    camera = cv2.VideoCapture(0)
    print("Scanning for QR Code...")

    while True:
        ret, frame = camera.read()
        if not ret:
            print("[ERROR] Unable to access the camera.")
            break

        # Process frame for QR code
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print(f"[SUCCESS] QR Code Detected: {qr_data}")
            camera.release()
            cv2.destroyAllWindows()
            return qr_data

        # Draw bounding boxes around detected QR codes
        for obj in decoded_objects:
            points = obj.polygon
            if len(points) > 4:  # If QR code is distorted
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                points = hull
            n = len(points)
            for j in range(n):
                cv2.line(frame, tuple(points[j]), tuple(points[(j + 1) % n]), (0, 255, 0), 3)

        # Display the video feed with bounding boxes
        cv2.imshow("QR Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    return None

if __name__ == "__main__":
    qr_data = scan_qr()
    if qr_data:
        print("[INFO] QR Code Data:", qr_data)
    else:
        print("[ERROR] No valid QR code detected.")
