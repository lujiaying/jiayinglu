# -*- coding: utf-8 -*-

"""
Random库常用API的实现
"""

class Random(object):
    def __init__(self, x=None):
        if x is None:
            import time
            self.seed = long(time.time())
        else:
            self.seed = long(x)
        self._seed = self.seed
        
    def random_LCG(self):
        '''
        线性同余产生0~1之间的随机数

        X(k) = [a * X(k-1) + c] mod m
        '''
        # 以下参数值参照GCC编译器
        m = 2**32
        a = 1103515245
        c = 12345
        self._seed = (a * self._seed + c) % m
        return self._seed / float(m-1)

    def random_MSM(self):
        '''
        平方取中法产生0~1之间的随机数

        X(i+1) = [10^(-m/2) * X(i)^2] mod (10^m)
        '''
        m = 8
        self._seed = long((10**(-m/2) * self._seed * self._seed) % (10**m))
        return self._seed / float(10**m -1)

if __name__ == '__main__':
    print('LCG random generator')
    random = Random()
    for i in range(10):
        print(random.random_LCG())

    print('MCM random generator')
    random = Random()
    for i in range(10):
        print(random.random_MSM())
