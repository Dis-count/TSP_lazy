import DistCost
import sys
import copy
import numpy as np
import pandas as pd
from itertools import combinations
import gurobipy as gp
from gurobipy import GRB

# set nodenum
n= 5
m = 6
nodeNum = n*m
dist = DistCost.randcenter(n,m)

# nodeNum = 50
# dist = DistCost.rand100(nodeNum)

cost = DistCost.dic2cost(dist, nodeNum)

model = gp.Model('RandomMTZ')

# creat decision variables
X = {}
mu = {}
for i in range(nodeNum + 1):
    mu[i] = model.addVar(lb = 0.0
                         , ub = 100 #GRB.INFINITY
                          # , obj = distance_initial
                         , vtype = GRB.CONTINUOUS
                         , name = "mu_" + str(i)
                        )

    for j in range(nodeNum + 1):
        if(i != j):
            X[i, j] = model.addVar(vtype = GRB.BINARY
                                  , name = 'x_' + str(i) + '_' + str(j)
                                  )

# set objective function
obj = gp.LinExpr(0)
for key in X.keys():
    i = key[0]
    j = key[1]
    if(i < nodeNum and j < nodeNum):
        obj.addTerms(cost[key[0]][key[1]], X[key])
    elif(i == nodeNum):
        obj.addTerms(cost[0][key[1]], X[key])
    elif(j == nodeNum):
        obj.addTerms(cost[key[0]][0], X[key])

model.setObjective(obj, GRB.MINIMIZE)

# add constraints 1
for j in range(1, nodeNum + 1):
    lhs = gp.LinExpr(0)
    for i in range(0, nodeNum):
        if(i != j):
            lhs.addTerms(1, X[i, j])
    model.addConstr(lhs == 1, name = 'visit_' + str(j))

# add constraints 2
for i in range(0, nodeNum):
    lhs = gp.LinExpr(0)
    for j in range(1, nodeNum + 1):
        if(i != j):
            lhs.addTerms(1, X[i, j])
    model.addConstr(lhs == 1, name = 'visit_' + str(j))

# add MTZ constraints
# for key in X.keys():
#     org = key[0]
#     des = key[1]
#     if(org != 0 or des != 0):
# #         pass
#         model.addConstr(mu[org] - mu[des] + 100 * X[key] <= 100 - 1)
for i in range(0, nodeNum):
    for j in range(1, nodeNum + 1):
        if(i != j):
            model.addConstr(mu[i] - mu[j] + 100 * X[i, j] <= 100 - 1)

# model.write('model.lp')
model.optimize()

def getValue(var_dict, nodeNum):
    x_value = np.zeros([nodeNum + 1, nodeNum + 1])
    for key in var_dict.keys():
        a = key[0]
        b = key[1]
        x_value[a][b] = var_dict[key].x

    return x_value

# input: x_value?????????
# output:???????????????[0, 4, 3, 7, 1, 2, 5, 8, 9, 6, 0]????????????
# ?????????5???????????????????????????????????????1-4-2-3-5-6????????????????????????????????????????????????
# ???????????????????????????6?????????????????????????????????????????????x_value???????????????
def getRoute(x_value):
    x=copy.deepcopy(x_value)
    # route_temp.append(0)
    previousPoint = 0
    route_temp = [previousPoint]
    count = 0
    while(len(route_temp) < len(x)):
        #print('previousPoint: ', previousPoint )
        if(x[previousPoint][count] > 0):
            previousPoint = count
            route_temp.append(previousPoint)
            count = 0
            continue
        else:
            count += 1
    return route_temp

x_value = getValue(X, nodeNum)
route = getRoute(x_value)
print('optimal route:', route)
