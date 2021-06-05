
import os
from time import time, sleep
import json
from pathlib import Path
import threading

from pynput import keyboard, mouse


class FantomePlay:
    """Rejoue ce qui a été enregistré par FantomeRecord"""

    def __init__(self):

        self.offset = 0
        self.previous = 0

        fantome = str(Path.home()) + "/fantome"
        self.fichiers = get_all_files_list(fantome, [".json"])
        print("Liste des fichiers à répéter")
        for fichier in self.fichiers:
            print("    ", fichier)

        self.all_data = []
        for fichier in self.fichiers:
            with open(fichier) as fd:
                data = fd.read()
            fd.close()
            data = json.loads(data)
            self.all_data.append(data)
            print("Longueur des datas =", len(data))

        self.loop = 1
        self.thread_repeat()

        with keyboard.GlobalHotKeys({'<ctrl>+<alt>+q': self.on_activate_q})\
                                    as hot:
            hot.join()
        print("je ne passe jamais par là")

    def on_activate_q(self):
        print('<ctrl>+<alt>+q pressed')
        print('je quitte ...')
        self.loop = 0
        print("C'est fini.")
        os._exit(0)

    def thread_repeat(self):
        t_play = threading.Thread(target=self.repeat)
        t_play.start()

    def repeat(self):
        kb_ctrl = keyboard.Controller()
        mouse_ctrl = mouse.Controller()

        for data in self.all_data:
            if self.loop:
                t_zero = time()
                self.offset = data[0][1]/1000
                self.previous = self.offset
                # #print(t_zero, self.offset)
                for action in data:
                    print(action)
                    # #print(time() - (t_zero + (action[1]/1000)))
                    # Attente
                    t_scale = action[1] * 1.4
                    while (time() - (t_zero + (t_scale/1000))) < 0:
                        sleep(0.01)

                    # action[0] "move" "click" "press" "scroll"
                    if action[0] == "move":
                        mouse_ctrl.position = action[2][0], action[2][1]

                    elif action[0] == "click":
                        mouse_ctrl.position = action[4]

                        if action[3] == 'Pressed':
                            if action[2] == "left":
                                mouse_ctrl.press(mouse.Button.left)
                                print("left pressed")
                            elif action[2] == "right":
                                mouse_ctrl.press(mouse.Button.right)
                            elif action[2] == "middle":
                                mouse_ctrl.press(mouse.Button.middle)

                        if action[3] == 'Released':
                            if action[2] == "left":
                                mouse_ctrl.release(mouse.Button.left)
                            elif action[2] == "right":
                                mouse_ctrl.release(mouse.Button.right)
                            elif action[2] == "middle":
                                mouse_ctrl.release(mouse.Button.middle)

                    elif action[0] == "scroll":
                        # a = 'down' if dy < 0 else 'up'
                        # ["scroll", dt, a, x, y, dx, dy]
                        mouse_ctrl.position = action[3], action[4]
                        mouse_ctrl.scroll(action[5], action[6])

                    elif action[0] == "press":
                        key = action[2]
                        if key == keyboard.Key.esc:
                            self.loop = 0
                        kb_ctrl.press(key)
                        kb_ctrl.release(key)
            else:
                print("break")
                break

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
