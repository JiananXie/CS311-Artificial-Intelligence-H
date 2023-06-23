from hmac import new
import math
from multiprocessing import parent_process

import numpy as np
import queue
from math import sqrt

import numpy.linalg
from utils.logger import logger
import heapq
from utils.timer import time_controller


class ProblemSolvingAgent:
    """
    Problem Solving Agent is a kind of goal-based agent who
    treat the environment as atomic states. The goal of the 
    Problem Solving Agent is to find a sequence of actions that
    will lead to the goal state from the initial state.
    """

    # DepthFirstSearch, BreadthFirstSearch, UniformCostSearch(Dijkstra), Greedy BestFirstSearch, Astar  
    supported_algorithms = ['DFS', 'BFS', 'UCS', 'GBFS', 'Astar']
    algorithm_indexes = {name: i for i, name in enumerate(supported_algorithms)}

    def solve_by_searching(self, obstacles, start_pos, goal_pos, algorithm='DFS'):
        """Let the agent solve problem by searching path on the graph. 
        Args:
            obstacles (set of bi-tuples): 
                Obstacles represents the graph information of the grid map, 
                by a set of points called obstacles.
                At any coordinate, you are allowed to move to 
                any node nearby that is not in the obstacles.
                When coding, you can use self.neighbours(obstacles, node) 
            start_pos (bi-tuples): the position of initial state. 
            goal_pos (bi-tuples): the position of goal state.
            algorithm (str, optional): The strategy applied by the agent. 
                Defaults to 'DFS'.
        Returns: tuple (path, visited)
            path (list of bi-tuples): the path chosen by the algorithm 
                to navigate from initial position to the goal position
            visited(list of bi-tuples): the position checked by the agent 
                during the searching process. 
        """
        logger.info(f'The agent starts using {algorithm} for searching. ')
        time_controller.start_to_time()
        index = ProblemSolvingAgent.algorithm_indexes[algorithm]
        path, visited = [self.DFS, self.BFS, self.UCS, self.GBFS, self.Astar][index](obstacles, start_pos, goal_pos)
        logger.info(f'The agent successfully searched a path! ')
        logger.info(f'Agent finishes after {time_controller.get_time_used()}s of computing. ')
        return path, visited

    def GBFS(self, obstacles, start_pos, goal_pos):
        path, visited = [], []
        parent = {}
        closed = [start_pos]
        frontier = [(self.euclidean_distance(start_pos, goal_pos), (start_pos, 0))]
        while len(frontier) != 0:
            state = heapq.heappop(frontier)
            visited.append(state[1][0])
            if goal_pos == state[1][0]:
                break
            for neighbor in self.neighbours_of(obstacles, state[1][0]):
                if neighbor[0] not in closed:
                    parent[neighbor[0]] = state[1][0]
                    heapq.heappush(frontier, (self.euclidean_distance(goal_pos, neighbor[0]), neighbor))
                    closed.append(neighbor[0])
            path = self.parents2path(parent, goal_pos, start_pos)
        return path, visited

    def Astar(self, obstacles, start_pos, goal_pos):
        path, visited = [], []
        parent = {}
        closed = [start_pos]
        frontier = [[self.euclidean_distance(start_pos, goal_pos), start_pos]]
        while len(frontier) != 0:
            state = heapq.heappop(frontier)
            visited.append(state[1])
            if goal_pos == state[1]:
                break
            for neighbor in self.neighbours_of(obstacles, state[1]):
                if neighbor[0] not in closed:
                    parent[neighbor[0]] = state[1]
                    heapq.heappush(frontier, [neighbor[1] + state[0] - self.euclidean_distance(state[1], goal_pos) + self.euclidean_distance(neighbor[0], goal_pos), neighbor[0]])
                    closed.append(neighbor[0])
                elif neighbor[0] not in visited:
                    for node in frontier:
                        if node[1] == neighbor[0]:
                            if node[0] > state[0] + neighbor[1] - self.euclidean_distance(state[1],goal_pos) + self.euclidean_distance(neighbor[0], goal_pos):
                                parent[neighbor[0]] = state[1]
                                node[0] = state[0] + neighbor[1] - self.euclidean_distance(state[1],goal_pos) + self.euclidean_distance(neighbor[0], goal_pos)
        path = self.parents2path(parent, goal_pos, start_pos)
        return path, visited

    def DFS(self, obstacles, start_pos, goal_pos):
        path, visited = [], []
        parent = {}
        frontier = [start_pos]
        closed = [start_pos]
        frontier.append(start_pos)
        while len(frontier) != 0:
            state = frontier.pop()
            visited.append(state)
            if goal_pos == state:
                break
            for neighbor in self.neighbours_of(obstacles, state):
                if neighbor[0] not in closed:
                    parent[neighbor[0]] = state
                    closed.append(neighbor[0])
                    frontier.append(neighbor[0])
        path = self.parents2path(parent, goal_pos, start_pos)
        return path, visited

    def BFS(self, obstacles, start_pos, goal_pos):
        path, visited = [], []
        parent = {}
        frontier = [start_pos]
        closed = [start_pos]
        while len(frontier) != 0:
            state = frontier[0]
            frontier.remove(state)
            visited.append(state)
            if goal_pos == state:
                break
            for neighbor in self.neighbours_of(obstacles, state):
                if neighbor[0] not in closed:
                    parent[neighbor[0]] = state
                    closed.append(neighbor[0])
                    frontier.append(neighbor[0])
        path = self.parents2path(parent, goal_pos, start_pos)
        return path, visited

    def UCS(self, obstacles, start_pos, goal_pos):
        path, visited = [], []
        parent = {}
        closed = [start_pos]
        frontier = [[0, (start_pos, 0)]]
        while len(frontier) != 0:
            state = heapq.heappop(frontier)
            visited.append(state[1][0])
            if goal_pos == state[1][0]:
                break
            for neighbor in self.neighbours_of(obstacles, state[1][0]):
                if neighbor[0] not in closed:
                    parent[neighbor[0]] = state[1][0]
                    heapq.heappush(frontier, [neighbor[1] + state[0], neighbor])
                    closed.append(neighbor[0])
                elif neighbor[0] not in visited:
                    for node in frontier:
                        if node[1][0] == neighbor[0]:
                            if node[0] > state[0] + neighbor[1]:
                                parent[neighbor[0]] = state[1][0]
                                node[0] = state[0] + neighbor[1]
            path = self.parents2path(parent, goal_pos, start_pos)
        return path, visited

    def neighbours_of(self, obstacles, node):
        """_summary_

        Args:
            obstacles (_type_): _description_
            node (_type_): _description_
        Returns: iterable generator of tuple(neighbour, moving_cost)
            neighbour(bi-tuple): a position near to the node. 
            moving_cost(float): the cost the agent has to pay to move from node to neighbour. 
        """
        directions = [[1, 0, 1], [0, 1, 1], [-1, 0, 1], [0, -1, 1],
                      [-1, -1, math.sqrt(2)], [-1, 1, math.sqrt(2)], [1, -1, math.sqrt(2)], [1, 1, math.sqrt(2)]]
        return filter(lambda nm: nm[0] not in obstacles
                      , map(lambda d: ((node[0] + d[0], node[1] + d[1]), d[2]), directions))

    def euclidean_distance(self, node1, node2, coefficient=1):
        """The Euclidean distance between two nodes.
        Args:
            node1 (bi-tuple): a point in 2d grid map. 
            node2 (bi-tuple): another point in 2d grid map. 
            coefficient (int, optional): The coefficient for decision. Defaults to 1.
        Returns:
            d: the distance value. 
        """
        return coefficient * sqrt(sum((x - y) ** 2 for x, y in zip(node1, node2)))

    def parents2path(self, parents, last_node, start_pos):
        """The function generates the path found by searching algorithm. 
        Args:
            parents (dict): given a node in the graph, return the predecessor of the node in the path. 
                For example, a->b->c is a path found by BFS, then parents should be {c:b, b:a, a:None} .
            last_node (bi-tuple): in the example, the last_node is c. 

        Returns:
            path: in the example, the generated path is [a, b, c]. 
        """
        path = [last_node]
        while last_node in parents:
            predecessor = parents[last_node]
            path.append(predecessor)
            last_node = predecessor
            if last_node == start_pos:
                break
        path.reverse()
        return path

    def inner_product(self, a, b):
        return sum(x * y for x, y in zip(a, b))
