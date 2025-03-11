import sys
import shutil
import time
import os
from multiprocessing import Process
from PIL import Image

# Configuration
MAX_WIDTH = 80
REFRESH_INTERVAL = 1  # seconds
ASCII_CHARS = "@%#*+=-:. "

class ASCIIBackgroundManager:
    def __init__(self, image_path):
        self.image_path = os.path.abspath(image_path)
        self.running = True
        self.current_size = None
        
    def calculate_ascii_art(self):
        img = Image.open(self.image_path).convert('RGBA')
        term_width, term_height = shutil.get_terminal_size()
        
        width, height = img.size
        ratio = height / width / 1.8
        new_width = min(MAX_WIDTH, term_width - 4)
        new_height = int(new_width * ratio)
        img = img.resize((new_width, new_height))
        
        ascii_art = []
        for y in range(new_height):
            line = []
            for x in range(new_width):
                r, g, b, a = img.getpixel((x, y))
                if a < 255:
                    line.append((' ', None))
                    continue
                brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
                char = ASCII_CHARS[int(brightness / 255 * (len(ASCII_CHARS) - 1))]
                line.append((char, (r, g, b)))
            ascii_art.append(line)
        return ascii_art

    def draw_art(self, ascii_art):
        term_width, term_height = shutil.get_terminal_size()
        art_height = len(ascii_art)
        
        sys.stdout.write('\033[s')  # Save cursor
        vertical_pos = term_height - art_height - 2
        horizontal_offset = term_width - MAX_WIDTH - 4
        
        sys.stdout.write(f'\033[{vertical_pos}H')
        
        for line in ascii_art:
            sys.stdout.write(f'\033[{horizontal_offset}C')
            for char, color in line:
                if color:
                    r, g, b = color
                    sys.stdout.write(f'\033[38;2;{r};{g};{b}m{char}\033[0m')
                else:
                    sys.stdout.write(char)
            sys.stdout.write('\n')
        
        sys.stdout.write('\033[u')  # Restore cursor
        sys.stdout.flush()

    def run(self):
        while self.running:
            new_size = shutil.get_terminal_size()
            if new_size != self.current_size:
                ascii_art = self.calculate_ascii_art()
                self.draw_art(ascii_art)
                self.current_size = new_size
            time.sleep(REFRESH_INTERVAL)

def start_background_process(image_path):
    manager = ASCIIBackgroundManager(image_path)
    process = Process(target=manager.run)
    process.daemon = True
    process.start()
    return process

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <image-path>")
        sys.exit(1)

    try:
        process = start_background_process(sys.argv[1])
        while True:  # Keep main process alive
            time.sleep(3600)
    except KeyboardInterrupt:
        sys.stdout.write('\033[2J\033[H')
        sys.exit(0)