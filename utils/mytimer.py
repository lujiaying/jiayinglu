# coding: utf-8
"""对代码计时
"""


import time
reps = 1000
repslist = range(reps)

def timer(func, *pargs, **kargs):
    start = time.time()
    for i in repslist:
        ret = func(*pargs, **kargs)
    elapsed = time.time() - start
    return (elapsed, ret)
