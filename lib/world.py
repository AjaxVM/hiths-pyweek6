import time

import pygame
from pygame.locals import *

class Actor(object):
    def __init__(self, image, pos = (0.5, 0.5)):
        """0.5 = middle of tile ;)
           image is the filename of the image - not the surface! - that way you can simply transfer
           the images stored in world through a network quicker..."""
        self.image = image

        self.pos = pos


class MapGrid(object):
    def __init__(self, #images={"n":None},
                 colors={"-":None},
                 grid = [[]]):
##        self.images = images
        self.colors = colors
        self.grid = grid

    def get_dimensions(self):
        return len(self.grid[0]), len(self.grid)


class World(object):
    def __init__(self, surface, tile_size=(15, 10),
                 map_grid=None, background=None):

        self.tile_size = tile_size

        self.display = surface

        self.background = background


        self.grid = map_grid
        self.center = (self.display.get_width()/2,
                       self.display.get_height()/2)
        self.center_view = self.center
        self.map_size = ()

        self.__images = {}
        self.actors = []

    def load_images(self, more=[]):
        self.__images = {}
        for i in self.actors:
            self.__images[i.image] = pygame.image.load(i.image).convert_alpha()
####        for i in self.grid.images:
####            self.__images[i] = pygame.image.load(
####                                self.grid.images[i]).convert_alpha()
        for i in more:
            self.__images[i] = pygame.image.load(i).convert_alpha()

        return None

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
        dx, dy = (self.center_view[0] - self.center[0],
                  self.center_view[1] - self.center[1])
        if dx < 0:
            dx = 0
        if dy < 0:
            dy = 0

        if dx > self.map_size[0]:
            dx = self.map_size[0]
        if dy > self.map_size[1]:
            dy = self.map_size[1]

        ypos = 0
        col = self.grid.colors
        for y in self.grid.grid:
            xpos = 0
            for x in y:
                if col[x]:
                    r = (xpos * tx - dx, ypos * ty - dy,
                         tx, ty)
                    pygame.draw.rect(self.display, col[x], r)
                xpos += 1
            ypos += 1

        for i in self.actors:
            self.display.blit(img[i.image], (i.pos[0] * tx - dx,
                                             i.pos[1] * ty - dy))

    def get_mouse_pos(self):
        p = pygame.mouse.get_pos()
        dx, dy = (self.center_view[0] - self.center[0],
                  self.center_view[1] - self.center[1])
        if dx < 0:
            dx = 0
        if dy < 0:
            dy = 0

        if dx > self.map_size[0]:
            dx = self.map_size[0]
        if dy > self.map_size[1]:
            dy = self.map_size[1]

        x = (p[0] + dx) / self.tile_size[0]
        y = (p[1] + dy) / self.tile_size[1]
        return x, y
            

        

        
