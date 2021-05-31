
from time import time, sleep
from pynput import keyboard

INPUT = []

def repeat():
    global INPUT
    kb_ctrl = keyboard.Controller()

    # Faire un espace avant de répèter
    kb_ctrl.press(keyboard.Key.space)
    kb_ctrl.release(keyboard.Key.space)

    # play INPUT
    for i in range(len(INPUT)):
        while time() < INPUT[i][1] + 10:
            sleep(0.01)
        key = INPUT[i][0]
        kb_ctrl.press(key)
        kb_ctrl.release(key)

def on_press(key):
    global INPUT
    try:  # alphanumeric key
        print(key.char)
        INPUT.append([key.char, time()])
    except AttributeError:  # special key
        if key.name == "space":
            print(" ")
            INPUT.append([" ", time()])

def on_release(key):
    if key == keyboard.Key.esc:
        repeat()
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_press, on_release) as listener:
    listener.join()
