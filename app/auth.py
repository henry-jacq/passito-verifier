import requests

# Read machine ID from /etc/machine-id
def get_machine_id():
    try:
        with open('/etc/machine-id', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            "The file /etc/machine-id does not exist on this system.")


# Test the availability of the API
def test_api(api_url):
    print("[!] Testing API availability...")
    test_endpoint = f"{api_url.rstrip('/')}/test"

    try:
        # Send a POST request with the required 'name' parameter
        response = requests.post(test_endpoint, json={"name": "Verifier"})
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)

        # Check the response status and message
        if response.status_code == 200 and response.json().get("status", False):
            print("[+] API is available and responding correctly.")
            # print("Message from API:", response.json().get("message"))
            return True
        else:
            print("[-] API is available but returned an unexpected response.")
            print(response.json())
            return False
    except requests.exceptions.RequestException as e:
        print("[-] API test failed.")
        print(f"Error: {e}")
        return False

# Register the device
def register_device(api_url, auth_token):
    print("[!] Registering Verifier...")

    if not test_api(api_url):
        print("[-] API is not available. Registration aborted.")
        return

    machine_id = get_machine_id()
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }
    data = {
        'machine_id': machine_id,
    }

    try:
        response = requests.post(
            f"{api_url.rstrip('/')}/register", headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)

        if response.status_code == 200:
            print("[+] Device registered successfully.")
        else:
            print("[-] Failed to register device.")
            print(response.json())
    except requests.exceptions.RequestException as e:
        print("[-] Failed to register device.")
        print(f"Error: {e}")
