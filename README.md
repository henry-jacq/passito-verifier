For a **Raspberry Pi (RPI)**-based verifier setup, the system will consist of a Python application that interacts with the server's API for data exchange. The Raspberry Pi will:

1. **Scan QR Codes** using a connected camera or QR scanner module.
2. **Verify Data** by communicating with the server's API over Wi-Fi.
3. **Display Results** (check-in, check-out, verification status) on an attached display (e.g., an LCD or a small monitor).
4. **Provide Audio Feedback** using distinct beep sounds for success, failure, or errors.

---

## **Code Setup for RPI Verifier**

### **1. Directory Structure**
```
rpi-verifier/
├── main.py                  # Main application file
├── scanner/
│   ├── qr_scanner.py        # QR code scanning module
│   ├── display.py           # Display management module
│   └── sounds.py            # Sound feedback module
├── api/
│   └── server_api.py        # Server API interaction
├── config/
│   └── config.json          # Configuration file (server URL, API keys)
├── requirements.txt         # Python dependencies
└── README.md                # Documentation
```

---

### **2. Code Implementation**

#### **2.1 `config/config.json`**
```json
{
    "server_url": "https://your-passito-server.com/api/verifier/verify",
    "verifier_key": "your_unique_verifier_key"
}
```

---

#### **2.2 `scanner/qr_scanner.py`**
Handles QR code scanning.

```python
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
```

---

#### **2.3 `scanner/display.py`**
Manages the output display.

```python
from time import sleep
from gpiozero import LED
import os

def show_status_on_display(message: str, status: str):
    print(f"Display: {message} ({status})")
    os.system(f'echo "{message}" > /dev/tty1')  # For connected display via serial

    # LED feedback (e.g., green for success, red for failure)
    green_led = LED(17)  # GPIO pin for green LED
    red_led = LED(27)    # GPIO pin for red LED

    if status == "success":
        green_led.on()
        sleep(2)
        green_led.off()
    elif status == "error":
        red_led.on()
        sleep(2)
        red_led.off()
```

---

#### **2.4 `scanner/sounds.py`**
Provides audio feedback.

```python
import os

def play_sound(status: str):
    if status == "success":
        os.system("aplay sounds/success.wav")  # Success beep
    elif status == "error":
        os.system("aplay sounds/error.wav")    # Error beep
    else:
        os.system("aplay sounds/neutral.wav")  # Neutral beep
```

---

#### **2.5 `api/server_api.py`**
Handles communication with the backend server.

```python
import requests
import json

def verify_with_server(qr_data: str):
    with open('config/config.json', 'r') as f:
        config = json.load(f)

    payload = {
        "verifier_key": config["verifier_key"],
        "student_id": qr_data,
        "action": "check-in"  # or "check-out"
    }

    try:
        response = requests.post(config["server_url"], json=payload, timeout=10)
        return response.json()
    except requests.RequestException as e:
        print(f"Error connecting to server: {e}")
        return {"error": "Failed to connect to the server."}
```

---

#### **2.6 `main.py`**
Main application logic.

```python
from scanner.qr_scanner import scan_qr
from scanner.display import show_status_on_display
from scanner.sounds import play_sound
from api.server_api import verify_with_server

def main():
    print("Verifier is starting...")
    while True:
        qr_data = scan_qr()
        if not qr_data:
            print("No QR code detected. Try again.")
            continue

        print("Verifying with server...")
        result = verify_with_server(qr_data)

        if "error" in result:
            show_status_on_display("Verification Failed!", "error")
            play_sound("error")
        else:
            status = result.get("status", "unknown")
            show_status_on_display(f"Verification {status.capitalize()}!", status)
            play_sound(status)

if __name__ == "__main__":
    main()
```

---

### **3. Installation Instructions**
1. **Install Required Libraries**:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip python3-opencv libzbar0
   pip3 install -r requirements.txt
   ```

2. **Add Required Dependencies** in `requirements.txt`:
   ```
   opencv-python
   pyzbar
   requests
   gpiozero
   ```

3. **Connect Hardware**:
   - **Camera**: Attach via USB.
   - **LEDs**: Connect to GPIO pins.
   - **Speaker**: Attach to audio jack or use a USB speaker.

4. **Run the Application**:
   ```bash
   python3 main.py
   ```

---

### **4. API Server Endpoint**
- **Endpoint**: `/api/verifier/verify`
- **Method**: `POST`
- **Payload**:
  ```json
  {
      "verifier_key": "your_unique_verifier_key",
      "student_id": "QR_code_data",
      "action": "check-in"  // or "check-out"
  }
  ```
- **Response**:
  ```json
  {
      "status": "success",
      "message": "Check-in successful"
  }
  ```

---

This code setup will enable your Raspberry Pi to function as a verifier device, scanning QR codes, verifying check-ins/outs with the server, and providing user feedback.