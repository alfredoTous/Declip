import ui_rofi

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

