import keyboard
import time
from rich.console import Console, Group  # FIX: Added Group to imports
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.ansi import AnsiDecoder
import pytermgui as ptg

# Helper to make PyTermGUI widgets compatible with Rich
def make_rich_compatible(widget):
    # FIX: Use get_lines() instead of render() to avoid AttributeError
    lines = widget.get_lines() 
    ansi_string = "\n".join(lines)
    decoder = AnsiDecoder()
    return list(decoder.decode(ansi_string))

# 1. FIX: Initialize Console without trailing syntax errors
console = Console() 

# 2. Define Layout
layout = Layout()
layout.split_column(Layout(name="upper", size=3), Layout(name="lower"))
layout["lower"].split_row(Layout(name="left", ratio=1), Layout(name="right", ratio=1))

menu_items = ["🚀 Start Project", "⚙️  Settings", "❌ Exit"]
idx = 0
done = False

# Create the PyTermGUI button
test_button = ptg.Button("Test Mouse Functionality")

with Live(layout, auto_refresh=False, screen=True) as live:
    while not done:
        # 3. FIX: Properly wrap compatible elements in a Group
        rich_button_elements = make_rich_compatible(test_button)
        layout["upper"].update(
            Panel(Group(*rich_button_elements), title="Mouse Test Zone")
        )

        # Menu rendering logic
        table = Table(show_header=False, box=None)
        for i, opt in enumerate(menu_items):
            style = "bold magenta reverse" if i == idx else "dim"
            table.add_row(f"[{style}] {opt} [/{style}]")

        layout["left"].update(Panel(table, title="Interactive Menu", border_style="cyan"))
        layout["right"].update(Panel(f"Index: {idx}", title="Status"))

        live.refresh()

        # Keyboard event handling via the keyboard library
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'up' and idx > 0: 
                idx -= 1
            elif event.name == 'down' and idx < len(menu_items) - 1: 
                idx += 1
            elif event.name == 'enter': 
                done = True

        time.sleep(0.05)
