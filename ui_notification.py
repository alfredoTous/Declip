import subprocess

# Show desktop notification (handled by dunst in my setup) on urgency mode 'critical' for errors
def print_error(error_msj, args):
    
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
def show_data(data, mode, args):

    if args.quiet:
        return

    subprocess.run([
        "notify-send",
        "-t", "5000",
        f"🧩 {mode}",
        str(data).strip()
    ])
