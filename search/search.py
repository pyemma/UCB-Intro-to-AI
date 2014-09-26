# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

class SearchNode:
    """
    Defination of a SearchNode, which contains the necessory informaion, like
    current node, parent node, and the cust might be used in UCS or A*
    """
    def __init__(self, cur, par, direction, cost):
        self.current = cur
        self.parent = par
        self.direction = direction
        self.cost = cost

    def getCost(self):
        return self.cost

    def getDirection(self):
        return self.direction

    def getState(self):
        return self.current

    def getParent(self):
        return self.parent

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    stack = util.Stack()
    
    from game import Directions
    
    node = SearchNode(start, None, Directions.STOP, 0)
    stack.push(node)
    visitedstates = set()
    actions = []
    while(stack.isEmpty() == False):
        node = stack.pop()
        current = node.getState()
        if current in visitedstates:
            continue
        
        if problem.isGoalState(current):
            while(node.getDirection() != Directions.STOP):
                actions.append(node.getDirection())
                node = node.getParent()
            actions.reverse()
            break;
        # only mark the poped state, since the other one on the stack should not be visited yet
        visitedstates.add(current);
        for triples in problem.getSuccessors(current):
            if not triples[0] in visitedstates:
                nn = SearchNode(triples[0], node, triples[1], triples[2]+node.getCost());
                stack.push(nn);
        
    return actions;
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState();
    queue = util.Queue();
    
    from game import Directions
    
    node = SearchNode(start, None, Directions.STOP, 0);
    queue.push(node)
    visitedstates = set()
    visitedstates.add(start)
    actions = [];
    while(queue.isEmpty() == False):
        node = queue.pop()
        current = node.getState()
        if problem.isGoalState(current):
            while(node.getDirection() != Directions.STOP):
                actions.append(node.getDirection())
                node = node.getParent()
            actions.reverse()
            break
        
        for triples in problem.getSuccessors(current):
            if not triples[0] in visitedstates:
                # mark the state in order to avoid visit it twice
                visitedstates.add(triples[0])
                nn = SearchNode(triples[0], node, triples[1], triples[2]+node.getCost())
                queue.push(nn)
        
    return actions
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    queue = util.PriorityQueue()

    from game import Directions
    node = SearchNode(start, None, Directions.STOP, 0)
    queue.push(node, 0)
    visitedstates = set()
    actions = []
    while(queue.isEmpty() == False):
        node = queue.pop()
        current = node.getState()
        if problem.isGoalState(current):
            while(node.getDirection() != Directions.STOP):
                actions.append(node.getDirection())
                node = node.getParent()
            actions.reverse()
            break
        # the node poped out would be the min-cost to the state, no futher path could
        # give a smaller path
        visitedstates.add(current)
        for triples in problem.getSuccessors(current):
            if not triples[0] in visitedstates:
                nn = SearchNode(triples[0], node, triples[1], triples[2]+node.getCost())
                queue.push(nn, nn.getCost())
        
    return actions
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    queue = util.PriorityQueue()

    from game import Directions
    node = SearchNode(start, None, Directions.STOP, 0);
    queue.push(node, 0 + heuristic(start, problem))
    visitedstates = set()
    actions = [];
    while(queue.isEmpty() == False):
        node = queue.pop()
        current = node.getState()
        if current in visitedstates:
            continue
        if problem.isGoalState(current):
            while(node.getDirection() != Directions.STOP):
                actions.append(node.getDirection())
                node = node.getParent()
            actions.reverse()
            break
        # the node poped out would be the min-cost to the state, no futher path could
        # give a smaller path
        visitedstates.add(current)
        for triples in problem.getSuccessors(current):
            if not triples[0] in visitedstates:
                nn = SearchNode(triples[0], node, triples[1], triples[2]+node.getCost())
                queue.push(nn, nn.getCost() + heuristic(triples[0], problem))
        
    return actions
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
