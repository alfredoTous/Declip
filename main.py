#!/usr/bin/env python3

import pyperclip
import sys
import os
import signal
import argparse
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

    parser.add_argument("-v", action="store_true", help="Activate logs on script dir")

    return parser.parse_args()

# Checks if rofi is available
def check_rofi():
    return shutil.which('rofi')


def exit_with_error(msg):
    if args.quiet not in ('error', 'all'):
        ui_notification.print_error(msg)
    sys.exit(1)


def main():
    # Ensure user local/bin is in Path for hashid when script is executed via sxhkd
    os.environ["PATH"] += os.pathsep + os.path.expanduser("~/.local/bin")
    # Set arguments to global scope, not the best practice but we can take the risk on a small tool like this ;)
    global args
    args = parse_args()

    # Get data from clipboard
    data = pyperclip.paste()

    if not check_rofi():
        exit_with_error('Rofi was not found')

    # Validate clipboard and arguments 
    if not data or len(data) == 0:
        exit_with_error('clipboard empty')

    if not args.decode and not args.encode:
        exit_with_error('Invalid Arguments: script needs --decode OR --encode argument')
 
    if args.decode and args.encode:
        exit_with_error('Invalid Arguments: use only one mode --decode OR --encode')

    result_data = None
    mode = None

    # Decode
    if args.decode:
        opt = ui_rofi.menu_select('Decode')
        if opt == None:
            exit_with_error('Option not valid')
        result_data = decode_data(data, opt)
        mode = 'Decode'

    # Encode
    if args.encode:
        opt = ui_rofi.menu_select('Encode')
        if opt == None:
            exit_with_error('Option not valid')
        result_data = encode_data(data, opt)
        mode = 'Encode'

    if result_data == None:
        exit_with_error('Unexpected Error')

    if not args.no_clip:
        pyperclip.copy(str(result_data)) 
    
    if args.quiet not in ('data', 'all'):
        ui_notification.show_data(result_data, mode)
   
    return result_data


if __name__ == '__main__':
    print(main())


