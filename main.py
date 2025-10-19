from Pile_et_File import *
from Jeu import *

jeu = Jeu()

if __name__ == "__main__":
    jeu.initialiser_jeu()
    fenetre.bind("<Button-1>", lambda event: jeu.determiner_carte_cliquee(event))
    fenetre.mainloop()