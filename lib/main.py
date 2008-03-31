import world
from world import *

import util

import random


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    mg = MapGrid({1:(150,90,110),
                  2:(255,0,255),
                  3:(255,0,0),
                  4:(255,255,0),
                  5:(0,255,255),
                  6:(0,0,255),
                  7:(0,255,0),
                  8:(125,125,125),
                  9:(125,0,125),
                  10:(125,0,0),
                  11:(125,125,0),
                  12:(0,125,125),
                  13:(0,0,125),
                  14:(0,0,255),
                  0:None},
                 util.make_random_map())

    world = World(screen, map_grid=mg)

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        screen.fill((0,0,0))
        world.render()

        pos = world.get_mouse_pos()
        pygame.draw.rect(screen, (255,255,255),
                         (pos[0] * world.tile_size[0],
                          pos[1] * world.tile_size[1],
                          world.tile_size[0], world.tile_size[1]),
                         1)
        pygame.display.flip()
