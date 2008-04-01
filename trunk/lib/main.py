import world
from world import *

import util

import random

import time, os


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
##    world_screen = pygame.Surface((640, 300))
    world_screen = screen.subsurface((0, 0, 640, 300))

    mg = MapGrid(util.make_random_map())

    p = Player(mg.comp_terrs[0], (255, 0, 0))
    p.territories = mg.comp_terrs

    world = World(world_screen, map_grid=mg)
    world.players = [p]

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_s:
                    a = time.localtime()
                    a = "%s-%s-%s-%s"%(a[1], a[2], a[3], a[4])
                    pygame.image.save(screen, os.path.join("data", "screenshots",
                                                           "screenie %s.jpg"%a))

                if event.key == K_SPACE:
                    world.map_size=()
                    mg = MapGrid(util.make_random_map())
                    world.grid = mg
                    p = Player(mg.comp_terrs[0], (255, 0, 0))
                    p.territories = mg.comp_terrs
                    world.players = [p]

        screen.fill((0,0,0))
        world.render()

        x = pygame.mouse.get_pos()

        if x[0] <= 5:
            world.offset[0] -= 1
        if x[0] >= 635:
            world.offset[0] += 1

        if x[1] <= 5:
            world.offset[1] -= 1
        if x[1] >= 475:
            world.offset[1] += 1

        pos = world.get_mouse_pos()
        pygame.draw.rect(screen, (255,255,255),
                         (pos[0] * world.tile_size[0] - world.offset[0],
                          pos[1] * world.tile_size[1] - world.offset[1],
                          world.tile_size[0], world.tile_size[1]),
                         1)
        pygame.display.flip()
