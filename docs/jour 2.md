# Jour 2 : Premier objet - Tout est dans la matrice

---

- Retour au [Sommaire](index.md)
- Jour 1 : [Le langage Python, l'IDE et la Classe (!)](jour 1.md)

---

Dans le cadre de notre développement, nous allons commencer par développer la logique de résolution du Sudoku. Dans un second temps, nous travaillerons sur l'interface avec l'utilisateur de l'application.

Aujourd'hui, nous allons donc modéliser et développer la matrice du Sudoku qui porte les chiffres.

## 1. La Classe

Au départ cette classe est donc une matrice de 9x9. Il va falloir lui adjoindre un certain nombre de méthodes permettant de la manipuler (la modifier, l'afficher, _etc._)

Voici donc un code qui permet d'assurer ces premiers besoins (`exercice3.py`) :

	#!/usr/bin/python
	# -*- coding: <encoding name> -*-
	
	"""Exercice 3a"""
	
	class Matrice:
	    """La Matrice est l'objet qui contient tous les chiffres du Sudoku dans un tableau de 9x9"""
	
	    def __init__(self, init : [] = None) -> None:
	        """Constructeur de l'instance qui initialise la matrice 9*9 à partir d'un tableau existant,
	            s'il est transmis, à vide sinon."""
	        if init == None:
	            self._matrice = [[None] * 9] * 9
	        else:
	            self._matrice = {}
	            for x in range(9):
	                self._matrice[x] = {}
	                for y in range(9):
	                    try:
	                        self._matrice[x][y] = init[x][y]
	                    except IndexError:
	                        self._matrice[x][y] = None
	            
	    def afficher(self) -> None:
	        """Cette méthode affiche une représentation de la matrice du Sudoku"""
	        print(self)
	        for x in range(9):
	            print(self._matrice[x])
	            
	    def __getitem__(self, key : (int,int) ) -> int:
	        """Cet accesseur (getter) permet de récupérer la valeur d'une cellule"""
	        (x, y) = key
	        assert (x >= 0), "Hors interval (négatif)"
	        assert (x <= 9), "Hors interval (sup. à 9)"
	        return self._matrice[y][x]
	
	    def __setitem__(self, key : (int,int), value : int) -> None:
	        """Cet accesseur (setter) permet de donner une valeur à une cellule"""
	        (x, y) = key
	        assert (x >= 0), "Hors interval (négatif)"
	        assert (x <= 9), "Hors interval (sup. à 9)"
	        self._matrice[y][x] = value
	        
    matrice = Matrice([
        [None, None, None, None,    5, None, None,    6, None],
        [   5,    8,    2, None, None,    9, None, None,    4],
        [None,    6, None, None, None, None, None, None,    9],
        [   8,    3, None,    4, None,    1,    6, None, None],
        [None,    7, None, None, None, None, None,    8, None],
        [None, None,    1,    7, None,    6, None,    3,    5],
        [   6, None, None, None, None, None, None,    4, None],
        [   3, None, None,    6, None, None,    7,    2,    8],
        [None,    1, None, None,    7, None, None, None, None]
    ])
	
    matrice.afficher()

