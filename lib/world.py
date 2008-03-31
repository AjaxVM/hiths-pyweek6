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
##        self.images = images
        self.grid = grid

    def get_dimensions(self):
        return len(self.grid[0]), len(self.grid)


class World(object):
    def __init__(self, surface, tile_size=(30, 15),
                 map_grid=None, background=None):

        self.tile_size = tile_size

        self.display = surface

        self.background = background


        self.grid = map_grid
        self.offset = [0,0]
        self.map_size = ()
        self.territories = []
        self.terr_points = []

        self.__images = {}
        self.actors = []

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
            self.territories = util.get_territories(self.grid.grid)
            self.terr_points = [util.get_points(i) for i in self.territories]

        if self.background:
            self.display.blit(self.background, (0,0))

        img = self.__images


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
                xpos += 1
            ypos += 1

        #render borders between territories...
        for i in self.terr_points:
            for x in i:
                pygame.draw.line(self.display, [255,255,255],
                                 [x[0][0]*self.tile_size[0]-self.offset[0],
                                  x[0][1]*self.tile_size[1]-self.offset[1]],
                                 [x[1][0]*self.tile_size[0]-self.offset[0],
                                  x[1][1]*self.tile_size[1]-self.offset[1]],
                                 1)

        for i in self.actors:
            self.display.blit(img[i.image], (i.pos[0] * tx - dx,
                                             i.pos[1] * ty - dy))

    def get_mouse_pos(self):
        p = pygame.mouse.get_pos()

        self.__fix_offset()

        dx, dy = self.offset

        x = (p[0] + dx) / self.tile_size[0]
        y = (p[1] + dy) / self.tile_size[1]
        return x, y
            

        

        
