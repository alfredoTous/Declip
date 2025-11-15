import subprocess

# Show desktop notification (handled by dunst in my setup) on urgency mode 'critical' for errors
def print_error(error_msg):

    subprocess.run([
        "notify-send",
        "-u", "critical",
        "-t", "6000",
        "⚠️ Error",
        error_msg.strip()
    ])

# Show desktop notification (handled by dunst in my setup) for correctly decoded/encoded data
def show_data(data, mode):

    subprocess.run([
        "notify-send",
        "-t", "5000",
        f"🧩 {mode}",
        str(data).strip()
    ])
