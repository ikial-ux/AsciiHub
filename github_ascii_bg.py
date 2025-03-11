# save as github_ascii_bg.py
import sys
import shutil
import time

def draw_background():
    cols, lines = shutil.get_terminal_size()
    
    # GitHub logo with dim colors
    art = [
        "          \x1b[38;5;240m.--.\x1b[0m      ",
        "       \x1b[38;5;240m.-'  '-.\x1b[0m     ",
        "      \x1b[38;5;240m/  \x1b[38;5;245mO\x1b[0m   \x1b[38;5;245mO\x1b[0m  \x1b[38;5;240m\\\x1b[0m  ",
        "     \x1b[38;5;240m|    \x1b[38;5;240m.-.    \x1b[38;5;240m|\x1b[0m  ",
        "      \x1b[38;5;240m\\  \x1b[38;5;240m'-'\x1b[0m  \x1b[38;5;240m/\x1b[0m   ",
        "       \x1b[38;5;240m'._____.'\x1b[0m    ",
        "          \x1b[38;5;240m| |\x1b[0m       ",
        "          \x1b[38;5;240m| |\x1b[0m       ",
        "          \x1b[38;5;240m'-'\x1b[0m       "
    ]

    # Save cursor position and disable scrolling
    sys.stdout.write("\x1b[s\x1b[?1049h")

    # Clear screen and move to bottom
    sys.stdout.write("\x1b[2J\x1b[999B")

    # Draw art at bottom-center
    for i, line in enumerate(reversed(art)):
        line_len = len(line.replace("\x1b[38;5;240m", "")
                         .replace("\x1b[38;5;245m", "")
                         .replace("\x1b[0m", ""))
        padding = (cols - line_len) // 2
        sys.stdout.write(f"\x1b[999H\x1b[{i + 1}A\x1b[{padding}C{line}")

    # Restore cursor and enable scrolling
    sys.stdout.write("\x1b[u\x1b[?1049l\x1b[0m")
    sys.stdout.flush()

if __name__ == "__main__":
    draw_background()
    # Keep running in background
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        sys.stdout.write("\x1b[2J\x1b[H")
        sys.exit(0)