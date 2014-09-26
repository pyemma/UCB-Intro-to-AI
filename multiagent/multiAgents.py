# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
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

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        mi = 999999
        L = newFood.asList(True)
        for pos in L:
            mi = min(mi, util.manhattanDistance(pos, newPos))
        if len(L) == 0:
            mi = 0
        ma = 999999
        for ghost in newGhostStates:
            ma = min(ma, util.manhattanDistance(newPos, ghost.getPosition()))
        gridSize = newFood.width + newFood.height
        if ma > 2:
            return 2 + 1.0/(gridSize*len(L)+mi+1)
        else:
            return ma + 1.0/(gridSize*len(L)+mi+1)
    
        return successorGameState.getScore()

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

    def dfs(self, gameState, agentIndex, k, n):
        v = 0
        if agentIndex == 0:
            v = -999999
        else:
            v = 999999
        bestAction = 0
        if k == 0:
            return (self.evaluationFunction(gameState), bestAction)
        elif k != 0 and agentIndex == n-1:
            actions = gameState.getLegalActions(agentIndex)
            if len(actions) == 0:
                return (self.evaluationFunction(gameState), 0)
            for act in actions:
                succ = gameState.generateSuccessor(agentIndex, act)
                (x, y) = self.dfs(succ, 0, k-1, n)
                if v > x:
                    v = x
                    bestAction = act

            return (v, bestAction)
        else:
            actions = gameState.getLegalActions(agentIndex)
            if len(actions) == 0:
                return (self.evaluationFunction(gameState), bestAction)
            if agentIndex == 0:
                for act in actions:
                    succ = gameState.generateSuccessor(agentIndex, act)
                    (x, y) = self.dfs(succ, agentIndex+1, k, n)
                    if v < x:
                        v = x
                        bestAction = act

                return (v, bestAction)
            else:
                for act in actions:
                    succ = gameState.generateSuccessor(agentIndex, act)
                    (x, y) = self.dfs(succ, agentIndex+1, k, n)
                    if v > x:
                        v = x
                        bestAction = act

                return (v, bestAction)

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        n = gameState.getNumAgents()
        (x, y) = self.dfs(gameState, 0, self.depth, n)
        print(x)
        return y
        util.raiseNotDefined()
            

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def dfs(self, gameState, agentIndex, k, n, alpha, beta):
        v = 0
        if agentIndex == 0:
            v = -999999
        else:
            v = 999999
        nalpha = alpha
        nbeta = beta
        bestAction = 0
        if k == 0:
            return (self.evaluationFunction(gameState), bestAction)
        elif k != 0 and agentIndex == n-1:
            actions = gameState.getLegalActions(agentIndex)           
            if len(actions) == 0:
                return (self.evaluationFunction(gameState), bestAction)
            for act in actions:
                succ = gameState.generateSuccessor(agentIndex, act)
                (x, y) = self.dfs(succ, 0, k-1, n, nalpha, nbeta)
                if v > x:
                    v = x
                    bestAction = act
                if v < nalpha:
                    return (v, bestAction)
                nbeta = min(nbeta, v)
                
            return (v, bestAction)
        else:
            actions = gameState.getLegalActions(agentIndex)
            if len(actions) == 0:
                return (self.evaluationFunction(gameState), 0)
            if agentIndex == 0:
                for act in actions:
                    succ = gameState.generateSuccessor(agentIndex, act)
                    (x, y) = self.dfs(succ, agentIndex+1, k, n, nalpha, nbeta)
                    if v < x:
                        v = x
                        bestAction = act
                    if v > nbeta:
                        return (v, bestAction)
                    nalpha = max(nalpha, v)
                return (v, bestAction)
            else:
                for act in actions:
                    succ = gameState.generateSuccessor(agentIndex, act)
                    (x, y) = self.dfs(succ, agentIndex+1, k, n, nalpha, nbeta)
                    if v > x:
                        v = x
                        bestAction = act
                    if v < nalpha:
                        return (v, bestAction)
                    nbeta = min(nbeta, v)
                
                return (v, bestAction)

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        n = gameState.getNumAgents()
        (x, y) = self.dfs(gameState, 0, self.depth, n, -999999, 999999)
        print(x)
        return y
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def dfs(self, gameState, agentIndex, k, n):
        v = 0.0
        if agentIndex == 0:
            v = -999999
        else:
            v = 0.0
        bestAction = 0
        if k == 0:
            return (self.evaluationFunction(gameState), bestAction)
        elif k != 0 and agentIndex == n-1:
            actions = gameState.getLegalActions(agentIndex)
            if len(actions) == 0:
                return (self.evaluationFunction(gameState), 0)
            for act in actions:
                succ = gameState.generateSuccessor(agentIndex, act)
                (x, y) = self.dfs(succ, 0, k-1, n)
                v += x

            return ((v+0.0)/(len(actions)+0.0), bestAction)
        else:
            actions = gameState.getLegalActions(agentIndex)
            if len(actions) == 0:
                return (self.evaluationFunction(gameState), bestAction)
            if agentIndex == 0:
                for act in actions:
                    succ = gameState.generateSuccessor(agentIndex, act)
                    (x, y) = self.dfs(succ, agentIndex+1, k, n)
                    if v < x:
                        v = x
                        bestAction = act

                return (v, bestAction)
            else:
                for act in actions:
                    succ = gameState.generateSuccessor(agentIndex, act)
                    (x, y) = self.dfs(succ, agentIndex+1, k, n)
                    v += x

                return ((v+0.0)/(len(actions)+0.0), bestAction)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        n = gameState.getNumAgents()
        (x, y) = self.dfs(gameState, 0, self.depth, n)
        return y
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    capsules = currentGameState.getCapsules()

    li = food.asList(True)
    mi = 999999
    ma = 999999
    ca = 999999
    gridSize = food.width*food.height
    foodNum = len(li)
    capsulesNum = len(capsules)
    if len(li) == 0:
        mi = 0
    for fo in li:
        mi = min(mi, util.manhattanDistance(pos, fo))
    for gh in ghostStates:
        ma = min(ma, util.manhattanDistance(pos, gh.getPosition()))
    if len(capsules) == 0:
        ca = 0
    for cp in capsules:
        ca = min(ca, util.manhattanDistance(pos, cp))

    score = currentGameState.getScore()
    return score
    if ma > 3:
        return 3 + 1.0/(capsulesNum + 1) + gridSize - foodNum + min(scaredTimes) + 1.0/(mi+1) + score 
    else:
        return ma + 1.0/(capsulesNum + 1) + gridSize - foodNum + min(scaredTimes) + 1.0/(mi+1) + score
    

    #e = -mi - gridSize*len(li) + ma/gridSize
    #return e
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

