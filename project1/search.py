# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    frontier = util.Stack()
    state = problem.getStartState()
    frontier.push((state,[]))
    expanded = set()

    while not frontier.isEmpty():
        state, path = frontier.pop()

        if problem.isGoalState(state):
            return path

        if state not in expanded:
            expanded.add(state)
            successors = problem.expand(state)
            for child in successors:
                    frontier.push( (child[0], path + [child[1]]) ) # child[0]:state & child[1]:action
    return [] # Failure

def breadthFirstSearch(problem):
    frontier = util.Queue()
    state = problem.getStartState()
    frontier.push((state,[]))
    expanded = set()

    while not frontier.isEmpty():
        state, path = frontier.pop()

        if problem.isGoalState(state):
            return path

        if state not in expanded:
            expanded.add(state)
            successors = problem.expand(state)
            for child in successors:
                    frontier.push( (child[0], path + [child[1]]) ) # child[0]:state & child[1]:action
    return [] # Failure

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    state = problem.getStartState()
    frontier = util.PriorityQueue()
    actions_list = []
    start_node  = (state, actions_list) # tuple holds: coordinates [5,5], empty list to actions path
    frontier.push(start_node, heuristic(state,problem))
    explored = [] 

    while not frontier.isEmpty():
        state, directions = frontier.pop()

        if problem.isGoalState(state):
            return directions

        if state not in explored:
            explored.append(state)
            successors = problem.expand(state)
            for child in successors:
                if not child[0] in explored: # child[0] are coordinates e.g [5,5]
                    actions_list = directions + [child[1]] # child[1] is the next action if we choose the node
                    g_cost = problem.getCostOfActionSequence(actions_list)
                    h_cost = heuristic(child[0],problem)
                    f_cost = h_cost + g_cost
                    next_node = (child[0], actions_list)
                    frontier.push(next_node, f_cost)
    return [] # Failure

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
