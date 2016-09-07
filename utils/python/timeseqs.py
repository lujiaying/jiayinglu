import sys, mytimer
reps = 10000
repslist = range(reps)

def forLoop():
    res = []
    for x in repslist:
        res.append(x+1)
    return res

def listComp():
    return [x+1 for x in repslist]

def genFunc():
    def gen():
        for x in repslist:
            yield x+1
    return list(gen())


if __name__ == '__main__':
    print(sys.version)
    for test in (forLoop, listComp, genFunc):
        elapsed, result = mytimer.timer(test)
        print '-' * 33
        print '%s: %.4fs => [%s...%s]' %(test.__name__, elapsed, result[0], result[-1])
