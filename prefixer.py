import tkinter as tk
import os, fnmatch
import re
import configparser
from tkinter import messagebox
from operator import itemgetter


'''
Last Changes:
    - Messagebox eingebaut
    - Redundanzenbehandlung
    - Umstellung von Dict auf Listen
        --> Fehler: Originaldateiname fehlt als Information.

To do:
    Filter setzen
    Pfad einstellen
        Configfile für Beides
            check   

Großer Fehler: 
    
Bugs:
    - wenn bereits sortiert und man nochmal drauf klickt, gibt es eine fiese Dauerschleife
    - dauerschleife, auch wenn nach Sortierung manuell eine Ziffer in der Mitte weggenommen wird und nochmal versucht wird
    - Problematisch: Eine Datei wurde sogar gelöscht
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
        self.List_Rename = [] # Liste, in der die alten und neuen Namen stehen
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
        for item in self.ITEMS:
            print(item)
        

    ''' Holt die Items in einem Angegebenen Ordner (Folder) '''
    def get_items(self):
        Filtered = []
        for item in os.listdir(self.SETTINGS[0]) :
            if fnmatch.fnmatch(item,self.SETTINGS[1]):
                match = re.search("(^\d+)(_)(.+)",item)
                if match:
                    Filtered.append([item, match.group(1),match.group(3)])
                else:
                    Filtered.append([item])
        return Filtered
    ''' aktualisiert den Inhalt des Ordners '''
    def refresh_list_unsorted(self):
        self.list_unsorted.delete(0, tk.END)
        self.ITEMS = []
        self.ITEMS = self.get_items()

        for item in self.ITEMS:
            self.list_unsorted.insert(tk.END, item[0])

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
    def order_ok_2(self,Liste,index = 0):
        ''' wenn True, dann nichts zu tun '''
        return Liste[index][1]<Liste[index+1][1]


    ''' Funktion zum Vertauschen von Elementen '''
    def swap(self,Liste,a,b):
        Liste[a], Liste[b] = Liste[b], Liste[a]
        return Liste  

    def Pre_Sort_2(self,Liste):
        n = 0
        START = 0
        END = len(Liste)-1
        Redundant_Number = False
        while(n < END-1):
            for n in range(START,END):
                if ( self.order_ok_2(Liste,n) == False ):
                    self.swap(Liste,n,n+1)
                    break
                else:
                    pass
        return Liste

    def Redundant( self, Liste = [] ):
        ''' Check auf Redundanz
            Return:       
                -1 - keine Redundanz 
                Ziffer >= 0 - Position der Redundanz
        '''
        for index, item in enumerate(Liste):
            if (item != Liste[len(Liste)-1]):
                if (item[1] == Liste[index+1][1]):
                    return index
        return -1        

    def sort_start(self):
        ''' Trennung von Dateinamen mit Ziffern und ohne Ziffern '''
        List_mit_Ziffern = []
        List_ohne_Ziffern = []

        for item in self.ITEMS:
            if(len(item)>1): # wenn der Name bereits eine Ziffer als Prefix und die richtige Bauart hat
                List_mit_Ziffern.append(item)
            else:
                List_ohne_Ziffern.append(item)


        ''' Sortierung von List_mit_Ziffern nach Ziffern '''
        # Zahl von String zu Integer casten um diese anschließend zu sortieren'''
        for item in List_mit_Ziffern:
            item[1] = int(item[1])
        List_mit_Ziffern = sorted(List_mit_Ziffern,key = itemgetter(1)) # soriert nach Ziffer - zweite Stelle innerhalb der Items
        # Check auf Redundanz
        pos = self.Redundant(List_mit_Ziffern)         
        if (pos > -1):
            messagebox.showinfo("Information","Der Prefix \"" + str(List_mit_Ziffern[pos][0])+ "\"\nscheint doppelt vorzukommen. Bitte manuell korrigieren, \n\"neu laden\" klicken und den Sortiervorgang erneut starten")
            return 0
        ''' Gesamtliste auf 1 normieren '''

        Smallest_Number = List_mit_Ziffern[0][1]
        Normiersubtrahent = Smallest_Number - 1 # um diesen Wert muss jede Position durch Subtraktion reduziert werden
        for item in List_mit_Ziffern:
            item[1] = item[1] - Normiersubtrahent

        ''' Beseitigen von Lücken in der Sortierung '''
        n = 0
        while(n < len(List_mit_Ziffern)-1): 
            if ( List_mit_Ziffern[n+1][1] == List_mit_Ziffern[n][1] + 1 ): # gehe eins weiter, wenn das nächste Element eins weiter ist
                n+=1
            else: # ziehe bei der Lücke eins ab
                List_mit_Ziffern[n+1][1] -= 1

        ''' Anfuegen der Ziffernlosen Dateien '''
        for key in List_ohne_Ziffern:
            List_mit_Ziffern.append([key[0], List_mit_Ziffern[-1:][0][1]+1])
        

        ''' Ziffern neu formatieren '''
        for item in List_mit_Ziffern:
            item[1] = "{0:03d}".format(item[1])
        

        ''' Rename der Dateien vorbereiten'''
        self.List_Rename = [] # sicherstellen, dass Liste leer ist        

        for key in List_mit_Ziffern:
            if ( len(key) == 3 ):
                self.List_Rename.append([key[2],str(key[1])+"_"+str(key[2])])                

            elif ( len(key) == 2 ):            
                self.List_Rename.append([key[0],str(key[1])+"_"+str(key[0])])                
            else:
                print("Fehler")
            
            ''' vergessen den Originalnamen im Dictionary zu speichern. Schlecht '''
        for key in self.List_Rename:
            print(key[0], " " , key[1])
            #os.rename(self.SETTINGS[0]+Filename, self.SETTINGS[0]+Filename)

                

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
