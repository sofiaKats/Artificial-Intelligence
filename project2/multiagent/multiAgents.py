# multiAgents.py
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        score = 0

        if childGameState.isWin():
            return float('inf')

        if childGameState.isLose():
            return -float('inf')

        # Find the distance from the closest food
        foodlist = newFood.asList()
        closestfood = float('inf')
        foodDists = [manhattanDistance(newPos,food) for food in foodlist]
        closestfood = min(foodDists)
            
        score += 8 / closestfood       

        minGhostDist = float('inf')
        for ghost in newGhostStates:
            currGhostPosition = ghost.getPosition()
            minGhostDist = min(minGhostDist, manhattanDistance(newPos,currGhostPosition))
            if minGhostDist < 1: # ghost too close
                return -float('inf')

        foodNum = childGameState.getNumFood()
        score -= 8 * foodNum
        capsuleCoordinates = currentGameState.getCapsules()
        # if the pacman ate a capsule and the ghosts are scared, the score is better
        if newPos in capsuleCoordinates and sum(newScaredTimes) > 0:
            score += 8 / minGhostDist
        else:
            score += - 16 / minGhostDist

        score += childGameState.getScore()
        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        #code based on pseudocode by cgi.di.uoa.gr/~ys02/dialekseis2020/anazitisi_me_antipalotita.pdf
        # Pacman(maximizer)  , the agent=0
        def maxValue(gameState, depth):
            # check if we reached a leaf node or the given depth
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None

            v = -float('inf')
            optimalAction = None

            # for the available moves
            for action in gameState.getLegalActions(0):
                # for each child of the state, call minValue
                child = gameState.getNextState(0, action)
                childScore, _ = minValue(child, 1, depth)
                # keep the max score calculated
                if childScore > v:
                    v, optimalAction = childScore, action
            return v, optimalAction

        # Ghost(minimizer)
        def minValue(gameState, agent, depth):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None

            v = float('inf')
            optimalAction = None

            for action in gameState.getLegalActions(agent):
                child = gameState.getNextState(agent, action)
                # if agent is NOT the last ghost left, call minValue for the rest ghosts
                if agent!=(gameState.getNumAgents()-1):
                    childScore, _ = minValue(child, agent+1, depth)
                else: 
                # if agent is the last ghost, time for pacman to make a move so we call maxValue
                    childScore, _ = maxValue(child, depth+1)
                # keep the min score calculated
                if childScore < v:
                    v, optimalAction = childScore, action
            return v, optimalAction

        # main code where minimax procedure begins
        # fetch the optimal action to be taken and return it
        _, optimalAction = maxValue(gameState, 0)
        return optimalAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Pacman(maximizer)  , the agent=0
        def maxValue(gameState, depth, a, b):
            # check if we reached a leaf node or the given depth
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None

            v = -float('inf')
            optimalAction = None

            # for the available moves
            for action in gameState.getLegalActions(0):
                # for each child of the state, call minValue
                child = gameState.getNextState(0, action)
                childScore, _ = minValue(child, 1, depth, a, b)
                # keep the max score calculated
                if childScore > v:
                    v, optimalAction = childScore, action
                if v > b:
                    return v, optimalAction
                a = max(a, v)
            return v, optimalAction

        # Ghost(minimizer)
        def minValue(gameState, agent, depth, a, b):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None

            v = float('inf')
            optimalAction = None

            for action in gameState.getLegalActions(agent):
                child = gameState.getNextState(agent, action)
                # if agent is NOT the last ghost left, call minValue for the rest ghosts
                if agent!=(gameState.getNumAgents()-1):
                    childScore, _ = minValue(child, agent+1, depth, a, b)
                else: 
                # if agent is the last ghost, time for pacman to make a move so we call maxValue
                    childScore, _ = maxValue(child, depth+1, a, b)
                # keep the min score calculated
                if childScore < v:
                    v, optimalAction = childScore, action
                if v < a:
                    return v, optimalAction
                b = min(b, v)
            return v, optimalAction

        # main code where minimax procedure begins
        a = -float('inf')
        b = float('inf')
        # fetch the optimal action to be taken and return it
        _, optimalAction = maxValue(gameState, 0, a, b)
        return optimalAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # the agent=0
        def maxValue(gameState, depth):
            # check if we reached a leaf node or the given depth
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None

            v = -float('inf')
            optimalAction = None

            # for the available moves
            for action in gameState.getLegalActions(0):
                # for each child of the state, call minValue
                child = gameState.getNextState(0, action)
                childScore = minValue(child, 1, depth)
                # keep the max score calculated
                if childScore > v:
                    v, optimalAction = childScore, action
            return v, optimalAction


        def minValue(gameState, agent, depth):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            # Randomly select action for ghost (Min) by calculating score
            score = 0
            actions = gameState.getLegalActions(agent)
            numActions = len(actions)
            
            for action in actions:
                child = gameState.getNextState(agent, action)
                # if agent is NOT the last ghost left, call minValue for the rest ghosts
                if agent!=(gameState.getNumAgents()-1):
                    childScore = minValue(child, agent+1, depth)
                else: 
                # if agent is the last ghost, time for pacman to make a move so we call maxValue
                    childScore, _ = maxValue(child, depth+1)
                # All ghosts should be modeled as choosing uniformly at random from their legal moves.
                score += childScore*(1.0/numActions)
            return score

        # main code where minimax procedure begins
        # fetch the optimal action to be taken and return it
        _, optimalAction = maxValue(gameState, 0)
        return optimalAction

def betterEvaluationFunction(currentGameState):
        """
        Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
        evaluation function (question 5).

        DESCRIPTION: <write something here so we know what you did>
        """
        newPos = currentGameState.getPacmanPosition()
        newFood = currentGameState.getFood()
        newGhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        score = 0

        if currentGameState.isWin():
            return float('inf')

        if currentGameState.isLose():
            return -float('inf')

        # Find the distance from the closest food
        foodlist = newFood.asList()
        closestfood = float('inf')
        foodDists = [manhattanDistance(newPos,food) for food in foodlist]
        closestfood = min(foodDists)
            
        score += 8 / closestfood       

        minGhostDist = float('inf')
        for ghost in newGhostStates:
            currGhostPosition = ghost.getPosition()
            minGhostDist = min(minGhostDist, manhattanDistance(newPos,currGhostPosition))
            if minGhostDist < 1: # ghost too close
                return -float('inf')

        foodNum = currentGameState.getNumFood()
        score -= 8 * foodNum
        capsuleCoordinates = currentGameState.getCapsules()
        # if the pacman ate a capsule and the ghosts are scared, the score is better
        if newPos in capsuleCoordinates and sum(newScaredTimes) > 0:
            score += 8 / minGhostDist
        else:
            score += - 16 / minGhostDist

        score += currentGameState.getScore()
        return score

# Abbreviation
better = betterEvaluationFunction
