import requests
import json

def verify_with_server(qr_data: str, config):
    payload = {
        "verifier_key": config["verifier_key"],
        "student_id": qr_data,
        "action": "check-in"  # or "check-out"
    }

    try:
        response = requests.post(config["server_url"], json=payload, timeout=10)
        return response.json()
    except requests.RequestException as e:
        print(f"Error connecting to server: {e}")
        return {"error": "Failed to connect to the server."}
