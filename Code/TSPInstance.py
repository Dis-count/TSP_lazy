import math
from os import path
import numpy as np
import matplotlib.pyplot as plt


class TSPInstance:
    '''
    设计一个类，实现从文件读入一个旅行商问题的实例
    文件格式为：
    city number
    best known tour length
    list of city position (index x y)
    best known tour (city index starts from 1)
    以文件01eil51.txt为例：
    第一行51为城市数
    第二行426为最优解的路径长度
    第三行开始的51行为各个城市的序号、x坐标和y坐标
    最后是最优解的访问城市系列（注意里面城市序号从1开始，而python的sequence是从0开始）
    Eil51Tour.png是最优解的城市访问顺序图
    '''

    def __init__(self, file_name):
        '''
        从文件file_name读入旅行商问题的数据
        '''
        self.file_name=file_name
        a= open(file_name)
        # 城市数量
        self.city_num = a.readline()
        # 返回坐标 51行，3列
        self.city = np.zeros((int(self.city_num), 3))
        # x坐标
        self.x = np.zeros(int(self.city_num))
        # y坐标
        self.y = np.zeros(int(self.city_num))
        # 城市ID
        self.id = np.zeros(int(self.city_num))
        b = a.readlines()
        for i, content in enumerate(b):
                if i in range(1, 52 ):
                    # 单行赋值
                    self.city[i-1] = content.strip('\n').split(' ')
                    self.x[i-1] = self.city[i-1][1]
                    self.y[i-1] = self.city[i-1][2]
        for i, content in enumerate(b):
                if i in range(53, 104):
                    self.id[i - 53] = content.strip('\n')
    @property
    def citynum(self):
        '''
        返回城市数
        '''
        return self.city_num

    @property
    def optimalval(self):
        '''
        返回最优路径长度
        '''
        c = 0
        i = 1
        s = open(self.file_name)
        str = s.readlines()
        for content in str:
            if i == 2:
                c = content
            i = i + 1
        return c

    @property
    def optimaltour(self):
        '''
        返回最优路径
        '''
        tour = np.array(self.id)
        return tour

    def __getitem__(self, n):
        '''
        返回城市n的坐标,由x和y构成的tuple:(x,y)
        '''
        (x, y) = (self.x[n-1], self.y[n-1])
        return (x, y)

    def get_distance(self, n, m):
        '''
        返回城市n、m间的整数距离（四舍五入）
        '''
        u=int(self.x[n-1] - self.x[m-1])
        v=int(self.y[n-1] - self.y[m-1])
        dis = math.sqrt(pow(u,2) + pow(v,2))
        return int(dis+0.5)

    def evaluate(self, tour):
        '''
        返回访问系列tour所对应的路径程度
        '''
        dis = 0
        for i in range(50):
            dis += self.get_distance(int(tour[i]), int(tour[i + 1]))
        dis += self.get_distance(int(tour[50]), int(tour[0]))
        return dis

    def plot_tour(self, tour):
        '''
        画出访问系列tour所对应的路径路
        '''
        for i in range(51):
            x0,y0 = self.__getitem__(i)
            plt.scatter(int(x0),int(y0),s=10,c='c')
        #记住坐标点的画法
        for i in range(len(tour)-1):
            x1,y1 = self.__getitem__(int(tour[i]))
            x,y = self.__getitem__(int(tour[i+1]))
            plt.plot([x1,x],[y1,y],c='b')
        x2,y2 = self.__getitem__(int(tour[0]))
        x3,y3 = self.__getitem__(int(tour[len(tour)-1]))

        plt.plot([x2,x3],[y2,y3],c='b')
        plt.xlabel('x label')
        plt.ylabel('y label')
        plt.title("City access sequence diagram")
        plt.plot()
        plt.show()

if __name__ == "__main__":
    file_name = path.dirname(__file__) + "/1.txt"
    instance = TSPInstance(file_name)
    print(instance.citynum)
    print(instance.evaluate(instance.optimaltour))
    print(instance.optimaltour)
    print(instance.__getitem__(2))
    print(instance.get_distance(0, 1))
    instance.plot_tour(instance.optimaltour)
    '''
    output:
    51
    426
    [  1.  22.   8.  26.  31.  28.   3.  36.  35.  20.   2.  29.  21.  16.  50.
      34.  30.   9.  49.  10.  39.  33.  45.  15.  44.  42.  40.  19.  41.  13.
      25.  14.  24.  43.   7.  23.  48.   6.  27.  51.  46.  12.  47.  18.   4.
      17.  37.   5.  38.  11.  32.]
    (49.0, 49.0)
    14
    '''
