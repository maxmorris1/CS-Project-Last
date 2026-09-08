import time
import sys
import os
import msvcrt
import shutil

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_terminal()

def limit_input(prompt, max_chars):
    print(prompt, end="", flush=True)
    user_input = ""
    
    while True:
        char = msvcrt.getch()
        
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

def padding(text):
    columns, _ = shutil.get_terminal_size()
    
    padding = (columns - len(text)) // 2
    if padding > 0:
        sys.stdout.write(" " * padding)
        sys.stdout.flush()

def type_out(text, delay=0.015):
    padding(text)
    for char in text:
      sys.stdout.write(char)
      sys.stdout.flush()
      time.sleep(delay)
    print()  

type_out(' '+'_'*48+' ')
type_out('|'+' '*48+'|')
type_out('|'+' '*18+'Staff Login'+' '*19+'|')
type_out('|'+' '*48+'|')
type_out('|'+' '*10+'Staff Username:'+' '*23+'|')
type_out('|'+' '*10+'Staff Password:'+' '*23+'|')
type_out('|'+' '*48+'|')
type_out('|'+'_'*48+'|')
sys.stdout.write("\033[4A\r")
sys.stdout.flush()

padding(' '*50)
staff_username = limit_input('|'+' '*10+'Staff Username:', 22)
while len(staff_username) < 4:
    sys.stdout.write("\033[1A\r")
    sys.stdout.flush()  
    padding(' '*50)
    print('|'+' '*10+'Staff Username:'+' '*23+'|')
    sys.stdout.write("\033[1A\r")
    sys.stdout.flush()  
    padding(' '*50)
    staff_username = limit_input('|'+' '*10+'Staff Username:', 22)


padding(' '*50)
staff_password = limit_input('|'+' '*10+'Staff Password:', 22)
while len(staff_password) < 4:
    sys.stdout.write("\033[1A\r")
    sys.stdout.flush()  
    padding(' '*50)
    print('|'+' '*10+'Staff Password:'+' '*23+'|')
    sys.stdout.write("\033[1A\r")
    sys.stdout.flush()  
    padding(' '*50)
    staff_password = limit_input('|'+' '*10+'Staff Password:', 22)

sys.stdout.write("\033[2B") 
sys.stdout.flush()