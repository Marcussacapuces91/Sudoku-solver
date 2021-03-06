# Jour 3 : Interface graphique - TKinter

---

- Retour au [Sommaire](index)
- Jour 2 : [Premier objet - Tout est dans la matrice](jour%202)

---

## TKinter

TKinter est une librairie qui permet de générer des fenêtres graphiques ainsi que tous les éléments (_widgets_) qui s'y trouvent.

Elle va nous permettre de faire une représentation plus jolie que la sortie texte de notre jeu du Sudoku, ainsi qu'une interface de saisie plus agréable à utiliser que des tableaux dans le code.

Voyez la page de cette librairie sur le site Python : [https://docs.python.org/fr/3/library/tkinter.html](https://docs.python.org/fr/3/library/tkinter.html). Il existe aussi plein de site présentant des cours pour utiliser TkInter.

## La classe (encore)

Cette fois on va définir une classe Application qui va hériter de la classe Tk. Elle va donc _récupérer_ toutes les méthodes et attributs de la classe mère. En particulier, après avoir initialisé notre application, il faut lancer la méthode `mainloop()` qui permet le fonctionnement des éléments de la fenêtre.

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Exercice 4a"""

from tkinter import Tk, Label, Frame, Entry, Button, LEFT, RIGHT, END, messagebox
from matrice import Matrice

class Application(Tk):
    """Classe de l'application.
        Hérite de Tk pour instancier automatiquement une fenètre."""

    def __init__(self):
		"""Constructeur de l'application. Initialise l'interface graphique."""
        super().__init__(None)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
```

## Constructeur

Comme d'habitude maintenant le constructeur va initialiser tous les éléments de notre application, c'est à dire ici dessiner la fenêtre avec tous les objets de rendu qui s'y trouvent (les _widgets_).

Cette fois, on va aussi devoir appeler le constructeur hérité dans notre propre constructeur, avant de définir les attributs de la la fenêtre et de la remplir avec des _widgets_.

```python
def __init__(self):
    """Constructeur de l'application. Initialise l'interface graphique."""
    super().__init__(None)
    self.title("Solveur de Sudoku")
    self.iconbitmap("lab-allen.ico")
    
    Label(self, text="Saisir les valeurs connues et lancer la résolution").pack()

    megaFrame = Frame(self)
    self._entries = [[None] * 9] * 9
# 3 x 3 blocs
    for y in range(3):
        for x in range(3):
# 3 x 3 Entry par bloc
            grid = Frame(megaFrame, bd=2, relief="ridge")
            for j in range(3):
                for i in range(3):
                    self._entries[y*3+j][x*3+i] = Entry(grid,
                        font=("Courier",40,"bold"),
                        width=2,
                        justify="center"
                    )
                    self._entries[y*3+j][x*3+i].grid(row=j, column=i, sticky="ew")
            grid.grid(row=y, column=x)
    megaFrame.pack()
    
    frameBoutons = Frame(self)
    Button(frameBoutons, text="Générer").pack(side=LEFT)
    Button(frameBoutons, text="Vider").pack(side=RIGHT)
    frameBoutons.pack()
```

_Et voilà_ (en anglais dans le texte) ! Mais expliquons quand même l'utilisation de quelques _widgets_.

Tout d'abord chaque _widget_ doit faire référence à un élément de niveau supérieur qui le contient puisque celui-ci aura la responsabilité de l'afficher quand certains paramètres changes (largeur de la fenêtre, _etc._). C'est ce que l'on retrouve dans chaque instanciation d'un _widget_.

Ensuite, chaque _widget_ doit être placé dans l'élément de niveau supérieur, soit avec la méthode `pack()`, soit avec `grid()` qui permet de placer l'objet dans une matrice ligne/colonne.

Enfin, les instances de `Frame` n'affichent rien d'autre que les objets qu'elle contiennent mais permettent de regrouper ces objets dans un carré correspondant.

Si je ne suis pas très clair, je vous recommande de vous plonger dans la doc de la librairie Tkinter dont vous avez un lien en introduction.

### Attributs

Déjà, on peut modifier ou définir des attributs de la fenêtre en appelant directement _self_ puisqu'on hérite de Tk, la fenêtre principale.

On ajoute donc un titre et une icone à notre fenêtre.

### Label

Il s'agit là d'un libellé fixe qui permet d'afficher n'importe quel texte. On lui applique sa méthode _pack()_ qui l'injecte dans la fenêtre.

### Entry

Cette fois, il nous faut définir la matrice graphique de 9 par 9 avec des sous-groupe de 3 par 3. L'ensemble est formé d'_Entry_ qui permettent des saisies et de _Frame_ qui les contiennent 3 par 3, l'ensemble étant placé dans une _Frame_ unique.

Par contre, il nous faudra garder des références sur ces _Entry_ afin de pouvoir lire leur contenu ultérieurement ; c'est ce qui est fait avec le tableau `self._entries`.

### Button

Pour terminer, on ajoute une dernière _Frame_ qui contient elle-même deux _Buttons_ qui vont permettre de déclencher des actions.

### Les _callback_

Les _callback_ sont des méthodes qui sont définies par l'utilisateur mais appelées automatiquement par l'environnement (le _framework_ Tkinter) lorsque des événements surviennent.

Dans notre cas, c'est utilisé par les _Button_ afin qu'ils indiquent à notre instance que l'un d'eux a été cliqué.

On devra donc ajouter une option supplémentaire à chacun de nos boutons, ainsi que les méthodes associées :

```python
...
    frameBoutons = Frame(self)
    Button(frameBoutons, text="Générer", command=self._generer).pack(side=LEFT)
    Button(frameBoutons, text="Vider", command=self._vider).pack(side=RIGHT)
    frameBoutons.pack()

def _generer(self):
    pass

def _vider(self):
    pass
```
                          
### Méthode `Generer`

Une fois que l'utilisateur de l'application aura rempli les éléments prédéfinis du Sudoku, il va cliquer sur le bouton Générer, ce qui va lancer la méthode homonyme comme indiqué précédemment.

Après avoir vérifié la validité des valeurs présentent dans le quadrillage formé par les `Entry`, cette méthode va maintenant instancier la classe `Matrice` que l'on a enregistrés à l'issue de l'exercice 3 dans le fichier `matrice.py`.

On pourra alors utiliser les méthodes à notre dispositions pour faire calculer le Sudoku et afficher le résultat.

Pour que cela soit « beau », on va utiliser un code couleur appliqué dans le rendu :

* En rouge, les valeurs invalides (avec une fenêtre d'erreur) ;
* En noir, les valeurs saisies par l'utilisateur ;
* En bleu, les valeurs calculées par le programme.

```python
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
```

### Méthode `Vider`

Pour terminer cet exercice, il nous reste à écrire la méthode qui permet d'effacer un résultat calculé. On va simplement tester la couleur d'une `Entry` pour savoir si elle est _Bleu_ et dans ce cas la vider.

```python
    def _vider(self):
        """Cette méthode vide les Entry bleu (ceux calculés précédemment),
            sans toucher aux saisies de l'utilisateur (noires)"""
        for y in range(9):
            for x in range(9):
                if self._entries[y][x]['fg'] == "blue" :
                    self._entries[y][x].delete(0, END)
                    self._entries[y][x]['fg'] = "black"
```

## Conclusion

J'espère que malgré la concision et la richesse de cette présentation, j'ai pu vous transmettre quelques notions et vous donner envie de recommencer ou même de vous lancer dans le développement de petites applications en Python.

Sachez que ce langage peut remplacer dans certains cas Excel ou d'autres produits similaires pour vous faciliter des taches quotidiennes et répétitives.

Marc

---

- Fin du _game_ !

---
