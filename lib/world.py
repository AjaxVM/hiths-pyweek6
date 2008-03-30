import time

import pygame
from pygame.locals import *

class Actor(object):
    def __init__(self, image, pos, life=-1):
        """pos = (x, y) pos.
           0.5, 0.5 = middle of tile 0, 0."""
        self.image = image
        self.pos = pos

        self.life = life
        self.start_time = time.time()

        self.dead = False

class Controller(object):
    def __init__(self, actor):
        self.actor = actor

class MapGrid(object):
    def __init__(self, images={"n":None},
                 grid = [[]]):
        self.images = images
        self.grid = grid

        self.make_map()

    def make_map(self):
        new = []
        for i in self.grid:
            cur = []
            for x in i:
                cur.append(self.images[x])
            new.append(cur)

class World(object):
    def __init__(self, surface, size, tile_size=(25),
                 background=None):

        self.size = size
        self.tile_size = tile_size

        self.display = surface

        self.background = background


        self.actors = []
        self.map = None

    def update(self):
        for i in self.actors:
            if not i.age == -1:
                if time.time() - i.start_time > i.life:
                    i.dead = True
                    self.actors.remove(i)

    def render(self):
        pass
