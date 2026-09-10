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
import threading
import time
import sys
import shutil

def clear_terminal():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def type_box_side(side_name, start_col, width, height, delay=0.002):
    """
    Draws a box border on a specific thread.
    Positions are calculated relative to the start_col.
    """
    # 1. Draw Top Border
    sys.stdout.write(f"\033[1;{start_col}H╔" + "═" * (width - 2) + "╗")
    sys.stdout.flush()
    time.sleep(delay)
    
    # 2. Draw Side Borders Concurrently line by line
    for row in range(2, height):
        # Left wall of this box
        sys.stdout.write(f"\033[{row};{start_col}H║")
        # Right wall of this box
        sys.stdout.write(f"\033[{row};{start_col + width - 1}H║")
        sys.stdout.flush()
        time.sleep(delay)
        
    # 3. Draw Bottom Border
    sys.stdout.write(f"\033[{height};{start_col}H╚" + "═" * (width - 2) + "╝")
    sys.stdout.flush()

def draw_split_interface():
    clear_terminal()
    
    # Hide the cursor during rendering so it doesn't flicker
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    
    # Fetch your newly maximized grid bounds
    term_width, term_height = shutil.get_terminal_size()
    
    # Calculate dimensions for side-by-side boxes with a 2-character center gap
    usable_height = term_height - 2
    box_width = (term_width - 6) // 2
    
    # Exact starting column positions
    left_start_col = 2
    right_start_col = left_start_col + box_width + 2
    
    # Create threads for the left and right layout components
    thread_left = threading.Thread(
        target=type_box_side, 
        args=("LeftBox", left_start_col, box_width, usable_height, 0.005)
    )
    thread_right = threading.Thread(
        target=type_box_side, 
        args=("RightBox", right_start_col, box_width, usable_height, 0.005)
    )
    
    # Spin both loops up at once
    thread_left.start()
    thread_right.start()
    
    # Wait for both borders to finish drawing
    thread_left.join()
    thread_right.join()
    
    # Restore cursor positioning safely below the boxes
    sys.stdout.write(f"\033[{term_height};1H")
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

# Run the split panel draw loop
draw_split_interface()
input("\nPress Enter to proceed...")


