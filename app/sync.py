import hashlib
from app.server import send_request

class DataSync:
    def __init__(self, file_path="qr_data.txt", api_url=None, auth_token=None, endpoint="sync"):
        self.file_path = file_path
        self.api_url = api_url
        self.auth_token = auth_token
        self.endpoint = endpoint
        self.last_hash = None

    def _compute_file_hash(self):
        """Compute a hash of the file contents."""
        try:
            with open(self.file_path, "r") as file:
                file_data = file.read()
                return hashlib.md5(file_data.encode()).hexdigest()
        except FileNotFoundError:
            print("File not found while computing hash.")
            return None

    def _read_data_from_file(self):
        """Read unique data from the file."""
        try:
            with open(self.file_path, "r") as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print("File not found while reading data.")
            return []

    def sync_with_server(self):
        """Sync data with the server if the file has changed."""
        if not self.api_url or not self.auth_token:
            print("API URL or auth token not provided. Sync aborted.")
            return False

        current_hash = self._compute_file_hash()

        # Skip sync if no changes detected
        if current_hash == self.last_hash:
            print("No changes detected. Skipping sync.")
            return False

        # Read data and prepare for sync
        data = self._read_data_from_file()
        if not data:
            print("No data found to sync. Skipping.")
            return False

        # Send request using the provided function
        success = send_request(self.api_url, self.auth_token,
                               self.endpoint, {"data": data})
        if success:
            print("Data successfully synced with the server.")
            self.last_hash = current_hash
            return True
        else:
            print("Failed to sync data with the server.")
            return False
