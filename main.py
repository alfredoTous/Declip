#!/usr/bin/env python3

import pyperclip
import sys
import os
import signal
import argparse
import logging
import logging.handlers
import base64
import shutil
from urllib.parse import unquote, quote

import ui_rofi
import ui_notification
import codec

"""
   TO-DO 
    4. Verify behavior on different cases 
    6. README.md 
    7. Improve xor
    8. Add logs and -o for output log, default ./declip.log
"""

# Ctrl+C
def def_handler(sig, frame):
    print('\nBye...')
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


# Decode given the data and mode
def decode_data(data, opt):

    try:
        if opt == 'base64':
            decoded_data = base64.b64decode(data).decode()
        elif opt == 'url':
            decoded_data = unquote(data)
        elif opt == 'hex':
            decoded_data = bytes.fromhex(data).decode('utf-8')
        elif opt == 'base32':
            decoded_data = base64.b32decode(data).decode()
        elif opt == 'rot':
            decoded_data = codec.rot_decode()(data)
        elif opt == 'xor':
            decoded_data = codec.xor_decrypt(data)
        elif opt == 'hash-id':
            decoded_data = codec.hash_id(data, 'decode')

        return decoded_data # type: ignore 

    except Exception as e:
        exit_with_error(f'Error at decoding: {e}')


# Encode given the data and mode
def encode_data(data, opt):

    try:
        if opt == 'base64':
            data_bytes = data.encode('utf-8')
            encoded_data_bytes = base64.b64encode(data_bytes)
            encoded_data = encoded_data_bytes.decode('utf-8')
        elif opt == 'url':
            encoded_data = quote(data)
        elif opt == 'hex':
            encoded_data = data.encode("utf-8").hex()
        elif opt == 'base32':
            data_bytes = data.encode('utf-8')
            encoded_data_bytes = base64.b32encode(data_bytes)
            encoded_data = encoded_data_bytes.decode('utf-8')
        elif opt == 'rot':
            encoded_data =  codec.rot_encode()(data)
        elif opt == 'xor':
            encoded_data = codec.xor_encrypt(data) 
        elif opt == 'hash-id':
            encoded_data = codec.hash_id(data, 'encode')
        
        return encoded_data #type: ignore

    except Exception as e:
        exit_with_error(f'Error at encoding: {e}')


# Parse arguments
def parse_args():
    parser = argparse.ArgumentParser(description= "Utils Tool for decoding and encoding data rapidly from clipboard")

    parser.add_argument("--decode", action="store_true", help="Setup tool for decoding")

    parser.add_argument("--encode", action="store_true", help="Setup tool for encoding")

    parser.add_argument("--no-clip", action="store_true", help="Don't copy result to clipboard")

    parser.add_argument(
        "--quiet", 
        nargs="?",
        const="all", # Default value
        choices=["error", "data", "all"],
        help="Silence notifications, 'error' to hide errors, 'data' to hide decoded/encoded data, 'all' to hide both (default)"
    )

    parser.add_argument("--log", action="store_true", help="Activate logs, defaults output to './declip.log'")

    parser.add_argument("-o", "--output", default="./declip.log", help="Select output dir for logs")

    return parser.parse_args()

# Checks if rofi is available
def check_rofi():
    return shutil.which('rofi')

# Get real script location for when executing via sxhkd
def get_script_dir():
    try:
        actual_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(actual_dir, args.output)
        # Test write permissions
        with open(path, 'a'):
            pass
        return path
    except Exception:
        # If no permissions, fallback to user dir
        return os.path.expanduser("~/")


# Setup logs only if --log passed as argument
def setup_logs():    
    # Ensure log directory exists
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    
    # Call get_script_dir if -o is referencing actual dir
    if str(args.output).startswith('./'):
        args.output = get_script_dir()

    # Handler for filename and rotating log files when size is > 5MB
    handler = logging.handlers.RotatingFileHandler(
        filename=args.output, 
        maxBytes=5 * 1024 * 1024,
        backupCount=3 
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[handler]
    )

    logger = logging.getLogger('declip')
    logger.info("=== Declip Started ===")
    return logger


def add_log_info(msg):
    if not args.log:
        return
    logger.info(msg)

def exit_with_error(msg):
    if args.quiet not in ('error', 'all'):
        ui_notification.print_error(msg)
    if args.log:
        logger.error(msg)
        logger.error('=== Bad Exit... ===')
    sys.exit(1)


def main():
    # Ensure user local/bin is in Path for hashid when script is executed via sxhkd
    os.environ["PATH"] += os.pathsep + os.path.expanduser("~/.local/bin")
    # Set arguments to global scope, not the best practice but we can take the risk on a small tool like this ;)
    global args
    args = parse_args()

    if args.log:
        global logger
        logger = setup_logs()

    # Get data from clipboard
    data = pyperclip.paste().strip()
    add_log_info(f'Copied from clipboard: {data}')
    
    if not check_rofi():
        exit_with_error('Rofi was not found')

    # Validate clipboard and arguments 
    if not data or not len(data) > 1:
        exit_with_error('clipboard empty')

    if not args.decode and not args.encode:
        exit_with_error('Invalid Arguments: script needs --decode OR --encode argument')
 
    if args.decode and args.encode:
        exit_with_error('Invalid Arguments: use only one mode --decode OR --encode')

    if not args.log and args.output != './declip.log':
        exit_with_error('Invalid Arguments: Can\'t use -o without passing argument --log')

    result_data = None
    mode = None

    # Decode
    if args.decode:
        add_log_info('Running mode: Decode')
        opt = ui_rofi.menu_select('Decode')
        add_log_info(f'Selected decode option: {opt}')
        if opt is None:
            exit_with_error('Option not valid')
        result_data = decode_data(data, opt)
        add_log_info(f'Decoded data: {result_data}')
        mode = 'Decode'

    # Encode
    if args.encode:
        add_log_info('Executing Declip on mode Encode...')
        opt = ui_rofi.menu_select('Encode')
        add_log_info(f'Selected encode option: {opt}')
        if opt is None:
            exit_with_error('Option not valid')
        result_data = encode_data(data, opt)
        add_log_info(f'Encoded data: {result_data}')
        mode = 'Encode'

    if result_data is None:
        exit_with_error('Unexpected Error')

    if not args.no_clip:
        pyperclip.copy(str(result_data)) 
        add_log_info(f'Copied result to clipboard')
    
    if args.quiet not in ('data', 'all'):
        ui_notification.show_data(result_data, mode)
    
    add_log_info("=== Declip Finished Successfully ===")
    return result_data


if __name__ == '__main__':
    print(main())


