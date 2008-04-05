import world
from world import *

import util
import rules

import gui, wui
import config

import random

import time, os, sys

pygame.mixer.init()

SCROLL_ZONE = 5
SCROLL_SPEED = 12

conf = None # Contains all user configs
if os.path.exists("settings.py"): # Get user settings if any
    import settings
    conf = settings.c
else: # Or load defaults
    conf = config.Config()

try:
    import psyco
    psyco.background()
except:
    pass

def make_map_players(world, num_players=2):
    mg = MapGrid(util.make_random_map())

    world.grid = mg
    world.map_size = ()

    players = []
    pterr = list(mg.comp_terrs)
    random.shuffle(pterr)

    colors = [(255, 0, 0),
              (0, 255, 0),
              (0, 0, 255),
              (255, 255, 0),
              (255, 0, 255),
              (0, 255, 255),
              (255, 125, 125)]
    for i in xrange(num_players):
        new = random.choice(pterr)
        pterr.remove(new)
        players.append([[new], colors[i]])

    

    while pterr:
        for i in players:
            if pterr:
                new = random.choice(pterr)
                pterr.remove(new)
                i[0].append(new)

    ret = []
    for i in players:
        ret.append(Player(i[0], i[1]))
        

    world.players = ret
    world.update()

def game(screen):
    screen_size = screen.get_size()
    world_height = round(screen_size[1]*0.666) # World uses 2/3 of the screen

    app = gui.App(screen, background_color=None)
    app.theme = gui.make_theme(os.path.join("data", "gui"))
    app.always_render = True
    end_turn_button = gui.Button(app, (-1, screen_size[1]), "End Turn", "End Turn",
                                widget_pos="bottomleft")
    whos_turn_label = gui.Label(app, (-1, screen_size[1]), "WT Label", "It is player 1's turn",
                          widget_pos="bottomright")
    whos_turn_label.theme.label["text-color"] = [255,0,0]
    whos_turn_label.make_image()

    fps_label = gui.Label(app, (0, screen_size[1]), "FPS Label", "FPS: ",
                          widget_pos="bottomleft")
    fps_label.theme.label["text-color"] = [255,0,0]
    fps_label.make_image()

    mg = MapGrid(util.make_random_map())

    pad_up_button = gui.Button(app, (0, 0), "PAD_UP_BUTTON", "",
                               widget_pos="topleft")
    pad_up_button.over_width = screen_size[0]
    pad_up_button.over_height = 15
    pad_up_button.make_image()

    pad_down_button = gui.Button(app, (0, world_height), "PAD_DOWN_BUTTON", "",
                               widget_pos="bottomleft")
    pad_down_button.over_width = screen_size[0]
    pad_down_button.over_height = 15
    pad_down_button.make_image()


    pad_left_button = gui.Button(app, (0, pad_up_button.image.get_height()), "PAD_LEFT_BUTTON", "",
                               widget_pos="topleft")
    pad_left_button.over_width = 15
    pad_left_button.over_height = world_height - pad_up_button.image.get_height()*2
    pad_left_button.make_image()

    pad_right_button = gui.Button(app, (screen_size[0], pad_up_button.image.get_height()), "PAD_RIGHT_BUTTON", "",
                               widget_pos="topright")
    pad_right_button.over_width = 15
    pad_right_button.over_height = world_height - pad_up_button.image.get_height()*2
    pad_right_button.make_image()

    pad_height = pad_up_button.image.get_height()
    pad_width = pad_left_button.image.get_width()


    world_screen = screen.subsurface((pad_width,
                                      pad_height,
                                      screen_size[0]-pad_width*2,
                                      world_height-pad_height*2))
    world = World(world_screen, map_grid=mg)
    make_map_players(world)

    if conf.music:
        pygame.mixer.music.load(os.path.join('data','music','slowtheme.ogg'))
        pygame.mixer.music.play(-1)

    picktwo = []
    whos_turn = 0

    keys_down = set()

    clock = pygame.time.Clock()

    zoom_states = [(10, 5), (20, 10), (40, 20), (80, 40)]
    zoom_state = 3

    while 1:
        clock.tick(600)
        if not pygame.time.get_ticks() % 10:
            fps_label.text = "FPS: %i" % clock.get_fps()
            fps_label.make_image()

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

                if event.key == K_LEFT or K_RIGHT or K_UP or K_DOWN:
                    keys_down.add(event.key)

            if event.type == KEYUP:
                try: # Ignore any attempts to remove non-existant keys
                    keys_down.remove(event.key)
                except KeyError:
                    continue

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = world.get_mouse_terr()
                    if x:
                        print "clicked player #%ss territory: %s"%(x[0]+1, x[1])
                        picktwo.append(x)
                if event.button == 4:
                    if zoom_state < 3:
                        zoom_state += 1
                        world.tile_size = zoom_states[zoom_state]
                        world.update()
                if event.button == 5:
                    if zoom_state > 0:
                        zoom_state -= 1
                        world.tile_size = zoom_states[zoom_state]
                        world.update()

            if event.type == gui.GUI_EVENT:
                if event.widget == gui.Button:
                    if event.name == "End Turn":
                        if event.action == gui.GUI_EVENT_CLICK:
                            world.players[whos_turn].end_turn()
                            whos_turn += 1
                            if whos_turn >= len(world.players):
                                whos_turn = 0
                            whos_turn_label.text = "It is player %ss turn"%(whos_turn+1)
                            whos_turn_label.theme.label["text-color"] = world.players[whos_turn].color
                            whos_turn_label.make_image()
                            world.update()

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

        for i in picktwo:
            if not i[1].highlighted: # Don't force a re-render if already highlighted
                i[1].highlighted = True
                world.update()


        #BATTLES!
        if len(picktwo) == 1:
            if (picktwo[0][0] != whos_turn) or\
               (picktwo[0][1].units == 1) or\
               (not picktwo[0][1].can_move):
                picktwo[0][1].highlighted = False
                picktwo = []
        if len(picktwo) == 2:
            if picktwo[0][0] == whos_turn:
                if (not picktwo[0][1] == picktwo[1][1]) and \
                   util.connected_mass(picktwo[0][1].terr, picktwo[1][1].terr):
                    if not picktwo[0][0] == picktwo[1][0]:
                        if picktwo[0][1].can_move:
                            if wui.do_battle(screen, picktwo, world):
                                x, y = rules.perform_battle(picktwo[0][1], picktwo[1][1])
                                picktwo[0][1].units -= x
                                picktwo[1][1].units -= y
                                
                                if picktwo[1][1].units == 0:
                                    world.players[picktwo[1][0]].territories.remove(picktwo[1][1])
                                    world.players[picktwo[0][0]].territories.append(picktwo[1][1])

                                    world.world_image = None #force rerender

                                    if world.players[picktwo[1][0]].territories == []:
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
                                print "attack canceled!"
                        else:
                            print "%s cannot move this turn!"%picktwo[0][1]
                    else:
                        print "player territories - moving units"
                        if picktwo[0][1].can_move:
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
                            print "%s cannot move this turn!"%picktwo[0][1]

                else:
                    print "not touching territories"
            else:
                print "it is player %ss turn!"%whos_turn
            for i in picktwo:
                i[1].highlighted = False
                world.update()
            picktwo = []

        screen.fill((0,0,0))
        world.render()

        if pad_up_button.is_clicked():
            world.offset[1] -= SCROLL_SPEED
        if pad_down_button.is_clicked():
            world.offset[1] += SCROLL_SPEED
        if pad_left_button.is_clicked():
            world.offset[0] -= SCROLL_SPEED
        if pad_right_button.is_clicked():
            world.offset[0] += SCROLL_SPEED

##        mpos = pygame.mouse.get_pos()
##
##        if mpos[0] <= SCROLL_ZONE or K_LEFT in keys_down:
##            world.offset[0] -= SCROLL_SPEED
##        if mpos[0] >= screen_size[0] - SCROLL_ZONE or K_RIGHT in keys_down:
##            world.offset[0] += SCROLL_SPEED
##
##        if mpos[1] <= SCROLL_ZONE or K_UP in keys_down:
##            world.offset[1] -= SCROLL_SPEED
##        if (mpos[1] >= world_height - SCROLL_ZONE and not mpos[1] > world_height) \
##            or K_DOWN in keys_down:
##            world.offset[1] += SCROLL_SPEED
##
##        if not mpos[1] > world_height: # Don't draw rect over the interface area
##            pos = world.get_mouse_pos()
##            pygame.draw.rect(screen, (255,255,255),
##                             (pos[0] * world.tile_size[0] - world.offset[0] + pad_width,
##                              pos[1] * world.tile_size[1] - world.offset[1] + pad_height,
##                              world.tile_size[0], world.tile_size[1]),
##                             1)

        app.render()
        pygame.display.flip()

def main():
    pygame.init()
    screen_size = (640, 480)
    screen = pygame.display.set_mode(screen_size)

    uname = wui.get_username(screen)

    game(screen)
