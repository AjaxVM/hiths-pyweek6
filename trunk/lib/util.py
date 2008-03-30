import random

def get_random_start(dim, avoid=[]):
    #first, cut the map into 9 areas, see where all the sees land, and then picka random area to go to :D
    quadsize = int(dim[0] / 3), int(dim[1] / 3)
    quads = [[0,0], [0,1], [0,2],
             [1,0], [1,1], [1,2],
             [2,0], [2,1], [2,2]]

    #now find which quads are "clean"
    for i in avoid:
        x = int(i[0] / 3)
        y = int(i[1] / 3)
        if [x, y] in quads:
            quads.remove([x, y])

    if quads:
        #pick a qood spot!
        q = random.choice(quads * 2) #in case we only have one thing
        spot = [random.randint(q[0]*3, q[0]*3+int(dim[0]/3)),
                random.randint(q[1]*3, q[1]*3+int(dim[1]/3))]
        return spot
    else:
        #just pick somewhere then!
        spot = [random.randint(0, dim[0]-1), random.randint(0, dim[1]-1)]
        while spot in avoid:
            spot = [random.randint(0, dim[0]-1), random.randint(0, dim[1]-1)]
        return spot

def get_random_adj(spot, dim, avoid=[]):
    if spot:
        available = []

        for val in [[spot[0]-1, spot[1]],
                    [spot[0]+1, spot[1]],
                    [spot[0], spot[1]-1],
                    [spot[0], spot[1]+1]]:
            if val[0] >= 0 and val[0] < dim[0]:
                if val[1] >= 0 and val[1] < dim[1]:
                    if not val in avoid:
                        available.append(val)
        if available:
            return random.choice(available)
        return None
    else:
        return get_random_start(dim, avoid)

def touching(x, y):
    if x[0] == y[0]:
        if x[1] - y[1] in [-1, 0, 1]:
            return True
    if x[0] - y[0] in [-1, 0, 1]:
        if x[1] == y[1]:
            return True
    return False
##    return (abs(x[0] - y[0]) <= 1 and abs(x[1] - y[1]) <= 1)

def inmass(x, mass):
    for i in mass:
        if touching(x, i):
            return True
    return False

def get_landmass(grid):
    all = []

    yp = 0
    xp = 0
    for y in xrange(len(grid)):
        for x in xrange(len(grid[0])):
            pos = [x, y]
            if grid[pos[1]][pos[0]]:
                im = False
                for mass in all:
                    if inmass(pos, mass):
                        mass.append(pos)
                        im = True
                        break
                if not im:
                    all.append([pos])
            xp += 1
        yp += 1
        xp = 0
    return all

##def get_dis(x, y):
##    return abs(x[0] - y[0]) + abs(x[1] - y[1])
##
##def allowed_locs(x, avoid=[]):
##    n = []
##    for a in [-1, 0, 1]:
##        for b in [-1, 0, 1]:
##            a = x[0]+a
##            b = x[1]+b
##            if not [a, b] == x or\
##               [a, b] in avoid:
##                n.append([a, b])
##    return n

##def get_pos_between(x, y, randomness=5):
##    total_rand = 0
##    new = [x]
##    while not new[-1] == y:
##        print new[-1]
##        #see whether we should go random
##        if total_rand < randomness and random.choice([True, False]):
##            a = allowed_locs(new[-1], new)
##            new.append(random.choice(a*2))
##            total_rand += 1
##        #test each pixel touching x
##        else:
##            a = allowed_locs(new[-1], new)
##            cur = [None, 999]
##            for i in a:
##                if get_dis(i, y) < cur[1]:
##                    cur = [i, get_dis(i, y)]
##            new.append(cur[0])
##    return new

##def connect_landmass(x, y):
##    #get closest points
##    cur = [None, 999]
##    for i in x:
##        for j in y:
##            if get_dis(i, j) < cur[1]:
##                cur[0] = [i, j]
##                cur[1] = get_dis(i, j)
##
##    a = get_pos_between(cur[0][0], cur[0][1])
##    print a

##def connect_landmass(x, y):
##    cur = [None, 999]
##    for i in x:
##        for j in y:
##            print i, j
##            if get_dis(i, j) < cur[1]:
##                cur[0] = [i, j]
##                cur[1] = get_dis(i, j)
##
##    a, b = cur[0]
####    print a, b
##
##def make_one_landmass(grid):
##    lm = get_landmass(grid)
##    topthree = []
##    for i in xrange(3):
##        t = max(lm)
##        lm.remove(t)
##        topthree.append(t)
##
##    connect_landmass(topthree[0], topthree[1])

def make_random_map(dim=(16, 16), density=60):
    amount_land = dim[0]*dim[1] * (0.01 * density)

    g = []
    am_water = False
    for x in xrange(dim[0]):
        g.append([])
        for y in xrange(dim[1]):
            g[x].append(1)

    max_water = dim[0]*dim[1] - amount_land
    spot = None
    all_water = []
    lifes = 0

    for i in xrange(max_water):
        if not spot:
            #pick spot
            spot = get_random_adj(spot, dim, all_water)
            g[spot[1]][spot[0]] = 0
            all_water.append(spot)
            spot = get_random_adj(spot, dim, all_water)
            lifes += 1
        else:
            #place at this spot
            g[spot[1]][spot[0]] = 0
            all_water.append(spot)
            spot = get_random_adj(spot, dim, all_water)
            lifes += 1
            if lifes >= int(max_water/8):
                spot = None
                lifes = 0

    #remove islands
##    g = make_one_landmass(g)
    print len(get_landmass(g))
    return g
##
##for i in make_random_map(density=60):
##    print i
