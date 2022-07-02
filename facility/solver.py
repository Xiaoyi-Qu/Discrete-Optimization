#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
import gurobipy as gp
from gurobipy import GRB

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    # use Gurobi commercial solver to solve this problem
    # https://blog.csdn.net/weixin_41596280/article/details/89112302

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    dist = [[0] * customer_count for i in range(facility_count)]
    # create the matrix
    for i in range(facility_count):
        for j in range(customer_count):
            dist[i][j] = length(facilities[i].location, customers[j].location)

    # create the model
    model = gp.Model("Work Schedule")
    model.setParam('TimeLimit', 5 * 60)

    # add variables
    x = model.addVars(facility_count, vtype=GRB.BINARY, name="facility")
    y = model.addVars(facility_count, customer_count, vtype=GRB.BINARY, name="customer")

    # integrate variables
    model.update()

    # add objective function
    # gp.quicksum(facilities[i].setup_cost*x[i] for i in range(facility_count)) +
    model.setObjective(gp.quicksum(facilities[i].setup_cost*x[i] for i in range(facility_count)) +\
        gp.quicksum(y[i,j] * dist[i][j] for i in range(facility_count) for j in range(customer_count)))

    # add constraints
    for i in range(facility_count):
        model.addConstrs(y[i, j] <= x[i] for j in range(customer_count))
    model.addConstrs(gp.quicksum(y[i,j] for i in range(facility_count)) == 1 for j in range(customer_count))
    model.addConstrs(gp.quicksum(y[i,j] * customers[j].demand for j in range(customer_count)) <= facilities[i].capacity
                     for i in range(facility_count))

    # redundant constraints but helpful to LP relaxation
    # add this later on
    model.optimize()

    # store the solution
    # https://www.gurobi.com/documentation/8.1/refman/attributes.html
    # X represents the value in the current solution
    solution = [0]*customer_count
    total_cost = model.getObjective().getValue()
    for i in range(facility_count):
        for j in range(customer_count):
            if y[i, j].x == 1:
                solution[j] = i

    '''
    # build a trivial solution
    # pack the facilities one by one until all the customers are served
    solution = [-1]*len(customers)
    capacity_remaining = [f.capacity for f in facilities]

    facility_index = 0
    for customer in customers:
        if capacity_remaining[facility_index] >= customer.demand:
            solution[customer.index] = facility_index
            capacity_remaining[facility_index] -= customer.demand
        else:
            facility_index += 1
            assert capacity_remaining[facility_index] >= customer.demand
            solution[customer.index] = facility_index
            capacity_remaining[facility_index] -= customer.demand

    used = [0]*len(facilities)
    for facility_index in solution:
        used[facility_index] = 1

    # calculate the cost of the solution
    obj = sum([f.setup_cost*used[f.index] for f in facilities])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)
    '''

    # prepare the solution in the specified output format
    output_data = '%.2f' % total_cost + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

'''
if __name__ == '__main__':
    file_location = "./data/fl_3_1"
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    print(solve_it(input_data))
# import sys
'''
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

