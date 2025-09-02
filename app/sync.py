import hashlib
import time
import threading
from app.server import send_request

class DataSync:
    def __init__(self, file_path="qr_data.txt", api_url=None, auth_token=None, endpoint="sync"):
        self.file_path = file_path
        self.api_url = api_url
        self.auth_token = auth_token
        self.endpoint = endpoint
        self.last_hash = None
        self._lock = threading.Lock()
        self._last_sync_ts = 0.0
        self._pending_data = None
        self._min_interval_secs = 2.0  # minimum gap between sync calls

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

    def sync_with_server(self, data, player):
        """Sync data with the server with a lock and rate limit to avoid bursts."""
        if not self.api_url or not self.auth_token:
            print("API URL or auth token not provided. Sync aborted.")
            return False

        now = time.time()

        # Coalesce if a sync is ongoing or within cooldown window
        if self._lock.locked() or (now - self._last_sync_ts) < self._min_interval_secs:
            self._pending_data = data
            return False

        ok = False
        with self._lock:
            resp = send_request(self.api_url, self.auth_token,
                                self.endpoint, {"data": data}, debug=True)
            # Treat dict with 'error' as failure
            if isinstance(resp, dict) and resp.get("error"):
                ok = False
            else:
                ok = bool(resp)

            if ok:
                print("[+] Data successfully synced with the server.")
                try:
                    player.mixer.music.play()
                except Exception:
                    pass
                self._last_sync_ts = time.time()
            else:
                print("[-] Failed to sync data with the server.")

        # If something new arrived during the sync, send the latest once after delay
        if self._pending_data is not None:
            remaining = self._min_interval_secs - (time.time() - self._last_sync_ts)
            if remaining > 0:
                time.sleep(remaining)
            pending = self._pending_data
            self._pending_data = None
            return self.sync_with_server(pending, player)

        return ok
