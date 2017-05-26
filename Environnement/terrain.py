# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 19:09:06 2017

@author: Pierre
"""



class Terrain(object):
    def __init__(self,liste_occupants):
        self.liste_occupants = []



class Herbe(Terrain):
    
    def __init__(self,liste_occupants,val_nutritive):
        Terrain.__init__(self,liste_occupants)
        self.valeur_nutritive = val_nutritive
        
    def pousse(self, entier):
        self.valeur_nutritive += entier

        
    def raser(self, animal):
        animal.modification_hp(self.valeur_nutritive)
        animal._valeur_nutritive += self.valeur_nutritive
        self.valeur_nutritive = 0


class Riviere(Terrain):
    def __init__(self,liste_occupants):
        Terrain.__init__(self, liste_occupants)

    
class Foret(Terrain):
    def __init__(self,liste_occupants):
        Terrain.__init__(self, liste_occupants)
