import os
import json
import logging
from app.system import get_machine_id, get_public_ip
from app.server import test_api_availability, send_request


# Register the device
def register_device(api_url, auth_token):
    if not test_api_availability(api_url, auth_token):
        exit(1)

    # Check if the device is already registered
    if is_device_registered():
        logging.info("Device registration verified.")
        logging.info("To re-register, delete the configuration file and restart the application.")
        return True

        logging.info("Initiating device registration.")

    # Gather device details
    ip_address = get_public_ip()
    machine_id = get_machine_id()

    data = {
        'machine_id': machine_id,
        'ip_address': ip_address,
    }

    # Use send_request to register the device
    if send_request(api_url, auth_token, "register", data):
        save_registration_state(
            {"registered": True, "machine_id": machine_id, "ip_address": ip_address})
        logging.info("Device registration completed successfully.")
        return True
    else:
        logging.error("Device registration unsuccessful.")
        return False


# Load the registration state from a file
def load_registration_state():
    config = os.environ.get('CONFIG_PATH')
    if config and os.path.exists(config):
        try:
            # Check if the file is not empty
            if os.path.getsize(config) > 0:
                with open(config, 'r') as f:
                    return json.load(f)
            else:
                logging.warning("Configuration file is empty.")
                return None
        except json.JSONDecodeError as e:
            logging.error("Configuration file parsing failed: %s", str(e))
            return None
    logging.warning("Configuration file not found or path not configured.")
    return None

# Save the registration state to a file
def save_registration_state(state):
    config = os.environ.get('CONFIG_PATH')
    if config:
        with open(config, 'w') as f:
            json.dump(state, f)


# Check if the device is already registered by reading the config
def is_device_registered():
    state = load_registration_state()
    return state is not None and state.get('registered', False)
