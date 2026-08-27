import keyboard
import time
from rich.markup import escape
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel

def create_menu(options, selected_idx):
    table = Table(show_header=False, box=None)
    for i, opt in enumerate(options):
        # Apply a bold reverse style for the currently selected item
        style = "bold magenta reverse" if i == selected_idx else "dim"
        table.add_row(f"[{style}] {opt} [/{style}]")
    return Panel(table, title="Interactive Menu", border_style="cyan")

console = Console()
menu_items = ["🚀 Start Project", "⚙️  Settings", "❌ Exit"]
idx = 0
done = False

with Live(create_menu(menu_items, idx), screen=True, auto_refresh=False) as live:
    while not done:
        live.update(create_menu(menu_items, idx), refresh=True)

        # keyboard.read_event() intercepts the key without needing Enter
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'up' and idx > 0:
                idx -= 1
            elif event.name == 'down' and idx < len(menu_items) - 1:
                idx += 1
            elif event.name == 'enter':
                done = True
            elif event.name == 'q':
                done = True

        # Small delay to prevent high CPU usage in the loop
        time.sleep(0.05)

console.print(f"You selected:{menu_items[idx]}", markup=False)
