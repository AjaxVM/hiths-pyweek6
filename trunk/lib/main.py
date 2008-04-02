import world
from world import *

import util

import random

import time, os

def make_map_players(world):
    mg = MapGrid(util.make_random_map())

    world.grid = mg
    world.map_size = ()

    players = []
    pterr = list(mg.comp_terrs)
    random.shuffle(pterr)
##    p = Player(mg.comp_terrs[0], (255, 0, 0))
##    p.territories = mg.comp_terrs
##    for i in xrange(7):
##        new = Player
    new = Player(mg.comp_terrs[0], mg.comp_terrs[0:4], (255, 0, 0))
    players.append(new)

    new = Player(mg.comp_terrs[4], mg.comp_terrs[4:8], (0, 255, 0))
    players.append(new)

    new = Player(mg.comp_terrs[8], mg.comp_terrs[8:12], (0, 0, 255))
    players.append(new)

    new = Player(mg.comp_terrs[12], mg.comp_terrs[12:16], (255, 255, 0))
    players.append(new)

    new = Player(mg.comp_terrs[16], mg.comp_terrs[16:20], (255, 0, 255))
    players.append(new)

    new = Player(mg.comp_terrs[20], mg.comp_terrs[20:24], (0, 255, 255))
    players.append(new)

    new = Player(mg.comp_terrs[24], mg.comp_terrs[24:28], (255, 125, 125))
    players.append(new)

    world.players = players


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
##    world_screen = pygame.Surface((640, 300))
    world_screen = screen.subsurface((0, 0, 640, 320))

    mg = MapGrid(util.make_random_map())

##    p = Player(mg.comp_terrs[0], (255, 0, 0))
##    p.territories = mg.comp_terrs

    world = World(world_screen, map_grid=mg)
##    world.players = [p]
    make_map_players(world)

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
##                    world.map_size=()
                    mg = MapGrid(util.make_random_map())
                    world.grid = mg
##                    p = Player(mg.comp_terrs[0], (255, 0, 0))
##                    p.territories = mg.comp_terrs
##                    world.players = [p]
                    make_map_players(world)

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = world.get_mouse_terr()
                    if x:
                        print "clicked player territry: %s"%x

        screen.fill((0,0,0))
        world.render()

        x = pygame.mouse.get_pos()

        if x[0] <= 5:
            world.offset[0] -= 4
        if x[0] >= 635:
            world.offset[0] += 4

        if x[1] <= 5:
            world.offset[1] -= 4
        if x[1] >= 475:
            world.offset[1] += 4

        pos = world.get_mouse_pos()
        pygame.draw.rect(screen, (255,255,255),
                         (pos[0] * world.tile_size[0] - world.offset[0],
                          pos[1] * world.tile_size[1] - world.offset[1],
                          world.tile_size[0], world.tile_size[1]),
                         1)
        pygame.display.flip()
