import json
import time
import threading
from app.sync import DataSync
import cv2
import base64, pygame
import hashlib
from Cryptodome.Cipher import AES


class CLIQRCodeDetector:
    def __init__(self, output_file="qr_data.txt", api_url=None, auth_token=None):
        self.output_file = output_file
        self.seen_data = self._load_seen_data()
        self.detector = cv2.QRCodeDetector()
        self.cap = cv2.VideoCapture(0)  # Initialize the camera
        self.api_url = api_url
        self.auth_token = auth_token
        self.sync = DataSync(file_path=self.output_file,
                             api_url=self.api_url, auth_token=self.auth_token)

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

    def detect_and_save(self, player: pygame.mixer.music):
        """Detect QR codes and save new ones in a CLI environment while syncing data in the background."""
        print("[+] Starting QR code detection. Press Ctrl+C to stop.")
        try:
            last_data = None  # Track the last detected data to avoid redundant syncing
            while True:
                ret, frame = self.cap.read()
                if not ret or frame is None or getattr(frame, 'size', 0) == 0:
                    print("Failed to grab valid frame. Retrying...")
                    time.sleep(0.05)
                    continue

                # Detect and decode QR code with safety guards
                data = None
                try:
                    data, _, _ = self.detector.detectAndDecode(frame)
                except cv2.error:
                    # Fallback to multi-decode if single decode errors out
                    try:
                        datas, _, _ = self.detector.detectAndDecodeMulti(frame)
                        if datas and len(datas) > 0:
                            data = datas[0]
                    except cv2.error:
                        data = None

                if data:
                    decrypted_data = self.decrypt_qr_data(data, 'passito')

                    # Convert to JSON object to standardize format
                    try:
                        # Convert string to dictionary
                        json_data = json.loads(decrypted_data)
                        standardized_data = json.dumps(
                            json_data, sort_keys=True)  # Convert back to string
                    except json.JSONDecodeError:
                        print("[!] Decryption failed or invalid JSON")
                        continue

                    if standardized_data:  # Only process new QR code data
                        print(f"->  New QR code detected: {standardized_data}")
                        last_data = standardized_data

                        # Sync data synchronously to pause further detection until network call finishes
                        self.sync.sync_with_server(standardized_data, player)

                        # Update seen data and save (not saving to file as per new instructions)
                        # self.seen_data.add(standardized_data)
                        # self._save_data(standardized_data)

                # Reduced delay to balance performance and efficiency
                time.sleep(0.2)
        except KeyboardInterrupt:
            print("\nQR code detection stopped by user.")
        finally:
            self.release_resources()

    def release_resources(self):
        """Release resources used by the camera."""
        if self.cap.isOpened():
            self.cap.release()

    def decrypt_qr_data(self, encrypted_data: str, shared_secret: str) -> str:
        """Decrypt the QR code data."""
        # Generate the key from the shared secret
        key = hashlib.sha256(shared_secret.encode()).digest()

        # Decode the Base64-encoded encrypted string
        decoded = base64.b64decode(encrypted_data)

        # Extract IV, Tag, and Ciphertext
        iv = decoded[:12]         # First 12 bytes = IV
        tag = decoded[12:28]      # Next 16 bytes = Tag
        ciphertext = decoded[28:]  # Remaining bytes = Ciphertext

        # Create AES cipher object for decryption
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)

        # Decrypt the ciphertext
        try:
            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
            return decrypted_data.decode()  # Convert bytes to string
        except (ValueError, TypeError) as e:
            print(f"[!] Decryption failed: {str(e)}")
            return "Decryption failed!"


# if __name__ == "__main__":
#     detector = CLIQRCodeDetector(api_url=API_URL, auth_token=AUTH_TOKEN)
#     detector.detect_and_save()
