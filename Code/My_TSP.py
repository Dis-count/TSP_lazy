#!/usr/bin/env python3.7

# Solve a traveling salesman problem on a randomly generated set of points using lazy constraints.
# The base MIP model only includes 'degree-2' constraints, requiring each node to have exactly
# two incident edges.  Solutions to this model may contain subtours -
# tours that don't visit every city.
# The lazy constraint callback adds new constraints to cut them off.

import sys
import math
import random
import pandas as pd
from itertools import combinations
import gurobipy as gp
from gurobipy import GRB
# import MatrixInstance
import PointsInstance

file_name = 'berlin52.tsp'

# instance = MatrixInstance.ReadInstance(file_name)
# n = instance.citynum
# dist = instance.matrix_dic

instance = PointsInstance.ReadInstance(file_name)
n = instance.citynum
dist =  instance.all_distance(n)


# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:
        # make a list of edges selected in the solution
        vals = model.cbGetSolution(model._vars)
        selected = gp.tuplelist((i, j) for i, j in model._vars.keys()
                                if vals[i, j] > 0.5)
        # find the shortest cycle in the selected edge list
        tour = subtour(selected)
        if len(tour) < n:
            # add subtour elimination constr. for every pair of cities in tour
            model.cbLazy(gp.quicksum(model._vars[i, j]
                                     for i, j in combinations(tour, 2))
                         <= len(tour)-1)


# Given a tuplelist of edges, find the shortest subtour

def subtour(edges):
    unvisited = list(range(n))
    cycle = range(n+1)  # initial length has 1 more city
    while unvisited:  # true if list is non-empty
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i, j in edges.select(current, '*')
                         if j in unvisited]
        if len(cycle) > len(thiscycle):
            cycle = thiscycle
    return cycle



m = gp.Model()

# Create variables

vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='e')
for i, j in vars.keys():
    vars[j, i] = vars[i, j]  # edge in opposite direction

# You could use Python looping constructs and m.addVar() to create
# these decision variables instead.  The following would be equivalent
# to the preceding m.addVars() call...
#
# vars = tupledict()
# for i,j in dist.keys():
#   vars[i,j] = m.addVar(obj=dist[i,j], vtype=GRB.BINARY,
#                        name='e[%d,%d]'%(i,j))


# Add degree-2 constraint

m.addConstrs(vars.sum(i, '*') == 2 for i in range(n))

# Using Python looping constructs, the preceding would be...
#
# for i in range(n):
#   m.addConstr(sum(vars[i,j] for j in range(n)) == 2)


# Optimize model

m._vars = vars
m.Params.lazyConstraints = 1
m.optimize(subtourelim)

vals = m.getAttr('x', vars)
selected = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)

tour = subtour(selected)
assert len(tour) == n

# opt_tour = [1, 36, 29, 13, 70, 35, 31, 69, 38, 59, 22, 66, 63, 57, 15, 24, 19, 7, 2, 4, 18, 42,
#             32, 3, 8, 26, 55, 49, 28, 14, 20, 30, 44, 68, 27, 46, 25, 45, 39, 61, 40, 9, 17, 43,
#             41, 6, 53, 5, 10, 52, 60, 12, 34, 21, 33, 62, 54, 48, 67, 11, 64, 65, 56, 51, 50, 58, 37, 47, 16, 23]
# #
# opt_tour = [x-1 for x in opt_tour]
# instance.evaluate(opt_tour)

instance.evaluate(tour)

print('')
print('Optimal tour: %s' % str(tour))
print('Optimal cost: %g' % m.objVal)
print('')
