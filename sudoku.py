#!/usr/bin/python
# -*- coding: <encoding name> -*-

"""Exercice 4"""

from tkinter import Tk, Label, Frame, Entry, Button, LEFT, RIGHT, END, messagebox
from matrice import Matrice

#from matrice import Matrice

class Application(Tk):
    """Classe de l'application.
        Hérite de Tk pour instancier automatiquement une fenètre."""
    
    def __init__(self):
        """Constructeur de l'application. Initialise l'interface graphique."""
        super().__init__(None)
        
        self.title("Solveur de Sudoku")
        self.iconbitmap("lab-allen.ico")
        
        Label(self, text="Saisir les valeurs connues et lancer la résolution").pack()

        megaFrame = Frame(self)
        self._entries = []
        for y in range(9):
            self._entries.append( [None] * 9 )
        
# 3 x 3 blocs
        for y in range(3):
            for x in range(3):
# 3 x 3 Entry par bloc
                grid = Frame(megaFrame, bd=2, relief="ridge")
                for j in range(3):
                    for i in range(3):
                        e = Entry(grid,
                            font=("Courier", 40, "bold"),
                            width=2,
                            justify="center"
                        )
                        e.grid(row=j, column=i, sticky="ew")
                        self._entries[y*3+j][x*3+i] = e 
                grid.grid(row=y, column=x)
        megaFrame.pack()
        
        frameBoutons = Frame(self)
        Button(frameBoutons, text="Générer", command=self._generer).pack(side=LEFT)
        Button(frameBoutons, text="Vider", command=self._vider).pack(side=RIGHT)
        frameBoutons.pack()

    def _generer(self):
        """Cette méthode vérifie la saisie puis transmet les valeurs à une instance de Matrice
            pour faire résoudre le Sudoku. Elle affiche le résultat, si le calcul s'est bien passé."""
        m = []
        erreur = False
        for y in range(9):
            m.append( [None] * 9 )
            for x in range(9):
                if self._entries[y][x].get() != "":
                    try:
                        m[y][x] = int(self._entries[y][x].get())
                        if m[y][x] < 1 or m[y][x] > 9:
                            raise ValueError()
                        
                        if self._entries[y][x]['fg'] == "red":
                            self._entries[y][x]['fg'] = "black"
                    except ValueError:
                        erreur = True
                        self._entries[y][x]['fg'] = "red"
        if erreur:
            return
        matrice = Matrice(m)
        if not(matrice.tester()):
            messagebox.showwarning("Matrice", "Matrice invalide. Corriger pour continuer !")
            return
        matrice.resoudre()

        for y in range(9):
            for x in range(9):
                if self._entries[y][x].get() == "" :
                    self._entries[y][x].delete(0, END)
                    self._entries[y][x].insert(0, matrice[x,y])
                    self._entries[y][x]['fg'] = "blue"

    def _vider(self):
        """Cette méthode vide les Entry bleu (ceux calculés précédemment),
            sans toucher aux saisies de l'utilisateur (noires)"""
        for y in range(9):
            for x in range(9):
                if self._entries[y][x]['fg'] == "blue" :
                    self._entries[y][x].delete(0, END)
                    self._entries[y][x]['fg'] = "black"

if __name__ == "__main__":
    
    app = Application()
    app.mainloop()
