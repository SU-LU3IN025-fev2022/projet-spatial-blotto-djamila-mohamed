# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random
import numpy as np
import sys
from itertools import chain


import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme




# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'blottoMap'
    game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 10 # frames per second
    game.mainiteration()
    player = game.player

def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()



    #-------------------------------
    # Initialisation
    #-------------------------------

    nbLignes = game.spriteBuilder.rowsize
    nbCols = game.spriteBuilder.colsize

    print("lignes", nbLignes)
    print("colonnes", nbCols)


    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    print("Trouvé ", nbPlayers, " militants")



    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    initStates = [o.get_rowcol() for o in players]
    print ("Init states:", initStates)

    # on localise tous les secteurs d'interet (les votants)
    # sur le layer ramassable
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)


    # on localise tous les murs
    # sur le layer obstacle
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    print ("Wall states:", wallStates)

    def legal_position(row,col):
        # une position legale est dans la carte et pas sur un mur
        return ((row,col) not in wallStates) and row>=0 and row<nbLignes and col>=0 and col<nbCols




    #-------------------------------
    # Attributaion aleatoire des fioles
    #-------------------------------

    objectifs = [] # liste de tuples
    for i in range (nbPlayers):
        objectifs.append(random.choice(goalStates))


    #-------------------------------
    # Carte demo
    # nbPlayers joueurs
    # Joueur i: A*
    #-------------------------------

    #-------------------------------
    # calcul A* pour chaque joueur i
    #-------------------------------

    ps = [] # liste de problemes pour chaque joueur
    paths = [] # liste de chemins pour chaque joueur

    for i in range (len(players)):

        print("Objectif joueur ", objectifs[i])

        g = np.ones((nbLignes,nbCols),dtype=bool)  # par defaut la matrice comprend des True
        for w in wallStates:            # putting False for walls
            g[w]=False
        p = ProblemeGrid2D(initStates[i],objectifs[i],g,'manhattan')
        ps.append(p)
        path = probleme.astar(p)
        paths.append(path)
        print ("Chemin trouvé:", path)


    #-------------------------------
    # Boucle principale de déplacements
    #-------------------------------


    nextStep = [0 for x in players]
    but_atteint = [False for x in players]
    posPlayers = initStates
    # les militants sont des lettres de l'alphabet (allant de a à e)
    matrice_resultats = [[chr(x)] for x in range(ord('a'), ord('f'))]

    for i in range(iterations):

        for p in range (nbPlayers): # on fait jouer chaque joueur
            if not(but_atteint[p]):
                row,col = paths[p][nextStep[p]]
                while True: # tant que pas legal on retire une position
                    x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
                    next_row = row+x_inc
                    next_col = col+y_inc
                    if legal_position(next_row,next_col):
                        break
                players[p].set_rowcol(next_row,next_col)
                print ("pos " +str(p)+ " :", row,col)
                if (row,col) == objectifs[p]:
                    print("le joueur "+str(p)+" a atteint son but!")
                    but_atteint[p] = True
                    break
                nextStep[p]+=1

        fini = False
        for atteint in but_atteint:
            fini = False
            if not(atteint):
                break
            else :
                fini = True

        if fini:
            print("tout le monde a fini")
            break

            # on passe a l'iteration suivante du jeu
        game.mainiteration()



    pygame.quit()

    # nom de l'electeur, score pour le parti 1, score pour le parti 2
    parti1 = [[x, 0, 0] for x in matrice_resultats]

    print("RESULTATS")
    for p in range(len(objectifs)):
        matrice_resultats[goalStates.index(objectifs[p])].append(p)

    print(matrice_resultats)

    # on considere que les nombre pairs sont le parti 1 et le reste parti 2
    for r in matrice_resultats:
        for p in r[1:]:
            if p%2 == 0:


    #-------------------------------









if __name__ == '__main__':
    main()
