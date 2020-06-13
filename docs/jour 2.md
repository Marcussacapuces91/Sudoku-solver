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

```
#!/usr/bin/python
# -*- coding: <encoding name> -*-

"""Exercice 3"""

class Matrice:
    """La Matrice est l'objet qui contient tous les chiffres du Sudoku dans un tableau de 9x9"""

    def __init__(self, init : [] = None) -> None:
        """Constructeur de l'instance qui initialise la matrice 9x9 à partir d'un tableau existant,
            s'il est transmis, à vide sinon."""
        if init == None:
            self._matrice = [[None] * 9] * 9
        else:
            self._matrice = {}
            for y in range(9):
                self._matrice[y] = {}
                for x in range(9):
                    try:
                        self._matrice[y][x] = init[y][x]
                    except IndexError:
                        self._matrice[y][x] = None
            
    def afficher(self) -> None:
        """Cette méthode affiche une représentation de la matrice du Sudoku"""
        for y in self._matrice:
            print(self._matrice[y])
            
    def _unVide(self) -> (int, int):
        """Cette méthode retourne une paire de coordonnées représentant un emplacement vide.
            Elle lance une exception quand aucune solution n'est possible (grille complète)."""
        for y in self._matrice:
            for x in self._matrice[y]:
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

print("Valeur de la matrice en x=0, y=1")
print(matrice[0,1])
```

Si l'on regarde ce code, on retrouve la déclaration de la classe `Matrice`. 

### Constructeur

Vient ensuite la déclaration du constructeur avec une petite astuce ; en effet, le constructeur peut être appelé avec le paramètre `init` qui est optionnel. S'il n'est pas précisé, il prend la valeur `None`. On pourra ensuite tester sa valeur pour créer la matrice, soit totalement vide, soit avec les nombres repris du paramètre.

### Affichage

Cette méthode permet d'obtenir une représentation de la matrice dans la console. On parcours chaque ligne de la matrice que l'on affiche sommairement.

### Accesseurs

Les _accesseurs_ sont une typologie de methodes qui donnent accès, _d'où leur nom_, à des attributs internes d'une classe, tout en vérifiant ou en contrôlant leur accès.

Ici on définit deux accesseurs `__getitem__` et `__setitem__` qui permettront d'atteindre le contenu de la matrice au travers d'un appel avec l'opérateur de tableau que l'on ci-dessous :

	print("Valeur de la matrice en x=0, y=1")
    print(matrice[0,1])

Il s'agit ici, comme pour le constructeur, de deux méthodes _magiques_ qui ne sont pas appelées directement mais qui permettent des actions en arrière plan. On verra surement plus tard d'autres méthodes magiques.

### Initialisation

On voit dans le programme lui-même, avec l'initialisation comment on peut charger la matrice avec une matrice de Sudoku, les veleurs sont indiquées alors que les cases vides reçoivent la valeur `None`.

## 2. La résolution du problème

Le problème du Sudoku fait partie d'une grande famille des problèmes dits _de satisfaction de contraintes_ ou CSP ([Wikipédia - Problème de satisfaction de contraintes](https://fr.wikipedia.org/wiki/Probl%C3%A8me_de_satisfaction_de_contraintes)). L'introduction de cet article de **Pour la Science** donne un aperçu du problème : https://www.pourlascience.fr/sd/mathematiques/le-probleme-du-sudoku-8241.php.

La méthode proposée ici pour résoudre le Sudoku est l'essai systématique de toutes les combinaisons possibles jusqu'au succès en tenant compte des contraintes du jeu que je rappelle ci-dessous :

- sur une ligne, chaque nombre de 1 à 9 ne peut apparaitre qu'une seule fois ;
- sur une colonne, chaque nombre de 1 à 9 ne peut apparaitre qu'une seule fois ;
- dans un bloc de 3x3 (9 au total), chaque nombre de 1 à 9 ne peut apparaitre qu'une seule fois.

On va donc remplir les cases vides avec les nombres autorisés jusqu'à la complétude de la matrice. Pour 81 cases, on a à chaque fois 10 possibilité soient environs 10^91 cas a étudier au maximum.

Les cases déjà remplies ne peuvent plus être modifiées et les contraintes qui s'appliquent à chaque fois vont limiter le nombre de possibilités. De fait, on a beaucoup moins de possibilités que le maximum théorique. Si en plus on s'arrête à la première solution découverte, on va grandement limiter la complexité de la recherche. Enfin, comme l'indique l'article de **Pour la Science** les Sudoku habituellement rencontrés comportent déjà entre 25 et 30 cases remplies. La théorie indique d'un Sudoku valide pourrait démarrer avec seulement 17 cases. Dans ce cas, il ne sera surement pas résolu en un temps raisonnable par ce programme. Il faudrait se tourner vers d'autres algorithmes, par exemple mettant en oeuvre des heuristiques ou des méthodes statistiques de recherche de solutions.

Afin de limiter la consommation de mémoire du programme, on va aussi utiliser une méthode dite de _backtracking_ ou « retour sur trace » ([Wikipédia - Retour sur trace](https://fr.wikipedia.org/wiki/Retour_sur_trace)).

### Validité de la matrice

Il nous faut donc d'abord une méthode qui nous indique la validité d'une grille et qui sera définie dans la classe `Matrice` :

```
def _tester(self) -> bool:
    """Cette méthode vérifie la validité de la matrice et la retourne sous la forme d'un booléen."""
# Test par ligne
    for y in range(9):				# chaque ligne
        c = [False] * 9				# vecteur de 9xFalse
        for x in range(9):			# pour chaque entrée dans la ligne
            try:
                s = self[x,y] - 1	# valeur -1 -> [0..8]
            except TypeError:		# si 'None'
                continue			# pas de comptage
            if c[s]:				# déjà compté 1 fois ?
                return False		# alors 2 apparitions -> invalide
            else:
                c[s] = True			# Enregistrer 1er comptage
# Test par colonne
    for x in range(9):				# chaque colonne
        c = [False] * 9				# idem...
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
    for i in range(3):				# chaque...
        for j in range(3):			# ...carré
            c = [False] * 9
            for x in range(3):		# matrice 3x3
                for y in range(3):
                    try:
                        s = self[x + i*3,y + j*3] - 1
                    except TypeError:
                        continue
                    if c[s]:
                        return False
                    else:
                        c[s] = True
    return True						# Aucune erreur -> matrice valide
```

Cette méthode va compter successivement pour chaque ligne, pour chaque colonne et pour chaque carré de 3x3, le nombre d'apparition de chaque nombre (hors `None`). Si un nombre apparait plus de 1 fois, la réponse est `False` puisque la matrice est erronnée.

À noter, l'utilisation de la capture d'exception avec la commande `try:` qui va forcer la poursuite du test sans compter l'apparition des valeurs vides (`None`).

### Résolution (enfin) !

C'est finalement assez facile de résoudre un Sudoku. Il suffit de :

1. prendre une grille partielle ;
2. de recherche un emplacement encore vide (s'il n'y en a plus c'est que la grille est complète : **succès** !) ;
3. d'y ajouter un nombre de 1 à 9 qui ne rende pas la grille invalide ;
4. d'appeler la même méthode ;
5. si succès une fois, succès toujours ;
6. sinon, essayer avec un autre nombre ;
7. quand on a testé tous les nombres pour cette position, on la vide à nouveau (laisser propre derrière soi...)

Ecrivons ça, sans plus réfléchir :

```
def resoudre(self) -> bool:
    """Cette méthode résoud la matrice de manière récursive dans la séquence suivante :
        - Chercher un emplacement libre, sinon on a terminé avec succès !
        - Essayer tous les nombres de 1 à 9 ;
        - Si c'est une matrice valide, appliquer la même méthode recursivement ;
        - Si le résultat est bon, succès ; sinon essayer encore."""
    try:
        x, y = self._unVide()
    except Exception:
        return True
    for n in range(9):
        self[x,y] = n + 1;		# tester les nombres de 1 à 9
        if self._tester() and self.resoudre():
            return True
    self[x,y] = None			# backtrack : remise dans l'état initial
    return False
```

C'est KISS (_Keep It Simple, Stupid_) et ça fonctionne. On vient de réaliser une méthode recursive pour résoudre un problème simplement en définissant une seule itération et ses conditions de sortie.

> _Comme c'est beau la programmation !_  
> _Coding Is Poetry_

## 3. Fichier complet

```
#!/usr/bin/python
# -*- coding: <encoding name> -*-

"""Exercice 3"""

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
    
class Matrice:
    """La Matrice est l'objet qui contient tous les chiffres du Sudoku dans un tableau de 9x9"""

    def __init__(self, init : [] = None) -> None:
        """Constructeur de l'instance qui initialise la matrice 9*9 à partir d'un tableau existant,
            s'il est transmis, à vide sinon."""
        if init == None:
            self._matrice = [[None] * 9] * 9
        else:
            self._matrice = {}
            for y in range(9):
                self._matrice[y] = {}
                for x in range(9):
                    try:
                        self._matrice[y][x] = init[y][x]
                    except IndexError:
                        self._matrice[y][x] = None
            
    def afficher(self) -> None:
        """Cette méthode affiche une représentation de la matrice du Sudoku"""
        for y in self._matrice:
            print(self._matrice[y])
            
    def _unVide(self) -> (int, int):
        """Cette méthode retourne une paire de coordonnées représentant un emplacement vide.
            Elle lance une exception quand aucune solution n'est possible (grille complète)."""
        for y in self._matrice:
            for x in self._matrice[y]:
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
        
    def _tester(self) -> bool:
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
            if self._tester() and self.resoudre():
                return True
        self[x,y] = None
        return False
        

if __name__ == "__main__":
    logger.info("Démarrage du programme")
    if False:
# Difficile        
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
    elif False:
# A l'envers (ligne 1 : 9 8 7 6 5 4 3 2 1)
        matrice = Matrice([
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None,    3, None,    8,    5],
            [None, None,    1, None,    2, None, None, None, None],
            [None, None, None,    5, None,    7, None, None, None],
            [None, None,    4, None, None, None,    1, None, None],
            [None,    9, None, None, None, None, None, None, None],
            [   5, None, None, None, None, None, None,    7,    3],
            [None, None,    2, None,    1, None, None, None, None],
            [None, None, None, None,    4, None, None, None,    9],
        ])
    elif False:
# 17 valeurs
        matrice = Matrice([
            [None, None, None, None,    4, None, None, None, None],
            [   1,    2, None, None, None, None, None,    7,    3],
            [None,    3, None, None, None,    8, None, None, None],
            [None, None,    4, None, None, None,    6, None, None],
            [None, None, None,    2, None,    3, None, None, None],
            [None, None,    5, None, None, None, None, None, None],
            [None, None,    6, None,    9, None,    5, None, None],
            [None,    7, None, None, None, None, None,    2, None],
            [None, None, None, None, None, None, None, None, None],
        ])
    else:
# 18 valeurs avec symétrie verticale
        matrice = Matrice([
            [None, None, None, None, None, None, None, None, None],
            [   1,    2, None, None, None, None, None,    8,    4],
            [None,    3, None, None, None, None, None,    7, None],
            [None, None,    4, None, None, None,    6, None, None],
            [None, None, None,    2, None,    3, None, None, None],
            [None, None,    5, None, None, None,    9, None, None],
            [None, None,    6, None,    9, None,    5, None, None],
            [None,    7, None, None, None, None, None,    2, None],
            [None, None, None, None,    5, None, None, None, None],
        ])
        
    matrice.afficher()
    
    matrice.resoudre()
    matrice.afficher()
    
    logger.info("Arrêt du programme")
```










