# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import random
import numpy as np

import Environnement.terrain as ter
import espece.espece as esp


class Environnement(object):
    def __init__(self, res, longueur, int_riviere, int_herbivore, int_carnivore, int_charognard):
        self.res = res
        self._longueur = longueur
        self._int_riviere = int_riviere
        self.grille = np.zeros((longueur, longueur))
        self.int_herbivore = int_herbivore
        self.int_carnivore = int_carnivore
        self.int_charognard = int_charognard

    @property
    def longueur(self):
        return self._longueur

    @property
    def int_riviere(self):
        return self._int_riviere

    '''ici se déroule dans un premier temps la création de l'environnement
        on utilise dans un premier remps un filtre de Perlin, ce filtre consiste en la dotation d'une valeur pour chaque point du terrain,
        de manière aléatoire mais cohérente, que l'on stocke dans une matrice
        puis, on applique un algorithme watershade pour la création des rivières
        enfin on transforme la matrice de valeurs trouvées en matrice composée de cases terrain
        on crée les animaux
        '''

    def creer_pts_aleatoires(self, res):
        '''
        fonction créant res+1*res+1 points aleatoires sous forme de matrice
        :param 
        res: représente une échelle arbitraire de cohérence; plus res est élevé, plus la répartition de l'herbe, foret et eau sera aléatoire,
        moins res est grand, plus le terrain est cohérent
        type: entier
        :return: 
        V: matrice de points aléatoires. Elle correspondra au canevas initial à partir duquel on vient créer le reste du terrain de manière cohérente
        type: matrice d'entiers
        '''
        L = []
        V = []
        for i in range(0, res + 1):
            for j in range(0, res + 1):
                L += [random.random()]
            V += [L]
            L = []
        return V

    def fct_interpolation(self, x, a, b):
        '''
        fonction cosinusoidale permettant l'interpolation d'un point entre ses deux plus proches voisins dans la matrice créée par
        la fonction précédente
        :param x: distance entre le point dont on cherche la valeur et son plus proche voisin de droite
        type: float (partie décimale)
        :param a: valeur du plus proche voisin de droite
        type: float
        :param b: valeur du plus proche voisin de gauche
        type: float
        :return: 
        couleur_point: valeur du point que l'on cherche
        type: float
        '''
        c = (1 - np.cos(x * np.pi)) / 2
        return ((1 - c) * a + c * b)

    def placement_X(self, x, y, V):
        '''
        fonction permettant de trouver la valeur de tout point de la matrice
        :param x: position en x du point 
        type: float
        :param y: position en y du point
        type: float
        :param V: matrice des points aléatoires trouvée précédemment
        type: matrice de flottants
        :return: 
        valeur_point: valeur du point cherchée déterminée par interpolation entre 4 points
        type: float
        '''
        x0 = int(x)
        y0 = int(y)
        if x0 - x != 0 or y0 - y != 0:
            valeur_ref0 = V[x0][y0]
            valeur_ref1 = V[x0 + 1][y0]
            valeur_ref2 = V[x0][y0 + 1]
            valeur_ref3 = V[x0 + 1][y0 + 1]
            interA = self.fct_interpolation(x0 - x, valeur_ref0, valeur_ref1)
            interB = self.fct_interpolation(x0 - x, valeur_ref2, valeur_ref3)
            valeur_point = self.fct_interpolation(y0 - y, interA, interB)
        else:
            valeur_point = V[x0][y0]
        return valeur_point

    def iteration(self, matrice, res):
        '''
        fonction permettant de trouver la valeur de tous les points du terrain et création de la matrice correspondante
        :param matrice: self.grille initial (matrice de zéros qui n'est ici que pour connaître la longueur du terrain)
        :param res: valeur de cohérence (permet la création du canevas de points aléatoires nécessaires à l'interpolation
        type: float
        :return: 
        matrice: matrice de Perlin, matrice de valeurs modélisant le terrain
        type: matrice de float
        '''
        V = self.creer_pts_aleatoires(res)
        for i in range(0, len(matrice)):
            for j in range(0, len(matrice[0])):
                matrice[i][j] = self.placement_X(i * res / len(matrice), j * res / len(matrice[0]), V)
        return matrice

    def riviere(self, matrice):
        '''
        algorithme de création des rivières (inspiré de l'algorithme watershade)
        :param matrice: matrice créée par la fonction précédente
        type: matrice de flottants
        :return: matrice: matrice terrain avec les rivières
        type: matrice flottants
        '''
        longueur = len(matrice)
        for i in range(0, self.int_riviere):
            x = random.randint(0, longueur - 1)
            y = random.randint(0, longueur - 1)
            mini = self.regarder_min_cases_voisines(x, y, longueur, matrice)
            while matrice[mini[0]][mini[1]] <= matrice[x][y]:
                matrice[x][y] = 10
                x = mini[0]
                y = mini[1]
                mini = self.regarder_min_cases_voisines(x, y, longueur, matrice)
        return matrice

    def regarder_min_cases_voisines(self, x, y, longueur, matrice):
        '''
        fonction utilisée par l'algorithme de création de rivières, elle permet de trouver la case voisine sur laquelle peut s'écouler la rivière
        :param x: position en x (ligne) du dernier point découlement de la rivière
        type: int
        :param y: position en y (colonne) du dernier point découlement de la rivière
        type: int
        :param longueur: longueur de l'environnement
        type: int
        :param matrice: matrice symbolique de l'environnement (créée par la fonction précédente)
        type: matrice de float
        :return: position de la prochaine case où peut s'écouler la rivière
        type: liste de deux flottants
        '''
        l = []
        if x + 1 >= longueur or x - 1 < 0 or y + 1 >= longueur or y - 1 < 0:
            if x + 1 >= longueur:
                if y + 1 >= longueur or y - 1 < 0:
                    if y + 1 >= longueur:
                        l = [[x - 1, y], [x, y - 1]]
                    if y - 1 < 0:
                        l = [[x - 1, y], [x, y + 1]]
                else:
                    l = [[x - 1, y], [x, y - 1], [x, y + 1]]
            if x - 1 < 0:
                if y + 1 >= longueur or y - 1 < 0:
                    if y + 1 >= longueur:
                        l = [[x, y - 1], [x + 1, y]]
                    if y - 1 < 0:
                        l = [[x, y + 1], [x + 1, y]]
                else:
                    l = [[x, y - 1], [x, y + 1], [x + 1, y]]
            if y + 1 >= longueur:
                if x + 1 >= longueur or x - 1 < 0:
                    if x + 1 >= longueur:
                        l = [[x - 1, y], [x, y - 1]]
                    if x - 1 < 0:
                        l = [[x, y - 1], [x + 1, y]]
                else:
                    l = [[x - 1, y], [x, y - 1], [x + 1, y]]
            if y - 1 < 0:
                if x + 1 >= longueur or x - 1 < 0:
                    if x + 1 >= longueur:
                        l = [[x, y + 1], [x - 1, y]]
                    if x - 1 < 0:
                        l = [[x, y + 1], [x + 1, y]]
                else:
                    l = [[x, y + 1], [x - 1, y], [x + 1, y]]
        else:
            l = [[x - 1, y], [x, y - 1], [x + 1, y], [x, y + 1]]
        mini = l[0]
        for case in l:
            if matrice[case[0]][case[1]] < matrice[mini[0]][mini[1]]:
                mini = case
        return mini

    @property
    def matrice_filtre(self):
        '''
        fonction qui remplit la matrice terrain (appel à l'utilitaire_filtre) sous forme de matrice d'objets terrain à partir
        de la matrice de valeurs (issus de l'algorithme de Perlin et du watershade) créée précédemment
        :return:
        matrice_f: matrice de valeur représentant l'environnement
        type: matrice de flottants
        '''
        matrice_0 = np.zeros((self.longueur, self.longueur))
        matrice_transition = self.iteration(matrice_0, self.res)
        matrice_f = self.riviere(matrice_transition)
        return (matrice_f)

    def conversion(self, matrice):
        '''
        fonction qui convertit la matrice précédente en matrice d'objets terrain
        :param matrice: matrice valeur du terrain
        type: matrice de floats
        '''
        L = []
        V = []
        for i in range(0, len(matrice)):
            for j in range(0, len(matrice[0])):
                if matrice[i][j] == 10 or matrice[i][j] < 0.3:
                    L += [ter.Riviere([])]
                elif matrice[i][j] > 0.7:
                    L += [ter.Foret([])]
                else:
                    L += [ter.Herbe([], 1)]
            V += [L]
            L = []
        U = np.asarray(V)
        self.grille = U

    def creer_animaux(self):
        '''
        dans cette fonction on crée les animaux dans les liste_occupants de chaque case
        :return: 
        '''
        for herbi in range(0, self.int_herbivore):
            x = random.randint(0, len(self.grille) - 1)
            y = random.randint(0, len(self.grille) - 1)
            while type(self.grille[x][y]) == ter.Riviere:
                x = random.randint(0, len(self.grille) - 1)
                y = random.randint(0, len(self.grille) - 1)
            self.grille[x][y].liste_occupants.append(esp.Espece(6, 5, 1, False, 'Herbivore'))
        for carni in range(0, self.int_carnivore):
            x = random.randint(0, len(self.grille) - 1)
            y = random.randint(0, len(self.grille) - 1)
            while type(self.grille[x][y]) == ter.Riviere:
                x = random.randint(0, len(self.grille) - 1)
                y = random.randint(0, len(self.grille) - 1)
            self.grille[x][y].liste_occupants.append(esp.Espece(8, 10, 2, False, 'Carnivore'))
        for charo in range(0, self.int_charognard):
            x = random.randint(0, len(self.grille) - 1)
            y = random.randint(0, len(self.grille) - 1)
            while type(self.grille[x][y]) == ter.Riviere:
                x = random.randint(0, len(self.grille) - 1)
                y = random.randint(0, len(self.grille) - 1)
            self.grille[x][y].liste_occupants.append(esp.Espece(10, 10, 3, False, 'Charognard'))

    def regarder(self,coord,espece):
        """
        L'animal regarde  la zone la plus favorable pour se déplacer,  un herbivore  cherche la meilleure herbe , un carnivore  l'herbivore le plus gras , un charognard  cherche un cadavre.
        retourne les coordonnées de cette zone.  on effectuera un retour aléatoire sinon
        :param coord: coordonnées  du terrain sur lequel se situe l'espece
        :param espece: animal dont on veut étudier le champ
        :type coord: list
        :return: coordonnées favorable pour le deplacement de l'espèce
      
        """
        chmp_vis=[]
        for i in range(coord[0] - espece.champ_vision , coord[0] + espece.champ_vision+1):
            for j in range(coord[1] - espece.champ_vision , coord[1] + espece.champ_vision+1):
                if not i<0 and not j<0 and not i>len(self.grille)-1 and not j>len(self.grille)-1:
                    chmp_vis += [[i,j]]
        for case in chmp_vis:
            if case[0]<0 or case[0]>=len(self.grille) or case[1]<0 or case[1]>=len(self.grille):
                chmp_vis.remove(case)
        if espece.cat == 'Herbivore':
            case_herbe=[]
            for case_bis in chmp_vis:
                if type(self.grille[case_bis[0]][case_bis[1]]) == ter.Herbe and self.grille[case_bis[0]][case_bis[1]].valeur_nutritive >1 :
                    case_herbe += [case_bis]
            if len(case_herbe) == 0:
                cible = random.choice(chmp_vis)
                while type(self.grille[cible[0],cible[1]]) == ter.Riviere:
                    cible = random.choice(chmp_vis)
            else:
                cible = random.choice(case_herbe)

            return cible
        if espece.cat == 'Carnivore':
            case_nourr=[]
            for case_bis in chmp_vis:
                if len(self.grille[case_bis[0]][case_bis[1]].liste_occupants)>0:
                    case_nourr+=[case_bis]
            if len(case_nourr) == 0:
                cible = random.choice(chmp_vis)
                while type(self.grille[cible[0],cible[1]]) == ter.Riviere:
                    cible = random.choice(chmp_vis)
            else:
                val_n = 0
                cible = 0
                for case_animal in case_nourr:
                    for animal in self.grille[case_animal[0]][case_animal[1]].liste_occupants:
                        if animal.cat == 'Herbivore' and animal.valeur_nutritive>=val_n:
                            val_n=animal.valeur_nutritive
                            cible=case_animal
                if cible == 0:
                    cible = random.choice(chmp_vis)
                    while type(self.grille[cible[0],cible[1]]) == ter.Riviere:
                        cible = random.choice(chmp_vis)
            return cible
        if espece.cat == 'Charognard':
            case_nourr=[]
            for case_bis in chmp_vis:
                if len(self.grille[case_bis[0]][case_bis[1]].liste_occupants)>0:
                    case_nourr+=[case_bis]
            if len(case_nourr) == 0:
                cible = random.choice(chmp_vis)
                while type(self.grille[cible[0],cible[1]]) == ter.Riviere:
                    cible = random.choice(chmp_vis)
            else:
                val_n = 0
                cible = 0
                for case_animal in case_nourr:
                    for animal in self.grille[case_animal[0]][case_animal[1]].liste_occupants:
                        if animal.cat == 'Cadavre' and animal.valeur_nutritive>=val_n:
                            val_n=animal.valeur_nutritive
                            cible=case_animal
                if cible == 0:
                    cible = random.choice(chmp_vis)
                    while type(self.grille[cible[0],cible[1]]) == ter.Riviere:
                        cible = random.choice(chmp_vis)
            return cible

    def deplacer_manger(self, coord):
        """
        Cette fonction déplace les animaux vers la zone qui leur est la plus favorable
        :param coord: coordonnée du terrain sur lequel ont déplace les animaux.
        :return: 
        """
        terrain = self.grille[coord[0]][coord[1]]

        for animal in terrain.liste_occupants:

            if not (animal.a_jouer is True or animal.cat == 'Cadavre'):
                if len(terrain.liste_occupants) != 0:
                    X = self.regarder(coord, animal)[0]
                    Y = self.regarder(coord, animal)[1]
                    dest = self.grille[X][Y]
                    dest.liste_occupants.append(animal)
                    terrain.liste_occupants.remove(animal)

                    if animal.cat == 'Herbivore':

                        if type(dest) == ter.Herbe:
                            self.grille[X][Y].raser(animal)
                    elif animal.cat == 'Carnivore':

                        for other in dest.liste_occupants:
                            if other.cat == 'Herbivore':
                                animal.modification_hp(other.hp)
                                other.mourir()
                else:

                    for cadavre in dest.liste_occupants:
                        if cadavre.cat == 'Cadavre':
                            animal.modification_hp(cadavre.valeur_nutritive)
                            dest.liste_occupants.remove(cadavre)
                animal._a_jouer = True

    def vivre(self, coord):
        """
        cette fonction fait se reproduire toutes les especes du terrain  et traite le cas des cadavres trop vieux pour etre encore affichés.
        regle de reproduction :
        -un animal de même espèce  au dessus, dessous ou sur les cotés
        -creer un animal de meme espece en echange de 1/2 des hp de chaque espece (entier) 
        :param coord: coordonnées du terrain avec lequel on souhaite interagir
        :return: 
        """
        terrain = self.grille[coord[0]][coord[1]]

        voisin = []
        if coord[0] == 0:
            if coord[1] == 0:
                voisin = [self.grille[coord[0] + 1][coord[1]], self.grille[coord[0]][coord[1] + 1]]
            elif coord[1] == len(self.grille) - 1:
                voisin = [self.grille[coord[0] + 1][coord[1]], self.grille[coord[0]][coord[1] - 1]]
            else:
                voisin = [self.grille[coord[0] + 1][coord[1]], self.grille[coord[0]][coord[1] - 1],
                          self.grille[coord[0]][coord[1] + 1]]
        elif coord[0] == len(self.grille) - 1:
            if coord[1] == 0:
                voisin = [self.grille[coord[0] - 1][coord[1]], self.grille[coord[0]][coord[1] + 1]]
            elif coord[1] == len(self.grille) - 1:
                voisin = [self.grille[coord[0] - 1][coord[1]], self.grille[coord[0]][coord[1] - 1]]
            else:
                voisin = [self.grille[coord[0] - 1][coord[1]], self.grille[coord[0]][coord[1] - 1],
                          self.grille[coord[0]][coord[1] + 1]]
        elif coord[1] == 0 and coord[0] != 0 and coord[0] != len(self.grille) - 1:
            voisin = [self.grille[coord[0] - 1][coord[1]], self.grille[coord[0] + 1][coord[1]],
                      self.grille[coord[0]][coord[1] + 1]]
        elif coord[1] == len(self.grille) - 1 and coord[0] != 0 and coord[0] != len(self.grille) - 1:
            voisin = [self.grille[coord[0] - 1][coord[1]], self.grille[coord[0] + 1][coord[1]],
                      self.grille[coord[0]][coord[1] - 1]]
        else:
            voisin = [self.grille[coord[0] + 1][coord[1]], self.grille[coord[0] - 1][coord[1]],
                      self.grille[coord[0]][coord[1] - 1], self.grille[coord[0]][coord[1]+1]]
        i = 0
        bebes = []

        for espece in terrain.liste_occupants:
            espece.vieillir()
            if espece.cat == 'Cadavre':
                if espece.valeur_nutritive <= 0:
                    terrain.liste_occupants.remove(espece)
            else:
                reproduit = False
                while not reproduit and i <= len(voisin) - 1:
                    for compagnon in voisin[i].liste_occupants:
                        if compagnon.cat == espece.cat and espece.hp>4:
                            hp = max(compagnon.hp, espece.hp) // 2

                            compagnon.modification_hp(-hp)
                            espece.modification_hp(-hp)
                            bebes.append(esp.Espece(hp, hp, espece.champ_vision, True, espece.cat))
                            reproduit = True
                    i += 1
        print('tamère')
        for bebe in bebes:
            terrain.liste_occupants.append(bebe)

    def tour_brut(self):
        """
        Permet d'effectuer un tour de jeu , les animaux sont d'abord nourri et déplacé , puis  on les fait vieillir et se reproduire. On inclue aussi la pousse de l'herbe non piétinée  
        
        :return: 
        """

        for i in range(self.longueur):
            for j in range(self.longueur):
                self.deplacer_manger([i, j])
        for k in range(self.longueur):
            for l in range(self.longueur):
                self.vivre([k, l])
                if type(self.grille[k][l]) == ter.Herbe and self.grille[k][l].liste_occupants == []:
                    self.grille[k][l].pousse(1)


    def compte_espece(self):
        """
        compte les especes
        :return: une phrase .
        """
        int_herbi = 0
        int_carni = 0
        int_charo = 0
        for ligne in self.grille:
            for case in ligne:
                for animal in case.liste_occupants:
                    if animal.cat == 'Herbivore':
                        int_herbi += 1
                    elif animal.cat == 'Carnivore':
                        int_carni += 1
                    elif animal.cat == 'Charognard':
                        int_charo += 1

        print('il reste {} herbivores,{} carnivores,{}charognards'.format(int_herbi, int_carni, int_charo))
