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
def get_public_ip(timeout: float = 3.0):
    """Return the public IP address using multiple providers with fallbacks."""
    providers = [
        ("https://api.ipify.org?format=json", "json", "ip"),
        ("https://ifconfig.me/ip", "text", None),
        ("https://ipinfo.io/ip", "text", None),
        ("https://checkip.amazonaws.com", "text", None),
    ]

    for url, mode, key in providers:
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            if mode == "json":
                data = resp.json()
                ip = data.get(key)
            else:
                ip = resp.text.strip()
            if ip:
                return ip
        except requests.exceptions.RequestException:
            continue

    print("Unable to fetch public IP from all providers.")
    return None
