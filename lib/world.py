import time
import os
import random

import pygame
from pygame.locals import *

import util, rules

def sort_actors(x, y):
    if x.pos[1] < y.pos[1]:
        return -1
    if x.pos[1] > y.pos[1]:
        return 1
    if x.pos[0] < y.pos[0]:
        return -1
    if x.pos[0] > y.pos[0]:
        return 1
    return 0

class Actor(object):
    def __init__(self, image, pos = (0, 0)):
        """image is the filename of the image - not the surface! - that way you can simply transfer
           the images stored in world through a network quicker..."""
        self.image = image

        self.pos = pos


class MapGrid(object):
    def __init__(self, #images={"n":None},
                 grid = [[]]):
        self.grid = grid
        self.territories = util.get_territories(self.grid)[1::]

        self.comp_terrs = []
        for i in self.territories:
            self.comp_terrs.append(PlayerTerritory(None, i, 0))

    def get_dimensions(self):
        return len(self.grid[0]), len(self.grid)

class PlayerTerritory(object):
    def __init__(self, player, terr, units):
        self.player = player

        self.terr = terr
        self.terr_points = util.get_points(self.terr)

        self.units = units

        self.max_units = len(self.terr)

        self.capitol = False
        self.supply = False

        self.update()

        self.can_move = True
        self.highlighted = False

    def get_middle_tile(self):
        t = None
        b = None
        l = None
        r = None
        for i in self.terr:
            if t == None:
                t = i[1]
                b = i[1]
                r = i[0]
                l = i[0]
            else:
                if i[0] < l:
                    l = i[0]
                elif i[0] > r:
                    r = i[0]
                if i[1] < t:
                    t = i[1]
                elif i[1] > b:
                    b = i[1]

        mid = (int(r - (r - l) / 2),
               int(b - (b - t) / 2))
        closest = self.terr[0]
        for i in self.terr:
            if abs(i[0] - mid[0]) + abs(i[1] - mid[1]) <\
               abs(closest[0] - mid[0]) + abs(closest[1] - mid[1]):
                closest = i
        return closest

    def update(self):
        self.max_units = len(self.terr)
        if self.capitol:
            self.max_units -= 1
        if self.supply:
            self.max_units -= 1
        self.actors = []
        x = list(self.terr)
        #random.shuffle(x)
        if self.capitol:
            c = self.get_middle_tile()
            x.remove(c)
            self.actors.append(Actor(os.path.join("data", "images", "capitol1.png"), c))
        if self.supply:
            c = self.get_middle_tile()
            x.remove(c)
            self.actors.append(Actor(os.path.join("data", "images", "supply1.png"), c))
        for i in xrange(self.units):
            c = x.pop()
            self.actors.append(Actor(os.path.join("data", "images", "robo1.png"), c))

        self.actors.sort(sort_actors)

class Player(object):
    def __init__(self, start_terr=None, all_terr=[], color=(255, 255, 0)):
        self.start_terr = start_terr
        self.start_terr.player = self
        self.start_terr.units = 4
        self.start_terr.capitol = True
        self.territories = all_terr

        # Place a supply center in one of the player's territories
        while True:
            index = random.randint(0, len(self.territories)-1)
            if not self.territories[index].capitol: # Unless there is a capitol
                self.territories[index].supply = True
                break

        for i in self.territories:
            i.units = 4
            i.update()

        self.color = color
        self.dead = False

    def test_connected(self, x, y):
        for t1 in x.terr:
            for t2 in y.terr:
                if util.touching(t1, t2):
                    return True
        return False

    def get_terr_holding(self):
        #return largest connected number of territories
        groups = []
        for i in self.territories:
            if groups == []:
                groups = [[i]]
            else:
                ing = False
                for x in groups:
                    for c in x:
                        if self.test_connected(i, c):
                            ing = True
                            x.append(i)
                            break
                    if ing:
                        break
                if not ing:
                    groups.append([i])
        largest = 0
        for i in groups:
            if len(i) > largest:
                largest = len(i)
        return largest

    def end_turn(self):
        extra = self.get_terr_holding()
        while extra:
            for i in self.territories:
                if extra:
                    use = random.randint(0, extra)
                    if i.units + use < i.max_units:
                        extra -= use
                        i.units += use
                    else:
                        use = i.max_units - i.units
                        extra -= use
                        i.units += use
                else:
                    break


        for i in self.territories:
            i.can_move = True
            if i.capitol:
                i.units += rules.capitol_troop_gain
            elif i.supply:
                i.units += rules.supply_troop_gain
            if i.units > i.max_units:
                i.units = i.max_units

            i.update()


class World(object):
    def __init__(self, surface, tile_size=(10, 7),
                 map_grid=None, background=None):

        self.tile_size = tile_size

        self.display = surface

        self.background = background


        self.grid = map_grid
        self.offset = [0,0]
        self.map_size = ()

        self.__images = {}

        self.players = []

    def one_winner(self):
        good=0
        best = None
        num = 0
        for i in self.players:
            if not i.dead:
                good += 1
                best = num
            num += 1
        return good == 1, best

    def __fix_offset(self):
        if self.offset[0] < 0:
            self.offset[0] = 0
        if self.offset[0] > self.tile_size[0] * len(self.grid.grid[0]) - self.display.get_width():
            self.offset[0] = self.tile_size[0] * len(self.grid.grid[0]) - self.display.get_width()

        if self.offset[1] < 0:
            self.offset[1] = 0
        if self.offset[1] > self.tile_size[1] * len(self.grid.grid) - self.display.get_height():
            self.offset[1] = self.tile_size[1] * len(self.grid.grid) - self.display.get_height()
        pass

    def get_image(self, name):
        if not name in self.__images:
            self.__images[name] = pygame.image.load(name).convert_alpha()
        return self.__images[name]

    def render(self):
        if self.map_size == ():
            x, y = self.grid.get_dimensions()
            x *= self.tile_size[0]
            y *= self.tile_size[1]
            self.map_size = x, y

        if self.background:
            self.display.blit(self.background, (0,0))

        img = self.__images


        tx, ty = self.tile_size

        self.__fix_offset()

        dx, dy = self.offset

        self.display.fill((255,255,255))

        for x in self.players:
            for i in x.territories:
                for s in i.terr: #render territories
                    r = (s[0] * tx - dx, s[1] * ty - dy,
                         tx, ty)
                    pygame.draw.rect(self.display, x.color, r)
                for s in i.terr_points: #render borders
                    if i.highlighted:
                        amt=4
                    else:
                        amt=1
                    pygame.draw.line(self.display, [0,0,0],
                                     [s[0][0]*self.tile_size[0]-self.offset[0],
                                      s[0][1]*self.tile_size[1]-self.offset[1]],
                                     [s[1][0]*self.tile_size[0]-self.offset[0],
                                      s[1][1]*self.tile_size[1]-self.offset[1]],
                                     amt)
        for x in self.players:
            for i in x.territories:
                for s in i.actors:
                    img = self.get_image(s.image)
                    r = img.get_rect()
                    r.bottomleft = (s.pos[0] * tx - dx, (s.pos[1]+1) * ty - dy)
                    self.display.blit(img, r.topleft)

    def get_mouse_pos(self):
        p = pygame.mouse.get_pos()

        self.__fix_offset()

        dx, dy = self.offset

        x = (p[0] + dx) / self.tile_size[0]
        y = (p[1] + dy) / self.tile_size[1]
        return x, y

    def get_mouse_terr(self):
        x = list(self.get_mouse_pos())
        for i in self.players:
            for j in i.territories:
                if x in j.terr:
                    return self.players.index(i), j
        return None
            

        

        