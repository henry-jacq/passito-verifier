from scanner.qr_scanner import scan_qr
from scanner.display import show_status_on_display
from scanner.sounds import play_sound
from api.server_api import verify_with_server
import json

def main():
    with open('./config.json', 'r') as f:
        config = json.load(f)
    print("Verifier is starting...")
    while True:
        qr_data = scan_qr()
        if not qr_data:
            print("No QR code detected. Try again.")
            continue

        print("Verifying with server...")
        result = verify_with_server(qr_data, config)

        if "error" in result:
            show_status_on_display("Verification Failed!", "error")
            play_sound("error")
        else:
            status = result.get("status", "unknown")
            show_status_on_display(f"Verification {status.capitalize()}!", status)
            play_sound(status)

if __name__ == "__main__":
    main()
