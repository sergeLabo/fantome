
import os
import subprocess
from time import time, sleep
from datetime import datetime
import webbrowser
import json
import threading
from pathlib import Path
import shutil

import psutil
from pynput import keyboard, mouse


class FantomeRecord:
    """Enregistre tous les événements clavier et souris
    dans un fichier pendant un certain temps,
    pour pouvoir ensuite les rejoueravec FantomePlay.
    """

    def __init__(self, periode, delete_previous_recordings):
        # Pour l'enregistrement
        self.lines = []
        self.loop = 1
        self.every = periode
        self.t_record = time()
        self.thread_save()

        if delete_previous_recordings:
            # Suppression du dossier
            fantome = str(Path.home()) + "/fantome"
            # Delete all contents of a directory
            try:
               shutil.rmtree(fantome)
            except:
               print('Error while deleting directory')

        # Ne recrée pas si existe
        print("Le dossier fantome est:", fantome)
        create_directory(fantome)

        # Creation d'un sous répertoire si plusieurs enregistrement
        dt = datetime.now().strftime("%Y_%m_%d_%H_%M")
        self.record_dir = f"{fantome}/cap_{dt}"

        print("Le dossier de record est:", self.record_dir)
        create_directory(self.record_dir)

        # pour le moindre offset possible
        self.t_zero = time()

    def on_move(self, x, y):
        # Différentiel de temps en 100 centième de secondes
        t = time()
        dt = int(1000*(t - self.t_zero))

        self.lines.append(["move", dt, (x, y)])

    def on_click(self, x, y, button, pressed):
        # Différentiel de temps en 100 centième de secondes
        dt = int(1000*(time() - self.t_zero))

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
        dt = int(1000*(time() - self.t_zero))

        a = 'down' if dy < 0 else 'up'
        print(f'Scrolled {a} at {(x, y)}')
        self.lines.append(["scroll", dt, a, x, y, dx, dy])

    def on_press(self, key):
        # Différentiel de temps en 100 centième de secondes
        dt = int(1000*(time() - self.t_zero))

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

                # #self.lines = []
                # #self.t_record = time()
                # Un seul enregistrement
                self.loop = 0
            sleep(1)



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



if __name__ == '__main__':

    fantome_record = FantomeRecord(120, 1)
    fantome_record.listen()
