from BDD import requete as req
from Environnement import environnement as envt
from interface import interface_utilisateur as iu
from interface import test_utilitaire as image
from interface.Thegif import in_gif_we_trust


def simulation():
    """
    Demande à l'utilisateur les conditions de la simulations , génère l'environnment  , enregistre les images après chaque tour d'interaction effectués ainsi que la base de données.
    :return:  une base de donnée du dernier effectué (si le programme est en pause du tour précèdent), une image de l'environnement a chaque tour, une phrase donnat le nombre d'animaux sur l'environment , un gif  récapitulatif.
    """
    int_herbi= iu.appel_herbi()
    int_carni= iu.appel_carni()
    int_charo= iu.appel_charo()
    taille=iu.longueur()
    riviere= iu.riviere()
    resolution=iu.res()
    nb_tour= iu.nb_tour()

    evt= envt.Environnement(resolution,taille,riviere,int_herbi,int_carni,int_charo)

    grid = evt.matrice_filtre
    evt.conversion(grid)
    evt.creer_animaux()
    image.main(evt,0)
    for  i in  range (0,nb_tour+1):
        evt.tour_brut()
        req.sauvegarde_tour_BDD(evt.grille)
        image.main(evt,i)
        for ligne in range (0, len(evt.grille)):
            for colonne in range (0, len(evt.grille[0])):
                for animal in evt.grille[ligne][colonne].liste_occupants:
                    animal._a_jouer=False
        print(evt.compte_espece())
    in_gif_we_trust(nb_tour)











