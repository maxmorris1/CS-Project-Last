import time
import sys
import os
import msvcrt
import shutil
import subprocess
import ctypes
import threading
from ctypes import wintypes
import shutil
from time import sleep
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
os.chdir(SCRIPT_DIR)

try:
    from QueryDB import db_action
except ImportError as e:
    print(f"CRITICAL ERROR: Could not find QueryDB.py in {SCRIPT_DIR}!")
    print(e)
    input("\nPress Enter to exit...")
    sys.exit(1)

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)

SW_MAXIMIZE = 3

RED = "\033[31m"
BOLD_GREEN = "\033[1;32m"
RESET = "\033[0m"

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

def get_maximized_size():
    from pynput.keyboard import Controller, Key
    keyboard_controller = Controller()
    keyboard_controller.press(Key.f11)
    keyboard_controller.release(Key.f11)
    time.sleep(0.15) 
    return shutil.get_terminal_size()

def repeatLine(line: str, repeat: int) -> None:
    for _ in range(repeat):
        exec(line)

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

def type_out(text, delay=0.002):
    padding(text)
    for char in text:
      sys.stdout.write(char)
      sys.stdout.flush()
      time.sleep(delay)
    print()  

def type_out_nopadding(text, delay=0.002):
    for char in text:
      sys.stdout.write(char)
      sys.stdout.flush()
      time.sleep(delay)
    print()  

def staff_or_customer():
    clear_terminal()
    padding_top(21)
    sys.stdout.write("\033[?25h")
    type_out('╔'+'═'*48+'╗')
    type_out('║'+' '*48+'║')
    type_out('║'+' '*48+'║')
    type_out('║'+' '*48+'║')
    type_out('║'+' '*48+'║')
    type_out('║'+' '*48+'║')
    type_out('║'+' '*48+'║')
    type_out('║'+' '*21+'Login'+' '*22+'║')
    type_out('║'+' '*48+'║')
    type_out('║'+' '*48+'║')
    type_out('║'+' '*17+'Staff'+' '*26+'║')
    type_out('║'+' '*17+'Customer'+' '*23+'║')
    type_out('║'+' '*48+'║')
    type_out('║'+' '*48+'║')
    type_out('║'+' '*48+'║')
    type_out('║'+' '*48+'║')
    type_out('║'+' '*48+'║')
    type_out('║'+' '*48+'║')
    type_out('╚'+'═'*48+'╝')
    type_out('║'+' '+'Esc: Back    Arrows: Select'+' '*20+'║')
    type_out('╚'+'═'*48+'╝')
    role = 'Staff'
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    sys.stdout.write("\033[11A\r")
    sys.stdout.flush()
    padding(' '*50)
    print('║'+' '*15+f'{BOLD_GREEN}> Staff{RESET}'+' '*26+'║')
    padding(' '*50)
    print('║'+' '*17+'Customer'+' '*23+'║')
    sys.stdout.write("\033[2A\r")
    sys.stdout.flush()
    def on_press(key):
        nonlocal role
        if key == keyboard.Key.up or (hasattr(key, 'char') and key.char == 'w'):
            if role == 'Customer':
                role = 'Staff'
                padding(' '*50)
                print('║'+' '*15+f'{BOLD_GREEN}> Staff{RESET}'+' '*26+'║')
                padding(' '*50)
                print('║'+' '*17+'Customer'+' '*23+'║')
                sys.stdout.write("\033[2A\r")
                sys.stdout.flush()
        elif key == keyboard.Key.down or (hasattr(key, 'char') and key.char == 's'):
            if role == 'Staff':
                role = 'Customer'
                padding(' '*50)
                print('║'+' '*17+'Staff'+' '*26+'║')
                padding(' '*50)
                print('║'+' '*15+f'{BOLD_GREEN}> Customer{RESET}'+' '*23+'║')
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
    padding_top(21)
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()
    padding(' '*50); print('╔'+'═'*48+'╗')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('╚'+'═'*48+'╝')
    padding(' '*50); print('║'+' '+'Esc: Back    Enter: Continue'+' '*19+'║')
    padding(' '*50); print('╚'+'═'*48+'╝')
    columns, _ = shutil.get_terminal_size()
    left_margin = (columns - 50) // 2
    if role == 'Staff':
        role_margin = 18
        role_input_limit = 22
    else:
        role_margin = 17
        role_input_limit = 19
    sys.stdout.write(f"\033[14A\r\033[{left_margin + 1 + role_margin}C")
    sys.stdout.flush()
    for char in f"{role} Login":
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    sys.stdout.write(f"\033[3B\r\033[{left_margin + 1 + 10}C")
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
    username = limit_input('║'+' '*10+f'{role} Username:', role_input_limit)
    if username == 'BACK':
        while msvcrt.kbhit():
            msvcrt.getch()
        return 'BACK', 'BACK'
    while len(username) < 4:
        if len(username) > 0:
            sys.stdout.write("\033[1A\r")
            sys.stdout.flush()
            padding(' '*50)
            print('║'+' '*10+ RED + f'{role} Username:' + username + RESET)
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()
            time.sleep(0.5)
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()
        sys.stdout.write("\033[1A\r")
        sys.stdout.flush()  
        padding(' '*50)
        print('║'+' '*10+f'{role} Username:'+' '*(role_input_limit+1)+'║')
        sys.stdout.write("\033[1A\r")
        sys.stdout.flush()  
        padding(' '*50)
        username = limit_input('║'+' '*10+f'{role} Username:', role_input_limit)

    if username == 'BACK':
        while msvcrt.kbhit():
            msvcrt.getch()
        return 'BACK', 'BACK'
    padding(' '*50)
    password = limit_input('║'+' '*10+f'{role} Password:', role_input_limit)
    if password == 'BACK':
        while msvcrt.kbhit():
            msvcrt.getch()
        return 'BACK', 'BACK'
    while len(password) < 4:
        if len(password) > 0:
            sys.stdout.write("\033[1A\r")
            sys.stdout.flush()
            padding(' '*50)
            print('║'+' '*10+ RED + f'{role} Password:' + password + RESET)
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()
            time.sleep(0.5)
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()
        sys.stdout.write("\033[1A\r")
        sys.stdout.flush()  
        padding(' '*50)
        print('║'+' '*10+f'{role} Password:'+' '*(role_input_limit+1)+'║')
        sys.stdout.write("\033[1A\r")
        sys.stdout.flush()  
        padding(' '*50)
        password = limit_input('║'+' '*10+f'{role} Password:', role_input_limit)
    
    sys.stdout.write("\033[H")
    sys.stdout.flush()
    sys.stdout.write("\033[?25l")

    return username, password

def staff_signup():
    clear_terminal()
    padding_top(21)
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()
    padding(' '*50); print('╔'+'═'*48+'╗')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('║'+' '*48+'║')
    padding(' '*50); print('╚'+'═'*48+'╝')
    padding(' '*50); print('║'+' '+'Esc: Back    Enter: Continue'+' '*19+'║')
    padding(' '*50); print('╚'+'═'*48+'╝')
    columns, _ = shutil.get_terminal_size()
    left_margin = (columns - 50) // 2
    title = "New Staff Member"
    question_1 = "First Name:"
    question_2 = "Last Name:"
    question_3 = "Staff Position:"
    inner_title_margin = (48 - len(title)) // 2
    sys.stdout.write(f"\033[15A\r\033[{left_margin + 1 + inner_title_margin}C")
    sys.stdout.flush()
    for char in title:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    sys.stdout.write(f"\033[3B\r\033[{left_margin + 1 + 10}C")
    sys.stdout.flush()
    for char in question_1:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    sys.stdout.write(f"\033[1B\r\033[{left_margin + 1 + 10}C")
    sys.stdout.flush()
    for char in question_2:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    sys.stdout.write(f"\033[1B\r\033[{left_margin + 1 + 10}C")
    sys.stdout.flush()
    for char in question_3:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)

    def question_input_limit(question_text):
        return 48 - 10 - len(question_text)

    def print_question(question_text):
        padding(' '*50)
        input_text = limit_input('║'+' '*10+question_text, question_input_limit(question_text))
        if input_text == 'BACK':
            return 'BACK'
        while len(input_text) == 0:
            sys.stdout.write("\033[1A\r")
            sys.stdout.flush()
            padding(' '*50)
            print('║'+' '*10+ RED + question_text + RESET)
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()
            time.sleep(0.5)
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()
            sys.stdout.write("\033[1A\r")
            sys.stdout.flush()  
            padding(' '*50)
            print('║'+' '*10+question_text+' '*question_input_limit(question_text)+'║')
            sys.stdout.write("\033[1A\r")
            sys.stdout.flush()  
            padding(' '*50)
            input_text = limit_input('║'+' '*10+question_text, question_input_limit(question_text))
        return input_text

    sys.stdout.write("\033[2A\r")
    sys.stdout.flush()
    staff_Name = print_question(question_1)
    if staff_Name == 'BACK':
        while msvcrt.kbhit():
            msvcrt.getch()
        return 'BACK', 'BACK', 'BACK'
    staff_Lastname = print_question(question_2)
    if staff_Lastname == 'BACK':
        while msvcrt.kbhit():
            msvcrt.getch()
        return 'BACK', 'BACK', 'BACK'
    staff_Position = print_question(question_3)
    if staff_Position == 'BACK':
        while msvcrt.kbhit():
            msvcrt.getch()
        return 'BACK', 'BACK', 'BACK'
    return staff_Name, staff_Lastname, staff_Position

def box_print(sidename, start_col, width, height, delay=0.005):
    sys.stdout.write(f"\033[1;{start_col}H╔")
    sys.stdout.flush()
    time.sleep(delay)
    for i in range(1, width - 1):
        sys.stdout.write(f"\033[1;{start_col + i}H═")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(f"\033[1;{start_col + width - 1}H╗")
    sys.stdout.flush()
    time.sleep(delay)
    for row in range(2, height - 1):
        sys.stdout.write(f"\033[{row};{start_col}H║")
        sys.stdout.flush()
        time.sleep(delay)
        sys.stdout.write(f"\033[{row};{start_col + 1}H" + " " * (width - 2))
        sys.stdout.flush()
        sys.stdout.write(f"\033[{row};{start_col + width - 1}H║")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(f"\033[{height - 1};{start_col}H╚")
    sys.stdout.flush()
    time.sleep(delay)
    for i in range(1, width - 1):
        sys.stdout.write(f"\033[{height - 1};{start_col + i}H═")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(f"\033[{height - 1};{start_col + width - 1}H╝")
    sys.stdout.flush()


def staffinterface(): 
    clear_terminal()
    def on_global_press(key):
        if key == keyboard.Key.esc:
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()
            os._exit(0)   
    escape_listener = keyboard.Listener(on_press=on_global_press)
    escape_listener.start()
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    terminal_width, terminal_height = get_maximized_size()
    box_width = (terminal_width - 6) // 2
    
    left_col = 2
    right_col = left_col + box_width + 2

    thread_left = threading.Thread(
        target=box_print, 
        args=("LeftBox", left_col, box_width, terminal_height, 0.002)
    )
    thread_right = threading.Thread(
        target=box_print, 
        args=("RightBox", right_col, box_width, terminal_height, 0.002)
    )
    
    thread_left.start()
    thread_right.start()
    thread_left.join()
    thread_right.join()
    
    sys.stdout.write(f"\033[{terminal_height};1H")
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

    sys.stdout.write(f"\033[5;0H")
    sys.stdout.flush()



def main():
    '''
    while True:
        role = staff_or_customer()
        username, password = login(role)
        if username == 'BACK' or password == 'BACK':
            continue
        if role == 'Staff':
            check_credentials = db_action('check staff credentials', [username, password])
            if check_credentials == 'New':
                staffName, staffLastname, staffPosition = staff_signup()
                if staffName == 'BACK' or staffLastname == 'BACK' or staffPosition == 'BACK':
                    continue
                info_array = [[username, password], staffName, staffLastname, staffPosition]
                db_action('new staff credentials', info_array)
        break 
    '''
    staffinterface()
    input("Press Enter to close...")
main()