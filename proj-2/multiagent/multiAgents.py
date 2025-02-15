# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # print scores
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
        # for ghosts
        newGhostPositions = [i.getPosition() for i in newGhostStates]
        newGhostDists = [manhattanDistance(newPos, i) for i in newGhostPositions]

        if 0 not in newScaredTimes and newScaredTimes[0] > 3: # if ghost is scared, then go towards it, but not go too near to it
            newGhostDistsScore = max(newGhostDists)
        else:
            newGhostDistsScore = min(newGhostDists)

        # for food
        newFoodDis = 0 # initialize with 0, suppose agent eats some food
        if successorGameState.data._foodEaten == None:
            newFoodPos = []
            for (x, row) in enumerate(newFood): # check food position in new state
                for (y, item) in enumerate(row):
                    if item == True:
                        newFoodPos.append((x,y))
            newFoodDis = sum(map(lambda x: manhattanDistance(x, newPos), newFoodPos))
            # if newGhostDistsScore > 3: # if ghost is too far, eat food first!
                # newFoodDis = min(map(lambda x: manhattanDistance(x, newPos), newFoodPos))

        # TODO: hard to deal with multiple ghosts

        return newGhostDistsScore * 1. / (newFoodDis + 0.01) # penalize food distance

        # return newGhostDistsScore * successorGameState.getScore() # incorrect, as state score could be negative
        # return successorGameState.getScore()

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

    def MinimaxFunction(self, MAXGameState, depth):
        """
          Min-Max Function
          return action based on depth and self.evaluationFunction
        """
        MAXScore = None # MAX score

        # for agent's move
        legalMoves = MAXGameState.getLegalActions()
        # if Directions.STOP in legalMoves:
        #     legalMoves.remove(Directions.STOP)

        if len(legalMoves) == 0:
            return self.evaluationFunction(MAXGameState)

        MINGameStatesWithAction = [(MAXGameState.generateSuccessor(0, legalMove), legalMove) for legalMove in legalMoves] # I don't know why here, it needs to change from genPac to gen
        MINScores = []
        # print 'MINGameStatesWithAction: {0}'.format(MINGameStatesWithAction)

        for MINGameState, initAction in MINGameStatesWithAction:
            if depth == self.depth:
                MINScores.append(self.evaluationFunction(MINGameState))
            else:
                currentScores = []
                curMINGameStates = [MINGameState]
                for ghostID in self.ghostIDs: # something wrong here
                    [curMINGameState.getLegalActions(ghostID) for curMINGameState in curMINGameStates]
                    actions = MINGameState.getLegalActions(ghostID)
                    if len(actions) != 0:
                        for action in actions:
                            nextMAXGameState = MINGameState.generateSuccessor(ghostID, action)
                            next_score = self.MinimaxFunction(nextMAXGameState, depth+1)
                            currentScores.append(next_score)
                # print "depth: {0}, currentScores: {1}".format(depth, currentScores)
                if len(currentScores) != 0:
                    MINScores.append(min(currentScores))
                else:
                    MINScores.append(self.evaluationFunction(MINGameState))

        # print "depth: {0}, MINScores: {1}".format(depth, MINScores)
        bestScore = max(MINScores)
        bestIndices = [index for index in range(len(MINScores)) if MINScores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        actionChosen = MINGameStatesWithAction[chosenIndex][1]
        
        if depth == 1:
            return bestScore, actionChosen
        else:
            return bestScore

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
        self.ghostIDs = range(1, gameState.getNumAgents())

        score, action = self.MinimaxFunction(gameState, 1)
        print "current score estimated: {0}, suggested action: {1}".format(score, action)
        return action
        # return legalMoves[random.randint(0, len(legalMoves)-1)]
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
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

