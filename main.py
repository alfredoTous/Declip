#!/usr/bin/env python3

import pyperclip
import sys
import signal
import argparse
import subprocess
import base64
from urllib.parse import unquote, urlencode
from rofi_css import ROFI_THEME

"""
   TO-DO 
    3. Check if Rofi is available
    4. Verify behavior on different cases 
    6. README.md 
    7. Add xor, rot, hash-id
    8. Add logs
"""

# Ctrl+C
def def_handler(sig, frame):
    print('\nBye...')
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# Rofi menu for selecting decode/encode mode
def rofi_menu_select(mode):
    options = "1. Base64\n2. URL\n3. Hex\n4. Base32"
    
    # Define command
    rofi_cmd = [
        "rofi",
        "-no-config",
        "-dmenu",
        "-p", mode,
        "-font", "JetBrainsMono Nerd Font 13",
        "-lines", "4",
        "-width", "18",
        "-no-fixed-num-lines",
        "-i",
        "-theme-str", ROFI_THEME
    ]
    # Execute command
    result = subprocess.run(
        rofi_cmd,
        input=options,
        text=True,
        capture_output=True
    )
    
    # Get stdout
    opt = result.stdout.strip()
    
    # Return mode
    if opt.startswith("1"):
        return 'base64'
    elif opt.startswith("2"):
        return 'url'
    elif opt.startswith("3"):
        return 'hex'
    elif opt.startswith("4"):
        return 'base32'
    else:
        return None


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

        return decoded_data # type: ignore 

    except Exception as e:
        print_error_notification(f"Error at decoding: {e}")
        sys.exit(1)

# Encode given the data and mode
def encode_data(data, opt):

    try:
        if opt == 'base64':
            data_bytes = data.encode('utf-8')
            encoded_data_bytes = base64.b64encode(data_bytes)
            encoded_data = encoded_data_bytes.decode('utf-8')
        elif opt == 'url':
            encoded_data = urlencode(data)
        elif opt == 'hex':
            encoded_data = data.encode("utf-8").hex()
        elif opt == 'base32':
            data_bytes = data.encode('utf-8')
            encoded_data_bytes = base64.b32encode(data_bytes)
            encoded_data = encoded_data_bytes.decode('utf-8')
        
        return encoded_data #type: ignore

    except Exception as e:
        print_error_notification(f"Error at encoding: {e}")
        sys.exit(1)


# Show desktop notification (handled by dunst in my setup) on urgency mode 'critical' for errors
def print_error_notification(error_msj):
    
    if args.quiet:
        return

    subprocess.run([
        "notify-send",
        "-u", "critical",
        "-t", "6000",
        "⚠️ Error",
        error_msj.strip()
    ])

# Show desktop notification (handled by dunst in my setup) for correctly decoded/encoded data
def show_data_notification(data, mode):

    if args.quiet:
        return

    subprocess.run([
        "notify-send",
        "-t", "5000",
        f"🧩 {mode}",
        str(data).strip()
    ])


# Parse arguments
def parse_args():
    parser = argparse.ArgumentParser(description= "Utils Tool for decoding and encoding data rapidly from clipboard")

    parser.add_argument("--decode", action="store_true", help="Setup tool for decoding")

    parser.add_argument("--encode", action="store_true", help="Setup tool for encoding")

    parser.add_argument("--no-clip", action="store_true", help="Don't copy result to clipboard")

    parser.add_argument("--quiet", action="store_true", help="Don't show notifications")

    parser.add_argument("-v", action="store_true", help="Activate logs on script dir")

    return parser.parse_args()


def check_rofi():
    # Checks if rofi is available
    pass

def main():
    # Set arguments to global scope, not the best practice but we can take the risk on a small tool like this ;)
    global args
    args = parse_args()

    # Get data from clipboard
    data = pyperclip.paste()

    # Validate clipboard and arguments 
    if not data or len(data) == 0: 
        print_error_notification('clipboard empty') 
        sys.exit(1) 

    if not args.decode and not args.encode:
        print_error_notification('Invalid Arguments: script needs --decode OR --encode argument')
        sys.exit(1)

    if args.decode and args.encode:
        print_error_notification('Invalid Arguments: use only one mode --decode OR --encode')
        sys.exit(1)

    result_data = None
    mode = None

    # Decode
    if args.decode:
        opt = rofi_menu_select('Decode')
        if opt == None:
            print_error_notification('Option not valid')
            sys.exit(1)
        result_data = decode_data(data, opt)
        mode = 'Decode'

    # Encode
    if args.encode:
        opt = rofi_menu_select('Encode')
        if opt == None:
            print_error_notification('Option not valid')
            sys.exit(1)
        result_data = encode_data(data, opt)
        mode = 'Encode'

    if result_data == None:
        print_error_notification("Unexpected Error")
        sys.exit(1)

    if not args.no_clip:
        pyperclip.copy(str(result_data)) 
    
    show_data_notification(result_data, mode)
   
    return result_data

if __name__ == '__main__':
    print(main())


