import os
import time
import json
from dotenv import load_dotenv
from app.auth import register_device
from app.server import is_active

# Load environment variables
os.environ.pop("DEBUG", None)
os.environ.pop("API_URL", None)
os.environ.pop("AUTH_TOKEN", None)
os.environ.pop("CONFIG_PATH", None)
os.environ.pop("VERSION", None)
load_dotenv(override=True)

# Get environment variables
API_URL = os.getenv("API_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
DEBUG = os.getenv("DEBUG", "0")
VERSION = os.getenv("VERSION", "0.1")

# Set default config path
config = os.environ.get('CONFIG_PATH', 'config.json')

if not os.path.exists(config):
    if DEBUG == "1":
        print("[DEBUG] Config file not found. Creating default config...")

    # Create a default config file with initial values
    default_config = {
        "registered": False,
        "machine_id": None,
        "ip_address": None
    }
    with open(config, 'w') as f:
        json.dump(default_config, f, indent=4)
        
    if DEBUG == "1":
        print(f"[+] Default config created at {os.path.abspath(config)}")

# Set CONFIG_PATH in the environment
os.environ['CONFIG_PATH'] = os.path.abspath(config)
# print(f"[+] Using config file: {os.environ['CONFIG_PATH']}")

# Ensure environment variables are loaded
if not AUTH_TOKEN or not API_URL:
    raise ValueError(
        "AUTH_TOKEN or API_URL is not set in the environment variables."
    )

# Starting the application
if __name__ == "__main__":    
    print(f"[*] Starting Passito Verifier v{VERSION}")
    time.sleep(1)

    # Register the device
    if not register_device(API_URL, AUTH_TOKEN):
        print("\n[-] Device registration failed. Exiting...")
        exit(1)
        
    if not is_active(API_URL, AUTH_TOKEN):
        print("\n[-] Device is not active. Exiting...")
        exit(1)

    print("[+] Proceeding with application logic...")
