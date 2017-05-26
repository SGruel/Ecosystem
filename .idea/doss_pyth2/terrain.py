# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 19:09:06 2017

@author: Pierre
"""

class Terrain(object):
    def __init__(self,liste_occupants):
        self.liste_occupants = liste_occupants
        
    def  enregistrer(self):
        pass


class Herbe(Terrain):
    
    def __init__(self,valeur_nutritive,liste_occupants):
        Terrain.__init__(self,liste_occupants)
        self.valeur_nutritive = valeur_nutritive
        
    def pousse(self, entier):
        self.valeur_nutritive += entier
        
    def raser(self):
        self.valeur_nutritive = 0        
        
class Riviere(Terrain):
    
    def __init__(self,liste_occupants):
        Terrain.__init__(self,liste_occupants)
        pass
    
class Foret(Terrain):
    def __init__(self,liste_occupants):
        Terrain.__init__(self,liste_occupants)
        pass