def depth(deepList):
    i = 0
    while type(deepList) == list:
        deepList = deepList[0]
        i+=1
    return i

def exists(position, grid):

    d = len(position)
    for i in range(d):
        if position[i] < 0:
            return False
        space = grid
        for j in range(i):
            space = space[0]
        #print(i)
        #print(space)
        if position[i] >= len(space):
            return False
    return True


def orthag(x):
    #this is ugly (but makes it play nice with tuples)
    f = type(x)

    res = []
    for i in range(len(x)):
        j = list(x)
        j = j.copy()
        j[i] += 1
        res.append(f(j.copy()))
        j[i] -= 2
        res.append(f(j.copy()))
    return res

from itertools import product

def adjacent(x):
    f = type(x)
    operate = list(x)
    for sequence in product("012", repeat = len(x)):
        if sequence == tuple(["0"] * len(x)):
            continue
        thisX = operate.copy()
        for s in range(len(sequence)):
            if sequence[s] == "1":
                thisX[s] +=1
            elif sequence[s] == "2":
                thisX[s] -=1
        yield f(thisX)
