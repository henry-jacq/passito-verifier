import os
import time
from dotenv import load_dotenv
from app.auth import register_device, test_api, is_registered
from app.sync import DataSync
from app.scan import QRScanner

# Load environment variables
# Reload the .env file to ensure fresh data
os.environ.pop("API_URL", None)
os.environ.pop("AUTH_TOKEN", None)
os.environ.pop("CONFIG_PATH", None)
load_dotenv(override=True)

# Get environment variables
API_URL = os.getenv("API_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

config = "config.json"

# Set config path to env if exists
if os.path.exists(config):
    os.environ['CONFIG_PATH'] = os.path.join(os.getcwd(), 'config.json')
else:
    print("[-] Config doesn't exist!")
    exit(1)

# Ensure environment variables are loaded
if not AUTH_TOKEN or not API_URL:
    raise ValueError(
        "AUTH_TOKEN or API_URL is not set in the environment variables."
    )


# Starting the application
if __name__ == "__main__":
    print("[*] Starting passito verifier...")
    time.sleep(1)

    # Register the device
    if not register_device(API_URL, AUTH_TOKEN):
        print("[-] Device registration failed. Exiting...")
        exit(1)

    print("[+] Proceeding with application logic...")

    # if not is_registered():
    #     # Test API connection
    #     test_api(API_URL, AUTH_TOKEN)

    # Register Device
    # register_device(API_URL, AUTH_TOKEN)

    # syncer = DataSync(file_path="qr_data.txt", api_url=f"{API_URL}/sync")

    # # Step 2: Sync with server
    # print("Attempting to sync with server...")
    # if syncer.sync_with_server():
    #     print("Sync completed successfully.")
    # else:
    #     print("Sync failed or not required.")
