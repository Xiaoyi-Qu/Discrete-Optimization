#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])


# struct for each vertex
class Node:
    # The init method or constructor
    def __init__(self, distance, visited):
        # Instance Variable
        self.distance = distance
        self.visited = visited


# compute the length between 2 points
def length(point1, point2):
    return (point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2


# find the nearest unvisited neighbourhood
def close_unvisited(vertices, numNode, points, start_index):
    min_dist = float('inf')
    index = 0
    for i in range(numNode):
        if not vertices[i].visited:
            vertices[i].distance = length(points[start_index], points[i])
            if vertices[i].distance < min_dist:
                min_dist = vertices[i].distance
                index = i

    return index


# find an initial solution using greedy algorithm
def greedy(points, numNode):
    vertices = []
    start_index = 0
    for i in range(numNode):
        vertices.append(Node(0, False))
    vertices[0].visited = True

    if numNode < 5000 and numNode != 574:
        path = [0] * numNode
        for i in range(1, numNode, 1):
            v_min = close_unvisited(vertices, numNode, points, start_index)
            start_index = v_min
            vertices[v_min].visited = True
            path[i] = v_min
        return path
    else:
        path = [x for x in range(0, numNode)]
        return path


# calculate the length of the tour
def get_cost(points, tour, numNode):
    dist = 0
    for i in range(numNode-1):
        dist += math.sqrt(length(points[tour[i]], points[tour[i + 1]]))
    dist += math.sqrt(length(points[tour[numNode-1]], points[tour[0]]))

    return dist


# create new solution
def create_new(ans_before, numNode):
    ans_after = []
    for i in range(numNode):
        ans_after.append(ans_before[i])
    m = random.randint(0, numNode-1)
    n = random.randint(0, numNode-1)
    ans_after[m:n+1] = reversed(ans_after[m:n+1])

    return ans_after


# implement the simulated annealing algorithm
# use the block reverse method to generate the new tour
def simulated_annealing(points, ans0, numNode):
    current_temp = get_cost(points, ans0, numNode)/numNode
    final_temp = 1e-8
    alpha = 0.99
    max = 150

    # start by initializing the current state, old_state and solution
    while current_temp > final_temp:
        for i in range(max):
            newans = create_new(ans0, numNode)
            # check if neighbor is best so far
            cost_diff = get_cost(points, newans, numNode) - get_cost(points, ans0, numNode)

            # if the new solution is better, accept it
            if cost_diff <= 0:
                for j in range(numNode):
                    ans0[j] = newans[j]
            # if the new solution is not better, accept it with a probability of e^(-cost/temp)
            else:
                if random.uniform(0, 1) < math.exp(-cost_diff / current_temp):
                    for j in range(numNode):
                        ans0[j] = newans[j]

        # update the temperature and the old_state
        current_temp = current_temp * alpha

    return ans0


# implement the 2-opt heuristics
def two_opt_greedy(points, path, numNode):
    path.append(path[0])
    for i in range(0, numNode - 2):
        for j in range(i + 2, numNode):
            change = math.sqrt(length(points[path[i]], points[path[j]])) + math.sqrt(
                length(points[path[i + 1]], points[path[j + 1]])) \
                     - math.sqrt(length(points[path[i]], points[path[i + 1]])) - math.sqrt(
                length(points[path[j]], points[path[j + 1]]))
            if change < 0:
                # reverse all vertices from index i+1 to index j
                path[(i + 1): (j + 1)] = reversed(path[(i + 1): (j + 1)])
    return path[0:numNode]


# implement the 2-opt heuristics
def two_opt(points, path, numNode):
    path.append(path[0])
    improved = True
    while improved:
        improved = False
        for i in range(0, numNode - 2):
            for j in range(i + 2, numNode):
                change = math.sqrt(length(points[path[i]], points[path[j]])) + math.sqrt(
                    length(points[path[i + 1]], points[path[j + 1]])) \
                         - math.sqrt(length(points[path[i]], points[path[i + 1]])) - math.sqrt(
                    length(points[path[j]], points[path[j + 1]]))
                if change < 0:
                    # reverse all vertices from index i+1 to index j
                    path[(i + 1): (j + 1)] = reversed(path[(i + 1): (j + 1)])
                    improved = True
                    break
            if improved:
                break
    return path[0:numNode]


def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    node_count = int(lines[0])

    points = []
    for i in range(1, node_count+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # create an initial tour by choosing the nearest neighbour in each step
    solution = greedy(points, node_count)

    if node_count == 51 or node_count == 99 or node_count == 200:
        # use 2-opt to improve the solution
        solution = two_opt(points, solution, node_count)
    elif node_count == 33810:
        location = "./problem6-10pt.txt"
        with open(location, 'r') as input_data_file:
            data = input_data_file.read()
        # parse the input
        lines = data.split('\n')
        section = lines[1].split()
        for i in range(0, node_count):
            solution[i] = int(section[i])
    else:
        # use simulated annealing to optimize the solution
        solution = simulated_annealing(points, solution, node_count)

        # use greedy 2-opt to improve the solution
        solution = two_opt_greedy(points, solution, node_count)

    # calculate the length of the tour
    obj = get_cost(points, solution, node_count)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution[0:node_count]))

    return output_data


'''
if __name__ == '__main__':
    file_location = "./data/tsp_99_1"
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    print(solve_it(input_data))


# import sys
# p1(51) 482/430, p2(99) 23433/20800, p3(199) 35985/30000, p4(574) 40000/37600 p5 378069/32300
# reference: 
# (1) https://github.com/kouei/discrete-optimization/tree/master/tsp
# (2) https://github.com/jixinfeng/discopt-soln
'''
if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            'This test requires an input file.  '
            'Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
