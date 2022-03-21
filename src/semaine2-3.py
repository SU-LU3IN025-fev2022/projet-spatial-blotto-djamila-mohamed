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
    game.fps = 10  # frames per second
    game.mainiteration()
    player = game.player

def aleatoire(objectifs):
    """ Strategie aleatoire, retourne un militant au hasard """
    return objectifs[random.randrange(0, len(objectifs))]

def tetu(strats, objectifs):
    return 0

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

    objectifs = goalStates
    joueur_objectif = []

    # les joueurs sont numerotes de 0 à 13 (il y en a 14)
    for p in range(len(players)):
        joueur_objectif.append(aleatoire(objectifs))
        print("Objectif joueur "+str(p)+" : "+str(joueur_objectif[p]))


    #-------------------------------
    # Carte demo
    # 14 militants, se deplacent avec astar
    # 5 electeurs
    #-------------------------------

    liste_path = []
    for p in range(len(players)):
        g =np.ones((nbLignes,nbCols),dtype=bool)  # par defaut la matrice comprend des True
        for w in wallStates:            # putting False for walls
            g[w]=False
        prob = ProblemeGrid2D(initStates[p],joueur_objectif[p],g,'manhattan')
        path = probleme.astar(prob)
        print ("Chemin trouvé:", path)
        liste_path.append(path)

    #-------------------------------
    # Boucle principale de déplacements
    #-------------------------------

    posPlayers = initStates
    nextStep = [0 for x in players]
    but_atteint = [False for x in players]

    for i in range(iterations):

        # deplacement des joueurs
        for p in range(len(players)):
            if not(but_atteint[p]):
                row,col = liste_path[p][nextStep[p]]

                # les strategies allant de 0 a 4 sont des strategies qui ne dependent pas des autres

                posPlayers[p]=(row, col)
                players[p].set_rowcol(row, col)
                print ("pos "+str(p)+" : ", row, col)
                if (row,col) == joueur_objectif[p]:
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




    #-------------------------------









if __name__ == '__main__':
    main()


# Combien de partis ? combien de militants par parti ?
