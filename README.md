# fantome

Simulation d'un travaileur du net par une activité clavier/souris

### Installation

```bash
sudo pip3 install pynput
```

### Lancement du script pour enregistrer

Toutes les fenêtres doivent être fermées

Pour faire un nouvel enregistrement et effacer les précédents:

Créer un lanceur sur le bureau avec

```bash
python3 /chemin/vers/fantome/fantome_record.py
```

Si ça marche bien, tester l'ajout de nouveaux enregistrement avec
```bash
python3 /chemin/vers/fantome/fantome_record.py 0
```

Les enregistrements se font dans votre home dans un dossier fantome

Ctrl + Alt + Q pour arrêter l'enregistrement
Enregistrement de 2 mn minimum

    usage = """fantome_record.py <0 ou 1>
    0 : le nouvel enregistrement est ajouté aux précédents
    1 : efface les précédents enregistrements, valeur par défaut
    """

### Lancement du script pour jouer

Créer un lanceur sur le bureau avec

```bash
python3 /chemin/vers/fantome/fantome_play.py
```

__C'est impossible de l'arrêter !!!!!!!!!!!!!!!!!!!!__
