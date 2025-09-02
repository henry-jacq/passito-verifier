# Deployment Guide for Passito Verifier Tool

This guide provides step-by-step instructions to deploy the Passito Verifier Tool on a device, including pre-deployment checks and configurations.

---

## **Pre-Deployment Checklist**

1. **Hardware Requirements**:
   - A device with a camera (e.g., Raspberry Pi with a compatible camera module).
   - Sufficient storage and memory to run the tool.

2. **Software Requirements**:
   - Docker installed on the device.
   - Python 3.11+ installed (if running without Docker).
   - Required Python libraries (listed in `requirements.txt`).

3. **Environment Variables**:
   - Ensure the following environment variables are set:
     - `API_URL`: The server URL for verification.
     - `AUTH_TOKEN`: The authentication token for API access.

4. **Camera Access**:
   - Verify that the camera is accessible on the device.
   - For Linux, check the camera device using:

     ```bash
     ls /dev/video*
     ```

   - Ensure the user has permissions to access the camera device.

5. **Network Configuration**:
   - Ensure the device has internet access to communicate with the server.
   - Open necessary ports (e.g., port 80 for HTTP communication).

---

## **Deployment Steps**

### **Option 1: Using Docker**

1. **Build the Docker Image**:

   ```bash
   docker build -t passito-verifier .
   ```

2. **Run the Docker Container**:

   ```bash
   docker run --privileged --device=/dev/video0:/dev/video0 -p 80:80 passito-verifier
   ```

   - Replace `/dev/video0` with the appropriate camera device on your system.

3. **Verify Camera Access**:

   ```bash
   v4l2-ctl --list-devices
   ```

### **Option 2: Running Locally**

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Tool**:

   ```bash
   python main.py
   ```

3. **Verify Camera Access**:
   - Ensure the camera is accessible by running the tool and checking for QR code detection.

---

## **Post-Deployment Checks**

1. **Verify Logs**:
   - Check the logs for any errors or warnings.
   - Logs are displayed in the console or can be redirected to a file.

2. **Test QR Code Detection**:
   - Place a QR code in front of the camera and verify detection and server synchronization.

3. **Monitor Performance**:
   - Ensure the tool runs smoothly without high CPU or memory usage.

---

## **Troubleshooting**

1. **Camera Not Detected**:
   - Ensure the camera is connected and accessible.
   - Restart the device and check camera permissions.

2. **Server Communication Issues**:
   - Verify `API_URL` and `AUTH_TOKEN` are correct.
   - Check network connectivity and firewall settings.

3. **Docker Issues**:
   - Ensure Docker is installed and running.
   - Use `docker logs <container-id>` to debug container issues.

---

## **Future Enhancements**

- Automate deployment using CI/CD pipelines.
- Add support for multiple camera devices.
- Integrate centralized logging and monitoring tools.

---

For further assistance, contact the development team.
