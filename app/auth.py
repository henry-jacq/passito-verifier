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
        print("[-] Device cannot be registered.")
        return

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
            print("[+] Device registered successfully.")
        else:
            print("[-] Failed to register device.")
            print(response.json())
    except requests.exceptions.RequestException as e:
        print("[-] Failed to register device.")
        print(f"Error: {e}")
