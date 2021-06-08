# fantome

Simulation d'un travaileur du net par une activité clavier/souris

### Wiki

* [Clavier Souris Fantôme](https://ressources.labomedia.org/clavier_souris_fantome)


### Installation

```bash
sudo pip3 install pynput psutil
```
Tous les requirements sont dans requirements.txt pour installation dans un [venv](https://ressources.labomedia.org/virtualenv)

### Utilisation

#### Enregistrement

* Aller dans le dossier fantome. Rendre exécutable les fichier record.sh et play.sh
* Double cliquer sur record.sh
* Lancer
* Maximiser votre navigateur
* Lancer avec __Ctrl + Alt + Q__
* Pour arrêter __Ctrl + Alt + Q__
* Toutes les fenêtres du navigateur seront fermèes par le script.

#### Jouer

* Double cliquer sur play.sh
* Lancer
* Maximiser votre navigateur
* Pour lancer le jeu __Ctrl + Alt + Q__
* Pour arrêter __Ctrl + Alt + Q__

### Bug en cours d'étude

__Le clavier AZERTY dans firefox est joué en QWERTY__


### Installation dans un venv

#### Documentation

* [venv](https://ressources.labomedia.org/virtualenv) sur ressources.labomedia.org

#### Pourquoi ?

L'installation des dépendances se fait dans le dossier fantome, cala ne touche pas à votre système, pas de sudo.

#### En terminal

```bash
python3.7 -m pip install --upgrade pip
sudo apt install python3-venv
```
Télécharger les sources de fantome
```bash
cd /le/dossier/de/votre/projet/fantome
python3 -m venv mon_env
source mon_env/bin/activate
python3 -m pip install -r requirements.txt
```
Pour excécuter fantome_record.py ou fantome_play.py
```bash
cd /le/dossier/de/votre/projet/fantome
./mon_env/bin/python3 ./fantome/fantome_record.py
# ou
./mon_env/bin/python3 ./fantome/fantome_play.py
```

### Merci à

  * [La Labomedia](https://labomedia.org)
