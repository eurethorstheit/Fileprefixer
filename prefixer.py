import tkinter as tk
import os, fnmatch
import re
import configparser
from tkinter import messagebox


'''
Last Changes:
    - Messagebox eingebaut
    - Redundanzenbehandlung
To do:
    Filter setzen
    Pfad einstellen
        Configfile für Beides

Bugs:
    - wenn bereits sortiert und man nochmal drauf klickt, gibt es eine fiese Dauerschleife
'''

''' Hole Configuration '''

config = configparser.ConfigParser()
config.read('settings.ini')


''' ENDE / Hole Configuration '''


class App(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()
        self.SETTINGS = ['./Test/','*.txt'] # [Ordner, Erweiterung]
        self.ITEMS = self.get_items()
        self.create_widgets()
        self.refresh_list_unsorted()
    ''' Erstellt die Widgets '''
    def create_widgets(self):


        self.l_folder = tk.Label(self)
        self.l_folder["text"] = "Dateiordner:", config['DEFAULT']['folder'] 
        self.l_folder.pack(side = "top")

        self.l_filter = tk.Label(self)
        self.l_filter["text"] = "Filter:", config['DEFAULT']['filter'] 
        self.l_filter.pack(side = "top")

        self.list_unsorted = tk.Listbox(self)
        self.list_unsorted.pack()

        self.b_refresh = tk.Button(self)
        self.b_refresh["text"] = "Liste neu laden"
        self.b_refresh["command"] = self.refresh_list_unsorted
        self.b_refresh.pack(side = "top")

        self.b_start = tk.Button(self, fg="red")
        self.b_start["text"] = "Neu Sortieren\nStart"
        self.b_start["command"] = self.sort_start
        self.b_start.pack(side = "top")

        self.b_test = tk.Button(self)
        self.b_test["text"] = "Testbutton"
        self.b_test["command"] = self.testfunktion
        self.b_test.pack(side = "top")

        self.b_quit = tk.Button(self, text="Quit", command=root.destroy)
        self.b_quit.pack(side="bottom")


    ''' Testfunktion '''
    def testfunktion(self):
        print(config['DEFAULT']['filter'])

    ''' Holt die Items in einem Angegebenen Ordner (Folder) '''
    def get_items(self):
        Filtered = []
        for file in os.listdir(self.SETTINGS[0]) :
            if fnmatch.fnmatch(file,self.SETTINGS[1]):
                Filtered.append(file)
        Filtered = [ item for item in Filtered if ( item != "prefixer.py") ]
        return Filtered
    ''' aktualisiert den Inhalt des Ordners '''
    def refresh_list_unsorted(self):
        self.list_unsorted.delete(0, tk.END)
        self.ITEMS = self.get_items()

        for item in self.ITEMS:
            self.list_unsorted.insert(tk.END, item)
    def get_number(self, name = ""):
        match = re.search("(^\d+)(_)(.+)",name)
        return int(match.group(1)), match.group(3)

    def order_ok(self,StringA,StringB):
        ''' 0 - A<B (ok), 1 - A>B (swap), 2 - A=B (NOK - abort) '''
        A = re.search("(^\d+)(_)(.+)",StringA)
        B = re.search("(^\d+)(_)(.+)",StringB)
        A = int(A.group(1))
        B = int(B.group(1))
        if A<B:
            return 0
        elif A>B:
            return 1
        else:
            return 2

    ''' Funktion zum Vertauschen vol Elementen '''
    def swap(self,Liste,a,b):
        Liste[a], Liste[b] = Liste[b], Liste[a]
        return Liste  

    def Pre_Sort(self,Liste):
        ''' Sortieren '''
        n = 0
        START = 0
        END = len(Liste)-1
        Redundant_Number = False
        while(n < END-1):
            for n in range(START,END):
                if ( self.order_ok(Liste[n],Liste[n+1]) == 1 ):
                    self.swap(Liste,n,n+1)
                    break
                elif ( self.order_ok(Liste[n],Liste[n+1]) == 2 ):
                    Redundant_Number = True
                    break
                else:
                    pass
            if Redundant_Number == True:
                break
        if Redundant_Number == False:
            return Liste
        else:
            return [ 'Redundant', Liste[n] ]

    def sort_start(self):
        List_mit_Ziffern = []
        List_ohne_Ziffern = []
        for name in self.ITEMS:
            if(re.search("(^\d+)(_)(.+)",name)): # wenn der Name bereits eine Ziffer als Prefix und die richtige Bauart hat
                List_mit_Ziffern.append(name)
            else:
                List_ohne_Ziffern.append(name)

        List_mit_Ziffern = self.Pre_Sort(List_mit_Ziffern) # Vorsortierung, damit es in den späteren Algorithmen keine Probleme gibt

        if List_mit_Ziffern[0] == 'Redundant':
            messagebox.showinfo("Information","Der Prefix der Datei\n\n\t"+List_mit_Ziffern[1]+ "\n\nscheint doppelt vorzukommen. Bitte manuell korrigieren, neu laden klicken und den Sortiervorgang erneut starten")
        else:

            D_List_mit_Ziffern = dict.fromkeys(List_mit_Ziffern) # Umwandeln in ein Dictionary
        
            for index, key in enumerate(D_List_mit_Ziffern):
                D_List_mit_Ziffern[key] = list(self.get_number(List_mit_Ziffern[index]))

            ''' Start der Gesamtliste auf 1 normieren '''
            if (len(D_List_mit_Ziffern) > 0 ) :
                while( next(iter(D_List_mit_Ziffern.values()))[0] > 1 ): # wenn das erste Element der Werte ungleich 1
                    for key in D_List_mit_Ziffern.keys():
                        D_List_mit_Ziffern[key][0] = D_List_mit_Ziffern[key][0]-1 # ziehe überall eins ab
                ''' ENDE / Start der Gesamtliste auf 1 normieren '''
                ''' Beseitigen von Lücken in der Sortierung '''
                n = 0
                d_keys = list(D_List_mit_Ziffern.keys())

                while(n < len(D_List_mit_Ziffern)-1): 
                    if ( D_List_mit_Ziffern[d_keys[n+1]][0] == D_List_mit_Ziffern[d_keys[n]][0] + 1 ): # gehe eins weiter, wenn das nächste Element eins weiter ist
                        n+=1
                    else: # ziehe bei der Lücke eins ab
                        D_List_mit_Ziffern[d_keys[n+1]][0]-=1

                ''' ENDE / Beseitigen von Lücken in der Sortierung '''
                ''' Prefixe auf 1 normiert und Lücken beseitigt in D_List_mit_Ziffern'''
            ''' Ziffernlose Dateien im Dictionary hinten anfügen '''
            n = len(D_List_mit_Ziffern) + 1
            for key in List_ohne_Ziffern:
                D_List_mit_Ziffern[key] = [n,key]
                n+=1
            ''' ENDE / Ziffernlose Dateien im Dictionary hinten anfügen '''

            ''' Normalisieren der Prefixe auf Format xxx_ '''
            for key in D_List_mit_Ziffern:
                D_List_mit_Ziffern[key][0] = "{0:03d}".format(D_List_mit_Ziffern[key][0])
            ''' ENDE / Normalisieren der Prefixe auf Format xxx_ '''

            for key in D_List_mit_Ziffern:
                os.rename(self.SETTINGS[0]+key, self.SETTINGS[0]+D_List_mit_Ziffern[key][0]+"_"+D_List_mit_Ziffern[key][1])

            self.refresh_list_unsorted()
            messagebox.showinfo("Information","Liste ist neu sortiert. Veränderungen sind in log_sort.log gespeichert")

Ordner = "C:\\Users\\Thorsten\\Documents\\Python"
Erweiterung = '*.txt'
root = tk.Tk()
app = App(master = root)
app.mainloop()


''' Setze Configuration '''

config['DEFAULT'] = {'Folder':'./Test/','Filter':'.txt' }

with open('settings.ini', 'w') as configfile:
    config.write(configfile)

''' ENDE / Setze Configuration '''
