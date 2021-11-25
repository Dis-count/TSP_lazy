import numpy as np
import math
import random

def randcenter(n,m):
    # n is number of center. m is number of points for each center.
    # random.seed(1)
    points =[]
    point = [[0 for i in range(m)] for j in range(n)]
    for i in range(n):
        center = [random.randint(10, 90), random.randint(10, 90)]
        point[i] = [(center[0]+random.randint(-10, 10), center[1]+ random.randint(-10, 10)) for j in range(m)]
        points = points + point[i]
    dist = {(x, y):
            math.sqrt(sum((points[x][k]-points[y][k])**2 for k in range(2)))
            for x in range(n*m) for y in range(x)}
    return dist
#  Some points as the center// (2,50)/(4,25)/(5,20)

def rand100(n):
    # n is number of center. m is number of points for each center.
    # random.seed(1)
    points = [(random.randint(0, 100), random.randint(0, 100)) for j in range(n)]
    dist = {(x, y):
            math.sqrt(sum((points[x][k]-points[y][k])**2 for k in range(2)))
            for x in range(n) for y in range(x)}
    return dist

def dic2cost(dist,nodeNum):
# This function is used to change dictionary to the form of matrix.
    lowerTri = [[0 for i in range(nodeNum)] for j in range(nodeNum)]

    for key,value in dist.items():

        lowerTri[key[0]][key[1]] = value

    lowerSym = np.array(lowerTri)

    for i in range(len(lowerSym)):
        for j in range(i):
                lowerSym[j,i] = lowerSym[i,j]

    return lowerSym

# Test
# dist = randcenter(5,5)
# cost =  dic2cost(dist,25)
