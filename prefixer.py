''' prefixer.py '''
import os
import fnmatch
import re
import configparser
import tkinter as tk
from operator import itemgetter

'''
Last Changes:
    - Rename-Logik in separate Klasse ausgelagert

To do:
    Filter setzen
    Pfad einstellen
        Configfile für Beides
            check

Großer Fehler:

Bugs:
'''


class FileRenamer:
    def __init__(self, directory, suffix):
        self.directory = directory
        self.suffix = suffix
        self.filter = "*" + self.suffix
        self.regex = (r"^(\d+_){0,1}(.+" + re.escape(suffix) + r")$")
        self.items = []

    def get_directory(self):
        return self.directory

    def get_suffix(self):
        return self.suffix

    def refresh(self):
        self.items = []

        for item in sorted(os.listdir(self.directory)):
            if fnmatch.fnmatch(item, self.filter):
                match = re.search(self.regex, item)
                if match:
                    # (orig, base, number or None)
                    self.items.append((item, match.group(2), match.group(1)))

        return [i[0] for i in self.items]

    def rename(self):
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
                print("renaming", orig, "skipped")
            else:
                print("renaming", orig, "->", renamed)
                os.rename(
                    os.path.join(self.directory, orig),
                    os.path.join(self.directory, renamed))


class App(tk.Frame):
    ''' Die Hauptklasse '''

    def __init__(self, renamer, master=None):
        self.renamer = renamer

        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.refresh_list_unsorted()

    def create_widgets(self):
        ''' Erstellt die Widgets '''

        self.l_folder = tk.Label(self.master)
        self.l_folder["text"] = "Dateiordner:", self.renamer.get_directory()
        self.l_folder.pack(side="top")

        self.l_filter = tk.Label(self.master)
        self.l_filter["text"] = "Filter:", self.renamer.get_suffix()
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

    def refresh_list_unsorted(self):
        ''' aktualisiert den Inhalt des Ordners '''
        self.list_unsorted.delete(0, tk.END)
        self.list_unsorted.insert(tk.END, *self.renamer.refresh())

    def sort_start(self):
        self.renamer.rename()
        self.refresh_list_unsorted()


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

    root = tk.Tk()
    app = App(master=root, renamer=filerenamer)
    app.mainloop()

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)
