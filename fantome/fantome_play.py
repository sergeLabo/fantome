
import os
from time import time, sleep
import json
from pathlib import Path
import threading
import webbrowser

from pynput import keyboard, mouse

from get_navigateur_pid import get_navigateur_pid


SPECIAL_KEYS = {
                "space": keyboard.Key.space,
                "backspace": keyboard.Key.backspace,
                "delete": keyboard.Key.delete,
                "enter": keyboard.Key.enter,
                "esc": keyboard.Key.esc,
                "f1": "f1",
                "up": keyboard.Key.up,
                "down": keyboard.Key.down,
                "left": keyboard.Key.left,
                "right": keyboard.Key.right
                }


class FantomePlay:
    """Rejoue ce qui a été enregistré par FantomeRecord"""

    def __init__(self):

        fantome = str(Path.home()) + "/fantome"
        self.fichiers = get_all_files_list(fantome, [".json"])
        print("Liste des fichiers à répéter")
        for fichier in self.fichiers:
            print("    ", fichier)

        self.kb_ctrl = keyboard.Controller()
        # #print(dir(self.kb_ctrl))
        self.mouse_ctrl = mouse.Controller()
        self.loop = 1
        self.backspace = 0

        self.all_data = []
        for fichier in self.fichiers:
            with open(fichier) as fd:
                data = fd.read()
            fd.close()
            data = json.loads(data)
            self.all_data.append(data)
            print("Longueur des datas =", len(data))

        url = "labomedia.org"
        webbrowser.open(url, new=1, autoraise=True)

        self.start = 0
        print("\n\n   Ctrl + Alt + Q pour commencer à répéter ...")

        with keyboard.GlobalHotKeys({'<ctrl>+<alt>+q': self.on_activate_q})\
                                    as hot:
            hot.join()
        print("je ne passe jamais par là")

    def on_activate_q(self):
        print('<ctrl>+<alt>+q pressed')

        if self.start == 0:
            self.start = 1
            self.thread_repeat()
            # zéro au début de l'enregistrement
            print("Répétition commencée ...")
            print("Ctrl + Alt + Q pour stopper ...")
        else:
            print('je quitte ...')
            self.loop = 0
            print("C'est fini.")
            os._exit(0)

    def thread_repeat(self):
        t_play = threading.Thread(target=self.repeat)
        t_play.start()

    def repeat(self):
        for data in self.all_data:
            t_zero = time()
            offset = data[1][1]/1000
            print("offset =", offset, "t_zero =", t_zero)

            # le 1er de data est le q du départ avec un t-zero faux
            for action in data[1:]:
                # #print(action)
                # Attente: action à (t_zero + action[1]/1000)
                while time() - t_zero  + offset - action[1]/1000 < 0:
                    # #print(time() - t_zero  - offset - action[1]/1000)
                    sleep(0.001)

                # action[0] "move" "click" "press" "scroll"
                if action[0] == "move":
                    self.mouse_ctrl.position = action[2][0], action[2][1]

                elif action[0] == "click":
                    self.mouse_ctrl.position = action[4]

                    if action[3] == 'Pressed':
                        if action[2] == "left":
                            self.mouse_ctrl.press(mouse.Button.left)
                        elif action[2] == "right":
                            self.mouse_ctrl.press(mouse.Button.right)
                        elif action[2] == "middle":
                            self.mouse_ctrl.press(mouse.Button.middle)

                    if action[3] == 'Released':
                        if action[2] == "left":
                            self.mouse_ctrl.release(mouse.Button.left)
                        elif action[2] == "right":
                            self.mouse_ctrl.release(mouse.Button.right)
                        elif action[2] == "middle":
                            self.mouse_ctrl.release(mouse.Button.middle)

                elif action[0] == "scroll":
                    # a = 'down' if dy < 0 else 'up'
                    # ["scroll", dt, a, x, y, dx, dy]
                    self.mouse_ctrl.position = action[3], action[4]
                    self.mouse_ctrl.scroll(action[5], action[6])

                elif action[0] == "press":
                    key = action[2]
                    # #print("\n", key)
                    # #print(self.kb_ctrl.keyboard_mapping)
                    if key == "backspace":
                        self.backspace = 1

                    if key in SPECIAL_KEYS:
                        self.kb_ctrl.tap(SPECIAL_KEYS[key])
                        # #print("\n", key)
                        # #print(self.kb_ctrl.keyboard_mapping)
                    else:
                        if self.backspace:
                            if key in AZERTY:
                                azerty_key = QWERTY[AZERTY.index(key)]
                                # #print(key, azerty_key)
                        else:
                            azerty_key = key
                        self.kb_ctrl.tap(azerty_key)

        # fermer le navigateur à la main sinon session restore
        #os._exit(0)


QWERTY = "qwertyuiopasdfghjkl,zxcvbnm."
AZERTY = "azertyuiopqsdfghjklmwxcvbn,:"

def get_all_files_list(directory, extentions):
    """Lit le dossier et tous les sous-dosssiers.
    Retourne la liste de tous les fichiers avec les extentions de
    la liste extentions.
    """

    file_list = []
    for path, subdirs, files in os.walk(directory):
        for name in files:
            for extention in extentions:
                if name.endswith(extention):
                    file_list.append(str(Path(path, name)))

    return file_list


if __name__ == '__main__':

    fantome_play = FantomePlay()

"""
['ALT_GR_MASK', 'ALT_MASK', 'CTRL_MASK', 'InvalidCharacterException', 'InvalidKeyException',
'SHIFT_MASK', '_Key', '_KeyCode', '__class__', '__del__', '__delattr__', '__dict__',
'__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__',
'__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__',
'__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__',
'__str__', '__subclasshook__', '__weakref__', '_add_listener', '_as_modifier',
'_borrow_lock', '_borrows', '_caps_lock', '_dead_key', '_display', '_emit', '_handle',
'_key_to_keysym', '_keyboard_mapping', '_keysym', '_listener_cache', '_listener_lock',
'_listeners', '_log', '_modifiers', '_modifiers_lock', '_receiver', '_remove_listener',
'_resolve', '_resolve_borrowed', '_resolve_borrowing', '_resolve_dead', '_resolve_normal',
'_resolve_special', '_send_key', '_shift_mask', '_update_keyboard_mapping', '_update_modifiers',

'alt_gr_pressed', 'alt_pressed', 'ctrl_pressed', 'keyboard_mapping', 'modifiers',
'press', 'pressed', 'release', 'shift_pressed', 'tap', 'touch', 'type']
"""
