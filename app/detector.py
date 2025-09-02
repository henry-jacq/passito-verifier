import json
import time
import threading
from app.sync import DataSync
import cv2
import base64, pygame, random
import hashlib
from Cryptodome.Cipher import AES
import logging


class CLIQRCodeDetector:
    def __init__(self, output_file="qr_data.txt", api_url=None, auth_token=None):
        self.output_file = output_file
        self.seen_data = self._load_seen_data()
        self.detector = cv2.QRCodeDetector()
        self.cap = cv2.VideoCapture(0)  # Initialize the camera
        # Lower resolution for faster decode; adjust as needed
        try:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        except Exception:
            pass
        self.api_url = api_url
        self.auth_token = auth_token
        self.sync = DataSync(file_path=self.output_file,
                             api_url=self.api_url, auth_token=self.auth_token)
        # Preload buzzer sound to avoid runtime loading delays
        try:
            self._buzzer = pygame.mixer.Sound("sounds/buzzer.mp3")
        except Exception:
            self._buzzer = None
        # Small dedup cache to prevent re-processing same payload quickly
        self._recent_set = set()
        self._recent_last_purge = time.time()
        self._recent_ttl = 5.0

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
        logging.info("QR scanner active. Press Ctrl+C to terminate.")
        try:
            last_data = None  # Track the last detected data to avoid redundant syncing
            while True:
                ret, frame = self.cap.read()
                if not ret or frame is None or getattr(frame, 'size', 0) == 0:
                    logging.debug("Failed to grab valid frame. Retrying...")
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
                    logging.debug("QR detected with %d chars", len(data))
                    decrypted_data = self.decrypt_qr_data(data, 'passito')

                    # Convert to JSON object to standardize format
                    try:
                        # Convert string to dictionary (avoid sorting to reduce CPU)
                        json_data = json.loads(decrypted_data)
                        standardized_data = json.dumps(json_data, separators=(',', ':'))
                    except json.JSONDecodeError:
                        logging.warning("QR validation failed: decryption error or invalid JSON format")
                        continue

                    if standardized_data and decrypted_data != "Decryption failed!":  # Only process valid QR code data
                        # Deduplicate recent payloads for a few seconds (valid path fast)
                        now_ts = time.time()
                        if (now_ts - self._recent_last_purge) > self._recent_ttl:
                            self._recent_set.clear()
                            self._recent_last_purge = now_ts
                        if standardized_data in self._recent_set:
                            # Minimal delay for valid duplicates
                            time.sleep(0.01)
                            continue
                        self._recent_set.add(standardized_data)
                        logging.info("QR verification successful: %s", standardized_data)
                        logging.debug("Valid QR after decrypt; syncing...")
                        last_data = standardized_data

                        # Sync data synchronously to pause further detection until network call finishes
                        t0 = time.perf_counter()
                        self.sync.sync_with_server(standardized_data, player)
                        logging.debug("Sync finished in %.1f ms", (time.perf_counter() - t0) * 1000)

                        # Update seen data and save (not saving to file as per new instructions)
                        # self.seen_data.add(standardized_data)
                        # self._save_data(standardized_data)
                    elif decrypted_data == "Decryption failed!":
                        logging.warning("QR validation failed: decryption unsuccessful with provided key")

                # Reduced delay to balance performance and efficiency
                time.sleep(0.2)
        except KeyboardInterrupt:
            logging.info("QR scanner terminated by user.")
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
        try:
            decoded = base64.b64decode(encrypted_data, validate=True)
        except Exception as e:
            logging.warning("Decryption failed: invalid base64 encoding - %s", str(e))
            try:
                if self._buzzer:
                    ch = self._buzzer.play()
                    if ch is not None:
                        while ch.get_busy():
                            time.sleep(0.01)
                    time.sleep(random.uniform(0.15, 0.35))
            except Exception:
                pass
            return "Decryption failed!"

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
            logging.warning("Decryption failed: %s", str(e))
            try:
                if self._buzzer:
                    ch = self._buzzer.play()
                    if ch is not None:
                        while ch.get_busy():
                            time.sleep(0.01)
                    time.sleep(random.uniform(0.15, 0.35))
            except Exception:
                pass
            return "Decryption failed!"


# if __name__ == "__main__":
#     detector = CLIQRCodeDetector(api_url=API_URL, auth_token=AUTH_TOKEN)
#     detector.detect_and_save()
