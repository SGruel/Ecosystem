# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""


import numpy
import terrain
import random
#import BDD.requete as rec
import espece as esp

class Environnement(object):
    
    def __init__(self, res , longueur, int_riviere, int_herbivore, int_carnivore, int_charognard):
        self._res         = res
        self._longueur    = longueur
        self._int_riviere = int_riviere
        self.grille     = numpy.zeros((longueur,longueur))
        self.int_herbivore = int_herbivore
        self.int_carnivore = int_carnivore
        self.int_charognard = int_charognard
    
    @property
    def res(self):
        return(self._res)
    @property
    def longueur(self):
        return(self._longueur)
    @property
    def int_herbe(self):
        return(self._int_herbe)
    @property
    def int_foret(self):
        return(self._int_foret)
    @property
    def int_riviere(self):
        return(self._int_riviere)
        
    def creer_pts_aleatoires(self, res):
        L=[]
        V=[]
        for i in range(0,res+1):
            for j in range(0,res+1):
                L += [random.random()]
            V+=[L]
            L=[]
        return V

    def fct_interpolation(self, x, a, b):
        c = (1-numpy.cos(x*numpy.pi))/2
        return ((1-c)*a+c*b)
    
    def placement_X(self,x,y,V):
        x0=int(x)
        y0=int(y)
        if x0-x != 0 or y0-y != 0: 
            couleur_ref0=V[x0][y0]
            couleur_ref1=V[x0+1][y0]
            couleur_ref2=V[x0][y0+1]
            couleur_ref3=V[x0+1][y0+1]
            interA=self.fct_interpolation(x0-x, couleur_ref0, couleur_ref1)
            interB=self.fct_interpolation(x0-x, couleur_ref2, couleur_ref3)
            couleur_point=self.fct_interpolation(y0-y, interA, interB)
        else:
            couleur_point=V[x0][y0]
        return couleur_point
    
    def iteration(self,matrice,res):
        V=self.creer_pts_aleatoires(res)
        for i in range(0,len(matrice)):
            for j in range(0,len(matrice[0])):
                matrice[i][j]=self.placement_X(i*res/len(matrice),j*res/len(matrice[0]),V)
        return matrice
    
    def riviere(self, matrice):
        longueur=len(matrice)
        for i in range(0,self.int_riviere):
            x=random.randint(0,longueur-1)
            y=random.randint(0,longueur-1)
            mini = self.regarder_min_cases_voisines(x,y,longueur,matrice)
            while matrice[mini[0]][mini[1]] <= matrice[x][y]:
                matrice[x][y]=10
                x=mini[0]
                y=mini[1]
                mini=self.regarder_min_cases_voisines(x,y,longueur,matrice)
        return matrice

                        
    def regarder_min_cases_voisines(self,x,y,longueur,matrice):
        if x+1>=longueur or x-1<0 or y+1>=longueur or y-1<0:
            if x+1>=longueur:
                if y+1>=longueur or y-1<0:
                    if y+1>=longueur:
                        l=[[x-1,y],[x,y-1]]
                    if y-1<0:
                        l=[[x-1,y],[x,y+1]]
                else:
                    l=[[x-1,y],[x,y-1],[x,y+1]]
            if x-1<0:
                if y+1>=longueur or y-1<0:
                    if y+1>=longueur:
                        l=[[x,y-1],[x+1,y]]
                    if y-1<0:
                        l=[[x,y+1],[x+1,y]]
                else:
                    l=[[x,y-1],[x,y+1],[x+1,y]]
            if y+1>=longueur:
                if x+1>=longueur or x-1<0:
                    if x+1>=longueur:
                        l=[[x-1,y],[x,y-1]]
                    if x-1<0:
                        l=[[x,y-1],[x+1,y]]
                else:
                    l=[[x-1,y],[x,y-1],[x+1,y]]
            if y-1<0:
                if x+1>=longueur or x-1<0:
                    if x+1>=longueur:
                        l=[[x,y+1],[x-1,y]]
                    if x-1<0:
                        l=[[x,y+1],[x+1,y]]
                else:
                    l=[[x,y+1],[x-1,y],[x+1,y]]            
        else:
            l=[[x-1,y],[x,y-1],[x+1,y],[x,y+1]]
        mini=l[0]
        for case in l:
            if matrice[case[0]][case[1]] < matrice[mini[0]][mini[1]]:
                mini=case
        return mini
            
        
    def creer_animaux(self):
        for herbi in range (0,self.int_herbivore):
            x=random.randint(0,len(self.grille)-1)
            y=random.randint(0,len(self.grille)-1)
            while type(self.grille[x][y]) == terrain.Riviere:
                x=random.randint(0,len(self.grille)-1)
                y=random.randint(0,len(self.grille)-1)
            self.grille[x][y].liste_occupants.append(esp.Espece(10, 10, 1, False, 'Herbivore'))
        for carni in range (0,self.int_carnivore):
            x=random.randint(0,len(self.grille)-1)
            y=random.randint(0,len(self.grille)-1)
            while type(self.grille[x][y]) == terrain.Riviere:
                x=random.randint(0,len(self.grille)-1)
                y=random.randint(0,len(self.grille)-1)
            self.grille[x][y].liste_occupants.append(esp.Espece(10, 10, 2, False, 'Carnivore'))
        for charo in range (0,self.int_charognard):
            x=random.randint(0,len(self.grille)-1)
            y=random.randint(0,len(self.grille)-1)
            while type(self.grille[x][y]) == terrain.Riviere:
                x=random.randint(0,len(self.grille)-1)
                y=random.randint(0,len(self.grille)-1)
            self.grille[x][y].liste_occupants.append(esp.Espece(10, 10, 2, False, 'Charognard'))
        
            
            
            
                
    
    @property    
    def matrice_filtre(self):
        '''
        fonction qui remplit la matrice terrain (appel à l'utilitaire_filtre)
        '''
        matrice_0=numpy.zeros((self.longueur,self.longueur))
        matrice_transition=self.iteration(matrice_0,self.res)
        matrice_f=self.riviere(matrice_transition)
        return(matrice_f)
        

        
    def conversion(self,matrice):
        L=[]
        V=[]
        for i in range(0,len(matrice)):
            for j in range(0,len(matrice[0])):
                if matrice[i][j] < 10:
                    if matrice[i][j]<0.3:
                        L+=[terrain.Riviere([])]
                    else:
                        if matrice[i][j]>0.7:
                            L+=[terrain.Foret([])]
                        else:
                            L+=[terrain.Herbe(1,[])]
                else:
                    L+=[terrain.Riviere([])]
            V+=[L]
            L=[]
        U=numpy.asarray(V)
        self.grille = U

    def clean_cadavre(self,case):
            for i in (0,len(case.liste_occupants)):
                animal=case.liste_occupants[i]
                if animal.type == 'Cadavre' and animal.valeur_nutritive <= 0:
                    print('le cadavre {} disparaît'.format(animal))
#                    rec.supprimer(case.liste_occupant[i])
                    del case.liste_occupants[i]

        
if __name__=="__main__":
    U=Environnement(3,9,2,3,3,3)
    grid=U.matrice_filtre
    U.conversion(grid)
    U.creer_animaux()
    print(U.grille)
    