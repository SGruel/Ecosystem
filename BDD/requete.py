import sqlite3
import Environnement.terrain as ter

def sauvegarde_tour_BDD(matrice):
    '''
    Fonction qui crée et actualise à chaque tour la Base de Données. Celle ci est appelée Environnement et possède 8 colonnes;
    position de la case étudiée en X dans la matrice,
    position de la case étudiée en Y dans la matrice,
    type de terrain dans la dite case,
    valeur nutritive associée à la case; par défaut 0 pour les cases qui ne sont pas de type 'Herbe',
    l'HP de l'animal étudié dans la liste d'occupants de la case,
    la valeur nutritive du dit étudié,
    son champ de vision (et donc de déplacement)
    sa catégorie (herbivore, carnivore, charognard ou cadavre)
    :param 
    matrice: l'attribut grille de l'objet environnement
    type: matrice d'objets terrain
    :return:
    bdd: base de donnée de l'environnement mise à jour 
    '''
    try:
        conn = sqlite3.connect('Resultats/donnees_tour.db')
        curs = conn.cursor()
        curs.execute('''DROP TABLE IF EXISTS Environnement''')
        curs.execute('''CREATE TABLE Environnement (positionX, positionY, type, valeur_nutritive_terrain, hp, valeur_nutritive_animal, champ_vision, cat)''')
        for ligne in range (0,len(matrice)):
            for colonne in range (0,len(matrice[0])):
                case = matrice[ligne][colonne]
    #            if len(matrice[ligne][colonne].liste_occupants) == 0:
                for animal in case.liste_occupants:
                    if type(case) == ter.Herbe:
                        liste=(ligne, colonne, 'Herbe', case.valeur_nutritive, animal.hp, animal.valeur_nutritive, animal.champ_vision, animal.cat)
                        curs.execute("""INSERT INTO Environnement(positionX, positionY, type, valeur_nutritive_terrain, hp, valeur_nutritive_animal, champ_vision, cat) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",liste)
                    if type(case) == ter.Riviere:
                        liste=(ligne, colonne, 'Riviere', 0, animal.hp, animal.valeur_nutritive, animal.champ_vision, animal.cat)
                        curs.execute("""INSERT INTO Environnement(positionX, positionY, type, valeur_nutritive_terrain, hp, valeur_nutritive_animal, champ_vision, cat) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",liste)
                    if type(case) == ter.Foret:
                        liste=(ligne, colonne, 'Foret', 0, animal.hp, animal.valeur_nutritive, animal.champ_vision, animal.cat)
                        curs.execute("""INSERT INTO Environnement(positionX, positionY, type, valeur_nutritive_terrain, hp, valeur_nutritive_animal, champ_vision, cat) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",liste)
        conn.commit()
        curs.close()
        conn.close()
    except OverflowError :
        print("Trop d'espece à enregister , pas de base de donnée disponible :c")
        pass
