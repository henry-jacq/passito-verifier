import os
from dotenv import load_dotenv
from app.auth import register_device, test_api
from app.sync import DataSync
from app.scan import QRScanner

# Load environment variables
load_dotenv()

# Get environment variables
API_URL = os.getenv("API_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# Ensure environment variables are loaded
if not AUTH_TOKEN or not API_URL:
    raise ValueError(
        "AUTH_TOKEN or API_URL is not set in the environment variables."
    )

if __name__ == "__main__":
    print("Starting passito verifier...")

    # Test API connection
    print("Testing API connection...")
    if test_api(API_URL, AUTH_TOKEN):
        print("API TEST SUCCESSFUL!")
    else:
        print("API TEST FAILED! Exiting...")
        exit(1)

    # Register Device
    print("Registering device...")
    if register_device(API_URL, AUTH_TOKEN):
        print("Device registration successful!")
    else:
        print("Device registration failed! Exiting...")
        exit(1)

    # Initialize modules for QR scanning and synchronization
    scanner = QRScanner(output_file="qr_data.txt")
    syncer = DataSync(file_path="qr_data.txt", api_url=f"{API_URL}/sync")

    # Step 1: Scan QR codes and save data
    print("Starting QR code scanning...")
    scanner.scan_and_save()

    # Step 2: Sync with server
    print("Attempting to sync with server...")
    if syncer.sync_with_server():
        print("Sync completed successfully.")
    else:
        print("Sync failed or not required.")
