import time
import sys
import os
import msvcrt
import shutil
import subprocess
from pathlib import Path

def install_requirements():
    requirements = Path(__file__).with_name("requirements.txt")

    try:
        import pynput
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements),
        ])

install_requirements()

from pynput import keyboard

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def limit_input(prompt, max_chars):
    print(prompt, end="", flush=True)
    user_input = ""
    
    while True:
        char = msvcrt.getch()

        if char == b'\x1b':
            return "BACK"
        
        if char in (b'\r', b'\n'):
            print()
            break
            
        if char == b'\x08':
            if len(user_input) > 0:
                user_input = user_input[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
            continue
            
        if len(user_input) < max_chars:
            char_str = char.decode('utf-8', errors='ignore')
            if char_str.isprintable() and len(char_str) > 0:
                user_input += char_str
                sys.stdout.write(char_str)
                sys.stdout.flush()
                
    return user_input

def padding_top(num_lines):
    terminal_width, terminal_height = shutil.get_terminal_size()
    top_padding = (terminal_height - num_lines) // 2
    if top_padding > 0:
        print("\n" * top_padding, end="")

def padding(text):
    columns, _ = shutil.get_terminal_size()
    
    padding = (columns - len(text)) // 2
    if padding > 0:
        sys.stdout.write(" " * padding)
        sys.stdout.flush()

def type_out(text, delay=0.01):
    padding(text)
    for char in text:
      sys.stdout.write(char)
      sys.stdout.flush()
      time.sleep(delay)
    print()  

def staff_or_customer():
    clear_terminal()
    padding_top(8)
    sys.stdout.write("\033[?25h")
    type_out(' '+'_'*48+' ')
    type_out('|'+' '*48+'|')
    type_out('|'+' '*48+'|')
    type_out('|'+' '*21+'Login'+' '*22+'|')
    type_out('|'+' '*48+'|')
    type_out('|'+' '*15+'> Staff'+' '*26+'|')
    type_out('|'+' '*17+'Customer'+' '*23+'|')
    type_out('|'+' '*48+'|')
    type_out('|'+' '*48+'|')
    type_out('|'+'_'*48+'|')
    role = 'Staff'
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    sys.stdout.write("\033[5A\r")
    sys.stdout.flush()
    def on_press(key):
        nonlocal role
        if key == keyboard.Key.up or (hasattr(key, 'char') and key.char == 'w'):
            if role == 'Customer':
                role = 'Staff'
                padding(' '*50)
                print('|'+' '*15+'> Staff'+' '*26+'|')
                padding(' '*50)
                print('|'+' '*17+'Customer'+' '*23+'|')
                sys.stdout.write("\033[2A\r")
                sys.stdout.flush()
        elif key == keyboard.Key.down or (hasattr(key, 'char') and key.char == 's'):
            if role == 'Staff':
                role = 'Customer'
                padding(' '*50)
                print('|'+' '*17+'Staff'+' '*26+'|')
                padding(' '*50)
                print('|'+' '*15+'> Customer'+' '*23+'|')
                sys.stdout.write("\033[2A\r")
                sys.stdout.flush()
        elif key == keyboard.Key.enter:
            return False
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    while msvcrt.kbhit():
        msvcrt.getch()
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    sys.stdout.write("\033[H")
    sys.stdout.flush()
    return role

def login(role):
    clear_terminal()
    padding_top(10)
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()
    padding(' '*50); print(' '+'_'*48+' ')
    padding(' '*50); print('|'+' '*48+'|')
    padding(' '*50); print('|'+' '*48+'|')
    padding(' '*50); print('|'+' '*48+'|')
    padding(' '*50); print('|'+' '*48+'|')
    padding(' '*50); print('|'+' '*48+'|')
    padding(' '*50); print('|'+' '*48+'|')
    padding(' '*50); print('|'+' '*48+'|')
    padding(' '*50); print('|'+' '*48+'|')
    padding(' '*50); print('|'+' '*48+'|')
    padding(' '*50); print('|'+'_'*48+'|')
    columns, _ = shutil.get_terminal_size()
    left_margin = (columns - 50) // 2
    if role == 'Staff':
        role_margin = 18
        role_input_limit = 22
    else:
        role_margin = 17
        role_input_limit = 19
    sys.stdout.write(f"\033[7A\r\033[{left_margin + 1 + role_margin}C")
    sys.stdout.flush()
    for char in f"{role} Login":
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    sys.stdout.write(f"\033[2B\r\033[{left_margin + 1 + 10}C")
    sys.stdout.flush()
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()
    for char in f"{role} Username:":
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    sys.stdout.write(f"\033[1B\r\033[{left_margin + 1 + 10}C")
    sys.stdout.flush()
    for char in f"{role} Password:":
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)

    sys.stdout.write("\033[1A\r")
    sys.stdout.flush()

    padding(' '*50)
    username = limit_input('|'+' '*10+f'{role} Username:', role_input_limit)
    if username == 'BACK':
        while msvcrt.kbhit():
            msvcrt.getch()
        return 'BACK', 'BACK'
    while len(username) < 4:
        sys.stdout.write("\033[1A\r")
        sys.stdout.flush()  
        padding(' '*50)
        print('|'+' '*10+f'{role} Username:'+' '*(role_input_limit+1)+'|')
        sys.stdout.write("\033[1A\r")
        sys.stdout.flush()  
        padding(' '*50)
        username = limit_input('|'+' '*10+f'{role} Username:', role_input_limit)


    padding(' '*50)
    password = limit_input('|'+' '*10+f'{role} Password:', role_input_limit)
    if password == 'BACK':
        return 'BACK', password
    while len(password) < 4:
        sys.stdout.write("\033[1A\r")
        sys.stdout.flush()  
        padding(' '*50)
        print('|'+' '*10+f'{role} Password:'+' '*(role_input_limit+1)+'|')
        sys.stdout.write("\033[1A\r")
        sys.stdout.flush()  
        padding(' '*50)
        password = limit_input('|'+' '*10+f'{role} Password:', role_input_limit)
    
    sys.stdout.write("\033[H")
    sys.stdout.flush()
    sys.stdout.write("\033[?25l")

    return username, password


def main():
    while True:
        role = staff_or_customer()
        username, password = login(role)
        if username == 'BACK' or password == 'BACK':
            continue
        break
    print(f'Role: {role}, Username: {username}, Password: {password}')

main()