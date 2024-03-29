import world
from world import *

import util
import rules, ai

import gui, wui
import config

import random

import time, os, sys

SCROLL_SPEED = 12

try:
    import psyco
    psyco.background()
except:
    pass

def make_map_players(world, num_players=7, num_ai=6):
    if num_players < 2:num_players = 2
    if num_players > 7:num_players = 7
    if num_ai < 0:num_ai = 0
    if num_ai > 7:num_ai = 7
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
        for x in i[0]:
            x.player = ret[-1]
        

    world.players = ret
    world.update()

    controllers = []
    for i in xrange(num_players-num_ai):
        controllers.append("human")
    for i in xrange(num_ai):
        controllers.append(ai.AI("AI-%s"%i, world))
    return controllers

def game(screen, myConfig, nump, numai):
    screen_size = screen.get_size()
    world_height = round(screen_size[1]*0.666) # World uses 2/3 of the screen

    app = gui.App(screen, background_color=None)
    aapp = gui.App(screen, background_color = None)
    aapp.always_render = True
    app.theme = gui.make_theme(os.path.join("data", "gui"))
    app.always_render = True
    end_turn_button = gui.Button(app, (-1, screen_size[1]), "End Turn", "End Turn",
                                widget_pos="bottomleft")
    whos_turn_label = gui.Label(app, (-1, screen_size[1]), "WT Label", "It is player 1's turn",
                          widget_pos="bottomright")
    whos_turn_label.theme.label["text-color"] = [255,0,0]
    whos_turn_label.make_image()

    if myConfig.fps_counter:
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

    aleft = wui.Arrow(aapp, (1, int(world_height/2)), "ArrowLeft", "left")
    aright = wui.Arrow(aapp, (screen_size[0]-16, int(world_height/2)), "ArrowRight", "right")
    aup = wui.Arrow(aapp, (int(screen_size[0]/2), 1), "ArrowUp", "up")
    adown = wui.Arrow(aapp, (int(screen_size[0]/2), world_height-16), "ArrowDown", "down")


    world_screen = screen.subsurface((pad_width,
                                      pad_height,
                                      screen_size[0]-pad_width*2,
                                      world_height-pad_height*2))
    world = World(world_screen, map_grid=mg,
                  background=pygame.image.load(os.path.join("data", "images", "bg1.png")).convert())
    controllers = make_map_players(world, nump, numai)
    world_rect = world.display.get_rect()
    world_rect.topleft = world.display.get_offset()

    if myConfig.music:
        pygame.mixer.music.load(os.path.join('data','music','slowtheme.ogg'))
        pygame.mixer.music.play(-1)

        sfx_battle = [pygame.mixer.Sound(os.path.join("data", "sfx", "battle1.ogg")),
                      pygame.mixer.Sound(os.path.join("data", "sfx", "battle2.ogg")),
                      pygame.mixer.Sound(os.path.join("data", "sfx", "battle3.ogg"))]
        for i in sfx_battle:
            i.set_volume(myConfig.sound_volume*0.02)

        sfx_victory = pygame.mixer.Sound(os.path.join("data", "sfx", "victory.ogg"))
        sfx_defeat = pygame.mixer.Sound(os.path.join("data", "sfx", "defeat.ogg"))

        sfx_victory.set_volume(myConfig.sound_volume*0.02)
        sfx_defeat.set_volume(myConfig.sound_volume*0.02)

        sfx_select = pygame.mixer.Sound(os.path.join("data", "sfx", "select.ogg"))

        sfx_select.set_volume(myConfig.sound_volume*0.02) 

    picktwo = []
    whos_turn = 0

    keys_down = set()

    clock = pygame.time.Clock()

    zoom_states = [(10, 5), (20, 10), (40, 20), (80, 40)]
    zoom_state = 0
    world_zoom_once = True

    while 1:
        clock.tick(600)
        if myConfig.fps_counter:
            if not pygame.time.get_ticks() % 10:
                fps_label.text = "FPS: %i" % clock.get_fps()
                fps_label.make_image()

        for event in app.get_events():
            if event.type == QUIT:
                return "QUIT"
            if event.type == KEYDOWN:
                if event.key == K_s:
                    a = time.localtime()
                    a = "%s-%s-%s-%s"%(a[1], a[2], a[3], a[4])
                    pygame.image.save(screen, os.path.join("data", "screenshots",
                                                           "screenie %s.jpg"%a))

                if event.key == K_ESCAPE:
                    a = wui.escape_screen(screen, myConfig)
                    if a == "QUIT" or a == "LEAVE":
                        return a
                    else:
                        pass#we returned to game!

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
                        if controllers[whos_turn] == "human":
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
                    if myConfig.music:
                        sfx_select.play()
                    if event.name == "End Turn":
                        if event.action == gui.GUI_EVENT_CLICK:
                            if controllers[whos_turn] == "human":
                                if myConfig.new_unit_dialog:
                                    a = wui.gain_troops(screen, world.players[whos_turn], myConfig)
                                    if a == "QUIT":
                                        return "QUIT"
                                    if a[1]: #don't do again!
                                        myConfig.new_unit_dialog = 0
                                        myConfig.save_settings()
                                world.players[whos_turn].end_turn()
                                whos_turn += 1
                                if whos_turn >= len(world.players):
                                    whos_turn = 0
                                whos_turn_label.text = "It is player %ss turn"%(whos_turn+1)
                                whos_turn_label.theme.label["text-color"] = world.players[whos_turn].color
                                whos_turn_label.make_image()
                                for i in picktwo:
                                    i[1].highlighted = False
                                picktwo = []
                                world.update()
            if event.type == MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if world_rect.collidepoint(pygame.mouse.get_pos()):
                        world.offset[0] -= event.rel[0]
                        world.offset[1] -= event.rel[1]

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
            world.update()
            world.render()
            return wui.win_screen(screen, world, myConfig)

        for i in picktwo:
            if not i[1].highlighted: # Don't force a re-render if already highlighted
                i[1].highlighted = True
                world.update()
                world.render()


        #BATTLES!
        if len(picktwo) == 1:
            if (picktwo[0][0] != whos_turn) or\
               (picktwo[0][1].units == 1) or\
               (not picktwo[0][1].can_move):
                picktwo[0][1].highlighted = False
                picktwo = []
                world.update()
        if len(picktwo) == 2:
            if picktwo[0][0] == whos_turn:
                if (not picktwo[0][1] == picktwo[1][1]) and \
                   util.connected_mass(picktwo[0][1].terr, picktwo[1][1].terr):
                    if not picktwo[0][0] == picktwo[1][0]:
                        if picktwo[0][1].can_move:
                            if myConfig.attack_dialog:
                                a = wui.do_battle(screen, picktwo, world, myConfig)
                                if a == "QUIT":
                                    return "QUIT"
                                if a[1]: #don't do again!
                                    myConfig.attack_dialog = 0
                                    myConfig.save_settings()
                                a = a[0]
                            else:
                                a = True
                            if a:
                                if myConfig.music:
                                    a = random.choice(sfx_battle)
                                    a.play()
                                    time.sleep(a.get_length()+0.1)
                                x, y = rules.perform_battle(picktwo[0][1], picktwo[1][1])
                                picktwo[0][1].units -= x
                                picktwo[1][1].units -= y

                                if x > y:
                                    if myConfig.music:
                                        sfx_defeat.play()
                                else:
                                    if myConfig.music:
                                        sfx_victory.play()
                                
                                if picktwo[1][1].units == 0:
                                    world.players[picktwo[1][0]].territories.remove(picktwo[1][1])
                                    world.players[picktwo[0][0]].territories.append(picktwo[1][1])
                                    picktwo[1][1].player = world.players[picktwo[0][0]]

                                    world.world_image = None #force rerender

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
                            if myConfig.move_dialog:
                                a = wui.move_troops(screen, picktwo, world, myConfig)
                                if a == "QUIT":
                                    return "QUIT"
                                if a[1]: #don't do again!
                                    myConfig.move_dialog = 0
                                    myConfig.save_settings()
                                a = a[0]
                            else:
                                a = True
                            if a:
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
                                pass
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

        if not controllers[whos_turn] == "human":
            end_turn_button.visible = False
            u = controllers[whos_turn]

            msg = u.update(whos_turn) # get messages from ai
            if msg[0] == "battle":
                u1, u2 = msg[1], msg[2]
                x, y = rules.perform_battle(u1, u2)
                u1.units -= x
                u2.units -= y
                
                if u2.units == 0:
                    u2.player.territories.remove(u2)
                    u1.player.territories.append(u2)
                    u2.player = u1.player

                    world.world_image = None #force rerender

                    if u2.max_units > u1.units - 1:
                        u2.units = u1.units - 1
                        u1.units = 1
                    else:
                        u2.units = u2.max_units
                        u1.units -= u2.units
                u1.update()
                u2.update()
            if msg[0] == "move":
                u1, u2 = msg[1], msg[2]
                x = u1.units - 1
                if u2.max_units >= u2.units + x:
                    pass
                else:
                    x = u2.max_units - u2.units
                u1.units -= x
                u2.units += x
                u1.update()
                u2.update()
                u1.can_move = False
            if msg[0] == "end_turn":
                controllers[whos_turn].mode = "attack"
                world.players[whos_turn].end_turn()
                whos_turn += 1
                if whos_turn >= len(world.players):
                    whos_turn = 0
                whos_turn_label.text = "It is player %ss turn"%(whos_turn+1)
                whos_turn_label.theme.label["text-color"] = world.players[whos_turn].color
                whos_turn_label.make_image()
                for i in picktwo:
                    i[1].highlighted = False
                picktwo = []
                world.update()
        else:
            end_turn_button.visible = True

        screen.fill((0,0,0))
        world.render()
        for i in world.players:
            if len(i.territories) == 0:
                i.dead = True

        if world_zoom_once:
            world_zoom_once = False
            world.tile_size = zoom_states[zoom_state]
            world.update()

        if pad_up_button.is_clicked():
            world.offset[1] -= SCROLL_SPEED
        if pad_down_button.is_clicked():
            world.offset[1] += SCROLL_SPEED
        if pad_left_button.is_clicked():
            world.offset[0] -= SCROLL_SPEED
        if pad_right_button.is_clicked():
            world.offset[0] += SCROLL_SPEED

        app.render()
        aapp.render()
        pygame.display.flip()
        if not controllers[whos_turn] == "human":
            time.sleep(0.1)

def do_settings(myConfig):
    screen_size = (myConfig.screen_width, myConfig.screen_height)
    if myConfig.fullscreen:
        screen = pygame.display.set_mode(screen_size, FULLSCREEN)
    else:
        screen = pygame.display.set_mode(screen_size)
    if myConfig.music:
        try:
            pygame.mixer.init()
        except:
            pass
        pygame.mixer.music.load(os.path.join('data','music','fasttheme.ogg'))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(myConfig.sound_volume*0.01)
    else:
        try:
            pygame.mixer.quit()
        except:
            pass
    return screen

def main():
    myConfig = config.Config()
    pygame.init()
    screen = do_settings(myConfig)

    goto = "MainMenu"
    while 1:
        if goto == "MainMenu":
            a = wui.MainMenu(screen, myConfig)
            if a == "QUIT":
                pygame.quit()
                return
            if a == "PlaySingle":
                goto = "Game"
            if a == "Options":
                goto = a
            if a == "Tut":
                goto = "Tut"
        if goto == "Tut":
            a = wui.Tutorial(screen, myConfig)
            if a == "QUIT":
                pygame.quit()
                return
            goto = "MainMenu"
        if goto == "Game":
            c = wui.pre_single_game(screen, myConfig)
            if c == "QUIT":
                pygame.quit()
                return
            if c == "MainMenu":
                goto = c
                continue
            wui.map_loading(screen)
            a = game(screen, myConfig, c[1], c[2])
            if a == "QUIT":
                pygame.quit()
                return
            goto = "MainMenu"
            if myConfig.music:
                pygame.mixer.music.load(os.path.join('data','music','fasttheme.ogg'))
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(myConfig.sound_volume*0.01)
        if goto == "Options":
            a = wui.Options(screen, myConfig)
            if a == "QUIT":
                pygame.quit()
                return
            goto = "MainMenu"
            screen = do_settings(myConfig)
