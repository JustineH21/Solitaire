import tkinter as tk
from tkinter import PhotoImage
from Pile_et_File import Pile, File

fenetre = tk.Tk()
fenetre.geometry("1000x750")
fenetre.configure(bg="bisque3")
canvas_jeu = tk.Canvas(fenetre, width=1200, height=1000, bg="bisque3")
canvas_jeu.pack()
fenetre.title("Solitaire")
fenetre.attributes('-topmost', 1)

class Carte:
    """ Représente une carte du jeu de Solitaire"""
    def __init__(self, couleur:str, valeur:int, visible: bool, pile: Pile, x:int = None, y:int = None) -> None:
        self.couleur: str = couleur
        self.valeur: int = valeur
        self.visible: bool = visible # True si la carte est face visible, False si la carte est face cachée
        self.pile: Pile = pile # Pile à laquelle la carte appartient
        self.label = tk.Label(canvas_jeu, borderwidth=0)
        self.x = x
        self.y = y
        self.afficher_carte() # affiche la carte à sa création

    def donner_couleur_et_valeur(self) -> tuple:
        """ 
        Retourne la couleur et la valeur de la carte sous forme de tuple (couleur, valeur) 
        donner_couleur_et_valeur()
        >>> ('coeur', 5)
        >>> ('pique', 12)
        """
        return (self.couleur, self.valeur)
    
    def afficher_carte(self) -> None:
        """ Affiche la carte sur la fenêtre """
        if self.visible == True:
            self.img = PhotoImage(file="cartes/"+self.valeur+"_"+self.couleur+".gif")
        else:
            self.img = PhotoImage(file="cartes/face_cachee.png")
        self.label.configure(image=self.img)
        if self.x != None and self.y != None:
            self.label.place(x=self.x, y=self.y)
        else:
            self.label.place(x=0, y=0)
    
    def deplacer_carte(self, x: int = None, y: int = None, carte_dessous = None) -> None:
        """ Change la position de la carte sur la fenêtre (interface graphique)"""
        if x == None and y == None:
            return
        elif x == None:
            self.label.place_configure(y=y)
            self.label.y = y
            self.y = y
        elif y == None:
            self.label.place_configure(x=x)
            self.label.x = x
            self.x = x
        else:
            self.label.place_configure(x=x, y=y)
            self.label.x = x
            self.label.y = y
            self.x = x
            self.y = y

        if carte_dessous != None:
            self.label.lift(carte_dessous.label) # permet de superposer les cartes correctement

    def changer_visibilite_image(self) -> None:
        """ Change l'image de la carte en fonction de sa visibilité """
        if self.visible == True:
            self.img = PhotoImage(file="cartes/face_cachee.png")
            self.visible = False
        else:
            self.img = PhotoImage(file="cartes/"+self.valeur+"_"+self.couleur+".gif")
            self.visible = True
        self.label.configure(image=self.img)

class PileInfos(Pile):
    """ Permet de stocker des informations sur une Pile de cartes : 
    - le numéro de la Pile si c'est une Pile du plateau de jeu, None sinon
    - la couleur si c'est une Pile de fondation, None sinon
    - la position x de la Pile sur la fenêtre
    """
    def __init__(self, numero: int, couleur:str, x: int) -> None:
        super().__init__()
        self.numero: int = numero 
        self.couleur: str = couleur
        self.x: int = x