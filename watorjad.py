import time
from random import randrange


H = 20   
V = 20  
G_REQUIN = 4  
E_REQUIN = 2  
G_THON = 2      
P_THON = 0.30 
P_REQUIN = 0.10 
PAS_AFFICHAGE = 20
PAS_TOTAL = H*V*PAS_AFFICHAGE   


def creer_grille(case_h, case_v):
    return [[(0, 0, 0) for _ in range(case_h)] for _ in range(case_v)]


def selection_case(case_h, case_v):
    return (randrange(case_h), randrange(case_v))


def init_case(nature):
    if nature == 0:
        tup = (nature, 0, 0)
    elif nature == 1:
        tup = (nature, G_THON, 0)
    elif nature == 2:
        tup = (nature, G_REQUIN, E_REQUIN)
    return tup

def placement_espece(grille, nature, nb_poissons):
    while nb_poissons > 0:
        case = selection_case(len(grille[0]), len(grille))
        if grille[case[1]][case[0]][0] not in (1, 2):
            grille[case[1]][case[0]] = init_case(nature)
            nb_poissons -= 1
    return grille


def denombre_espece(grille, espece):
    nbre_espece = 0
    for ligne in grille:
        for case in ligne:
            if case[0] == espece:
                nbre_espece += 1
    return nbre_espece


def init_grille(p_thon, p_requin, case_h, case_v):
    grille = creer_grille(case_h, case_v)
    n_thon = p_thon*case_h*case_v  
    grille = placement_espece(grille, 1, n_thon)
    n_requin = p_requin*case_h*case_v  
    grille = placement_espece(grille, 2, n_requin)
    return grille


def afficher_grille(grille):
    affichage = ""
    for ligne in grille:
        for case in ligne:
            if case[0] == 0:
                affichage += "_"+" "
            elif case[0] == 1:
                affichage += "🐟"+" "
            elif case[0] == 2:
                affichage += "🦈"+" "
        affichage += "\n"
    print(affichage)


def afficher_grille2(grille, pas_simul, nb_thons, nb_requins):
    affichage = f'pas de simulation : {pas_simul}/{PAS_TOTAL} \n \
Nombre de thons :{nb_thons} Nombre de requins: {nb_requins}  \n\n'
    for ligne in grille:
        for case in ligne:
            if case[0] == 0:
                affichage += "_"+" "
            elif case[0] == 1:
                affichage += "🐟"+" "
            elif case[0] == 2:
                affichage += "🦈"+" "
        affichage += "\n"
    print(affichage)


def cases_voisines(case, case_h, case_v):
    x = case[0]
    y = case[1]
    coordos_voisins = [(x, y-1), (x-1, y), ((x+1) % case_h, y), (x, (y+1) % case_v)]
    return coordos_voisins


def evol_gestation(case, grille):
    return grille[case[1]][case[0]][1]-1  


def evol_energie(case, grille):
    return grille[case[1]][case[0]][2]-1  


def deplace_vers_mer(nature, case, case_mer, grille, gestation, energie=0):
    if gestation == 0:  
        if nature == 1:
            grille[case_mer[1]][case_mer[0]] = init_case(nature)
        elif nature == 2:
            grille[case_mer[1]][case_mer[0]] = (2, G_REQUIN, energie)
        grille[case[1]][case[0]] = init_case(nature)  
    else:
        grille[case_mer[1]][case_mer[0]] = (nature, gestation, energie)
        grille[case[1]][case[0]] = init_case(0)  
    return grille


def tour_thon(case, liste, grille):
    gestation = evol_gestation(case, grille)
    case_mer = recherche_case(liste, grille, 0)
    if case_mer:
        grille = deplace_vers_mer(1, case, case_mer, grille, gestation)
    else: 
        if gestation == 0: 
            grille[case[1]][case[0]] = init_case(1)  
        else:
            grille[case[1]][case[0]] = (1, gestation, 0)
    return grille


def recherche_case(liste, grille, nature):
 
    liste_voisins = list(liste)
    n_voisins_test = 4
    while n_voisins_test > 0:
        choix = randrange(n_voisins_test)
        case_voisine_testee = liste_voisins[choix]  
        if grille[case_voisine_testee[1]][case_voisine_testee[0]][0] == nature:
            return case_voisine_testee
        else:
            del liste_voisins[choix]
            n_voisins_test -= 1
    return False


def chasse_au_thon(case, case_thon, grille, gestation):
    
    if gestation == 0:  
        grille[case[1]][case[0]] = init_case(2) 
        grille[case_thon[1]][case_thon[0]] = init_case(2)
       
    else:
        grille[case_thon[1]][case_thon[0]] = (2, gestation, E_REQUIN)
        grille[case[1]][case[0]] = init_case(0)  
    return grille




def tour_requin(case, liste, grille):
    gestation = evol_gestation(case, grille)  
    energie = evol_energie(case, grille)
    case_thon = recherche_case(liste, grille, 1) 
    if case_thon:
        grille = chasse_au_thon(case, case_thon, grille, gestation)
    else: 
        case_mer = recherche_case(liste, grille, 0)
        if case_mer:  
            if energie == 0:  
                grille[case_mer[1]][case_mer[0]] = init_case(0) 
                grille[case[1]][case[0]] = init_case(0) 
            else:  
                grille = deplace_vers_mer(2, case, case_mer, grille, gestation, energie)
        else:  
            if energie == 0:  
                grille[case[1]][case[0]] = init_case(0) 
            else:
                if gestation == 0: 
                    grille[case[1]][case[0]] = (2, G_REQUIN, energie)
                else:
                    grille[case[1]][case[0]] = (2, gestation, energie)
    return grille


def evol_population(grille):
    case_h = len(grille[0])  
    case_v = len(grille)  
    case_choisie = selection_case(case_h, case_v)
    if grille[case_choisie[1]][case_choisie[0]][0] == 1:
        grille = tour_thon(case_choisie, cases_voisines(case_choisie, case_h, case_v), grille)
    elif grille[case_choisie[1]][case_choisie[0]][0] == 2:
        grille = tour_requin(case_choisie, cases_voisines(case_choisie, case_h, case_v), grille)
    return grille


def simulation(grille, p_affichage, n_pas_total):
    liste_thons = [] 
    liste_requins = []  
    for i in range(n_pas_total//p_affichage):
        for _ in range(p_affichage):
            evol_population(grille)
            nb_thons = denombre_espece(grille, 1)
            nb_requins = denombre_espece(grille, 2)
            liste_thons.append(nb_thons)
            liste_requins.append(nb_requins)
        afficher_grille2(grille, (i+1)*p_affichage, nb_thons, nb_requins)
        time.sleep(0.05)
    (liste_thons, liste_requins, n_pas_total)



def demarrage():
    grille = init_grille(P_THON, P_REQUIN, H, V)  
    simulation(grille, PAS_AFFICHAGE, PAS_TOTAL)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=False)
    demarrage()

