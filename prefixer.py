''' prefixer.py '''
import os
import fnmatch
import re
import configparser
import tkinter as tk
from operator import itemgetter

'''
Last Changes:
    - Linter-Warnungen behoben
    - Kein globaler Code
    - Nicht verwendeten Code entfernt
    - Einlesen sortierter Dateiliste
    - Regex gehärtet
    - Widgets root-Windows zugeordnet, Dateiliste Fenster-füllend
    - Sortierung/Umbenennung vereinfacht
    - Dateiliste wird nach Umbenennung aktualisiert

To do:
    Filter setzen
    Pfad einstellen
        Configfile für Beides
            check

Großer Fehler:

Bugs:
'''


class App(tk.Frame):
    ''' Die Hauptklasse '''

    def __init__(self, config, master=None):
        super().__init__(master)
        self.config = config
        self.pack()
        # [Ordner, Dateierweiterung]
        self.setting = [
            self.config['DEFAULT']['folder'],
            "*" + self.config['DEFAULT']['filter']]
        self.regex = (
            r"^(\d+_){0,1}(.+" +
            re.escape(self.config['DEFAULT']['filter']) +
            r")$")

        self.create_widgets()
        self.refresh_list_unsorted()

    def create_widgets(self):
        ''' Erstellt die Widgets '''

        self.l_folder = tk.Label(self.master)
        self.l_folder["text"] = "Dateiordner:", self.config['DEFAULT']['folder']
        self.l_folder.pack(side="top")

        self.l_filter = tk.Label(self.master)
        self.l_filter["text"] = "Filter:", self.config['DEFAULT']['filter']
        self.l_filter.pack(side="top")

        self.list_unsorted = tk.Listbox(self.master)
        self.list_unsorted.pack(fill=tk.BOTH, expand=1)

        self.b_refresh = tk.Button(self.master)
        self.b_refresh["text"] = "Liste aktualisieren"
        self.b_refresh["command"] = self.refresh_list_unsorted
        self.b_refresh.pack(side="top")

        self.b_start = tk.Button(self.master, fg="red")
        self.b_start["text"] = "Sortieren"
        self.b_start["command"] = self.sort_start
        self.b_start.pack(side="top")

        self.b_quit = tk.Button(self.master, text="Quit", command=root.destroy)
        self.b_quit.pack(side="bottom")

    def get_items(self):
        ''' Holt die Items in einem Angegebenen Ordner (Folder) '''
        filtered = []

        for item in sorted(os.listdir(self.setting[0])):
            if fnmatch.fnmatch(item, self.setting[1]):
                match = re.search(self.regex, item)
                if match:
                    # (orig, base, number or None)
                    filtered.append((item, match.group(2), match.group(1)))

        return filtered

    def refresh_list_unsorted(self):
        ''' aktualisiert den Inhalt des Ordners '''
        self.items = self.get_items()

        self.list_unsorted.delete(0, tk.END)
        self.list_unsorted.insert(tk.END, *[i[0] for i in self.items])

    def sort_start(self):
        sorted_list = (
            # sort numbered items by existimg number
            sorted((i for i in self.items if i[2]),
                   key=itemgetter(2)) +
            # sort unnumbered items by name
            sorted((i for i in self.items if not i[2]),
                   key=itemgetter(1))
        )

        for number, (orig, base, _) in enumerate(sorted_list, 1):
            renamed = "{0:03d}_{1}".format(number, base)
            if orig == renamed:
                print(orig, "skipped")
            else:
                print(orig, "->", renamed)
                os.rename(
                    os.path.join(self.setting[0], orig),
                    os.path.join(self.setting[0], renamed))
        self.refresh_list_unsorted()


if __name__ == "__main__":
    # get configuration
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # set fallback configuration
    config.setdefault('DEFAULT', {
        'Folder': './Test/',
        'Filter': '.txt'})

    root = tk.Tk()
    app = App(master=root, config=config)
    app.mainloop()

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)
