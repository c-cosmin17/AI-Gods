# ghostAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util

#definire clasa care mosteneste clasa parinte Agent
#A class that generalizes the Agent superclass

class GhostAgent( Agent ):
    #constructor in care se initializeaza o variabila de instanta 
    #variabila este specifica fiecarui obiect instantiat

    #The constructor of the class
    def __init__( self, index ):
        self.index = index #Sets the ID of the ghost

    #definire metoda pentru stabilirea actiunii pe care trebuie sa o faca packman-ul 
    def getAction( self, state ):
        #apel metoda, pe obiectul instantiat pentru a prelua starea in care se afla 
        dist = self.getDistribution(state)
        if len(dist) == 0: #daca lungimea este zero atunci este caz de oprire
            return Directions.STOP
        else: #daca nu este preluata o noua directie 
            return util.chooseFromDistribution( dist )

    def getDistribution(self, state): #returneaza nr de actiuni pt acel state???? idk #este suprascrisa in clasele copii
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()

class RandomGhost( GhostAgent ): #clasa pt fantomita random e o subclasa a lui GhostAgent

    def getDistribution( self, state ): #functia returneaza o actinue legala pe care o poate face fantomita???
        dist = util.Counter() #un obiect gol pt distributia de actiuni??
        for a in state.getLegalActions( self.index ): dist[a] = 1.0 #trece prin fiecare actiune si seteapa probabilitatea de alegere cu 1
        dist.normalize()#???
        return dist #returneaza dist

#o alta clasa care mosteneste clasa GhostAgent
class DirectionalGhost( GhostAgent ):
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution( self, state ):
        # Read variables from state
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5

        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
        if isScared:
            bestScore = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min( distancesToPacman )
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist
