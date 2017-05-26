# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 10:00:28 2017

@author: Pierre
"""

import environnement as c_m
import sys
from PyQt4 import QtGui
import terrain

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        
        
    def initUI(self, mat):
        for i in range(0, len(mat.grille)):
            for j in range(0, len(mat.grille[0])):
                if type(mat.grille[i][j]) ==  terrain.Herbe:
                    self.col = QtGui.QColor(0, 255, 0)       
                    self.square = QtGui.QFrame(self)
                    self.square.setGeometry(i*10, j*10, 10, 10)
                    self.square.setStyleSheet("QWidget { background-color: %s }" %  
                    self.col.name())
                if type(mat.grille[i][j]) ==  terrain.Foret:
                    self.col = QtGui.QColor(0, 100, 0)       
                    self.square = QtGui.QFrame(self)
                    self.square.setGeometry(i*10, j*10, 10, 10)
                    self.square.setStyleSheet("QWidget { background-color: %s }" %  
                    self.col.name())
                if type(mat.grille[i][j]) ==  terrain.Riviere:
                    self.col = QtGui.QColor(0, 0, 255)       
                    self.square = QtGui.QFrame(self)
                    self.square.setGeometry(i*10, j*10, 10, 10)
                    self.square.setStyleSheet("QWidget { background-color: %s }" %  
                    self.col.name()) 
                for animal in mat.grille[i][j].liste_occupants:
                    if animal.cat == 'Herbivore':
                        self.col = QtGui.QColor(255,255,255)
                        self.square = QtGui.QFrame(self)
                        self.square.setGeometry(i*10+2, j*10+2, 5, 5)
                        self.square.setStyleSheet("QWidget { background-color: %s }" %  
                        self.col.name())
                    if animal.cat == 'Carnivore':
                        self.col = QtGui.QColor(255,0,0)
                        self.square = QtGui.QFrame(self)
                        self.square.setGeometry(i*10+2, j*10+2, 5, 5)
                        self.square.setStyleSheet("QWidget { background-color: %s }" %  
                        self.col.name())
                    if animal.cat == 'Charognard':
                        self.col = QtGui.QColor(100,0,0)
                        self.square = QtGui.QFrame(self)
                        self.square.setGeometry(i*10+2, j*10+2, 5, 5)
                        self.square.setStyleSheet("QWidget { background-color: %s }" %  
                        self.col.name())
        self.setGeometry(300+len(mat.grille)*10, 300+len(mat.grille)*10, 280, 170)
        self.setWindowTitle('Ecosysteme')
        self.show()

            
        
def main():
    
    
    U=c_m.Environnement(5,100,10,100,100,100)
    grid=U.matrice_filtre
    U.conversion(grid) 
    U.creer_animaux()
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.initUI(U)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()