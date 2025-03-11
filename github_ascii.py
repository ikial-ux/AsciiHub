import os
import sys
import shutil

def github_ascii():
    cols, lines = shutil.get_terminal_size()
    
    ascii_art = r'''
          .--.      
       .-'  '-.     
      /  \033[38;5;255mO\033[0m   \033[38;5;255mO\033[0m  \  
     |    \033[38;5;240m.-.\033[0m    |  
      \  \033[38;5;240m'-'\033[0m  /   
       '._____.'    
          | |       
          | |       
          '-'      '''
    
    # Split colored art and calculate padding
    art_lines = [line for line in ascii_art.split('\n') if line.strip()]
    v_padding = (lines - len(art_lines)) // 2
    
    # Clear screen and set cursor
    sys.stdout.write('\033[2J\033[3J\033[H')
    
    # Print vertical padding
    sys.stdout.write('\n' * v_padding)
    
    # Center each line
    for line in art_lines:
        line_len = len(line.replace('\033[38;5;255m', '').replace('\033[38;5;240m', '').replace('\033[0m', ''))
        h_padding = (cols - line_len) // 2
        sys.stdout.write(' ' * h_padding + line + '\n')
    
    # Move cursor to bottom
    sys.stdout.write('\033[999B\r')
    sys.stdout.flush()

if __name__ == '__main__':
    github_ascii()