#!/usr/bin/python
# -*- coding: utf-8 -*-
# The code is based on the idea of iterated greedy algorithm

import numpy as np


def greedy(graph, node_list, node_count):
    solution = [-1] * node_count

    # store the color used before
    current_color = []

    # assign the first color to first vertex
    solution[node_list[0]] = 0
    current_color.append(0)

    '''
    First step: figure out adjacent color for each vertex
    Second step: divide into two cases
                 (a) select color in the current_color list
                 (b) select color not in the current_color list
    '''
    for i in range(1, node_count):
        adj_color = set()
        for j in range(0, len(graph[node_list[i]])):
            if solution[graph[node_list[i]][j]] != -1:
                adj_color.add(solution[graph[node_list[i]][j]])
        if len(adj_color) == len(current_color):
            new_color = len(current_color)
            current_color.append(new_color)
            solution[node_list[i]] = new_color
        else:
            # find the smallest index in current_color that does not appear in adj_color
            for k in range(len(current_color)-1, -1, -1):
                if current_color[k] in adj_color:
                    continue
                else:
                    solution[node_list[i]] = current_color[k]
    return solution


def solve_it(input_dataset):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_dataset.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    # store the graph information in the list
    graph = [[] for i in range(node_count)]
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        graph[int(parts[0])].append(int(parts[1]))
        graph[int(parts[1])].append(int(parts[0]))

    # create a dictionary to store the degree
    degree = dict()
    for i in range(0, node_count):
        degree[i] = len(graph[i])

    # find an initial approximate solution
    node_list = range(0, node_count)
    solution = greedy(graph, node_list, node_count)

    counter = 0
    while counter < 10:
        # group nodes by color
        num_color = len(set(solution))
        group_node = [[] for i in range(num_color)]
        for i in range(0, node_count):
            group_node[solution[i]].append(i)

        # randomly pick one group
        # sort the subset by degree in descending order
        node_list = []
        permuted_seq = np.random.permutation(range(0, num_color))
        for i in range(0, num_color):
            node_list = node_list + sorted(group_node[permuted_seq[i]], key=lambda ele: degree[ele], reverse=True)

        # perform the greedy algorithm
        solution = greedy(graph, node_list, node_count)
        counter = counter + 1

    # prepare the solution in the specified output format
    output_data = str(len(set(solution))) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


'''
if __name__ == '__main__':
    file_location = "./data/gc_4_1"
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    print(solve_it(input_data))
'''

# import sys
if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  '
              'Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')
