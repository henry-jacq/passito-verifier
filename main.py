import os
import time
from dotenv import load_dotenv
from app.auth import register_device

# Load environment variables
os.environ.pop("API_URL", None)
os.environ.pop("AUTH_TOKEN", None)
os.environ.pop("CONFIG_PATH", None)
load_dotenv(override=True)

# Get environment variables
API_URL = os.getenv("API_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# Set default config path
config = os.environ.get('CONFIG_PATH', 'config.json')

if os.path.exists(config):
    os.environ['CONFIG_PATH'] = os.path.abspath(config)
else:
    print("[-] Config file does not exist. Exiting...")
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
