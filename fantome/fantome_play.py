
import os
import subprocess
from time import time, sleep
from datetime import datetime
import webbrowser
import json
import threading
from pathlib import Path

import psutil
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

        for fichier in self.fichiers:
            with open(fichier) as fd:
                data = fd.read()
            fd.close()
            self.data = json.loads(data)
            print("Longueur des datas =", len(self.data))
            self.repeat()

    def repeat(self):
        kb_ctrl = keyboard.Controller()
        mouse_ctrl = mouse.Controller()

        t_zero = time()
        self.offset = self.data[0][1]/1000
        self.previous = self.offset

        for action in self.data:
            # print(time() - (t_zero + (action[1]/1000)))
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

def get_navigateur_pid():
    """python3 -m webbrowser -t 'http://www.python.org'
        'mozilla' Mozilla('mozilla')
        'firefox' Mozilla('mozilla')
        'netscape' Mozilla('netscape')
        'galeon' Galeon('galeon')
        'epiphany' Galeon('epiphany')
        'skipstone' BackgroundBrowser('skipstone')
        'kfmclient' Konqueror()
        'konqueror' Konqueror()
        'kfm' Konqueror()
        'mosaic' BackgroundBrowser('mosaic')
        'opera' Opera()
        'grail' Grail()
        'links' GenericBrowser('links')
        'elinks' Elinks('elinks')
        'lynx' GenericBrowser('lynx')
        'w3m' GenericBrowser('w3m')
        'windows-default' WindowsDefault
        'macosx' MacOSX('default')
        'safari' MacOSX('safari')
        'google-chrome' Chrome('google-chrome')
        'chrome' Chrome('chrome')
        'chromium' Chromium('chromium')
        'chromium-browser' Chromium('chromium-browser')
    """

    a = webbrowser.get()
    # #print(dir(a))
    # #print(a)
    # #print(a.background, a.basename, a.name)
    procs = {p.pid: p.info for p in psutil.process_iter(['name', 'username'])}
    for key, val in procs.items():
        if a.name in val["name"]:
            print("bingo:", key)


if __name__ == '__main__':

    fantome_play = FantomePlay()
