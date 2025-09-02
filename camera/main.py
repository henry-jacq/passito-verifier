import logging
import threading
import time
from scanner.qr_scanner import scan_qr
from scanner.display import show_status_on_display
from scanner.sounds import play_sound
from api.server_api import verify_with_server
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Cache to store recently processed QR codes
processed_qr_cache = set()
cache_lock = threading.Lock()
CACHE_TIMEOUT = 10  # seconds

def clear_cache():
    while True:
        time.sleep(CACHE_TIMEOUT)
        with cache_lock:
            processed_qr_cache.clear()
            logging.debug("Cleared processed QR cache.")

def main():
    try:
        with open('./config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logging.error("Config file not found. Ensure 'config.json' exists.")
        return
    except json.JSONDecodeError:
        logging.error("Config file is not a valid JSON. Please check its contents.")
        return

    logging.info("Verifier is starting...")

    # Start a background thread to clear the cache periodically
    threading.Thread(target=clear_cache, daemon=True).start()

    while True:
        qr_data = scan_qr()
        if not qr_data:
            logging.warning("No QR code detected. Try again.")
            continue

        with cache_lock:
            if qr_data in processed_qr_cache:
                logging.info("QR code already processed. Skipping.")
                continue
            processed_qr_cache.add(qr_data)

        logging.info("Verifying with server...")
        result = verify_with_server(qr_data, config)

        if "error" in result:
            show_status_on_display("Verification Failed!", "error")
            play_sound("error")
            logging.error("Verification failed: %s", result["error"])
        else:
            status = result.get("status", "unknown")
            show_status_on_display(f"Verification {status.capitalize()}!", status)
            play_sound(status)
            logging.info("Verification %s", status.capitalize())

if __name__ == "__main__":
    main()
