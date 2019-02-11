import pygame
from pygame.locals import *
import random

from Grille import Grille
from Grille import Piece
from Grille import Generateur
from Grille import Menu
from Grille import Jeu

    
pygame.init()

a = True


m = Menu (a)
m.getA()

j = Jeu(m)


j.play()
j.getK()




while m.getA():

    if j.getK()==1 :

        screenMenu = pygame.display.set_mode((800,600))
        m.afficherMenu(screenMenu, j, j.s)
        j = Jeu(m)
        m.getEvent(j)




pygame.quit()
