#!/usr/bin/python        # Emplacement de l’interpréteur Python (sous Linux)
# -*- coding: utf-8 -*-  # Définition l'encodage des caractères

# Copyright 2020 Marc SIBERT
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import tkinter
import tkinter.messagebox

class App:
    """Cette classe implémente l'ensemble de l'application."""
    
    def __init__(self):
        """Constructeur de l'instance. Initialise toutes les propriétés."""
        self._matriceUI = {} # Matrice des objets Entry tkinker du Sudoku
        
        self._window = tkinter.Tk()
        self._window.title("Sudoku")
#        self.window.minsize(480,360)
        self._window.iconbitmap("lab-allen.ico")
#        self.window.config(background=None)

        frame = tkinter.Frame(self._window)
        frame.pack()

        tkinter.Label(
            frame,
            text="Saisir les valeurs connues :",
            anchor="nw"
        ).pack()

        megaGrid = tkinter.Frame(frame)

# 3 x 3 blocs
        for y in range(3):
            for x in range(3):
# 3 x 3 Entry par bloc
                grid = tkinter.Frame(megaGrid, bd=2, relief="ridge")
                for j in range(3):
                    for i in range(3):
                        entry = tkinter.Entry(grid,
                            font=("Courier",40,"bold"),
                            width=2,
                            justify="center"
                        )
                        entry.grid(row=j, column=i, sticky="ew")
                        self._matriceUI[x*3 + i, y*3 + j] = entry
                grid.grid(row=y, column=x)
        megaGrid.pack()
#Frame pour les boutons
        frameBoutons = tkinter.Frame(frame)
        tkinter.Button(frameBoutons, text="Générer", command=self._generer).pack(side=tkinter.LEFT)
        tkinter.Button(frameBoutons, text="Vider", command=self._vider).pack(side=tkinter.RIGHT)
        frameBoutons.pack()
        
        return

    def run(self):
        """Méthode a lancer une seule fois. Elle se termine avec la fin de l'application."""
        self._window.mainloop()
        
    def _generer(self):
        """Lance la génération du Sudoku et affiche le résultat."""
        for i, j in self._matriceUI: self._matriceUI[i,j].config(fg="black")
        
        m = {}
        error = False
        for i, j in self._matriceUI:
            if self._matriceUI[i,j].get() != '':
                try:
                    m[i,j] = int( self._matriceUI[i,j].get() )
                    if m[i,j] < 1 or m[i,j] > 9: raise(ValueError)
                    self._matriceUI[i,j].config(fg='black')
                except ValueError:
                    self._matriceUI[i,j].config(fg='red')
                    error = True
            else:
                m[i,j] = None;
        if error:
            tkinter.messagebox.showerror("Saisie invalide", "Une ou plusieurs valeurs sont invalides : chiffres de 1 à 9 seulement !");
            return    

        if not self._tabValide(m):
            tkinter.messagebox.showerror("Saisie invalide", "Le Sudoku est invalide : vérifiez !");
            return
        
        if self._tester(m) == None:
            tkinter.messagebox.showwarning("Pas de solution", "Je ne trouve pas de solution à ce Sudoku ; désolé !");
            return

# Mettre à jour tous les Widgets vides avec la valeur calculée.
        for i, j in m:
            if self._matriceUI[i,j].get() == '':
                self._matriceUI[i,j].insert(0, m[i,j])
                self._matriceUI[i,j].config(fg="blue")
                
        return
    
    def _vider(self):
        """Vide tous les widgets Entry présents dans la dict matriceUI."""
# Parcourir tous les Widget Entry du dict.
        for entry in self._matriceUI.values():
# Efface tout le texte.
            entry.delete(0, tkinter.END)
# Remet la couleur noire.
            entry.config(fg="black")
        return        

    def _tabValide(self, m):
        """Vérifie la validité du Sudoku transmis sous la forme d'un dict de clés 9x9"""
# Vérification des lignes    
        for j in range(9):
            l = [0] * 9
            for i in range(9):
                if m[i,j]:
                    if l[m[i,j]-1] == 1: return False
                    else: l[m[i,j]-1] += 1
# Vérification des colonnes
        for i in range(9) :
            l = [0] * 9
            for j in range(9) :
                if m[i,j]:
                    if l[m[i,j]-1] == 1: return False
                    else: l[m[i,j]-1] += 1
# Vérification des blocs
        for x in range(3) :
            for y in range(3) :
                l = [0] * 9
                for i in range(3) :
                    for j in range(3) :
                        if m[x*3 + i, y*3 + j] :
                            if l[m[x*3 + i, y*3 + j]-1] == 1: return False
                            else: l[m[x*3 + i, y*3 + j]-1] += 1
        return True

    def _tester(self, m):
        """Teste de manière récursive la validité des propositions jusqu'au remplissage complet du Sudoku"""
        vide = self._caseVide(m)
        if vide == None: return True
        (i, j) = vide
        for v in range(1, 10) :
            m[i,j] = v
            if not self._tabValide(m): continue
            if self._tester(m): return m
        m[i,j] = None
        return None


    def _caseVide(self, m):
        """Propose une case encore vide ou None si aucune de reste"""
        for i, j in m:
            if m[i,j] == None: return (i,j)
        return None
   
if __name__ == "__main__":
    app = App()
    app.run()
