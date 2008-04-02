import world
from world import *

import util
import rules

import gui, wui

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
    world_screen = screen.subsurface((0, 0, 640, 320))

    app = gui.App(screen, background_color=None)
    app.theme = gui.make_theme(os.path.join("data", "gui"))
    app.always_render = True
    end_turn_button = gui.Button(app, (-1, 480), "End Turn", "End Turn",
                                widget_pos="bottomleft")
    whos_turn_label = gui.Label(app, (-1, 480), "WT Label", "It is player 1's turn",
                          widget_pos="bottomright")
    whos_turn_label.theme.label["text-color"] = [255,0,0]
    whos_turn_label.make_image()

    mg = MapGrid(util.make_random_map())

    world = World(world_screen, map_grid=mg)
    make_map_players(world)

    picktwo = []
    whos_turn = 0

    while 1:
        for event in app.get_events():
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
                    mg = MapGrid(util.make_random_map())
                    world.grid = mg
                    make_map_players(world)

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = world.get_mouse_terr()
                    if x:
                        print "clicked player #%ss territory: %s"%(x[0]+1, x[1])
                        picktwo.append(x)
                if event.button == 4:
                    #zoom in
                    world.tile_size = [world.tile_size[0] * 2,
                                       world.tile_size[1] * 2]
                if event.button == 5:
                    #zoom out
                    if world.tile_size[1] >= 5:
                        world.tile_size = [int(world.tile_size[0] / 2),
                                           int(world.tile_size[1] / 2)]

            if event.type == gui.GUI_EVENT:
                if event.widget == gui.Button and event.name == "End Turn":
                    if event.action == gui.GUI_EVENT_CLICK:
                        world.players[whos_turn].end_turn()
                        whos_turn += 1
                        if whos_turn >= len(world.players):
                            whos_turn = 0
                        whos_turn_label.text = "It is player %ss turn"%(whos_turn+1)
                        whos_turn_label.theme.label["text-color"] = world.players[whos_turn].color
                        whos_turn_label.make_image()

        if world.players[whos_turn].dead:
            whos_turn += 1
            if whos_turn >= len(world.players):
                whos_turn = 0
            whos_turn_label.text = "It is player %ss turn"%(whos_turn+1)
            whos_turn_label.theme.label["text-color"] = world.players[whos_turn].color
            whos_turn_label.make_image()

        if world.one_winner()[0]:
            finish_label = gui.Label(app, (-1, 375), "Finish Label", "Player %s WON!"%(world.one_winner()[1]+1),
                          widget_pos="center")
            finish_label.theme.label["text-color"] = world.players[world.one_winner()[1]].color
            finish_label.theme.label["font"] = pygame.font.Font(None, 45)
        #BATTLES!
        if len(picktwo) == 2:
            if picktwo[0][0] == whos_turn:
                if util.connected_mass(picktwo[0][1].terr, picktwo[1][1].terr):
                    if not picktwo[0][0] == picktwo[1][0]:
                        if picktwo[0][1].can_move:
                            x, y = rules.perform_battle(picktwo[0][1], picktwo[1][1])
                            picktwo[0][1].units -= x
                            picktwo[1][1].units -= y
                            if picktwo[1][1].units == 0:
                                world.players[picktwo[1][0]].territories.remove(picktwo[1][1])
                                world.players[picktwo[0][0]].territories.append(picktwo[1][1])
                                if world.players[picktwo[1][0]].territories == []:
##                                    dead.append(picktwo[1][0])
                                    world.players[picktwo[1][0]].dead = True

                                if picktwo[1][1].max_units > picktwo[0][1].units - 1:
                                    picktwo[1][1].units = picktwo[0][1].units - 1
                                    picktwo[0][1].units = 1
                                else:
                                    picktwo[1][1].units = picktwo[1][1].max_units
                                    picktwo[0][1].units -= picktwo[1][1].units
                            picktwo[0][1].update()
                            picktwo[1][1].update()

                            print "casualties: %s, %s"%(x, y)
                        else:
                            print "%s cannot move this turn!"%picktwo[0][1]
                    else:
                        print "player territories - moving units"
                        x = picktwo[0][1].units - 1
                        if picktwo[1][1].max_units >= picktwo[1][1].units + x:
                            pass
                        else:
                            x = picktwo[1][1].max_units - picktwo[1][1].units
                        picktwo[0][1].units -= x
                        picktwo[1][1].units += x
                        picktwo[0][1].update()
                        picktwo[1][1].update()
                        picktwo[1][1].can_move = False

                else:
                    print "not touching territories"
            else:
                print "it is player %ss turn!"%whos_turn

            picktwo = []

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

        app.render()
        pygame.display.flip()
