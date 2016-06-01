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

        公式：X(k) = [a * X(k-1) + c] mod m
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
        '''
        m = 8
        _seed_square = str(self._seed ** 2)
        if len(_seed_square) < m * 2:
            _seed_square.zfill(m*2 - len(_seed_square))
        self._seed = long(_seed_square[4:12])
        return self._seed / float(10 ** m)


if __name__ == '__main__':
    random = Random()
    for i in range(100):
        print(random.random_LCG())

    random = Random()
    for i in range(100):
        print(random.random_MSM())
