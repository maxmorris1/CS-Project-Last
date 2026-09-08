import msvcrt
import sys

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

text = limit_input("Enter your username (max 5 chars): ", 5)
print(f"Stored text: {text}")
