import os
import logging
import requests
from app.system import get_machine_id

# Configure logging
logging.basicConfig(level=logging.DEBUG if os.getenv("DEBUG", "0") == "1" else logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Test the availability of the Server API
def test_api_availability(api_url, auth_token):
    logging.debug("Testing API availability")
    logging.debug(f"API URL: {api_url}")
    logging.debug(f"Auth Token: {auth_token}")

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
            logging.debug("API Response: %s", response.json().get("message"))
            return True
        else:
            logging.warning("API is available but returned an unexpected response.")
            logging.warning(response.json())
            return False
    except requests.exceptions.RequestException as e:
        logging.error("API test failed.")
        logging.error(f"Reason: {str(e)}")
        return False

# Send a request to the server API
def send_request(api_url, auth_token, endpoint, data, debug=False):
    if not test_api_availability(api_url, auth_token):
        logging.error("Exiting due to API unavailability.")
        exit(1)

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    try:
        if debug:
            logging.debug("Sending request to endpoint: %s", endpoint)
            logging.debug("Data: %s", data)

        response = requests.post(f"{api_url.rstrip('/')}/{endpoint}", headers=headers, json=data)
        response.raise_for_status()
        logging.info("Request successful: %s", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error("Request failed.")
        logging.error(f"Reason: {str(e)}")
        return {"error": str(e)}


# Check if the device is active on the server
def is_active(api_url, auth_token):
    # Uses send_request to check if the device is active
    data = {
        'machine_id': get_machine_id()
    }
    
    return send_request(api_url, auth_token, "is_active", data)
