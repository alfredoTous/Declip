# Declip

Utility tool for **encoding and decoding data rapidly from the clipboard**, designed for **developers and security enthusiasts** who constantly work with encoded or obfuscated data and want a faster, cleaner workflow.

---

## Demo

https://github.com/user-attachments/assets/24bf7388-1a57-4f4c-99a3-a2f1303e1f1d

## 🧠 Overview

Please note: **Declip** was developed as a small but efficient tool for my personal red-team workflow. Feel free to adapt it to your own setup.  
It's not meant to be perfect, just **fast, minimal, and effective**.

Available parameters:

```bash
./declip.py --help
usage: declip.py [-h] [--decode] [--encode] [--no-clip] [--quiet [{error,data,all}]] [--log] [-o OUTPUT]

Utils Tool for decoding and encoding data rapidly from clipboard

options:
  -h, --help            show this help message and exit
  --decode              Setup tool for decoding
  --encode              Setup tool for encoding
  --no-clip             Don't copy result to clipboard
  --quiet [{error,data,all}]
                        Silence notifications, 'error' to hide errors, 'data' to hide decoded/encoded data, 'all' to hide both (default)
  --log                 Activate logs, defaults output to './declip.log'
  -o, --output OUTPUT   Select output dir for logs
```

Declip was tested on **Arch Linux** and **Kali Linux**  
Currently, there is **no support for Windows**


---

## ⚙️ Workflow

In my setup, Declip is managed by my shortcut manager **SXHKD**  
If you also use SXHKD, you can simply add a shortcut in `~/.config/sxhkd/sxhkdrc` to call the script with your preferred arguments

```bash
# Decode clipboard content
super + d
  ~/path/to/declip/declip.py --decode --log 

# Encode clipboard content
super + shift + d
  ~/path/to/declip/declip.py --encode --log 
```

Select some data → press your shortcut → choose an encoding scheme (Base64, URL, Hex, ROT, etc.) → and instantly get the result via `notify-send` or directly copied back to your clipboard

Notifications are shown using **notify-send** (handled by **dunst** in my setup), but it should work natively with any compatible notification daemon  
You can freely customize the notification aesthetics through your preferred notification manager

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

You’ll also need:
- **rofi**: for the selection menus  
- **notify-send**: for displaying notifications (comes by default with most distros)

For hash identification:
- `pip install hashid`  
  or  
- Clone [hash-identifier](https://github.com/blackploit/hash-identifier/)

> On *hash-id* mode, the encode/decode flag doesn’t change behavior, it will simply use a different tool if both are installed.

---

## ✨ Features

- Fast and lightweight, designed for rapid clipboard operations  
- Rofi integration 
- Supports **Base64**, **Base32**, **Hex**, **URL**, **ROT**, **XOR**, and **Hash-ID**  
- Logging system (`--log`, `-o`) with automatic rotation  
- Configurable quiet mode (`--quiet error|data|all`)  
- Clipboard content logged in full (not truncated) for traceability  
- Designed for execution via **SXHKD** shortcuts  
- Notifications handled via `notify-send`

> ⚠️ When logs are active and Declip is executed via SXHKD, passing `--output ./...`  
> will use the **script's directory** as the base path, not SXHKD's runtime directory.

---

## To-Do

- [ ] Improve XOR functionality to support non-ASCII data (hex, base64, binary)  
- [ ] Add clipboard history integration on menu
- [ ] Support `--no-rofi` mode with a native Python GUI (Tkinter or similar)  
- [ ] Bug maintenance  

---

