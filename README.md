## **Raspberry Pi Verifier Setup for Passito**

It is a **Raspberry Pi (RPI)**-based verifier setup, the system will consist of a Python application that interacts with the server's API for data exchange. The Raspberry Pi will:

1. **Scan QR Codes** using a connected camera or QR scanner module.
2. **Verify Data** by communicating with the server's API over Wi-Fi.
3. **Display Results** (check-in, check-out, verification status) on an attached display (e.g., an LCD or a small monitor).
4. **Provide Audio Feedback** using distinct beep sounds for success, failure, or errors.

---

### **Installation Instructions**

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
   # Default now uses the CLI; start subcommand is implied
   python -m cli.main
   # or, if installed with entry points
   passito-verifier start
   ```

---

### **3. API Server Endpoint**

- **Endpoint**: `/api/verifier/verify`
- **Method**: `POST`
- **Payload**:
  ```json
  {
    "verifier_key": "your_unique_verifier_key",
    "student_id": "QR_code_data",
    "action": "check-in" // or "check-out"
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

---

## CLI Usage (New)

You can use the new CLI to control the verifier without changing existing behavior.

Install dependencies and run via module or entry point:

```bash
python -m cli.main --help
passito-verifier --help  # after installing with entry points
```

Examples:

```bash
# Start the verifier loop (uses env API_URL/AUTH_TOKEN unless overridden)
passito-verifier start --config config.json

# Register device only
passito-verifier register --api-url http://passito.local --auth-token XXX

# Test API availability
passito-verifier test-api --api-url http://passito.local --auth-token XXX

# Check active status
passito-verifier is-active --api-url http://passito.local --auth-token XXX

# Show local config cache
passito-verifier config --config config.json

# Decrypt an encrypted QR payload for debugging
passito-verifier decrypt --data <base64-payload> --secret passito
```