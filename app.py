'''GUI'''

import tkinter as tk


class App(tk.Frame):
    ''' Die Hauptklasse '''

    def __init__(self, renamer):
        self.renamer = renamer

        self.root = tk.Tk()
        super().__init__(self.root)
        self.create_widgets()
        self.refresh_list_unsorted()

    def create_widgets(self):
        ''' Erstellt die Widgets '''

        self.l_folder = tk.Label(self.root)
        self.l_folder["text"] = "Dateiordner:", self.renamer.get_directory()
        self.l_folder.pack(side="top")

        self.l_filter = tk.Label(self.root)
        self.l_filter["text"] = "Filter:", self.renamer.get_suffix()
        self.l_filter.pack(side="top")

        self.list_unsorted = tk.Listbox(self.root)
        self.list_unsorted.pack(fill=tk.BOTH, expand=1)

        self.b_refresh = tk.Button(self.root)
        self.b_refresh["text"] = "Liste aktualisieren"
        self.b_refresh["command"] = self.refresh_list_unsorted
        self.b_refresh.pack(side="top")

        self.b_start = tk.Button(self.root, fg="red")
        self.b_start["text"] = "Sortieren"
        self.b_start["command"] = self.sort_start
        self.b_start.pack(side="top")

        self.b_quit = tk.Button(
            self.root, text="Quit", command=self.root.destroy)
        self.b_quit.pack(side="bottom")

    def refresh_list_unsorted(self):
        ''' aktualisiert den Inhalt des Ordners '''
        self.list_unsorted.delete(0, tk.END)
        self.list_unsorted.insert(tk.END, *self.renamer.refresh())

    def sort_start(self):
        self.renamer.rename()
        self.refresh_list_unsorted()
