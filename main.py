import os
from dotenv import load_dotenv
from app.auth import register_device

# Load environment variables
load_dotenv()

# Get environment variables
API_URL = os.getenv('API_URL')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

# Ensure environment variables are loaded
if not AUTH_TOKEN or not API_URL:
    raise ValueError(
        "AUTH_TOKEN or API_URL is not set in the environment variables.")

# Main execution
if __name__ == '__main__':
    register_device(API_URL, AUTH_TOKEN)
