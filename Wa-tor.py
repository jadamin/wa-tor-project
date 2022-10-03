from mimetypes import init
from random import randint, choice, random
from re import X
from time import sleep
import os

class Monde:
    def __init__(self, largeur, hauteur):
        """
        Fonction qui créer le monde
        """
        self.largeur = largeur
        self.hauteur = hauteur 
        self.grille = [[ None for _ in range(largeur)] for _ in range(hauteur)]
    
    def afficher_monde(self):
        """
        Fonction qui affiche la grille
        param grille: dictionnaire qui représente le monde
        """
        for ligne in self.grille:
            for case in ligne:
                if isinstance ( case , Poisson):
                    print ( " 🐠 " , end=" | ")
                elif isinstance ( case , Requin):
                    print ( " 🦈 " , end=" | ")
                else:
                    print ( " __ ", end= " | ")
            print ( "\n" )
            
    def peupler(self, nb_poisson, nb_requin):
        
        """
        Fonction qui insert des poissons et des requins aléatoirement
        param nb_poisson: nombre de poisson à faire apparaitre
        param nb_requin : nombre de requin à faire
        """
        
         # Vérifie si une case est vide pour y mettre des poissons
        for i in range (nb_poisson):
            x_rand = randint( 0, self.largeur-1 )
            y_rand = randint ( 0 , self.hauteur-1 )
            if self.grille [y_rand] [x_rand] == None :
                self.grille [y_rand] [x_rand] = Poisson (x_rand , y_rand)
        # Vérifie si une case est vide pour y mettre des requins
        for i in range (nb_requin):
            x_rand = randint( 0, self.largeur-1 )
            y_rand = randint ( 0 , self.hauteur-1 )
            if self.grille [y_rand] [x_rand] == None :
                self.grille [y_rand] [x_rand] = Requin (x_rand , y_rand)
       

    def jouer_un_tour(self):
        for ligne in self.grille :
            for case in ligne :
                if isinstance (case , Poisson):
                    case.vivre_une_journee(self)
                elif isinstance (case, Requin) :
                    case.vivre_une_journee(self)


                

class Poisson:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.compteur_reproduction = 0

    
    def deplacement_possible(self, monde):
        """
        Foction qui définie les mouvement possible pour le poisson
        param monde : renvoie à l'emplacement des éléments monde
        param return : renvoie les coups possible
        """

        coup_possible = []
        
        if monde.grille [(self.y -1) % monde.hauteur][self.x] == None :
            coup_possible.append((self.x, (self.y-1)% monde.hauteur))
        if monde.grille [(self.y +1) % monde.hauteur][self.x] == None :
            coup_possible.append((self.x, (self.y+1)% monde.hauteur))
        if monde.grille [self.y][(self.x -1) % monde.largeur] == None :
            coup_possible.append((((self.x-1)% monde.largeur), self.y))
        if monde.grille [self.y][(self.x +1) % monde.largeur] == None :
            coup_possible.append((((self.x+1)% monde.largeur), self.y))
        return coup_possible

    def se_deplacer(self, monde):
        """
        Fonction qui fait se déplacer un poisson
        param monde : renvoie à l'emplacement des éléments monde
        """

        coup_possible = self.deplacement_possible (monde)

        if len(coup_possible) != 0 :
            
            coup_a_jouer = choice (coup_possible)
            x_coup = coup_a_jouer [0]
            y_coup = coup_a_jouer [1]
            x_preced = self.x
            y_preced = self.y
            self.x = x_coup
            self.y = y_coup
            monde.grille[y_coup][x_coup] = self
            if self.compteur_reproduction >= 5:
                monde.grille[y_preced][x_preced] = Poisson(x_preced, y_preced)
                self.compteur_reproduction = 0
            else:
                monde.grille[y_preced][x_preced] = None

    def vivre_une_journee(self, monde):
        """
        Fonction qui permet au thon de vivre
        param monde : renvoie à l'emplacement des éléments monde
        """

        self.compteur_reproduction +=1
        self.se_deplacer(monde)


class Requin:
    def __init__(self , x , y) -> None:
        self.x = x
        self.y = y
        self.compteur_reproduction = 0
        self.energie = 6

    def deplacement_possible (self , monde):
        """
        Foction qui définie les mouvement possible pour le requin
        param monde : renvoie à l'emplacement des éléments monde
        param returne : renvoie les coups possible
        """
        coup_possible = []
       
        if monde.grille [(self.y -1) % monde.hauteur][self.x] == None :
            coup_possible.append((self.x, (self.y-1)% monde.hauteur))
        if monde.grille [(self.y +1) % monde.hauteur][self.x] == None :
            coup_possible.append((self.x, (self.y+1)% monde.hauteur))
        if monde.grille [self.y][(self.x -1) % monde.largeur] == None :
            coup_possible.append((((self.x-1)% monde.largeur), self.y))
        if monde.grille [self.y][(self.x +1) % monde.largeur] == None :
            coup_possible.append((((self.x+1)% monde.largeur), self.y))
        return coup_possible

    def se_deplacer (self , monde):
        """
        Fonction qui fait se déplacer un requin
        param monde : renvoie à l'emplacement des éléments monde
        """
        coup_possible = self.deplacement_possible (monde)

        if len(coup_possible) != 0 :
            coup_a_jouer = choice (coup_possible)
            x_coup = coup_a_jouer [0]
            y_coup = coup_a_jouer [1]
            x_preced = self.x
            y_preced = self.y
            self.x = x_coup
            self.y = y_coup
            monde.grille[y_coup][x_coup] = self
            if self.compteur_reproduction >= 10:
                monde.grille[y_preced][x_preced] = Requin (x_preced, y_preced)
                self.compteur_reproduction = 0
            else:
                monde.grille[y_preced][x_preced] = None


    def trouver_poisson (self, monde):
        """
        Fonction qui permet au requin de trouver un poisson
        param monde : renvoie à l'emplacement des éléments monde
        param return : renvoi si un poisson est à proximité
        """
        poisson_disponible = []
        if isinstance (monde.grille [(self.y -1) % monde.hauteur][self.x], Poisson) :
            poisson_disponible.append((self.x, (self.y-1)% monde.hauteur))
        if isinstance (monde.grille [(self.y +1) % monde.hauteur][self.x], Poisson) :
            poisson_disponible.append((self.x, (self.y+1)% monde.hauteur))
        if isinstance (monde.grille [self.y][(self.x -1) % monde.largeur], Poisson) :
            poisson_disponible.append((((self.x-1)% monde.largeur), self.y))
        if isinstance (monde.grille [self.y][(self.x +1) % monde.largeur], Poisson) :
            poisson_disponible.append((((self.x+1)% monde.largeur), self.y))
        return poisson_disponible


    def manger_poisson (self , monde):
        """
        fonction qui permet au requin de manger un poisson
        param monde : renvoie à l'emplacement des éléments monde
        """
        manger_possible = self.trouver_poisson (monde)

        if len(manger_possible) != 0 :
            coup_a_jouer = choice (manger_possible)
            x_coup = coup_a_jouer [0]
            y_coup = coup_a_jouer [1]
            x_preced = self.x
            y_preced = self.y
            self.x = x_coup
            self.y = y_coup
            monde.grille[y_coup][x_coup] = self
            if isinstance(monde.grille[y_coup][x_coup],Poisson) :
                if self.compteur_reproduction >= 10 and self.energie != 0:
                    monde.grille[y_preced][x_preced] = Requin (x_preced, y_preced)
                    self.compteur_reproduction = 0
                else:
                    monde.grille[y_preced][x_preced] = None
                self.energie += 5
            elif self.compteur_reproduction >= 10:
                monde.grille[y_preced][x_preced] = Requin (x_preced, y_preced)
                self.compteur_reproduction = 0
            else:
                monde.grille[y_preced][x_preced] = None
    
    def vivre_une_journee (self , monde):
        """
        Fonction qui permet au thon de vivre
        param monde : renvoie à l'emplacement des éléments monde
        """
        self.energie -= 1
        if len(self.trouver_poisson(monde)) != 0:
            self.manger_poisson(monde)
        self.se_deplacer(monde)
        if self.energie == 0:
            monde.grille[self.y][self.x] = None
        elif self.energie >= 10 :
            self.energie = 10
        self.compteur_reproduction += 1
        print(self.compteur_reproduction)



monde = Monde (5 , 3)
monde.peupler (10, 1)

while True:
    monde.jouer_un_tour()
    monde.afficher_monde()
    sleep(0.5)
    os.system("clear")
