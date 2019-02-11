import pygame
import random
from pygame.locals import *



class Grille:

    longeur = 0
    largeur = 0
    positionDepart = ()
    tailleCellule = 0

    pos = []
    casePleine = []

    backgroundColor = (0, 0, 0)


    score = 0

    def __init__(self, l, L, positionD, tCell, screen):
        self.longeur = l
        self.largeur = L
        self.positionDepart = positionD
        self.tailleCellule = tCell
        self.screen = screen
        self.initialiserGrille(screen)
        self.initialiserMurs()
        self.caseATomber = []

    def initialiserGrille(self, screen):
        for i in range(0, self.longeur - 1):
            self.pos.append([0] * (self.largeur - 1))

        for i in range(0, self.largeur - 1):
            for j in range(0, self.longeur - 1):
                self.pos[j][i] = ((j * 32) + self.positionDepart[0], (i * 32) + self.positionDepart[1])
                pygame.draw.rect(screen, self.backgroundColor, (self.pos[j][i][1], self.pos[j][i][0], 32, 32))

    def initialiserMurs(self):

        for j in range(0, self.longeur - 1):
            for i in range(0, self.largeur - 1):

                if i == 0:
                    self.casePleine.append(self.pos[j][i])

                elif i == self.largeur - 2:
                    self.casePleine.append(self.pos[j][i])

                elif j == self.longeur - 2:
                    self.casePleine.append(self.pos[j][i])

        for i in range(0, len(self.casePleine)):

            self.casePleine[i] = (self.casePleine[i][1], self.casePleine[i][0])


    def getPos(self, x, y):
        return (self.pos[x][y][0], self.pos[x][y][1])

    def getCasePleine(self):
        return self.casePleine

    def isPlein(self, pos):
        a = False

        if pos in self.casePleine:
            a = True

        return a

    def checkLigne(self, y):

        a = True;
        currentPos = []

        for i in range(1, self.largeur-2):
            currentPosition = self.getPos(y, i)
            currentPosition = (currentPosition[1], currentPosition[0])

            currentPos.append(currentPosition)

            if currentPosition not in self.casePleine:
                a = False

        if a == True:
            for i in range(0, len(currentPos)):
                self.clearCasePleine(currentPos[i])
                
            
            
            self.remplirCaseATomber(y)
            self.tomber()
            self.score += 100
                    

    def update(self):

        self.checkLastLigne()
        self.drawCell()
        


    def checkLastLigne(self):

        x = (self.largeur - 3)*32 + 100
        a = False


        for i in self.casePleine :
            if i[1] == 132 and x > i[0] > 100 :
                a = True

        return a
                               
               


    def checkGrille(self):

        for i in range(self.longeur - 3, 0, -1):
            self.checkLigne(i)



    def remplirCaseATomber(self, y):

        for i in self.casePleine:
            if i[0] > self.getPos(0,0)[1] and i[0] < self.getPos(0,self.largeur-2)[1] and i[1] < self.getPos(y, 0)[0]:
                self.caseATomber.append(i)
                
        for i in self.caseATomber:
            if i in self.casePleine:
                self.clearCasePleine(i)
             


    def addInCasePleine(self, pos):

        self.casePleine.append(pos)


    def clearCasePleine(self, pos):

        pygame.draw.rect(self.screen, self.backgroundColor, (pos[0], pos[1], 32, 32))
        grille = pygame.image.load("grille2.png")
        self.screen.blit(grille, (132,132))
        self.casePleine.remove(pos)
        
    def ViderCaseATomber(self):

        self.caseATomber = []  

    def viderCasePleine(self):

        self.casePleine = []
        self.initialiserMurs()        

    def collision(self, dX, dY, pos):

        a = self.isPlein( (pos[0] + (dX * self.tailleCellule) , pos[1] + (dY * self.tailleCellule) ))

        return a

    def tomber(self):

        i = 0
        while i < len(self.caseATomber):

            self.caseATomber[i] = (self.caseATomber[i][0], self.caseATomber[i][1] + self.tailleCellule)
            self.addInCasePleine(self.caseATomber[i])
            i += 1     

        self.ViderCaseATomber()

    def drawCell(self):
    
        for i in self.casePleine:
            if i[0] > self.getPos(0,0)[1] and i[0] < self.getPos(0,self.largeur-2)[1] and i[1] < self.getPos(20, 0)[0]:

                pc = pygame.image.load("TetrisPiece.png").convert_alpha()
                self.screen.blit(pc, (i[0], i[1]))
                
                
    def getLargeur(self):
        return self.largeur

    def getScore(self):
        return self.score


    def afficherScore(self, font):

        pygame.draw.rect(self.screen, (0, 0, 0), (560, 450, 100, 100))

        sc = font.render(str(self.getScore()), True, (255, 255, 255))
        self.screen.blit(sc, (600,450))
            

class Piece:

    def __init__(self, startPosition, grille, l, L, screen, tailleCel, vitesse, couleur):
        self.pos = (grille.getPos(startPosition[0], startPosition[1])[0], grille.getPos(startPosition[0], startPosition[1])[1])
        self.g = grille
        self.longeur = l
        self.largeur = L
        self.screen = screen
        self.tailleCellule = tailleCel
        self.positionCell = []
        self.vitesse = vitesse
        self.vitesseInitiale = vitesse
        self.compteur = 0
        self.couleur = couleur
        self.canMove = False
        self.index = 0

    def spawnPiece(self):

        for i in range(0, self.longeur):
            for j in range(0, self.largeur):

                self.positionCell.append((self.g.getPos(j, i)[0] + (self.pos[0] - 100), self.g.getPos(j, i)[1] + (self.pos[1] - 100)))

        self.canMove = True

        
    def drawPiece(self, screen):


        for i in range(0, len(self.positionCell)):


            pc = pygame.image.load("TetrisPiece.png").convert_alpha()
            pc.fill(self.couleur, special_flags=pygame.BLEND_MULT)
            self.screen.blit(pc, (self.positionCell[i][0], self.positionCell[i][1]))
            
    def clearPiece(self) :
		
        for i in range(0, len(self.positionCell)):
			
            pygame.draw.rect(self.screen, (0, 0, 0), (self.positionCell[i][0], self.positionCell[i][1], 32, 32))
            gl = pygame.image.load("grille2.png").convert_alpha()
            self.screen.blit(gl, (132,132))

    def update(self, event):

        self.compteur += 1

        if self.canMove == True:
            self.bouger(event)


        if self.compteur >= self.vitesse:
            self.tomber()
            self.compteur = 0


    def tomber(self):

        self.clearPiece()

        if(self.collision(0, 1) == False):

            for i in range(0, len(self.positionCell)):

                self.positionCell[i] = (self.positionCell[i][0], self.positionCell[i][1] + 32)
        else:
            self.canMove = False

            for i in range(0, len(self.positionCell)):

                self.g.addInCasePleine(self.positionCell[i])

        self.drawPiece(self.screen)

    def bouger(self, event):

        direction = 0

        if event.type == pygame.KEYUP:

            direction = 0
            self.vitesse = self.vitesseInitiale

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT and self.collision(-1, 0) == False:
                direction = -1

            if event.key == pygame.K_RIGHT and self.collision(1, 0) == False:
                direction = 1

            if event.key == pygame.K_UP and self.colRotation() == False:
                self.rotation()

            if event.key == pygame.K_DOWN: 
                self.vitesse = 2


            self.clearPiece()

            for i in range(0, len(self.positionCell)):

                self.positionCell[i] = (self.positionCell[i][0] + (direction * self.tailleCellule), self.positionCell[i][1])

            self.drawPiece(self.screen)

    def collision(self, dX, dY):

        a = False

        for i in range(0, len(self.positionCell)):

            a = self.g.isPlein((self.positionCell[i][0] + (dX * self.tailleCellule), self.positionCell[i][1] + (dY * self.tailleCellule)))

            if a == True:
                break

        return a

    def rotation(self):
        #On prends la deuxieme cellule
        

        if(self.longeur != self.largeur):

            origin = self.positionCell[1]
            self.clearPiece()
            self.detruirePiece()
            facteurX = 0
            facteurY = 0

            if(self.longeur > self.largeur):
                
                temp = self.longeur
                self.longeur = self.largeur
                self.largeur = temp
                facteurX = -1
                facteurY = 0

            else:
                temp = self.largeur
                self.largeur = self.longeur
                self.longeur = temp
                facteurX = 0
                facteurY = -1

            for i in range(0, self.longeur):
                    for j in range(0, self.largeur):

                        self.positionCell.append((self.g.getPos(j, i)[0] + ((origin[0] + (facteurX * self.tailleCellule)) - 100), self.g.getPos(j, i)[1] + ((origin[1] + (facteurY * self.tailleCellule)) - 100)))


    def detruirePiece(self):

        self.positionCell = []

    def colRotation(self):

        a = False

        if (self.longeur > self.largeur) and (self.collision(-1, 0) or self.collision(self.longeur - 2, 0) or self.collision(self.longeur - 3, 0)):
            a = True

        if (self.largeur > self.longeur) and (self.collision(0, self.largeur - 2) or self.collision(0, self.largeur - 3)):
            a = True

        return a



    def hasEnded(self):

        return not self.canMove

    def afficherPiece (self):

        pygame.draw.rect(self.screen, (0, 0, 0), (582, 200, 64, 128))

        for i in range(0, self.longeur):
            for j in range(0, self.largeur):

                pc = pygame.image.load("TetrisPiece.png").convert_alpha()
                pc.fill(self.couleur, special_flags=pygame.BLEND_MULT)
                self.screen.blit(pc, (582 + j*32, 200 + i*32))







        
class Generateur:

    def __init__(self, g, screen):
    
        self.piecesDisponible = [
            (2,2),
            (2,1),
            (3,1),
            (4,1)
        ]
        
        self.g = g
        self.screen = screen
        self.vitesse = 30
        self.pallier = 200
        self.listPiece = []
        self.c = 0
        
    
    def generatePiece(self):
        
        a = random.randint(0,3)
        x = random.randint(1, self.g.getLargeur() - 2 - self.piecesDisponible[a][1])
        self.adapterVitesse()
        self.adapterCouleur(a)
        
        p = Piece( (x, 0), self.g, self.piecesDisponible[a][0], self.piecesDisponible[a][1], self.screen, 32, self.vitesse, self.c)
        
        return p

    def getPiece(self):

        p = self.generatePiece()
        pnext = self.generatePiece()

        self.listPiece.append(p)
        self.listPiece.append(pnext)

        return self.listPiece


    def adapterVitesse(self):


        score = self.g.getScore()

        if score >= self.pallier:
            self.vitesse -= 10 
            self.pallier += 200

    def adapterCouleur (self, a) :

        if a == 0 :
            self.c = (255,0,0)

        elif a == 1 :
            self.c = (255,255,0)

        elif a == 2 :
            self.c = (0,255,255)

        elif a == 3 :
            self.c = (0, 200, 0)

        return self.c



class Menu :

    def __init__ (self, a):
        self.a = a



    def initMenu(self, screen, j, s):

        pygame.init()

        re = pygame.image.load("rejouer.png").convert_alpha()
        qu = pygame.image.load("quitter.png").convert_alpha()

        screen.blit(re, (150, 400))
        screen.blit(qu, (450, 400))

        font = pygame.font.SysFont("arial", 42)

        texte = font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(texte, (250, 100))

        sc = font.render("Votre score :", True, (255,255,255))
        screen.blit(sc, (200, 200))

        s = font.render(s, True, (255,255,255))
        screen.blit(s, (500,200))


    def getEvent(self,j):

        k = 0

        while True :

            event = pygame.event.poll()

            if event.type == pygame.QUIT :
                self.a = False
                break

            if event.type == MOUSEBUTTONDOWN :

                if event.button == 1 and  150<event.pos[0]<387 and 500>event.pos[1]>400 :
                    k = 1
                    break
                    

                if event.button == 1 and  450<event.pos[0]<677 and 500>event.pos[1]>400 :
                    self.a = False
                    break


            pygame.display.flip()

        if k == 1 :
            j.rejouer()

    def getA(self):
        return self.a

    def changerA(self):
        self.a = False



    def afficherMenu(self, screen,j, s):

        self.initMenu(screen, j, s)
        self.getA()



class Jeu :

    def __init__(self, menu):

        self.nbPieceEnJeu = 0
        self.k = 0
        self.s = 0
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 23)
        self.g = 0
        self.p = 0
        self.menu = menu



    def play(self) :

        screen = pygame.display.set_mode((800,800))

        g = Grille(22, 13, (100, 100), 32, screen)
        g.viderCasePleine()
        self.generateur = Generateur(g, screen)
        self.liste = self.generateur.getPiece()

        titre = pygame.image.load("Titre.png").convert_alpha()
        screen.blit(titre, (150,0))

        texte = self.font.render("Score :", True, (255, 255, 255))
        screen.blit(texte, (570, 400))

        t = self.font.render("Prochaine piece :", True, (255,255,255))
        screen.blit(t, (500, 150))

        while True:

            event = pygame.event.poll()

            if event.type == pygame.QUIT :
                self.menu.changerA()
                self.menu.getA()
                break


            if g.checkLastLigne() == True :
                self.k = 1
                self.s = str(g.getScore())
                break
            
                

            if self.nbPieceEnJeu == 0:
                self.nbPieceEnJeu += 1
                self.p = self.liste[0]
                pnext = self.liste[1]
                pnext.afficherPiece()
                self.p.spawnPiece()

            g.afficherScore(self.font)
            g.checkGrille()
            g.update()
            self.p.update(event)

            if self.p.hasEnded():
                self.liste[0] = self.liste[1]
                self.liste [1] = self.generateur.generatePiece()
                self.nbPieceEnJeu -= 1
                g.score += 1

            self.clock.tick(60)
            pygame.display.flip()



    def getK(self):
        return self.k

    def getS(self):
        return self.s


    def rejouer(self):

        self.play()
