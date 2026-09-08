from pynput import keyboard

def on_press(key):
    if key == keyboard.Key.up:
        return("Up arrow pressed!")
    elif key == keyboard.Key.down:
        return("Down arrow pressed!")
    elif key == keyboard.Key.left:
        return("Left arrow pressed!")
    elif key == keyboard.Key.right:
        return("Right arrow pressed!")
    elif key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
    print
