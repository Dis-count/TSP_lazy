import math
from os import path
import numpy as np
import re
#  return

class ReadInstance:
    '''
    Design a class to realize that read a TSP instance from a file.
    The format of this file is：
    ...
    Take the file bays29 as an example.
    The first line: bays29 is the name of the file.
    The second line: TSP is the type of the file.
    The third line: Comment about this file.
    The fourth line: the dimention of this file.
    The fifth line: EXPLICIT weight type
    The sixth line: FUll Matrix
    The seven line: data type, two dimention
    The eighth line: edge weight
    From the ninth line, the following file is what we want.
    '''

    def __init__(self, file_name):
        '''
        Read the TSP data from file_name
        '''
        self.file_name = file_name
        a = open(file_name)
        # 城市数量
        b = a.readlines()

        firstline = b[0]
        self.city_num  = int(re.findall(r"\d+", firstline)[0])
        # 返回坐标 51行，3列
        self.city = np.zeros((self.city_num, 3))
        # x坐标
        self.x = np.zeros(self.city_num)
        # y坐标
        self.y = np.zeros(self.city_num)
        # distance matrix
        self.matrix = np.zeros((self.city_num,self.city_num))

        while b[-1] == '\n':
            del b[-1]
        del b[-1]
        b = b[(len(b)-self.city_num):-1]        # when b is not matrix, is x-y point

        for i in b:
                    # 单行赋值
                points_list = i.strip('\n').split()
                index = int(points_list[0])
                self.city[index-1] = [float(x) for x in points_list]
                self.x[index-1] = self.city[index-1][1]
                self.y[index-1] = self.city[index-1][2]

    @property
    def citynum(self):
        '''
        Return the number of city.
        '''
        return self.city_num


    def __getitem__(self, n):
        '''
        返回城市n的坐标,由x和y构成的tuple:(x,y)
        '''
        (x, y) = (self.x[n-1], self.y[n-1])
        return (x, y)

    def get_distance(self, n, m):
        '''
        return the distance between city n and m.
        '''
        u=int(self.x[n] - self.x[m])
        v=int(self.y[n] - self.y[m])
        dis = math.sqrt(pow(u,2) + pow(v,2))
        return int(dis+0.5)

    def all_distance(self, n):
        '''
        return all distances
        '''
        dist = {(i,j): int(math.sqrt(pow(int(self.x[i] - self.x[j]),2) + pow(int(self.y[i] - self.y[j]),2))+0.5)
        for i in range(n) for j in range(i)}

        return dist

    def matrix_distance(self, n):
        disMatrix = [([0] * n) for p in range(n)] # 初始化距离矩阵的维度,防止浅拷贝

        for i in range(0, n):
            for j in range(0, n):
                temp = (self.x[i] - self.x[j])**2 + (slef.y[i] - slef.y[j])**2;
                disMatrix[i][j] = int(math.sqrt(temp)+0.5);
        return disMatrix

    def evaluate(self, tour):
        '''
        返回访问系列tour所对应的路径长度
        '''
        dis = 0
        for i in range(self.city_num-1):
            dis += self.get_distance(int(tour[i]), int(tour[i + 1]))
        dis += self.get_distance(int(tour[self.city_num-1]), int(tour[0]))
        return dis

if __name__ == "__main__":
    # file_name = path.dirname(__file__) + "/1.txt"
    file_name = 'berlin52.tsp'
    instance = ReadInstance(file_name)
