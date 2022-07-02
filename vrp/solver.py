#!/usr/bin/python
# -*- coding: utf-8 -*-
# (1)387/280 (2)1019/630 (3)713/540 (4)1193/830 (5)3719/1400 (6)2392
# three main goals:
# add a time constraint
# check the correctness of shift function

import math
import itertools
import vrp as vrp
from collections import namedtuple
from time import time

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])


# calculate the distance between two locations
def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x) ** 2 + (customer1.y - customer2.y) ** 2)


# check if the tour is valid or not
def is_valid_tour(tour, customers, capacity):
    total_demand = 0
    for i in range(len(tour) - 1):
        total_demand += customers[tour[i].index].demand
    is_valid = (total_demand <= capacity)
    return is_valid


# calculate the tour distance
def single_tour_dist(tour, customers, capacity):
    if not is_valid_tour(tour, customers, capacity):
        return math.inf
    tour_dist = 0
    for i in range(1, len(tour)):
        customer_1 = customers[tour[i - 1].index]
        customer_2 = customers[tour[i].index]
        tour_dist += length(customer_1, customer_2)
    return tour_dist


# input:
#       tours(the greedy solution)
#       i_from(the index of the tour shift from)
#       start_from(start index of the segment)
#       end_from(end index of the segment)
#       i_to(the index of the tour shift to)
#       j_to(end of the segment on the shift to tour)
def shift(tours, customers, capacity, i_from, start_from, end_from, i_to, j_to):
    improved = False
    tour1_old = tours[i_from]
    tour2_old = tours[i_to]
    tour1_old_dist = single_tour_dist(tour1_old, customers, capacity)
    tour2_old_dist = single_tour_dist(tour2_old, customers, capacity)
    seg_shift = tour1_old[start_from: end_from + 1]

    tour1_new = tour1_old[:start_from] + tour1_old[end_from + 1:]
    tour2_new1 = tour2_old[:j_to] + seg_shift + tour2_old[j_to:]
    tour2_new2 = tour2_old[:j_to] + seg_shift[::-1] + tour2_old[j_to:]


    tour1_new_dist = single_tour_dist(tour1_new, customers, capacity)
    tour2_new_dist1 = single_tour_dist(tour2_new1, customers, capacity)
    tour2_new_dist2 = single_tour_dist(tour2_new1, customers, capacity)

    if tour1_old_dist + tour2_old_dist > tour1_new_dist + tour2_new_dist1:
        tours[i_from] = tour1_new
        tours[i_to] = tour2_new1
        improved = True

    if tour1_old_dist + tour2_old_dist > tour1_new_dist + tour2_new_dist2:
        tours[i_from] = tour1_new
        tours[i_to] = tour2_new2
        improved = True

    return tours, improved


# interchange method
def interchange(tours, customers, capacity, i_1, start_1, end_1, i_2, start_2, end_2):
    tour_1_old = tours[i_1]
    tour_2_old = tours[i_2]
    improved = False

    seg_1 = tour_1_old[start_1: end_1 + 1]
    seg_2 = tour_2_old[start_2: end_2 + 1]

    # tour1 <- seg2, not reversed
    tour_1_new_1 = tour_1_old[: start_1] + seg_2 + tour_1_old[end_1 + 1:]
    # tour1 <- seg2, reversed
    tour_1_new_2 = tour_1_old[: start_1] + seg_2[::-1] + tour_1_old[end_1 + 1:]
    # tour2 <- seg1, not reversed
    tour_2_new_1 = tour_2_old[: start_2] + seg_1 + tour_2_old[end_2 + 1:]
    # tour2 <- seg1, reversed
    tour_2_new_2 = tour_2_old[: start_2] + seg_1[::-1] + tour_2_old[end_2 + 1:]

    # old tour lengths
    dist_1_old = single_tour_dist(tour_1_old, customers, capacity)
    dist_2_old = single_tour_dist(tour_2_old, customers, capacity)

    # new tour lengths
    dist_1_new_1 = single_tour_dist(tour_1_new_1, customers, capacity)
    dist_1_new_2 = single_tour_dist(tour_1_new_2, customers, capacity)
    dist_2_new_1 = single_tour_dist(tour_2_new_1, customers, capacity)
    dist_2_new_2 = single_tour_dist(tour_2_new_2, customers, capacity)

    # comparison
    if dist_1_old + dist_2_old > dist_1_new_1 + dist_2_new_1:
        tours[i_1] = tour_1_new_1
        tours[i_2] = tour_2_new_1
        improved = True

    if dist_1_old + dist_2_old > dist_1_new_1 + dist_2_new_2:
        tours[i_1] = tour_1_new_1
        tours[i_2] = tour_2_new_2
        improved = True

    if dist_1_old + dist_2_old > dist_1_new_2 + dist_2_new_1:
        tours[i_1] = tour_1_new_2
        tours[i_2] = tour_2_new_1
        improved = True

    if dist_1_old + dist_2_old > dist_1_new_2 + dist_2_new_2:
        tours[i_1] = tour_1_new_2
        tours[i_2] = tour_2_new_2
        improved = True

    return tours, improved


# exchange(2-opt) method
def exchange(tours, customers, capacity, i, start, end):
    improved = False
    tour_old = tours[i]
    seg = tour_old[start: end + 1]
    tour_new = tour_old[:start] + seg[::-1] + tour_old[end + 1:]

    # single_tour_dist(tour_old), single_tour_dist(tour_new)
    if single_tour_dist(tour_old, customers, capacity) > single_tour_dist(tour_new, customers, capacity):
        tours[i] = tour_new
        improved = True
    return tours, improved


# ladder method
def ladder(tours, customers, capacity, i_1, i_2, j_1, j_2):
    # two options to reconnect the path
    tour_1_old = tours[i_1]
    tour_2_old = tours[i_2]
    improved = False

    seg_1_head = tour_1_old[:j_1]
    seg_1_tail = tour_1_old[j_1:]
    seg_2_head = tour_2_old[:j_2]
    seg_2_tail = tour_2_old[j_2:]

    # head + tail
    tour_1_new_1 = seg_1_head + seg_2_tail
    tour_2_new_1 = seg_2_head + seg_1_tail

    # head + head(reversed) / tail(reversed) + tail
    tour_1_new_2 = seg_1_head + seg_2_head[::-1]
    tour_2_new_2 = seg_1_tail[::-1] + seg_2_tail

    # old tour lengths
    dist_1_old = single_tour_dist(tour_1_old, customers, capacity)
    dist_2_old = single_tour_dist(tour_2_old, customers, capacity)

    # new tour lengths
    dist_1_new_1 = single_tour_dist(tour_1_new_1, customers, capacity)
    dist_1_new_2 = single_tour_dist(tour_1_new_2, customers, capacity)
    dist_2_new_1 = single_tour_dist(tour_2_new_1, customers, capacity)
    dist_2_new_2 = single_tour_dist(tour_2_new_2, customers, capacity)

    if dist_1_old + dist_2_old > dist_1_new_1 + dist_2_new_1:
        tours[i_1] = tour_1_new_1
        tours[i_2] = tour_2_new_1
        improved = True

    if dist_1_old + dist_2_old > dist_1_new_2 + dist_2_new_2:
        tours[i_1] = tour_1_new_2
        tours[i_2] = tour_2_new_2
        improved = True

    return tours, improved

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])

    customers = []
    for i in range(1, customer_count + 1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i - 1, int(parts[0]), float(parts[1]), float(parts[2])))

    # the depot is always the first customer in the input
    depot = customers[0]

    # build a trivial solution
    # assign customers to vehicles starting by the largest customer demands
    vehicle_tours = [[] for i in range(0, vehicle_count)]

    remaining_customers = set(customers)
    remaining_customers.remove(depot)

    if customer_count > 400:
        dist_matrix = vrp.calculate_distance_matrix(customers)
        demand = [i.demand for i in customers]
        vec_cap = [vehicle_capacity] * vehicle_count
        vehicle_tours = vrp.or_vrp_solution(dist_matrix, vehicle_count, demand, vec_cap)
        # calculate the cost of the solution; for each vehicle the length of the route
        obj = 0
        for v in range(0, vehicle_count):
            vehicle_tour = vehicle_tours[v]
            if len(vehicle_tour) > 0:
                for i in range(0, len(vehicle_tour) - 1):
                    obj += length(customers[vehicle_tour[i]], customers[vehicle_tour[i + 1]])

        # prepare the solution in the specified output format
        outputData = '%.2f' % obj + ' ' + str(0) + '\n'
        for v in range(0, vehicle_count):
            outputData += ' '.join([str(customer) for customer in vehicle_tours[v]]) + '\n'
    else:
        # greedy initial solution
        for v in range(0, vehicle_count):
            # print "Start Vehicle: ",v
            vehicle_tours[v].append(depot)
            capacity_remaining = vehicle_capacity
            while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
                used = set()
                order = sorted(remaining_customers, reverse=False,
                               key=lambda customer: -customer.demand * customer_count + customer.index)
                for customer in order:
                    if capacity_remaining >= customer.demand:
                        capacity_remaining -= customer.demand
                        vehicle_tours[v].append(customer)
                        used.add(customer)
                remaining_customers -= used
        for v in range(0, vehicle_count):
            vehicle_tours[v].append(depot)

        t_start = time()
        t_threshold = 60 * 5

        improved = True
        while improved:
            # set time limit
            if time() - t_start > t_threshold:
                break
            # shift operator
            is_shift = True
            shift_improved = False
            if is_shift:
                for i_from, tour_from in enumerate(vehicle_tours):
                    if shift_improved:
                        break
                    for start_from, end_from in itertools.combinations(range(1, len(tour_from) - 1), 2):
                        if shift_improved:
                            break
                        for i_to, tour_to in enumerate(vehicle_tours):
                            if shift_improved:
                                break
                            if i_from == i_to:
                                continue
                            for j_to in range(1, len(tour_to) - 1):
                                vehicle_tours, shift_improved = shift(vehicle_tours, customers, vehicle_capacity,
                                                                      i_from, start_from, end_from, i_to, j_to)
                                if shift_improved:
                                    break

            # interchange operator
            is_interchange = True
            interchange_improved = False
            if is_interchange:
                for i_1, tour_1 in enumerate(vehicle_tours):
                    if interchange_improved: break
                    for start_1, end_1 in itertools.combinations(range(1, len(tour_1) - 1), 2):
                        if interchange_improved:
                            break
                        for i_2, tour_2 in enumerate(vehicle_tours):
                            if interchange_improved:
                                break
                            if i_1 == i_2:
                                continue
                            for start_2, end_2 in itertools.combinations(range(1, len(tour_2) - 1), 2):
                                vehicle_tours, interchange_improved = interchange(vehicle_tours, customers,
                                                                                  vehicle_capacity, i_1, start_1, end_1,
                                                                                  i_2, start_2, end_2)
                                if interchange_improved:
                                    break

            # 2-exchange(2-opt) operator
            is_exchange = True
            if is_exchange:
                for repeat in range(1):
                    for i, tour in enumerate(vehicle_tours):
                        for start, end in itertools.combinations(range(1, len(tour) - 1), 2):
                            vehicle_tours, exchange_improved = exchange(vehicle_tours, customers, vehicle_capacity, i,
                                                                        start,
                                                                        end)
                            if exchange_improved:
                                break

            # ladder operator
            is_ladder = True
            ladder_improved = False
            if is_ladder:
                for i_1, tour_1 in enumerate(vehicle_tours):
                    if ladder_improved:
                        break
                    for j_1 in range(2, len(tour_1) - 2):
                        if ladder_improved:
                            break
                        for i_2, tour_2 in enumerate(vehicle_tours):
                            if i_1 == i_2:
                                continue
                            if ladder_improved:
                                break
                            for j_2 in range(2, len(tour_2) - 2):
                                vehicle_tours, ladder_improved = ladder(vehicle_tours, customers, vehicle_capacity, i_1,
                                                                        i_2, j_1, j_2)
                                if ladder_improved:
                                    break
            improved = shift_improved or interchange_improved or exchange_improved or ladder_improved

        # calculate the distance
        obj = 0
        for i in range(vehicle_count):
            obj += single_tour_dist(vehicle_tours[i], customers, vehicle_capacity)

        # prepare the solution in the specified output format
        outputData = '%.2f' % obj + ' ' + str(0) + '\n'
        for v in range(0, vehicle_count):
            outputData += ' '.join(
                [str(customer.index) for customer in vehicle_tours[v]]) + '\n'

    return outputData

'''
if __name__ == '__main__':
    file_location = "./data/vrp_16_3_1"
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

        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

