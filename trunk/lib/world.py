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
    def __init__(self, image, pos = (0, 0), type="robot"):
        """image is the filename of the image - not the surface! - that way you can simply transfer
           the images stored in world through a network quicker..."""
        self.image = image
        self.type = type
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

        self.actors = []

        self.update()

        self.can_move = True
        self.highlighted = False

    def set_capitol(self):
        self.capitol = True
        self.max_units -= 1
        c = self.get_middle_tile()
        self.actors.append(Actor(os.path.join("data", "images", "capitol1.png"), c, "capitol"))

    def set_supply(self):
        self.supply = True
        self.max_units -= 1
        c = self.get_middle_tile()
        self.actors.append(Actor(os.path.join("data", "images", "supply1.png"), c, "supply"))

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
        """Update the units in the territory."""
        # Get the change in units between what is displayed and what we actually have
        unit_count = self.units - len(self.actors)
        if self.supply or self.capitol: # Adjust for supply or capitol
            unit_count += 1

        # Add more units?
        if unit_count > 0:
            empty_tiles = self._get_empty_tiles()
            random.shuffle(empty_tiles)

            for i in xrange(unit_count):
                c = empty_tiles.pop()
                self.actors.append(Actor(os.path.join("data", "images", "robo1.png"), c))
        # Are some units dead?
        elif unit_count < 0:
            # Make sure we aren't marking the capitol or supply dead
            all_are_bots = False
            while not all_are_bots:
                death_list = random.sample(self.actors, unit_count * -1)
                all_are_bots = True
                for i in death_list:
                    if i.type != "robot":
                        all_are_bots = False

            for i in death_list:
                self.actors.remove(i)

        self.actors.sort(sort_actors)

    def _get_empty_tiles(self):
        """Returns a list of tiles without an Actor in them"""
        occupied_tiles = []
        terr = list(self.terr)

        for i in self.actors:
            occupied_tiles.append(i.pos)

        for i in occupied_tiles:
            if i in terr:
                terr.remove(i)

        return terr # All tiles without an actor

class Player(object):
    def __init__(self, all_terr=[], color=(255, 255, 0)):
        self.territories = all_terr

        # Place a supply center in one of the player's territories
        big1 = big2 = None
        for i in self.territories:
            if not big1:
                big1 = i
                continue
            if not big2:
                if len(i.terr) > len(big1.terr):
                    big2 = big1
                    big1 = i
                else:
                    big2 = i
                continue

            if len(i.terr) > len(big1.terr):
                big2 = big1
                big1 = i
            elif len(i.terr) > len(big2.terr):
                big2 = i
        big1.set_capitol()
        big2.set_supply()

        num_troops = len(self.territories) - 2
        while num_troops:
            for i in self.territories:
                if not i.capitol or i.supply:
                    if num_troops:
                        new = random.randint(0, 1)
                        if i.units + new > i.max_units:
                            new = i.max_units - i.units
                        i.units += new
                        num_troops -= new

        for i in self.territories:
            if i.capitol or i.supply:
                i.units = 4
            else:
                i.units += 1
                if i.units > i.max_units:
                    i.units = i.max_units
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

    def has_open_spots(self):
        for i in self.territories:
            if i.units < i.max_units:
                return True

    def end_turn(self):
        extra = self.get_terr_holding()
        while extra:
            if not self.has_open_spots():
                break
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
    def __init__(self, surface, tile_size=(80, 40),
                 map_grid=None, background=None):

        self.tile_size = tile_size

        self.display = surface

        self.background = background


        self.grid = map_grid
        self.offset = [0,0]
        self.map_size = ()

        if self.background:
            x = self.tile_size[0]*len(self.grid.grid[0])
            y = self.tile_size[1]*len(self.grid.grid)+self.tile_size[1]
            if x < self.display.get_width():
                x = self.display.get_width()
            if y < self.display.get_height()+self.tile_size[1]:
                y = self.display.get_height()+self.tile_size[1]
            self.use_bg = pygame.transform.scale(self.background, (x, y))

        self.__images = {}
        self.__use_images = {}

        self.players = []

        self.world_image = None

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
        if self.offset[1] > self.tile_size[1] * len(self.grid.grid) - self.display.get_height() + self.tile_size[1]:
            self.offset[1] = self.tile_size[1] * len(self.grid.grid) - self.display.get_height() + self.tile_size[1]
        pass

    def get_image(self, name):
        if not name in self.__images:
            self.__images[name] = pygame.image.load(name).convert_alpha()
            self.__use_images[name] = self.__images[name]
        if not self.__use_images:
            self.__use_images = self.__images
        return self.__use_images[name]

    def render(self):
        if self.map_size == () or self.world_image == None:
            x, y = self.grid.get_dimensions()
            x *= self.tile_size[0]
            y *= self.tile_size[1]
            self.map_size = x, y

        if not self.__use_images:
            self.__use_images = self.__images

        img = self.__use_images


        tx, ty = self.tile_size

        self.__fix_offset()

        dx, dy = self.offset

        if not self.world_image:
            self.world_image = pygame.Surface((self.map_size[0],
                                               self.map_size[1]+self.tile_size[1])).convert_alpha()
            if self.background:
                self.world_image.fill((0,0,0,0))
            else:
                self.world_image.fill((255,255,255))
            for x in self.players:
                for i in x.territories:
                    for s in i.terr: #render territories
                        r = (s[0] * tx, s[1] * ty+self.tile_size[1],
                             tx, ty)
                        pygame.draw.rect(self.world_image, x.color, r)
                    for s in i.terr_points: #render borders
                        if i.highlighted:
                            amt=4
                        else:
                            amt=1
                        pygame.draw.line(self.world_image, [0,0,0],
                                         [s[0][0]*self.tile_size[0],
                                          s[0][1]*self.tile_size[1]+self.tile_size[1]],
                                         [s[1][0]*self.tile_size[0],
                                          s[1][1]*self.tile_size[1]+self.tile_size[1]],
                                         amt)
            for x in self.players:
                for i in x.territories:
                    for s in i.actors:
                        img = self.get_image(s.image)
                        r = img.get_rect()
                        r.bottomleft = (s.pos[0] * tx, (s.pos[1]+1) * ty+self.tile_size[1])
                        self.world_image.blit(img, r.topleft) 

        if self.background:
            x = -dx
            y = -dy
            if x > 0:
                x = 0
            if y > 0:
                y = 0
            self.display.blit(self.use_bg, (x, y))
        self.display.blit(self.world_image, (-dx, -dy))

    def get_mouse_pos(self):
        p = pygame.mouse.get_pos()
        x = self.display.get_offset()
        p = p[0] - x[0], p[1] - x[1]

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

    def update(self):
        self.world_image = None
        self.__use_images = {}
        for i in self.__images:
            self.__use_images[i] = pygame.transform.scale(self.__images[i], (self.tile_size[0],
                                                                             self.tile_size[1]*2))
        if self.background:
            #image must be as big as the display!
            x = self.tile_size[0]*len(self.grid.grid[0])
            y = self.tile_size[1]*len(self.grid.grid)+self.tile_size[1]
            if x < self.display.get_width():
                x = self.display.get_width()
            if y < self.display.get_height()+self.tile_size[1]:
                y = self.display.get_height()+self.tile_size[1]
            self.use_bg = pygame.transform.scale(self.background, (x, y))

    def get_biggest_player(self):
        cur = None
        for i in self.players:
            if not i.dead:
                if not cur:
                    cur = i
                else:
                    if len(i.territories) > len(cur.territories):
                        cur = i
        return cur

        

        
