# Jour 3 : Interface graphique - TKinter

---

- Retour au [Sommaire](index.md)
- Jour 2 : [Premier objet - Tout est dans la matrice](jour%202.md)

---

## TKinter

TKinter est une librairie qui permet de générer des fenêtres graphiques ainsi que tous les éléments (_widgets_) qui s'y trouvent.

Elle va nous permettre de faire une représentation plus jolie que la sortie texte de notre jeu du Sudoku, ainsi qu'une interface de saisie plus agréable à utiliser que des tableaux dans le code.

Voyez la page de cette librairie sur le site Python : [https://docs.python.org/fr/3/library/tkinter.html](https://docs.python.org/fr/3/library/tkinter.html). Il existe aussi plein de site présentant des cours pour utiliser TkInter.

### La classe (encore)

Cette fois on va définir une classe Application qui va hériter de la classe Tk. Elle va donc _récupérer_ toutes les méthodes et attributs de la classe mère. En particulier, après avoir initilisé notre application, il faut lancer la méthode `mainloop()` qui permet le fonctionnement des éléments de la fenètre.

```python3
#!/usr/bin/python
# -*- coding: <encoding name> -*-

"""Exercice 4a"""

from tkinter import Tk

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

### Constructeur

Comme d'habitude maintenant le constructeur va initialiser tous les éléments de notre application, c'est à dire ici dessiner la fenètre avec tous les objets de rendu qui s'y trouvent (les _widgets_).

Cette fois on va aussi devoir appeler le constructeur hérité dans notre propre constructeur, avant de définir les attributs de la la fenètre et de la remplir avec des _widgets_.

```python3
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

Et voilà ! Mais expliquons quand même l'utilisation de quelques _widgets_.

Tout d'abord chaque _widget_ doit faire référence à un élément de niveau supérieur qui le contient puisque celui-ci aura la responsabilitée de l'afficher quand certains paramètres changes (largeur de la fenètre, _etc._). C'est ce que l'on retrouve dans chaque instanciation d'un _widget_.

#### Attributs

Déjà on peut modifier ou définir des attributs de la fenètre en appelant directement _self_ puisqu'on hérite de Tk, la fenètre principale.

On ajoute donc un titre et une icone à notre fenètre.

#### Label

Il s'agit là d'un libellé fixe qui permet d'afficher n'importe quel texte. On lui applique sa méthode _pack()_ qui l'injecte dans la fenètre.

#### Entry

Cette fois, il nous faut définir la matrice graphique de 9 par 9 avec des sous-groupe de 3 par 3. L'ensemble est formé d'_Entry_ qui permettent des saisies et de _Frame_ qui les contiennent 3 par 3, l'ensemble étant placé dans une _Frame_ unique.

Par contre, il nous faudra garder des références sur ces _Entry_ afin de pouvoir lire leur contenu ultérieurement ; c'est ce qui est fait avec le tableau `self._entries`.

#### Button

Pour terminer, on ajoute une dernière _Frame_ qui contient elle-même deux _Buttons_ qui vont permettre de déclencer des actions.

#### Les _callback_

Les _callback_ sont des méthodes qui sont définies par l'utilisateur mais appelées automatiquement par l'environnement (le _framework_ Tkinter) lorsque des évènements surviennent.

Dans notre cas, c'est utilisé par les _Button_ afin qu'ils indiquent à notre instance que l'un d'eux a été cliqué.

On devra donc ajouter une option supplémentaire à chacun de nos boutons, ainsi que les méthodes associées :

```python3
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











---

- Fin du _game_ !

---








