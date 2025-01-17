import cv2


class QRScanner:
    def __init__(self, output_file):
        """
        Initialize the QRScanner module.
        :param output_file: File to save scanned QR code data.
        """
        self.output_file = output_file

    def _write_unique_data(self, data):
        """
        Write unique QR code data to the file.
        :param data: The QR code data to write.
        """
        try:
            # Read existing data
            with open(self.output_file, "r") as file:
                existing_data = set(file.read().splitlines())
        except FileNotFoundError:
            existing_data = set()

        # Write only if the data is unique
        if data not in existing_data:
            with open(self.output_file, "a") as file:
                file.write(data + "\n")
            print(f"New data saved: {data}")
        else:
            print(f"Data already exists: {data}")

    def scan_and_save(self):
        """
        Scan QR codes and save unique data to a file.
        """
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()

        try:
            while True:
                ret, img = cap.read()
                if not ret:
                    print("Failed to grab frame. Exiting...")
                    break

                data, bbox, _ = detector.detectAndDecode(img)

                # If a QR code is detected
                if bbox is not None and data:
                    # Draw bounding box
                    bbox = bbox.astype(int)
                    for i in range(len(bbox)):
                        cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]),
                                 color=(255, 0, 0), thickness=2)

                    # Display the decoded data
                    cv2.putText(img, data, (bbox[0][0][0], bbox[0][0][1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    print(f"QR Code Data: {data}")
                    self._write_unique_data(data)

                # Display the video feed
                cv2.imshow("QR Code Scanner", img)

                # Exit on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("Exiting QR code scanner.")
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
