#!/usr/bin/python
# -*- coding: <encoding name> -*-

class Matrice:
    """La Matrice est l'objet qui contient tous les chiffres du Sudoku dans un tableau de 9x9"""

    def __init__(self, init : [] = None) -> None:
        """Constructeur de l'instance qui initialise la matrice 9*9 à partir d'un tableau existant,
            s'il est transmis, à vide sinon."""
        self._matrice = []
        for y in range(9):
            self._matrice.append( [None] * 9 )
        if init != None:
            for y in range(9):
                for x in range(9):
                    try:
                        self[x,y] = init[y][x]
                    except IndexError:
                        pass
            
    def afficher(self) -> None:
        """Cette méthode affiche une représentation de la matrice du Sudoku"""
        for l in self._matrice:
            print(l)
            
    def _unVide(self) -> (int, int):
        """Cette méthode retourne une paire de coordonnées représentant un emplacement vide.
            Elle lance une exception quand aucune solution n'est possible (grille complète)."""
        for y in range(9):
            for x in range(9):
                if self[x,y] == None:
                    return x, y
        raise Exception("Grille complète") 
        
    def __getitem__(self, key : (int,int) ) -> int:
        """Cet accesseur (getter) permet de récupérer la valeur d'une cellule"""
        x, y = key
        assert (x >= 0), "Hors interval (négatif)"
        assert (x <= 9), "Hors interval (sup. à 9)"
        return self._matrice[y][x]

    def __setitem__(self, key : (int,int), value : int) -> None:
        """Cet accesseur (setter) permet de donner une valeur à une cellule"""
        x, y = key
        assert (x >= 0), "Hors interval (négatif)"
        assert (x <= 9), "Hors interval (sup. à 9)"
        self._matrice[y][x] = value
        
    def tester(self) -> bool:
        """Cette méthode vérifie la validité de la matrice et la retourne sous la forme d'un booléen."""
# Test par ligne
        for y in range(9):
            c = [False] * 9
            for x in range(9):
                try:
                    s = self[x,y] - 1
                except TypeError:
                    continue
                if c[s]:
                    return False
                else:
                    c[s] = True
# Test par colonne
        for x in range(9):
            c = [False] * 9
            for y in range(9):
                try:
                    s = self[x,y] - 1
                except TypeError:
                    continue
                if c[s]:
                    return False
                else:
                    c[s] = True
# Test par carré
        for i in range(3):
            for j in range(3):
                c = [False] * 9
                for x in range(3):
                    for y in range(3):
                        try:
                            s = self[x + i*3,y + j*3] - 1
                        except TypeError:
                            continue
                        if c[s]:
                            return False
                        else:
                            c[s] = True
        return True
                
    def resoudre(self) -> bool:
        """Cette méthode résoud la matrice de manière récursive dans la séquence suivante :
            1. Chercher un emplacement libre, sinon on a terminé avec succès !
            2. Essayer tous les nombres de 1 à 9 ;
            3. Si c'est une matrice valide, appliquer la même méthode recursivement ;
            4. Si le résultat est bon, succès ; sinon essayer encore."""
        try:
            x, y = self._unVide()
        except Exception:
            return True
        for n in range(9):
            self[x,y] = n + 1;
            if self.tester() and self.resoudre():
                return True
        self[x,y] = None
        return False
        