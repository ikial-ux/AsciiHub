import sys
import shutil
from PIL import Image
import signal

def handle_resize(signum, frame):
    global ascii_art
    ascii_art = png_to_ascii(image_path, max_width=max_width, colored=True)
    print_ascii_art(ascii_art)

def png_to_ascii(image_path, max_width=100, colored=True):
    img = Image.open(image_path).convert('RGBA')
    term_width, term_height = shutil.get_terminal_size()
    
    # Adjust for terminal character aspect ratio
    width, height = img.size
    ratio = height / width / 1.8
    new_width = min(max_width, term_width - 4)
    new_height = int(new_width * ratio)
    
    img = img.resize((new_width, new_height))
    
    ascii_chars = "@%#*+=-:. "
    ascii_art = []
    
    for y in range(new_height):
        line = []
        for x in range(new_width):
            r, g, b, a = img.getpixel((x, y))
            if a < 255:
                line.append((' ', None))
                continue
                
            brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
            char = ascii_chars[int(brightness / 255 * (len(ascii_chars) - 1))]
            line.append((char, (r, g, b) if colored else None))
        ascii_art.append(line)
    
    return ascii_art

def print_ascii_art(ascii_art):
    term_width, term_height = shutil.get_terminal_size()
    art_height = len(ascii_art)
    
    # Save cursor position
    sys.stdout.write('\033[s')
    
    # Draw at bottom-right with offset
    vertical_pos = term_height - art_height - 2  # 2 lines above bottom
    horizontal_offset = term_width - max_width - 4
    
    # Move to starting position
    sys.stdout.write(f'\033[{vertical_pos}H')
    
    for line in ascii_art:
        # Move right and print line
        sys.stdout.write(f'\033[{horizontal_offset}C')
        for char, color in line:
            if color:
                r, g, b = color
                sys.stdout.write(f'\033[38;2;{r};{g};{b}m{char}\033[0m')
            else:
                sys.stdout.write(char)
        sys.stdout.write('\n')
    
    # Restore cursor position
    sys.stdout.write('\033[u')
    sys.stdout.flush()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <image-path> [max-width]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    max_width = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    
    # Initial draw
    ascii_art = png_to_ascii(image_path, max_width, colored=True)
    print_ascii_art(ascii_art)
    
    # Handle terminal resize
    signal.signal(signal.SIGWINCH, handle_resize)
    
    # Keep process running in background
    try:
        while True:
            # Reduce CPU usage
            sys.stdin.read(1)
    except KeyboardInterrupt:
        sys.exit(0)