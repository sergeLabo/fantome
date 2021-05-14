from pynput import keyboard

INPUT = ""

def on_press(key):
    try:
        print(key.char)
        INPUT += key.char
        # #print(f'alphanumeric key {key.char} pressed')
    except AttributeError:
        # #print(f'special key {key} pressed')
        # #print(key.name, key.value)
        if key.name == "space":
            print(" ")
            INPUT += " "

def on_release(key):
    # #print('f{key} released')
    if key == keyboard.Key.esc:
        play_input()
        # Stop listener
        return False

def play_input():
    pass

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
# #listener = keyboard.Listener(
    # #on_press=on_press,
    # #on_release=on_release)
# #listener.start()

#   fdfggh fdhrt rtygrty
