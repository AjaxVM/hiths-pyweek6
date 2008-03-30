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
    return (abs(x[0] - y[0]) <= 1 and abs(x[1] - y[1]) <= 1)

def inmass(x, mass):
    for i in mass:
        if touching(x, i):
            return True
    return False

def connected_mass(x, y):
    for a in x:
        if inmass(a, y):
            return True
    return False

def get_landmass(grid):
    all = []

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

    for mass in all:
        for m2 in all:
            if not mass == m2:
                if connected_mass(mass, m2):
                    mass.extend(m2)
                    all.remove(m2)
    return all

def make_random_map(dim=(16, 16), density=60):
    amount_land = int(dim[0]*dim[1] * (0.01 * density))

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
    a = get_landmass(g)    return g
