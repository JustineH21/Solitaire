import random
from Carte_et_PileInfos import *
from Pile_et_File import *

class Jeu:
    def __init__(self, pioche: list = None):
        self.cartes: list = [] # liste de toutes les cartes du jeu
        self.pioche: File = File(pioche)
        self.pioche_cartes_sorties: Pile = Pile()
        self.carte_cliquee = None # carte qui a été cliquée par le joueur, None si pas de carte cliquée ou déplacement terminé
        self.nb_cartes_pioche_sorties: int = 0 # nombre de cartes sorties de la pioche et visibles
        
        self.pile_jeu1: PileInfos = PileInfos(1, None, 10)
        self.pile_jeu2: PileInfos = PileInfos(2, None, 150)
        self.pile_jeu3: PileInfos = PileInfos(3, None, 290)
        self.pile_jeu4: PileInfos = PileInfos(4, None, 430)
        self.pile_jeu5: PileInfos = PileInfos(5, None, 570)
        self.pile_jeu6: PileInfos = PileInfos(6, None, 710)
        self.pile_jeu7: PileInfos = PileInfos(7, None, 850)
        self.liste_pile: list [PileInfos] = [self.pile_jeu1, self.pile_jeu2, self.pile_jeu3, self.pile_jeu4, self.pile_jeu5, self.pile_jeu6, self.pile_jeu7]

        self.pile_couleur_coeur: PileInfos = PileInfos(None, 'coeur', 600)
        self.pile_couleur_carreau: PileInfos = PileInfos(None, 'carreau', 750)
        self.pile_couleur_trefle: PileInfos = PileInfos(None, 'trefle', 900)
        self.pile_couleur_pique: PileInfos = PileInfos(None, 'pique', 1050)

    def initialiser_jeu(self) -> None:
        # création des cartes
        self.cartes = [Carte(couleur, valeur, False, None, 10, 10) for couleur in ['coeur', 'carreau', 'trefle', 'pique'] for valeur in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']]
        self.distribuer_cartes()

    def distribuer_cartes(self):
        random.shuffle(self.cartes)

        for i in range(7): # pour chaque pile de jeu
            for j in range(i, 7): 
                carte = self.cartes.pop(0) # premiere carte de la liste                
                carte.pile = self.liste_pile[j]

                if carte.pile.est_vide():
                    carte.deplacer_carte(self.liste_pile[j].x, 200 + 35 * i)
                else:
                    carte.deplacer_carte(carte.pile.x, 200 + 35 * i, carte.pile.sommet())

                self.liste_pile[j].empiler(carte) # on le fait après pour encore avoir accès à la carte juste avant

        self.devoiler_carte_dessus() # dévoile la carte du dessus de chaque pile de jeu
        self.pioche = File(self.cartes) # le reste des cartes constitue la pioche
        #print([self.pioche.f[i].valeur + " de " + self.pioche.f[i].couleur for i in range(self.pioche.taille())])

    def distribuer_cartes_pioche(self, file_cartes: File) -> None:
        """ Distribue les cartes qui lui sont données vers la défausse (pioche_cartes_sorties) """
        #print([file_cartes.f[i].valeur + " de " + file_cartes.f[i].couleur for i in range(file_cartes.taille())])
        x = 145
        for _ in range(min(3, file_cartes.taille())): # pour éviter qu'il y ait plus que 3 cartes 
            carte = file_cartes.defiler()
            carte.pile = self.pioche_cartes_sorties
            if not carte.visible:
                carte.changer_visibilite_image()
            if self.pioche_cartes_sorties.taille() > 0: # s'il y a encore des cartes dans la défausse
                carte.deplacer_carte(x, 10, carte_dessous=self.pioche_cartes_sorties.sommet())
            else:
                carte.deplacer_carte(x, 10)
            self.pioche_cartes_sorties.empiler(carte)
            x += 40
        #print([self.pioche_cartes_sorties.p[i].valeur + " de " + self.pioche_cartes_sorties.p[i].couleur for i in range(self.pioche_cartes_sorties.taille())])

    def determiner_carte_cliquee(self, event):
        x = event.x_root - fenetre.winfo_rootx()
        y = event.y_root - fenetre.winfo_rooty()
        carte_cliquee = None

        if 10 <= x <= 137 and 10 <= y <= 190: # coordonnées de la pioche
            if not self.pioche.est_vide():
                print("Pioche cliquée")
                self.piocher(nb_cartes_a_piocher = min(3, self.pioche.taille()))
            else:
                print("Pioche vide")
                self.renfiler_pioche()
        elif 225 <= x <= 355 and 10 <= y <= 190: # coordonnées des cartes de la défausse
            pile_intermediaire = Pile()
            for _ in range(min(3, self.pioche_cartes_sorties.taille())):
                pile_intermediaire.empiler(self.pioche_cartes_sorties.depiler())
                label = pile_intermediaire.sommet().label
                x0 = label.winfo_x()
                x1 = x0 + label.winfo_width()
                if x0 < x < x1:
                    carte_cliquee = pile_intermediaire.sommet()
                    break
            while not pile_intermediaire.est_vide():
                self.pioche_cartes_sorties.empiler(pile_intermediaire.depiler())
            self.carte_cliquee = carte_cliquee
            print("Carte cliquée :", self.carte_cliquee.couleur, self.carte_cliquee.valeur)
        else:
            pile_cliquee = None
            for pile in self.liste_pile:
                if not pile.est_vide():
                    sommet = pile.sommet()
                    label = sommet.label
                    x0 = label.winfo_x()
                    x1 = x0 + label.winfo_width()
                    if x0 < x < x1:
                        pile_cliquee = pile
                        break

            pile_intermediaire = Pile()
            for _ in range(pile_cliquee.taille()):
                carte = pile_cliquee.sommet()
                label = carte.label
                if pile_cliquee != self.pioche_cartes_sorties:
                    coor0 = label.winfo_y()
                    coor1 = coor0 + label.winfo_height()
                    coor_clic = y
                else:
                    coor0 = label.winfo_x()
                    coor1 = coor0 + label.winfo_height()
                    coor_clic = x

                if coor0 < coor_clic < coor1 and carte.visible:
                    carte_cliquee = carte
                    break
                else:
                    pile_intermediaire.empiler(pile_cliquee.depiler())

            for _ in range(pile_intermediaire.taille()):
                pile_cliquee.empiler(pile_intermediaire.depiler())

            self.carte_cliquee = carte_cliquee
            if self.carte_cliquee != None:
                print("Carte cliquée :", self.carte_cliquee.couleur, self.carte_cliquee.valeur)

        if carte_cliquee != None:
            self.bouger_carte()

    def verifier_validite_deplacement(self, carte_source: Carte, pile_cible: PileInfos) -> bool:
        if pile_cible.est_vide():
            if pile_cible.numero != None:
                if carte_source.valeur == '13':  # Roi
                    return True
                else:
                    return False
            # si pile de fondation (cœur, carreau, trèfle, pique)
            else:
                if carte_source.valeur == '1' and carte_source.couleur == pile_cible.couleur:  # As
                    return True
                else:
                    return False

        carte_cible = pile_cible.sommet()
        val_source = int(carte_source.valeur)
        val_cible = int(carte_cible.valeur)

        if pile_cible.couleur != None:
            # Même couleur et valeur +1
            if carte_source.couleur == carte_cible.couleur and val_source == val_cible + 1:
                return True
            else:
                return False
        else:
            # Couleurs différentes (rouge/noir)
            couleurs_rouges = ['coeur', 'carreau']
            source_rouge = carte_source.couleur in couleurs_rouges
            cible_rouge = carte_cible.couleur in couleurs_rouges

            if source_rouge != cible_rouge and val_source == val_cible - 1:
                return True
            else:
                return False

    def verifier_victoire(self) -> bool:

        # On rassemble les piles de fondation dans une liste
        piles_fondation = [
            self.pile_couleur_coeur,
            self.pile_couleur_carreau,
            self.pile_couleur_trefle,
            self.pile_couleur_pique
        ]
        victoire = True
        for pile in piles_fondation:
            if pile.taille() != 13:  
                victoire = False
                break  # victoire impossible

            if victoire:
                print(" YOU WINNER ")
            return True
        else:
            # Partie pas encore gagnée
            return False

    def devoiler_carte_dessus(self):
        for pile in self.liste_pile:
            if not pile.est_vide():         
                carte_sommet = pile.sommet()  
                if not carte_sommet.visible:  
                    carte_sommet.changer_visibilite_image() 

    def piocher(self, nb_cartes_a_piocher:int = 0) -> None:
        nb_cartes_a_decaler = min(3, self.pioche_cartes_sorties.taille())
        pile_intermediaire = Pile()
        for _ in range(nb_cartes_a_decaler):
            carte = self.pioche_cartes_sorties.depiler()
            carte.deplacer_carte(145, 10)
            pile_intermediaire.empiler(carte)
        for _ in range(pile_intermediaire.taille()):
            carte = pile_intermediaire.depiler()
            self.pioche_cartes_sorties.empiler(carte)

        nb_cartes_a_recuperer = 3 - nb_cartes_a_piocher
        pile_intermediaire = File()
        for _ in range(nb_cartes_a_recuperer): # on récupère les cartes sorties de la pioche pour les remettre dans la pioche
            carte = self.pioche_cartes_sorties.depiler()
            pile_intermediaire.enfiler(carte)
        for _ in range(nb_cartes_a_piocher): # on pioche les nouvelles cartes
            carte = self.pioche.defiler()
            pile_intermediaire.enfiler(carte)
        
        self.distribuer_cartes_pioche(pile_intermediaire)

        if self.pioche.est_vide():
            self.nb_cartes_pioche_sorties = min(3, self.pioche_cartes_sorties.taille())
        else:
            self.nb_cartes_pioche_sorties = 3

    def renfiler_pioche(self) -> None:
        if not self.pioche_cartes_sorties.est_vide():
            pile_intermediaire = Pile()
            for _ in range(self.pioche_cartes_sorties.taille()):
                carte = self.pioche_cartes_sorties.depiler()
                pile_intermediaire.empiler(carte)
            for _ in range(pile_intermediaire.taille()):
                carte = pile_intermediaire.depiler()
                self.pioche.enfiler(carte)
                carte.pile = self.pioche
                carte.changer_visibilite_image()
                carte.deplacer_carte(10, 10)

        #print([self.pioche.f[i].valeur + " de " + self.pioche.f[i].couleur for i in range(self.pioche.taille())])

    def bouger_carte_1(self) -> None:
        """ Déplace la carte cliquée vers une pile valide si possible"""
        if self.carte_cliquee is None:
            return  # aucune carte à déplacer

        # On parcourt toutes les piles de jeu pour trouver une pile valide
        for pile_cible in self.liste_pile + [
            self.pile_couleur_coeur,
            self.pile_couleur_carreau,
            self.pile_couleur_trefle,
            self.pile_couleur_pique
        ]:
            
            if (not pile_cible == self.carte_cliquee.pile) and self.verifier_validite_deplacement(self.carte_cliquee, pile_cible):
                pile_source = self.carte_cliquee.pile
                if pile_source == self.pioche_cartes_sorties:
                    self.nb_cartes_pioche_sorties -= 1
                carte_a_deplacer = pile_source.depiler()
                carte_a_deplacer.pile = pile_cible
                nouvelle_y = 200 + 35 * pile_cible.taille() if pile_cible.numero else 10
                if pile_cible.est_vide():
                        carte_a_deplacer.deplacer_carte(x=pile_cible.x, y=nouvelle_y)
                else:
                    carte_a_deplacer.deplacer_carte(x=pile_cible.x, y=nouvelle_y, carte_dessous=pile_cible.sommet())
                pile_cible.empiler(carte_a_deplacer)

                print(f"La carte {carte_a_deplacer.valeur} de {carte_a_deplacer.couleur} déplacée vers la pile {pile_cible.numero if pile_cible.numero else pile_cible.couleur}")
                self.carte_cliquee = None
                break  # une seule carte déplacée à la fois

        self.devoiler_carte_dessus()
        self.verifier_victoire()
        
    def bouger_carte (self) -> None:
        """ Déplace la carte cliquée et toutes les cartes en dessous vers une pile valide si possible"""

        if self.carte_cliquee is None:
            return
        
        pile_deplacement: Pile = Pile()
        pile_source: PileInfos = self.carte_cliquee.pile

        while pile_source.sommet() != self.carte_cliquee: #tant qu'on retrouve pas la carte
            pile_deplacement.empiler(pile_source.depiler())

        pile_deplacement.empiler(pile_source.depiler())

        for pile_cible in self.liste_pile + [self.pile_couleur_coeur, self.pile_couleur_carreau, self.pile_couleur_trefle, self.pile_couleur_pique]:
            
            if not(pile_cible == pile_source) and self.verifier_validite_deplacement(self.carte_cliquee, pile_cible):                
                while pile_deplacement.taille() > 0:
                    carte = pile_deplacement.depiler()
                    carte.pile = pile_cible
                    nouvelle_y = 200 + 35 * pile_cible.taille() if pile_cible.numero else 10
                    if pile_cible.est_vide():
                        carte.deplacer_carte(x=pile_cible.x, y=nouvelle_y)
                    else:
                        carte.deplacer_carte(x=pile_cible.x, y=nouvelle_y, carte_dessous=pile_cible.sommet())
                    pile_cible.empiler(carte) 
                    print(f"La carte {carte.valeur} de {carte.couleur} déplacée vers la pile {pile_cible.numero if pile_cible.numero else pile_cible.couleur}")

                if pile_source == self.pioche_cartes_sorties:
                    if self.pioche_cartes_sorties.taille() > 3:
                        self.piocher(nb_cartes_a_piocher = 0) # pour réajuster l'affichage des cartes sorties de la pioche
                        self.nb_cartes_pioche_sorties = 3
                    else:
                        self.nb_cartes_pioche_sorties -= pile_deplacement.taille()
                
                self.carte_cliquee = None
                self.devoiler_carte_dessus()
                self.verifier_victoire()
                return # déplacement réussi

        #si on ne peut pas déplacer les cartes, on les remet dans leur pile d'origine

        while pile_deplacement.taille() > 0:
            carte = pile_deplacement.depiler()
            pile_source.empiler(carte)
            self.carte_cliquee = None