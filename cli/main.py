import argparse
import json
import logging
import os
import sys
from dotenv import load_dotenv

# Hide pygame support prompt when pygame is imported
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

# Load .env early so version and other envs are available for help text
load_dotenv(override=True)

from app.auth import register_device, load_registration_state
from app.server import test_api_availability, is_active, send_request
from app.detector import CLIQRCodeDetector


def setup_logging(debug: bool):
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def ensure_config(config_path: str):
    if not os.path.exists(config_path):
        default_config = {"registered": False, "machine_id": None, "ip_address": None}
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        logging.info("Default configuration file created at %s", os.path.abspath(config_path))
    os.environ['CONFIG_PATH'] = os.path.abspath(config_path)


def cmd_start(args):
    setup_logging(args.debug)
    load_dotenv(override=True)
    api_url = args.api_url or os.getenv('API_URL')
    auth_token = args.auth_token or os.getenv('AUTH_TOKEN')
    if not api_url or not auth_token:
        logging.error('API_URL and AUTH_TOKEN are required (arguments or environment variables).')
        sys.exit(1)

    ensure_config(args.config)

    if not register_device(api_url, auth_token):
        logging.error('Device registration unsuccessful. Exiting...')
        sys.exit(1)

        logging.info('Initializing QR verification system...')
        from pygame import mixer
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/success.mp3")
        detector = CLIQRCodeDetector(api_url=api_url, auth_token=auth_token)
        detector.detect_and_save(player=pygame)
    except Exception as e:
        logging.error(f"Failed to start detector: {e}")
        sys.exit(1)


def cmd_register(args):
    setup_logging(args.debug)
    load_dotenv(override=True)
    api_url = args.api_url or os.getenv('API_URL')
    auth_token = args.auth_token or os.getenv('AUTH_TOKEN')
    if not api_url or not auth_token:
        logging.error('API_URL and AUTH_TOKEN are required (arguments or environment variables).')
        sys.exit(1)
    ensure_config(args.config)
    ok = register_device(api_url, auth_token)
    sys.exit(0 if ok else 2)


def cmd_test_api(args):
    setup_logging(args.debug)
    load_dotenv(override=True)
    api_url = args.api_url or os.getenv('API_URL')
    auth_token = args.auth_token or os.getenv('AUTH_TOKEN')
    if not api_url or not auth_token:
        logging.error('API_URL and AUTH_TOKEN are required (arguments or environment variables).')
        sys.exit(1)
    ok = test_api_availability(api_url, auth_token)
    print(json.dumps({"ok": ok}))
    sys.exit(0 if ok else 3)


def cmd_is_active(args):
    setup_logging(args.debug)
    load_dotenv(override=True)
    api_url = args.api_url or os.getenv('API_URL')
    auth_token = args.auth_token or os.getenv('AUTH_TOKEN')
    if not api_url or not auth_token:
        logging.error('API_URL and AUTH_TOKEN are required (arguments or environment variables).')
        sys.exit(1)
    resp = is_active(api_url, auth_token)
    print(json.dumps(resp or {}))
    sys.exit(0 if resp and (resp.get('ok') or resp.get('status') in (True, 'success')) else 4)


def cmd_config(args):
    setup_logging(args.debug)
    ensure_config(args.config)
    state = load_registration_state() or {}
    print(json.dumps(state, indent=2))


def cmd_decrypt(args):
    # Utility to decrypt a QR payload for debugging
    from app.detector import CLIQRCodeDetector
    det = CLIQRCodeDetector(api_url=None, auth_token=None)
    print(det.decrypt_qr_data(args.data, args.secret))


def build_parser():
    version = os.getenv('VERSION', '0.1')
    epilog = (
        "Quick start:\n"
        "  passito-verifier [--api-url URL --auth-token TOKEN] [--config config.json] [--debug]\n\n"
        "Common commands:\n"
        "  passito-verifier               # Start (default)\n"
        "  passito-verifier start --debug\n"
        "  passito-verifier register --api-url http://passito.local --auth-token TOKEN\n"
        "  passito-verifier test-api --api-url http://passito.local --auth-token TOKEN\n"
        "  passito-verifier is-active --api-url http://passito.local --auth-token TOKEN\n"
        "  passito-verifier config --config config.json\n"
        "  passito-verifier decrypt --data <base64> --secret passito\n\n"
        "Environment variables:\n"
        "  API_URL, AUTH_TOKEN, CONFIG_PATH, VERSION\n\n"
        "Notes:\n"
        "  - The 'start' command is the default; you can omit it.\n"
        "  - CLI flags override environment variables when provided.\n"
    )
    parser = argparse.ArgumentParser(
        prog=f'passito-verifier v{version}',
        description=f'Passito Verifier CLI v{version}',
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=argparse.SUPPRESS
    )
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--config', default='config.json', help='Path to config file')
    parser.add_argument('--api-url', dest='api_url', help='API base url')
    parser.add_argument('--auth-token', dest='auth_token', help='Auth token')
    parser.add_argument('--version', action='version', version=f'%(prog)s {version}')

    sub = parser.add_subparsers(dest='command', required=False, metavar='command', title=f'Commands')

    p_start = sub.add_parser('start', help='Start QR verifier loop')
    p_start.set_defaults(func=cmd_start)

    p_reg = sub.add_parser('register', help='Register device with server')
    p_reg.set_defaults(func=cmd_register)

    p_tapi = sub.add_parser('test-api', help='Test API availability')
    p_tapi.set_defaults(func=cmd_test_api)

    p_act = sub.add_parser('is-active', help='Check if device is active')
    p_act.set_defaults(func=cmd_is_active)

    p_cfg = sub.add_parser('config', help='Show local registration cache')
    p_cfg.set_defaults(func=cmd_config)

    p_dec = sub.add_parser('decrypt', help='Decrypt a QR payload')
    p_dec.add_argument('--data', required=True, help='Base64 AES-GCM payload')
    p_dec.add_argument('--secret', default='passito', help='Shared secret')
    p_dec.set_defaults(func=cmd_decrypt)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    # Default to 'start' if no subcommand provided
    if not hasattr(args, 'func'):
        args.func = cmd_start
    args.func(args)


if __name__ == '__main__':
    main()


