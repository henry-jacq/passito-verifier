import cv2


class CLIQRCodeDetector:
    def __init__(self, output_file="qr_data.txt"):
        self.output_file = output_file
        self.seen_data = self._load_seen_data()
        self.detector = cv2.QRCodeDetector()
        self.cap = cv2.VideoCapture(0)  # Initialize the camera

        # Suppress ECI warnings
        cv2.setLogLevel(0)

        if not self.cap.isOpened():
            raise RuntimeError(
                "Failed to access the camera. Ensure it's connected and not in use.")

    def _load_seen_data(self):
        """Load previously stored QR code data."""
        seen_data = set()
        try:
            with open(self.output_file, "r") as file:
                seen_data.update(line.strip() for line in file)
        except FileNotFoundError:
            pass
        return seen_data

    def _save_data(self, data):
        """Save new QR code data to the output file."""
        with open(self.output_file, "a") as file:
            file.write(data + "\n")

    def detect_and_save(self):
        """Detect QR codes and save new ones in a CLI environment."""
        print("[+] Starting QR code detection. Press Ctrl+C to stop.")
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to grab frame. Retrying...")
                    continue

                # Detect and decode QR code
                data, _, _ = self.detector.detectAndDecode(frame)

                if data and data not in self.seen_data:
                    print(f"New QR code detected: {data}")
                    self.seen_data.add(data)
                    self._save_data(data)
        except KeyboardInterrupt:
            print("\nQR code detection stopped by user.")
        finally:
            self.release_resources()

    def release_resources(self):
        """Release resources used by the camera."""
        if self.cap.isOpened():
            self.cap.release()


# if __name__ == "__main__":
#     detector = CLIQRCodeDetector()
#     detector.detect_and_save()
