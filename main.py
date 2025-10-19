import random
from Pile_et_File import *
from Carte_et_PileInfos import *
from Jeu import *

# vérifier fonctionnement de la pioche
"""jeu = Jeu([3, 1, 5, 8, 9, 14, 23, 12])
for i in range(5):
    jeu.piocher()
    print(jeu.pioche_cartes_sorties.p)"""

# vérifier fonctionnement de l'affichage des cartes
jeu = Jeu()

if __name__ == "__main__":
    
    jeu.initialiser_jeu()
    """pioche1 = [jeu.pioche.f[i].valeur + " de " + jeu.pioche.f[i].couleur for i in range(jeu.pioche.taille())]
    for _ in range(8):
        jeu.piocher(3)
    jeu.renfiler_pioche()
    pioche2 = [jeu.pioche.f[i].valeur + " de " + jeu.pioche.f[i].couleur for i in range(jeu.pioche.taille())]
    print(pioche1)
    print(pioche2)
    assert pioche1 == pioche2"""
    fenetre.bind("<Button-1>", lambda event: jeu.determiner_carte_cliquee(event))
    fenetre.mainloop()
    #print (jeu.pile_couleur_carreau.p)
