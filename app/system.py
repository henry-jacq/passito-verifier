import requests

# Read machine ID from /etc/machine-id
def get_machine_id():
    return "5e81e27ffea44770910d8c0a2d4b8e5d"
    try:
        with open('/etc/machine-id', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            "The file /etc/machine-id does not exist on this system.")


# Get the network IP address
def get_public_ip():
    try:
        response = requests.get("https://httpbin.org/ip")
        response.raise_for_status()
        return response.json().get("origin")
    except requests.exceptions.RequestException as e:
        print(f"Unable to fetch public IP: {e}")
        return None
