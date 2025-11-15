import subprocess
import ui_rofi
from itertools import cycle
import shutil


def rot_get_n(mode):
    n = ui_rofi.input_prompt(mode, 'Enter a number from 1 to 26')
    if not n:
        raise Exception('Invalid Input')
    try:
        n = int(n)
        if not (1 <= n <= 26):
            raise Exception('Number out of range (1–26)')
        return n
    except Exception as e:
        raise Exception(f'Expected a valid integer: {e}')

def rot_encode(n=None):
    if not n:
        n = rot_get_n('Encode')

    from string import ascii_lowercase as lc, ascii_uppercase as uc
    lookup = str.maketrans(lc + uc, lc[n:] + lc[:n] + uc[n:] + uc[:n])
    return lambda s: s.translate(lookup)

def rot_decode():
    n = rot_get_n('Decode')
    return rot_encode(-n)


def xor_decrypt(data):
    key = ui_rofi.input_prompt('Decrypt', 'Enter Key')
    return ''.join(chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(data, key * (len(data) // len(key) + 1)))

def xor_encrypt(data):
    key = ui_rofi.input_prompt('Encrypt', 'Enter Key')
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, cycle(key)))

# Checks which hash Identification tool is available
def check_hash_tools():
    tools = []
    for tool in ('hashid', 'hash-identifier'):
        if shutil.which(tool):
            tools.append(tool)
    if len(tools) == 0:
        raise Exception('No Hash Identification Tool found')
    
    return tools


def hash_id(data, mode):
    # Mode doesn't really matter, just uses a different tool to determine hash type
    hash_tools = check_hash_tools() 
    # Select hash tool, if both exists let mode decide which to use
    if len(hash_tools) == 1:
        tool = hash_tools[0]
    elif len(hash_tools) >= 2:
        if mode == 'encode':
            tool = hash_tools[0]
        elif mode == 'decode':
            tool = hash_tools[1]

    # Execute command
    result = subprocess.run(
        [tool, data],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f'{tool} failed: {result.stderr.strip()}')
    
    return result.stdout.strip()


