from random import randint, choice, random
from re import X
from time import sleep
import os

class Monde:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur 
        self.grille = [[ None for _ in range(largeur)] for _ in range(hauteur)]
    
    def afficher_monde(self):
        
        for ligne in self.grille:
            print(ligne)

    def peupler(self, nb_poisson, nb_requin):
        for i in range (nb_poisson):
            x_rand = randint( 0, self.largeur-1 )
            y_rand = randint ( 0 , self.hauteur-1 )
            if self.grille [y_rand] [x_rand] == None :
                self.grille [y_rand] [x_rand] = Poisson (x_rand , y_rand)
        for i in range (nb_requin):
            x_rand = randint( 0, self.largeur-1 )
            y_rand = randint ( 0 , self.hauteur-1 )
            if self.grille [y_rand] [x_rand] == None :
                self.grille [y_rand] [x_rand] = Requin (x_rand , y_rand)
       

    def jouer_un_tour(self):
        pass

class Poisson:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.compteur_reproduction = 0

    
    def deplacement_possible(self, monde):
        pass
    
    def se_deplacer(self, monde):
        pass
        
    def vivre_une_journee(self, monde):
        pass

    def se_reproduire () :
        pass

class Requin:
    def __init__(self , x , y) -> None:
        self.x = x
        self.y = y
        self.compteur_reproduction = 0
        self.energie = 6

    def deplacement_possible (self , monde):
        pass

    def se_deplacer (self , monde):
        pass

    def vivre_une_journee (self , monde):
        pass

    def se_reproduire ():
        pass       

    def manger_poisson ():
        pass
        



monde = Monde (8 , 10)
monde.peupler (2 , 3)
monde.afficher_monde ()
