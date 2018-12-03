# coding: utf-8

def cal_pi(epoch=100000):
    """
    蒙特卡洛方法计算圆周率

    正方形面积与其内切圆面积之比为 pi:4
    """
    import random
    import tqdm
    import math
    in_circle_cnt = 0
    for i in tqdm.trange(epoch):
        x, y = random.random(), random.random()
        if (x**2 + y**2) <= 1:
            in_circle_cnt += 1
    pi = float(in_circle_cnt) / epoch * 4
    print('The diff is +-%s%%' % (abs(math.pi-pi)/math.pi*100))
    return pi

if __name__ == '__main__':
    print(cal_pi())
