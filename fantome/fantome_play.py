
import os
from time import time, sleep
import json
from pathlib import Path
import threading
import webbrowser

from pynput import keyboard, mouse


class FantomePlay:
    """Rejoue ce qui a été enregistré par FantomeRecord"""

    def __init__(self):

        fantome = str(Path.home()) + "/fantome"
        self.fichiers = get_all_files_list(fantome, [".json"])
        print("Liste des fichiers à répéter")
        for fichier in self.fichiers:
            print("    ", fichier)

        self.kb_ctrl = keyboard.Controller()
        self.mouse_ctrl = mouse.Controller()
        self.loop = 1

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
                            print("left pressed")
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
                    if key == 'enter':
                        self.kb_ctrl.press(keyboard.Key.enter)
                        self.kb_ctrl.release(keyboard.Key.enter)
                    else:
                        self.kb_ctrl.press(key)
                        self.kb_ctrl.release(key)
        os._exit(0)

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
