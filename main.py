import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AUTH_TOKEN = os.getenv('AUTH_TOKEN')
API_URL = os.getenv('API_URL')

# Ensure environment variables are loaded
if not AUTH_TOKEN or not API_URL:
    raise ValueError("AUTH_TOKEN or API_URL is not set in the environment variables.")

# Read machine ID from /etc/machine-id
def get_machine_id():
    try:
        with open('/etc/machine-id', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("The file /etc/machine-id does not exist on this system.")

# Register the device
def register_device():
    print("Registering device...")
    machine_id = get_machine_id()
    
    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'machine_id': machine_id,
    }
    
    try:
        response = requests.post(f"{API_URL.rstrip('/')}/register", headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        print("Device registered successfully:", response.json())
    except requests.exceptions.RequestException as e:
        print("Failed to register device.")
        print(f"Error: {e}")

if __name__ == '__main__':
    register_device()
