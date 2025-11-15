
ROFI_THEME = """
        * {
            background: rgba(10, 10, 10, 0.90);
            border: 0;
            border-radius: 10px;
            font: "JetBrainsMono Nerd Font 11";
            text-color: #eaeaea;
            spacing: 4px;
        }

        window {
            width: 18em;
            padding: 8px;
            transparency: "real";
            location: center;
        }

        inputbar {
            background-color: transparent;
            border: 0;
            margin: 0 0 8px 0;
            children: [prompt, entry];
        }

        prompt {
            text-color: #a3be8c;
            font: "JetBrainsMono Nerd Font Bold 12";
            padding: 2px 4px;
        }

        entry {
            expand: true;
            text-color: #ffffff;
            background-color: rgba(255,255,255,0.08);
            border-radius: 6px;
            padding: 4px 6px;
        }

        listview {
            scrollbar: false;
            spacing: 3px;
            lines: 4;
            background-color: rgba(10,10,10,0.90);
        }

        element {
            padding: 3px 8px;
            border-radius: 6px;
            background-color: rgba(25,25,25,0.85); 
        }

        element normal.normal, element alternate.normal {
            background-color: rgba(25,25,25,0.85); 
            text-color: #e5e9f0;
        }

        element selected.normal, element selected.active, element selected.urgent {
            background-color: rgba(136, 192, 208, 0.25);
            text-color: #88c0d0;
        }

        element-text, element-icon {
            text-color: #e5e9f0;
        }

        element-text selected {
            text-color: #88c0d0;
        }
"""

ROFI_INPUT_PROMPT_THEME = """
        * {
            background: rgba(10,10,10,0.94);
            font: "JetBrainsMono Nerd Font 13";
            text-color: #e5e9f0;
        }

        window {
            location: center;
            width: 19em;
            border: 2px;
            border-color: #88c0d0;
            border-radius: 6px;
            padding: 0;
        }

        mainbox {
            children: [inputbar, message];
            spacing: 2px;
            margin: 0;
            padding: 2px 0;
        }

        inputbar {
            children: [prompt, entry];
            spacing: 2px;
            margin: 0;
            padding: 2px 4px;
        }

        prompt {
            text-color: #88c0d0;
            font: "JetBrainsMono Nerd Font Bold 13";
            padding: 0 4px 0 0;
        }

        entry {
            expand: true;
            text-color: #9ece6a;
            background-color: rgba(255,255,255,0.08);
            border-radius: 4px;
            padding: 1px 6px;
        }

        message {
            font: "JetBrainsMono Nerd Font 10";
            padding: 0 6px 2px 6px;
            margin: 0;
        }

"""
