
import os
import sys
import subprocess
from time import time, sleep
from datetime import datetime
import json
import webbrowser
from pathlib import Path
import shutil

import pynput


SPECIAL_KEYS = {
                "space": " ",
                "alt_l": "alt_l",
                "backspace": "backspace",
                "ctrl_l": "ctrl_l",
                "delete": "delete",
                "enter": "enter",
                "esc": "esc",
                "f1": "f1",
                "up": "up",
                "down": "down",
                "left": "left",
                "right": "right"
                }

class FantomeRecord:
    """Enregistre tous les événements clavier et souris
    dans un fichier pendant un certain temps,
    pour pouvoir ensuite les rejoueravec FantomePlay.
    """

    def __init__(self, periode, delete_previous_recordings):
        # Pour l'enregistrement
        self.lines = []
        self.start = 0

        # Suppression du dossier
        fantome = str(Path.home()) + "/fantome"

        if delete_previous_recordings:
            # Delete all contents of a directory
            try:
               shutil.rmtree(fantome)
               print("Effacement des précédents enregistrements")
            except:
               print('Error while deleting directory')

        # Ne recrée pas si existe
        print("Le dossier fantome est:", fantome)
        create_directory(fantome)

        # Creation d'un sous répertoire
        # pour pouvoir faire plusieurs enregistrements avec
        # delete_previous_recordings = 0
        dt = datetime.now().strftime("%Y_%m_%d_%H_%M")
        self.record_dir = f"{fantome}/cap_{dt}"

        print("Le dossier de record est:", self.record_dir)
        create_directory(self.record_dir)

        url = "labomedia.org"
        webbrowser.open(url, new=1, autoraise=True)

    def on_move(self, x, y):
        if self.start:
            # Différentiel de temps en millièmes de secondes
            t = time()
            dt = int(1000*(t - self.t_zero))
            self.lines.append(["move", dt, (x, y)])

    def on_click(self, x, y, button, pressed):
        if self.start:
            # Différentiel de temps en millièmes de secondes
            dt = int(1000*(time() - self.t_zero))

            a = 'Pressed' if pressed else 'Released'
            print(f'{a} at {(x, y)} with {button}')

            if button == pynput.mouse.Button.left:
                button = "left"
            elif button == pynput.mouse.Button.right:
                button = "right"
            elif button == pynput.mouse.Button.middle:
                button = "middle"

            self.lines.append(["click", dt, button, a, (x, y)])

    def on_scroll(self, x, y, dx, dy):
        if self.start:
            # Différentiel de temps en millièmes de secondes
            dt = int(1000*(time() - self.t_zero))

            a = 'down' if dy < 0 else 'up'
            print(f'Scrolled {a} at {(x, y)}')
            self.lines.append(["scroll", dt, a, x, y, dx, dy])

    def on_press(self, key):
        global SPECIAL_KEYS
        # Différentiel de temps en millièmes de secondes
        dt = int(1000*(time() - self.t_zero))

        try:  # alphanumeric key
            print("Action press de", key.char)
            self.lines.append(["press", dt, key.char])
        except AttributeError as e:
            print("Special Key =", key.name)
            if key.name in SPECIAL_KEYS:
                self.lines.append(["press", dt, SPECIAL_KEYS['enter']])

    def on_release(self, key):
        # pas appelé !
        if key == pynput.keyboard.Key.esc:
            print("bizarre")

    def on_activate_q(self):
        print('\nGlobal hotkey <ctrl>+<alt>+q activated!\n')

        if self.start == 0:
            self.start = 1
            print("Enregistrement commencé ...")
            print("Ctrl + Alt + Q pour stopper ...")
        elif self.start == 1:
            self.final_save()
            self.keyboard_listener.stop()
            self.mouse_listener.stop()
            self.hot_listener.stop()
            print("Fichier enregistré", self.fichier)
            os._exit(0)

    def on_activate_d(self):
        print('\nGlobal hotkey <ctrl>+<alt>+d activated!\n')
        print("non utilisé ! ...")

    def final_save(self):
        dt = datetime.now().strftime("%Y_%m_%d_%H_%M")
        self.fichier = self.record_dir + f"/cap_{dt}.json"
        with open(self.fichier, "w") as fd:
            fd.write(json.dumps(self.lines))
            print(f"{self.fichier} enregistré.")
        fd.close()

    def for_canonical(self, f):
        return lambda k: f(self.keyboard_listener.canonical(k))

    def listen(self):
        """Collect events until released"""
        print("Listener Start ...")
        print("\n\n   Ctrl + Alt + Q pour commencer l'enregistrement ...")
        # zéro au début de l'enregistrement
        self.t_zero = time()

        self.mouse_listener = pynput.mouse.Listener(self.on_move, self.on_click,
                                                    self.on_scroll)
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press,
                                                    on_release=self.on_release)
        self.hot_listener = pynput.keyboard.GlobalHotKeys({
                                        '<ctrl>+<alt>+q': self.on_activate_q,
                                        '<ctrl>+<alt>+d': self.on_activate_d
                                        })
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.hot_listener.start()
        self.keyboard_listener.join()
        self.mouse_listener.join()
        self.hot_listener.join()


def create_directory(directory):
    """Crée le répertoire avec le chemin absolu, ou relatif"""
    try:
        # mode=0o777 est par défaut
        Path(directory).mkdir(mode=0o777, parents=False)
        print("Création du répertoire: {}".format(directory))
    except FileExistsError as e:
        print(e)
        print("Le répertoire {} existe.".format(directory))
    except PermissionError as e:
        print(e)
        print("Problème de droits avec le répertoire {}".format(directory))
    except:
        print("Erreur avec {}".format(directory))
        os._exit(0)

def main(argv):

    print("Ctrl + Alt + Q pour arrêter l'enregistrement")
    print("Enregistrement de 2 mn minimum")

    usage = """fantome_record.py <0 ou 1>
    0 : le nouvel enregistrement est ajouté aux précédents
    1 : efface les précédents enregistrements, valeur par défaut
    """

    if len(argv) == 2:
        d = argv[1]
        try:
            delete = int(d)
            if delete not in [0, 1]:
                print(usage)
                os._exit(0)
        except:
            print(usage)

    elif len(argv) == 1:
        delete = 1

    periode = 120
    fantome_record = FantomeRecord(periode, delete)
    fantome_record.listen()


if __name__ == "__main__":
   main(sys.argv)



        # #hotkey = pynput.keyboard.HotKey(pynput.keyboard.HotKey.parse('<ctrl>+<alt>+q'),
                                                              # #self.on_activate_q)

        # #with mouse.Listener(self.on_move, self.on_click, self.on_scroll)\
                            # #as self.listener:
            # #with keyboard.Listener(on_press=self.for_canonical(hotkey.press),
                                   # #on_release=self.for_canonical(hotkey.release))\
                                   # #as self.listener:
                # #self.listener.join()

        # ## Listen to mouse events
        # #with pynput.mouse.Listener(self.on_move, self.on_click, self.on_scroll) as mouse_listener:
            # #mouse_listener.join()

        # ## Listen to keyboard events
        # #with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
            # #keyboard_listener.join()

        # #with pynput.keyboard.GlobalHotKeys({'<ctrl>+<alt>+q': self.on_activate_q,
                                    # #'<ctrl>+<alt>+d': self.on_activate_d}) as hot:
            # #hot.join()
