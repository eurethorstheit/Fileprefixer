''' prefixer.py '''

import configparser

from filerenamer import FileRenamer
from app import App

'''
Last Changes:
    - Klassen in separate Module ausgelagert

To do:
    Filter setzen
    Pfad einstellen
        Configfile für Beides
            check

Großer Fehler:

Bugs:
'''

if __name__ == "__main__":
    # get configuration
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # set fallback configuration
    config.setdefault('DEFAULT', {
        'folder': './Test/',
        'filter': '.txt'})

    filerenamer = FileRenamer(
        config['DEFAULT']['folder'],
        config['DEFAULT']['filter'])

    app = App(renamer=filerenamer)
    app.mainloop()

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)
