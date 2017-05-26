def appel_herbi():
    int_herbi = int(input("nombre d'herbivores ?\n"))
    return int_herbi


def appel_carni():
    int_carni = int(input("nombre de carnivores ?\n"))
    return int_carni


def appel_charo():
    int_charo = int(input("nombre de charognard ?\n"))
    return int_charo


def longueur():
    longueur = int(input("dimension de l'environnement , doit etre inférieure ou égale à 100\n"))
    if longueur > 100:
        raise IndexError(" Doit être inférieur  à 100 !!!!!")
    return longueur


def res():
    res = int(input(
        "Entrez la resolution , celle ci joue sur la répartion des herbes ,lacs et forets. (une trop grande résolution peut rendre l'environnement trop aléatoire, résolution conseillé :3)\n"))

    return res

def riviere ():
    riviere =  int(input("nombre de rivières s'écoulant sur l'environnement  , ne joue pas  sur le nombre de lacs.\n"))
    return riviere
def nb_tour ():
    nb_tour = int(input("nombre de tours\n"))
    return nb_tour