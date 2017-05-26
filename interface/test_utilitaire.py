# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 10:00:28 2017

@author: Pierre
"""

from Environnement import environnement as c_m
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import Environnement.terrain as terrain


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()

    def initUI(self, mat):
        """
        
        :param mat: matrice de type environnement
        :return: 
        """
        for i in range(0, len(mat.grille)):
            for j in range(0, len(mat.grille[0])):
                if type(mat.grille[i][j]) == terrain.Herbe:
                    if mat.grille[i][j].valeur_nutritive != 0:
                        self.col = QColor(0, 255, 0)
                        self.square = QFrame(self)
                        self.square.setGeometry(i * 10, j * 10, 10, 10)
                        self.square.setStyleSheet("QWidget { background-color: %s }" %
                                                  self.col.name())
                    else:
                        self.col = QColor(100, 50, 30)
                        self.square = QFrame(self)
                        self.square.setGeometry(i * 10, j * 10, 10, 10)
                        self.square.setStyleSheet("QWidget { background-color: %s }" %
                                                self.col.name())

                if type(mat.grille[i][j]) == terrain.Foret:
                    self.col = QColor(0, 100, 0)
                    self.square = QFrame(self)
                    self.square.setGeometry(i * 10, j * 10, 10, 10)
                    self.square.setStyleSheet("QWidget { background-color: %s }" %
                                              self.col.name())
                if type(mat.grille[i][j]) == terrain.Riviere:
                    self.col = QColor(0, 0, 255)
                    self.square = QFrame(self)
                    self.square.setGeometry(i * 10, j * 10, 10, 10)
                    self.square.setStyleSheet("QWidget { background-color: %s }" %
                                              self.col.name())
                for animal in mat.grille[i][j].liste_occupants:
                    if animal.cat == 'Herbivore':
                        self.col = QColor(255, 255, 255)
                        self.square = QFrame(self)
                        self.square.setGeometry(i * 10 + 2, j * 10 + 2, 5, 5)
                        self.square.setStyleSheet("QWidget { background-color: %s }" %
                                                  self.col.name())
                    if animal.cat == 'Carnivore':
                        self.col = QColor(255, 0, 0)
                        self.square = QFrame(self)
                        self.square.setGeometry(i * 10 + 2, j * 10 + 2, 5, 5)
                        self.square.setStyleSheet("QWidget { background-color: %s }" %
                                                  self.col.name())
                    if animal.cat == 'Charognard':
                        self.col = QColor(100, 0, 0)
                        self.square = QFrame(self)
                        self.square.setGeometry(i * 10 + 2, j * 10 + 2, 5, 5)
                        self.square.setStyleSheet("QWidget { background-color: %s }" %
                                                  self.col.name())
                    if animal.cat == 'Cadavre':
                        self.col = QColor(0, 0, 0)
                        self.square = QFrame(self)
                        self.square.setGeometry(i * 10 + 2, j * 10 + 2, 5, 5)
                        self.square.setStyleSheet("QWidget { background-color: %s }" %
                                                  self.col.name())
        self.setGeometry(300 + len(mat.grille) * 10, 300 + len(mat.grille) * 10, 1000, 1000)
        self.setWindowTitle('Ecosysteme')


def main(env, n):
    #    U=c_m.Environnement(5,100,10,100,100,100)
    #    grid=U.matrice_filtre
    #    U.conversion(grid)
    #    U.creer_animaux()
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI(env)
    pixmap = QPixmap(len(env.grille) * 10, len(env.grille[0]) * 10)
    ex.render(pixmap, QPoint(), QRegion())
    pixmap.save('Resultats/Image_tour/file{}.jpg'.format(n))

    ex.close()


if __name__ == '__main__':
    main()
