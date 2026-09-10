'''
from interface import padding
def repeatLine(line: str, repeat: int) -> None:
    for _ in range(repeat):
        exec(line)

padding(' '*50); print('╔'+'═'*48+'╗')
repeatLine("padding(' '*50); print('║'+' '*48+'║')", 16)
padding(' '*50); print('╚'+'═'*48+'╝')
padding(' '*50); print('║'+' '+'Esc: Back    Enter: Continue'+' '*19+'║')
padding(' '*50); print('╚'+'═'*48+'╝')
'''
'''
import threading
import time
import sys

# Sample data: (Row number on screen, Text to type)
LINES_TO_TYPE = [
    (1, "Loading system core components..."),
    (2, "Establishing secure connection to proxy..."),
    (3, "Fetching encrypted data packets..."),
    (4, "Decrypting payload headers...")
]

def type_line(row, text, delay=0.1):
    for i, char in enumerate(text):
        # \033[{row};{col}H moves the cursor to that specific row and column
        sys.stdout.write(f"\033[{row};{i+1}H{char}")
        sys.stdout.flush()
        time.sleep(delay)

# Clear the screen first to give us a clean slate
sys.stdout.write("\033[2J")
sys.stdout.flush()

threads = []
for row, text in LINES_TO_TYPE:
    t = threading.Thread(target=type_line, args=(row, text, 0.08))
    threads.append(t)
    t.start()

# Wait for all threads to finish typing
for t in threads:
    t.join()

# Move cursor below the text when done so the prompt looks normal
sys.stdout.write(f"\033[{len(LINES_TO_TYPE) + 2};1H\n")
sys.stdout.flush()
'''
'''
import ctypes
import time

# 1. Wait a moment to switch to your test application
print("Testing starts in 3 seconds... Switch to the app you want to maximize.")
time.sleep(3)

# 2. Get the handle of the currently active (foreground) window
hwnd = ctypes.windll.user32.GetForegroundWindow()

# 3. Maximize the window (3 is the command ID for SW_MAXIMIZE)
# Reference: https://microsoft.com
ctypes.windll.user32.ShowWindow(hwnd, 3)

print("Window maximized! Holding for 5 seconds of testing...")
time.sleep(5)
print("Testing complete.")
'''


