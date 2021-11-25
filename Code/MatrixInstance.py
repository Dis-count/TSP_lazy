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

        # distance matrix
        self.matrix = np.zeros((self.city_num,self.city_num))


        count = 0
        for line in b:
            first_char = line.lstrip()[0]
            if first_char.isdigit() and (count < self.city_num):
                number = line.strip('\n').split()
                self.matrix[count][:] = number
                count +=1


    @property
    def citynum(self):
        '''
        Return the number of city.
        '''
        return self.city_num

    @property
    def matrix_dic(self):
        '''
        Return the dictionary of matrix.
        '''
        dist = {(i,j): self.matrix[i][j]
        for i in range(self.city_num-1) for j in range(i+1,self.city_num)}

        return dist

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
    file_name = 'swiss42.tsp'
    instance = ReadInstance(file_name)
    instance.matrix_dic
