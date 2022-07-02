#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from queue import Queue

Item = namedtuple("Item", ['index', 'value', 'weight', 'price'])


# Class for Dog
class Node:
    # The init method or constructor
    def __init__(self, level, value, weight, upper_bound):
        # Instance Variable
        self.level = level
        self.value = value
        self.weight = weight
        self.bound = upper_bound
        self.contains = []


def lowerbound(item_count, capacity, items):
    total_weight = 0
    value_bound = 0
    j = 0

    while j < item_count and total_weight + items[j].weight <= capacity:
        total_weight += items[j].weight
        value_bound += items[j].value
        j += 1

    return value_bound


def upperbound(node, item_count, capacity, items):
    if node.weight > capacity:
        return 0

    total_weight = node.weight
    value_bound = node.value
    j = node.level + 1

    while j < item_count and total_weight + items[j].weight <= capacity:
        total_weight += items[j].weight
        value_bound += items[j].value
        j += 1

    if j < item_count:
        value_bound += (capacity - total_weight)*(items[j].value/items[j].weight)

    return value_bound


def solve_it(input_dat):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_dat.split('\n')

    first_line = lines[0].split()
    item_count = int(first_line[0])
    capacity = int(first_line[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1]), int(parts[0])/int(parts[1])))

    # small(easy) problem
    # use dynamic programming to find the optimal solution
    # large scale problem
    # use branch&bound to find the approximate solution
    taken = [0] * item_count

    if item_count <= 200:
        # create a memo matrix to store value
        memo = [[0 for j in range(capacity + 1)] for i in range(item_count + 1)]

        # build upon the memo matrix
        for i in range(item_count):
            for j in range(capacity + 1):
                if j < items[i].weight:
                    memo[i + 1][j] = memo[i][j]
                else:
                    memo[i + 1][j] = max(memo[i][j], memo[i][j - items[i].weight] + items[i].value)

        # knapsack reconstruction process
        rem_cap = capacity
        for i in range(item_count, 0, -1):
            if items[i - 1].weight <= rem_cap:
                if memo[i - 1][rem_cap - items[i - 1].weight] + items[i - 1].value >= memo[i][rem_cap]:
                    taken[i - 1] = 1
                    rem_cap = rem_cap - items[i - 1].weight

        value = memo[item_count][capacity]
    else:
        # branch & bound implementation
        # sort the item by the value per weight
        items = sorted(items, key=lambda x: x.price, reverse=True)

        # max_profit is the lower bound
        max_profit = lowerbound(item_count, capacity, items)
        best_items = []

        # create a dummy node to start up the bst
        node = Node(-1, 0, 0, 0)

        # push element to the queue
        q = Queue()
        q.put(node)

        while not q.empty():
            v = Node(0, 0, 0, 0)
            u = q.get()
            # if starting node, assign level 0
            # if reach the end, skip the rest code
            if u.level == -1:
                v.level = 0
            elif u.level == item_count - 1:
                continue
            else:
                # else increment the level
                v.level = u.level + 1

            v.weight = u.weight + items[v.level].weight
            v.value = u.value + items[v.level].value
            v.contains = list(u.contains)
            v.contains.append(items[v.level].index)

            if v.weight <= capacity and v.value > max_profit:
                max_profit = v.value
                best_items = v.contains

            # compute the upper bound
            v.bound = upperbound(v, item_count, capacity, items)

            # compare upper bound and max_profit(lower bound)
            if v.bound > max_profit:
                q.put(v)

            # Do the same thing but
            # without taking items in the knapsack
            v = Node(0, 0, 0, 0)
            v.level = u.level + 1
            v.weight = u.weight
            v.value = u.value
            v.contains = list(u.contains)

            v.bound = upperbound(v, item_count, capacity, items)
            if v.bound > max_profit:
                q.put(v)

        value = max_profit

        for i in range(len(best_items)):
            taken[best_items[i]] = 1

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


'''
if __name__ == '__main__':
    file_location = "./data/ks_4_0"
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    print(solve_it(input_data))
'''
if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file. '
              'Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
