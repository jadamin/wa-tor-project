from random import randint, choice
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
        for i in range

monde = Monde (8 , 10)
monde.afficher_monde ()