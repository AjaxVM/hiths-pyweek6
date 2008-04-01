import time

import pygame
from pygame.locals import *

import util

class Actor(object):
    def __init__(self, image, pos = (0.5, 0.5)):
        """0.5 = middle of tile ;)
           image is the filename of the image - not the surface! - that way you can simply transfer
           the images stored in world through a network quicker..."""
        self.image = image

        self.pos = pos


class MapGrid(object):
    def __init__(self, #images={"n":None},
                 grid = [[]]):
        self.grid = grid
        self.territories = util.get_territories(self.grid)[1::]
##        self.terr_points = [util.get_points(i) for i in self.territories]
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

class Player(object):
    def __init__(self, start_terr=None, color=(255, 255, 0)):
        self.start_terr = start_terr
        self.start_terr.player = self
        self.start_terr.units = 4
        self.territories = [self.start_terr]

        self.actors = []

        self.color = color


class World(object):
    def __init__(self, surface, tile_size=(15, 10),
                 map_grid=None, background=None):

        self.tile_size = tile_size

        self.display = surface

        self.background = background


        self.grid = map_grid
        self.offset = [0,0]
        self.map_size = ()

        self.__images = {}
##        self.actors = []

        self.players = []

    def load_images(self, more=[]):
        self.__images = {}
        for i in self.actors:
            self.__images[i.image] = pygame.image.load(i.image).convert_alpha()
        for i in more:
            self.__images[i] = pygame.image.load(i).convert_alpha()

        return None

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

    def render(self):
        if self.map_size == ():
            x, y = self.grid.get_dimensions()
            x *= self.tile_size[0]
            y *= self.tile_size[1]
            self.map_size = x, y

        if self.background:
            self.display.blit(self.background, (0,0))

        img = self.__images

        f = pygame.font.Font(None, 14)


        tx, ty = self.tile_size

        self.__fix_offset()

        dx, dy = self.offset

        ypos = 0
        col = {1: (255, 0, 0),
                    2: (0, 255, 0),
                    3: (0, 0, 255),
                    4: (255, 255, 0),
                    5: (255, 0, 255),
                    6: (0, 255, 255),
                  0:(0,125,0)}
        for y in self.grid.grid:
            xpos = 0
            for x in y:
                r = (xpos * tx - dx, ypos * ty - dy,
                     tx, ty)
                if x == 0:
                    pygame.draw.rect(self.display, (125, 125, 125), r)
                else:
                    pygame.draw.rect(self.display, col[x%7], r)
                self.display.blit(f.render(str(x), 1, (0,0,0)), [r[0], r[1]])
                xpos += 1
            ypos += 1

        #render borders between territories...
##        tp = self.grid.terr_points
##        for i in tp:
##            for x in i:
##                pygame.draw.line(self.display, [255,255,255],
##                                 [x[0][0]*self.tile_size[0]-self.offset[0],
##                                  x[0][1]*self.tile_size[1]-self.offset[1]],
##                                 [x[1][0]*self.tile_size[0]-self.offset[0],
##                                  x[1][1]*self.tile_size[1]-self.offset[1]],
##                                 1)

##        for i in self.actors:
##            self.display.blit(img[i.image], (i.pos[0] * tx - dx,
##                                             i.pos[1] * ty - dy))

        for x in self.players:
            for i in x.territories:
                for s in i.terr:
                    r = (s[0] * tx - dx, s[1] * ty - dy,
                         tx, ty)
                    pygame.draw.rect(self.display, x.color, r)
                for s in i.terr_points:
                    pygame.draw.line(self.display, [255,255,255],
                                     [s[0][0]*self.tile_size[0]-self.offset[0],
                                      s[0][1]*self.tile_size[1]-self.offset[1]],
                                     [s[1][0]*self.tile_size[0]-self.offset[0],
                                      s[1][1]*self.tile_size[1]-self.offset[1]],
                                     1)
            for i in x.actors:
                self.display.blit(img[i.image], (i.pos[0] * tx - dx,
                                                 i.pos[1] * ty - dy))

    def get_mouse_pos(self):
        p = pygame.mouse.get_pos()

        self.__fix_offset()

        dx, dy = self.offset

        x = (p[0] + dx) / self.tile_size[0]
        y = (p[1] + dy) / self.tile_size[1]
        return x, y
            

        

        
