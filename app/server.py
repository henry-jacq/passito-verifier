import os
import requests
from app.system import get_machine_id

# Test the availability of the Server API
def test_api_availablity(api_url, auth_token):
    print("[*] Testing API availability")
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
            if os.environ.get("DEBUG") == "1":
                print("DEBUG: API Response:", response.json().get("message"))
            return True
        else:
            print("[-] API is available but returned an unexpected response.")
            print(response.json())
            return False
    except requests.exceptions.RequestException as e:
        print("[-] API test failed.")
        print(f"[-] Reason: {e.response.reason}")
        return False

# Send a request to the server API
def send_request(api_url, auth_token, endpoint, data):
    if not test_api_availablity(api_url, auth_token):
        exit(1)

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.post(
            f"{api_url.rstrip('/')}/{endpoint}", headers=headers, json=data)
        # Raises an HTTPError for bad responses (4xx, 5xx)
        response.raise_for_status()

        if str(response.status_code).startswith('2') and not response.is_redirect:
            return True
        else:
            print(response.json())
            return False
        
    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {e.response.reason}")
    return False


# Check if the device is active on the server
def is_active(api_url, auth_token):
    # Uses send_request to check if the device is active
    data = {
        'machine_id': get_machine_id()
    }
    
    return send_request(api_url, auth_token, "is_active", data)
