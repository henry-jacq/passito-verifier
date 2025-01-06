import os
import json
import requests

# Read machine ID from /etc/machine-id
def get_machine_id():
    try:
        with open('/etc/machine-id', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("The file /etc/machine-id does not exist on this system.")


# Test the availability of the API
def test_api(api_url, auth_token):
    print("[!] Testing API availability...")
    test_endpoint = f"{api_url.rstrip('/')}/test"

    try:
        data = {
            'name': 'RPI-Verifier',
            'auth_token': auth_token
        }
        response = requests.post(test_endpoint, json=data)
        
        # Raises an HTTPError for bad responses (4xx, 5xx)
        response.raise_for_status()

        # Check the response status and message
        if str(response.status_code).startswith('2') and response.json().get("status", False):
            print("[+] API Response:", response.json().get("message"))
            return True
        else:
            print("[-] API is available but returned an unexpected response.")
            print(response.json())
            return False
    except requests.exceptions.RequestException as e:
        print("[-] API test failed.")
        print(f"[-] Reason: {e.response.reason}")
        return False


# Get the network IP address
def get_public_ip():
    try:
        response = requests.get("https://httpbin.org/ip")
        response.raise_for_status()
        return response.json().get("origin")
    except requests.exceptions.RequestException as e:
        print(f"Unable to fetch public IP: {e}")
        return None


# Register the device
def register_device(api_url, auth_token):
    if not test_api(api_url, auth_token):
        exit(1)

    # Register the device if not already registered
    if is_device_registered():
        print("[+] Device is already registered. Skipping registration.")
        return True
    
    print("[!] Registering device...")

    ip_address = get_public_ip()
    machine_id = get_machine_id()
        
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'machine_id': machine_id,
        'ip_address': ip_address,
    }

    try:
        response = requests.post(
            f"{api_url.rstrip('/')}/register", headers=headers, json=data)
        # Raises an HTTPError for bad responses (4xx, 5xx)
        response.raise_for_status()

        if response.status_code == 200:
            save_registration_state({"registered": True, "machine_id": machine_id, "ip_address": ip_address})
            print("[+] Device registered successfully.")
            # Save the registration state
            return True
        else:
            print("[-] Failed to register device.")
            print(response.json())
            return False
    except requests.exceptions.RequestException as e:
        print("[-] Failed to register device.")
        print(f"Error: {e}")


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
                print("[!] Config file is empty.")
                return None
        except json.JSONDecodeError as e:
            print(f"[!] Failed to parse config file. Error: {e}")
            return None
    print("[!] Config file does not exist or path is not set.")
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
