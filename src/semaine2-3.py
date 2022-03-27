# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random
import numpy as np
import sys
import time
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
    game.fps = 40  # frames per second
    game.mainiteration()
    player = game.player

def aleatoire(objectifs):
    """ Strategie aleatoire, retourne la position d'un electeur au hasard """
    return objectifs[random.randrange(0, len(objectifs))]

def tetu(strats, objectifs, parti, joueur_objectif):
    return 0

def stochaExp(strats, objectifs, parti, joueur_objectif):
    return 0

def bestAnswer(strats, objectifs, parti, joueur_objectif):
    return 0

def fictitious(strats, objectifs, parti, joueur_objectif):
    return 0

def equitable(players, objectifs, parti, joueur_objectif):
    """ Strategie equitable, repartit les militants de manière equitable sur les electeurs """
    repartition = [[x] for x in objectifs]
    div = len(players) // len(objectifs)
    rem = len(players) % len(objectifs)
    joueurs_pris = []
    joueurs = random.sample(players, len(players))
    i = 0
    o = 0
    nb_joueurs = 0
    while i < len(joueurs):
        repartition[o].append(joueurs[i])
        i+=1
        nb_joueurs+=1
        if o == len(objectifs) - 1:
            continue
        if nb_joueurs >= div:
            o+=1
            nb_joueurs = 0
    res = []
    for i in repartition:
        for j in i[0:]:
            res.append(i[0])
    for i in range(len(joueur_objectif)):
        if parti == 1:
            if i%2 == 0:
                joueur_objectif[i] = res[i]
        else:
            if i%2 != 0:
                joueur_objectif[i] = res[i]
    return res

def deuxPrem(objectifs, parti, joueur_objectif):
    return 0

def repartir_strategies(players, objectifs, strategie1, strategie2, joueur_objectif):

    #-------------------------------
    # Application des strategies des militants
    # 0 = aleatoire
    # 1 = tetu
    # 2 = stochastique expert
    # 3 = meilleure reponse
    # 4 = fictitious play
    # 5 = repartir de maniere equitable
    # 6 = repartir tout sur les deux premiers electeurs uniquement
    #-------------------------------

    # les joueurs sont numerotes de 0 à N-1 (il y en a N)
    # STARTS PARTI1
    if strategie1 == 0 :
        for p in range(0, len(players), 2):
            joueur_objectif[p] = aleatoire(objectifs)

    elif strategie1 == 1 :
        joueur_objectif.append(tetu(objectifs, 1))

    elif strategie1 == 2 :
        joueur_objectif.append(stochaExp(objectifs, 1))

    elif strategie1 == 3 :
        joueur_objectif.append(bestAnswer(objectifs, 1))

    elif strategie1 == 4 :
        joueur_objectif.append(fictitious(objectifs, 1))

    elif strategie1 == 5 :
        equitable(players, objectifs, 1, joueur_objectif)

    elif strategie1 == 6 :
        joueur_objectif.append(deuxPrem(objectifs, 1))


    # STARTS PARTI2

    if strategie2 == 0 :
        for p in range(1, len(players), 2):
            joueur_objectif[p] = aleatoire(objectifs)

    elif strategie2 == 1 :
        joueur_objectif.append(tetu(objectifs, 2))

    elif strategie2 == 2 :
        joueur_objectif.append(stochaExp(objectifs, 2))

    elif strategie2 == 3 :
        joueur_objectif.append(bestAnswer(objectifs, 2))

    elif strategie2 == 4 :
        joueur_objectif.append(fictitious(objectifs, 2))

    elif strategie2 == 5 :
        equitable(players, objectifs, 2, joueur_objectif)

    elif strategie2 == 6 :
        joueur_objectif.append(deuxPrem(objectifs, 2))

def jour(iterations, nbLignes, nbCols, players, goalStates, initStates, wallStates, strategie1, strategie2):
    def legal_position(row,col):
        # une position legale est dans la carte et pas sur un mur
        return ((row,col) not in wallStates) and row>=0 and row<nbLignes and col>=0 and col<nbCols

    objectifs = goalStates

    joueur_objectif = [0 for x in range(len(players))]

    repartir_strategies(players, objectifs, strategie1, strategie2, joueur_objectif)

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
                #print ("pos "+str(p)+" : ", row, col)
                if (row,col) == joueur_objectif[p]:
                    #print("le joueur "+str(p)+" a atteint son but!")
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

    print("\n----------------RESULTATS----------------\n")

    matrice_resultats = [[chr(x)] for x in range(ord('a'), ord('f'))]
    for p in range(len(joueur_objectif)):
        matrice_resultats[goalStates.index(joueur_objectif[p])].append(p)

    # on considere que les nombre pairs sont le parti 1 et le reste parti 2
    voix_parti1 = 0
    voix_parti2 = 0
    for r in matrice_resultats:
        nombre_parti1 = 0
        nombre_parti2 = 0
        for p in r[1:]:
            if p%2 == 0:
                nombre_parti1+=1
            else:
                nombre_parti2+=1
        if nombre_parti1 > nombre_parti2:
            voix_parti1+=1
        elif nombre_parti2 > nombre_parti1:
            voix_parti2+=1

    print("le parti 1 a remporté "+str(voix_parti1)+" voix")
    print("le parti 2 a remporté "+str(voix_parti2)+" voix")

    win = 0

    if voix_parti1 > voix_parti2:
        print("le gagnant est le parti 1")
        win = 1
    elif voix_parti1 < voix_parti2:
        print("le gagnant est le parti 2")
        win = 2
    else:
        print("les deux partis sont à égalité")

    #-------------------------------

    return win

def main(tableau_strategies, jours):
    tableau_score = [] # chaque indice est le numéro du jour-1
    i = 0
    while i < jours:
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
        # condition juste pour masquer le bloc dans l'editeur, inutile au programme
        if 1==1:
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

        tableau_score.append(jour(iterations, nbLignes, nbCols, players, goalStates, initStates, wallStates, tableau_strategies[0][i], tableau_strategies[1][i]))
        time.sleep(2) # pour avoir le temps de regarder les resultats
        i+=1

        print("\n------------- FIN DE LA CAMPAGNE - RESULTATS -------------\n")
        print(tableau_score)

if __name__ == '__main__':

    jours = 5

    tableau_strategies = [[], []]
    tableau_strategies[0] = [5 for x in range(jours+1)]
    tableau_strategies[1] = [0 for x in range(jours+1)]
    main(tableau_strategies, jours)
