import requests
import json


def sync_logs(api_url, auth_token, log_data):
    """
    Function to sync logs to the server.
    Args:
        api_url (str): The server API URL.
        auth_token (str): The authorization token.
        log_data (dict): The log data to be sent to the server.
    """
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(
            f"{api_url.rstrip('/')}/sync", headers=headers, json=log_data)
        # Raise exception for unsuccessful status codes.
        response.raise_for_status()

        if response.status_code == 200:
            print("[+] Logs synced successfully.")
        else:
            print("[-] Failed to sync logs.")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("[-] Error syncing logs.")
        print(f"Error: {e}")


def format_log_data(log_message, log_level="INFO"):
    """
    Function to format log data before sending it to the server.
    Args:
        log_message (str): The log message.
        log_level (str): The log level (e.g., INFO, ERROR).
    """
    return {
        'message': log_message,
        'level': log_level,
        'timestamp': '2025-01-06T12:00:00',  # Replace with actual timestamp logic
    }
