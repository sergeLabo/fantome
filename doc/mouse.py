from pynput import mouse

def play():
    souris = mouse.Controller()

    # Read pointer position
    print('The current pointer position is {0}'.format(
        souris.position))

    # Set pointer position
    souris.position = (10, 20)
    print('Now we have moved it to {0}'.format(
        souris.position))

    # Move pointer relative to current position
    souris.move(5, -5)

    # Press and release
    souris.press(mouse.Button.left)
    souris.release(mouse.Button.left)

    # Double click; this is different from pressing and releasing
    # twice on macOS
    souris.click(mouse.Button.left, 2)

    # Scroll two steps down
    souris.scroll(0, 2)


def on_move(x, y):
    print('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    a = 'Pressed' if pressed else 'Released'
    print(f'{a} at {(x, y)}')
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    a = 'down' if dy < 0 else 'up'
    print(f'Scrolled {a} at {(x, y)}')

# Collect events until released
with mouse.Listener(on_move=on_move,
                    on_click=on_click,
                    on_scroll=on_scroll) as listener:
    listener.join()

# ## ...or, in a non-blocking fashion:
# #listener = mouse.Listener(
    # #on_move=on_move,
    # #on_click=on_click,
    # #on_scroll=on_scroll)
# #listener.start()
