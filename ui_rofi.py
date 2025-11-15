from rofi_css import ROFI_THEME, ROFI_INPUT_PROMPT_THEME
import subprocess

# Rofi menu for selecting decode/encode mode
def menu_select(mode):
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

# Aux rofi menu for prompting when more data is needed for the decode/encode
def input_prompt(mode, msg):

    rofi_cmd = [
        "rofi",
        "-no-config",
        "-dmenu",
        "-p", mode,
        "-mesg", msg,
        "-lines", "0",
        "-width", "26",
        "-theme-str", ROFI_INPUT_PROMPT_THEME
    ]

    result = subprocess.run(
        rofi_cmd,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()



