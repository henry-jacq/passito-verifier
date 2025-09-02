import logging
import pygame
import os
import time
import json
from dotenv import load_dotenv
from app.auth import register_device
from app.server import is_active
from app.detector import CLIQRCodeDetector

# Configure logging
logging.basicConfig(level=logging.DEBUG if os.getenv("DEBUG", "0") == "1" else logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv(override=True)

# Get environment variables
API_URL = os.getenv("API_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
DEBUG = os.getenv("DEBUG", "0")
VERSION = os.getenv("VERSION", "0.1")

# Set default config path
config_path = os.environ.get('CONFIG_PATH', 'config.json')

if not os.path.exists(config_path):
    logging.debug("Config file not found. Creating default config...")

    # Create a default config file with initial values
    default_config = {
        "registered": False,
        "machine_id": None,
        "ip_address": None
    }
    with open(config_path, 'w') as f:
        json.dump(default_config, f, indent=4)

    logging.info(f"Default config created at {os.path.abspath(config_path)}")

# Set CONFIG_PATH in the environment
os.environ['CONFIG_PATH'] = os.path.abspath(config_path)
logging.info(f"Using config file: {os.environ['CONFIG_PATH']}")

# Ensure environment variables are loaded
if not AUTH_TOKEN or not API_URL:
    logging.error("AUTH_TOKEN or API_URL is not set in the environment variables.")
    raise ValueError("AUTH_TOKEN or API_URL is not set in the environment variables.")

"""
Startup now performs a single API preflight check during registration.
Subsequent requests skip the ping for performance. Audio playback is non-blocking.
Registration state is primarily validated against the server; local file is advisory.
"""

# Initialize the pygame mixer (best-effort)
try:
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/success.mp3")
except Exception as e:
    logging.warning(f"Audio init failed: {e}")

# Starting the application
if __name__ == "__main__":
    logging.info(f"Starting Passito Verifier v{VERSION}")
    time.sleep(1)

    # Register the device
    if not register_device(API_URL, AUTH_TOKEN):
        logging.error("Device registration failed. Exiting...")
        exit(1)

    active_resp = is_active(API_URL, AUTH_TOKEN)
    if not active_resp or not active_resp.get('ok'):
        logging.error("Device is not active. Contact Administrator!")
        exit(1)

    logging.info("Proceeding with application logic...")
    detector = CLIQRCodeDetector(api_url=API_URL, auth_token=AUTH_TOKEN)
    detector.detect_and_save(player=pygame)
