import hashlib
import requests


class DataSync:
    def __init__(self, file_path="qr_data.txt", api_url=None):
        self.file_path = file_path
        self.api_url = api_url
        self.last_hash = None

    def _compute_file_hash(self):
        """Compute a hash of the file contents."""
        try:
            with open(self.file_path, "r") as file:
                file_data = file.read()
                return hashlib.md5(file_data.encode()).hexdigest()
        except FileNotFoundError:
            return None

    def _read_data_from_file(self):
        """Read unique data from the file."""
        try:
            with open(self.file_path, "r") as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            return []

    def sync_with_server(self):
        """Sync data with the server if the file has changed."""
        current_hash = self._compute_file_hash()

        # Skip sync if no changes detected
        if current_hash == self.last_hash:
            print("No changes detected. Skipping sync.")
            return False

        # Read data and sync with server
        data = self._read_data_from_file()
        if self.api_url:
            try:
                response = requests.post(self.api_url, json={"data": data})
                if response.status_code == 200:
                    print("Data successfully synced with the server.")
                    self.last_hash = current_hash
                    return True
                else:
                    print(f"Failed to sync data. Server responded with: {
                          response.status_code}")
                    return False
            except requests.exceptions.RequestException as e:
                print(f"API not available: {e}")
                return False
        else:
            print("API URL not provided. Sync aborted.")
            return False
