
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

class FantomeRecord:
    """Enregistre tous les événements clavier et souris
    dans un fichier pendant un certain temps,
    pour pouvoir ensuite les rejoueravec FantomePlay.
    """

    def __init__(self):
        # Temps au lancement du script = temps origine
        # pour rejouer ensuite à cette origine
        self.t_zero = time()

        # Pour l'enregistrement
        self.lines = []
        self.loop = 1
        self.every = 20
        self.t_record = time()
        self.thread_save()
        dt = datetime.now().strftime("%Y_%m_%d_%H_%M")
        create_directory("./recordings")
        self.record_dir = f"./recordings/cap_{dt}"
        create_directory(self.record_dir)

    def on_move(self, x, y):
        # Différentiel de temps en 100 centième de secondes
        dt = int(10000*(time() - self.t_zero))

        # #print('Pointer moved to {0}'.format((x, y)))
        self.lines.append(["move", dt, (x, y)])

    def on_click(self, x, y, button, pressed):
        # Différentiel de temps en 100 centième de secondes
        dt = int(10000*(time() - self.t_zero))

        a = 'Pressed' if pressed else 'Released'
        print(f'{a} at {(x, y)} with {button}')

        if button == mouse.Button.left:
            button = "left"
        elif button == mouse.Button.right:
            button = "right"
        elif button == mouse.Button.middle:
            button = "middle"

        self.lines.append(["click", dt, button, a, (x, y)])

    def on_scroll(self, x, y, dx, dy):
        # Différentiel de temps en 100 centième de secondes
        dt = int(10000*(time() - self.t_zero))

        a = 'down' if dy < 0 else 'up'
        print(f'Scrolled {a} at {(x, y)}')
        self.lines.append(["scroll", dt, a, x, y, dx, dy])

    def on_press(self, key):
        # Différentiel de temps en 100 centième de secondes
        dt = int(10000*(time() - self.t_zero))

        try:  # alphanumeric key
            print(key.char)
            self.lines.append(["press", dt, key.char])
        except AttributeError:  # special key
            if key.name == "space":
                print(" ")
                self.lines.append(["press", dt, ' '])

    def on_release(self, key):
        if key == keyboard.Key.esc:
            self.loop = 0
            self.listener.stop()

    def listen(self):
        """Collect events until released"""
        print("Listener Start ...")

        with mouse.Listener(self.on_move, self.on_click, self.on_scroll)\
                            as self.listener:
            with keyboard.Listener(self.on_press, self.on_release)\
                            as self.listener:
                self.listener.join()

        print("Listener Stop ...")

    def thread_save(self):

        t_save = threading.Thread(target=self.save)
        t_save.start()

    def save(self):
        while self.loop:
            if time() - self.t_record > self.every:
                dt = datetime.now().strftime("%Y_%m_%d_%H_%M")
                self.fichier = self.record_dir + f"/cap_{dt}.json"
                with open(self.fichier, "w") as fd:
                    fd.write(json.dumps(self.lines))
                    print(f"{self.fichier} enregistré.")
                fd.close()

                self.lines = []
                self.t_record = time()
            sleep(1)


class FantomePlay:
    """Rejoue ce qui a été enregistré par FantomeRecord"""

    def __init__(self, dossier):

        self.t_zero = time()

        self.fichiers = get_all_files_list(dossier, [".json"])
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

        loop = 1
        while loop and self.data:
            for action in self.data:
                while  time() - (self.t_zero + (action[1]/10000)) < 0:

                    # action[0] "move" "click" "press" "scroll"
                    if action[0] == "move":
                        mouse_ctrl.position = action[2][0], action[2][1]

                    elif action[0] == "click":
                        if action[2] == "left":
                            mouse_ctrl.press(mouse.Button.left)
                            mouse_ctrl.release(mouse.Button.left)
                        elif action[2] == "right":
                            mouse_ctrl.press(mouse.Button.right)
                            mouse_ctrl.release(mouse.Button.right)
                        elif action[2] == "middle":
                            mouse_ctrl.press(mouse.Button.middle)
                            mouse_ctrl.release(mouse.Button.middle)

                    elif action[2] == "scroll":
                        # Scroll two steps down
                        # ["scroll", 389848, "down", 1114, 1118, 0, -1]
                        # ["scroll", dt, a, x, y, dx, dy]
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

    fantome_record = FantomeRecord()
    fantome_record.listen()

    # #dossier = "/media/data/3D/projets/fantome/fantome/recordings"
    # #fantome_play = FantomePlay(dossier)
    # #fantome_play.repeat()

    # #get_navigateur_pid()