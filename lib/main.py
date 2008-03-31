import world
from world import *

import util

import random


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    mg = MapGrid({1: (255, 0, 0),
                    2: (0, 255, 0),
                    3: (0, 0, 255),
                    4: (255, 255, 0),
                    5: (255, 0, 255),
                    6: (0, 255, 255),
                    7: (255, 255, 255),
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
