import requests
import json
import uuid

# Configuration
SERVER_API_URL = "https://your-server-url/api/admin/register-verifier"
VERIFIER_NAME = "Verifier 1"
LOCATION = "Main Gate"
REGISTRATION_CODE = "YOUR_SECURE_REGISTRATION_CODE"  # Pre-shared secret

def generate_api_key():
    """Generate a unique API key."""
    return str(uuid.uuid4())

def register_verifier():
    """Register the verifier with the server."""
    api_key = generate_api_key()
    
    data = {
        "verifier_name": VERIFIER_NAME,
        "location": LOCATION,
        "api_key": api_key,
        "registration_code": REGISTRATION_CODE  # Include the secure code
    }
    
    try:
        response = requests.post(SERVER_API_URL, json=data)
        if response.status_code == 200:
            print("Verifier registered successfully:", response.json())
        else:
            print("Failed to register verifier:", response.content)
    except Exception as e:
        print("Error during registration:", str(e))

if __name__ == "__main__":
    register_verifier()
