import os

import pygame
from pygame.locals import *

import gui, rules

class CheckBox(object):
    def __init__(self, parent, pos, name, widget_pos="topleft"):
        self.name = name
        self.button = gui.Button(parent, pos, name, "X", widget_pos)
        self.button.over_width = self.button.image.get_width()
        self.button.over_height = self.button.image.get_height()
        self.state = True

        self.toggle()

    def toggle(self):
        self.state = not self.state
        if self.state:
            self.button.text = "X"
        else:
            self.button.text = " "
        self.button.make_image()

    def set_state(self, s):
        self.state = s
        if self.state:
            self.button.text = "X"
        else:
            self.button.text = " "
        self.button.make_image()

    def event(self, event):
        if event.name == self.button.name:
            if event.action == gui.GUI_EVENT_CLICK:
                self.toggle()

class Arrow(gui.Widget):
    def __init__(self, parent, pos, name,
                 arrow="up"):
        gui.Widget.__init__(self, parent, pos, name, "center", None)

        self.over_width = None

        self.image = pygame.image.load(os.path.join("data", "gui", "arrow_%s.png"%arrow)).convert_alpha()

    def render(self, surface):
        self.rect.center = self.pos
        surface.blit(self.image, self.rect.topleft)
        return None

def get_username(screen):
    app = gui.App(pygame.Surface(screen.get_size()))
    app.theme = gui.make_theme(os.path.join("data", "gui"))

    inp = gui.TextInputBox(app, (-1, -1), "Input1",
                           "username", "testy",
                           widget_pos="center")
    inp.focused = True
    inp.make_text()

    while 1:
        for event in app.get_events():
            if event.type == QUIT:
                return "QUIT"
            if event.type == gui.GUI_EVENT:
                if event.widget == gui.TextInputBox:
                    if event.name == "Input1":
                        if event.action == gui.GUI_EVENT_INPUT:
                            return event.string
            if event.type == QUIT:
                pygame.quit()
                return

        screen.blit(app.render(), (0,0))
        pygame.display.flip()

def get_bad_username(screen):
    app = gui.App(pygame.Surface(screen.get_size()))
    app.theme = gui.make_theme(os.path.join("data", "gui"))

    l = gui.Label(app, (-1, -1), "Label1", "User name already in use",
                  widget_pos="midbottom")

    inp = gui.TextInputBox(app, (-1, -1), "Input1",
                           "username", "pick new username",
                           widget_pos="midtop")
    inp.focused = True
    inp.make_text()

    while 1:
        for event in app.get_events():
            if event.type == QUIT:
                return "QUIT"
            if event.type == gui.GUI_EVENT:
                if event.widget == gui.TextInputBox:
                    if event.name == "Input1":
                        if event.action == gui.GUI_EVENT_INPUT:
                            return event.string
            if event.type == QUIT:
                pygame.quit()
                return

        screen.blit(app.render(), (0,0))
        pygame.display.flip()

def do_battle(screen, picktwo, world, myConfig):
    bg = screen.copy()
    app = gui.App(pygame.Surface(screen.get_size()).convert_alpha(), background_color=(0,0,0,0))
    app.theme = gui.make_theme(os.path.join("data", "gui"))

    main_win = gui.Window(app, (-1, -1), "MainWindow", "center", [300, 260],
                          caption="Fight!")

    p1_label1 = gui.Label(main_win, (-1, -1), "P1_LABEL1", "Player %s:"%(picktwo[0][0]+1),
                          widget_pos="bottomright")
    p1_label2 = gui.Label(main_win, (-1, -1), "P1_LABEL2", "%s    "%picktwo[0][1].units,
                          widget_pos="topright")
    p1_label1.theme.label["text-color"] = world.players[picktwo[0][0]].color
    p1_label2.theme.label["text-color"] = world.players[picktwo[0][0]].color
    p1_label1.make_image()
    p1_label2.make_image()

    p2_label1 = gui.Label(main_win, (-1, -1), "P2_LABEL1", "Player %s:"%(picktwo[1][0]+1),
                          widget_pos="bottomleft")
    p2_label2 = gui.Label(main_win, (-1, -1), "P2_LABEL2", "    %s"%picktwo[1][1].units,
                          widget_pos="topleft")
    if picktwo[1][1].capitol:
        p2_label2.text = p2_label2.text + " + capitol"
    p2_label1.theme.label["text-color"] = world.players[picktwo[1][0]].color
    p2_label2.theme.label["text-color"] = world.players[picktwo[1][0]].color
    p2_label1.make_image()
    p2_label2.make_image()


    attack_button = gui.Button(main_win, (-1, 260), "ATTACK", "Attack!",
                               widget_pos="bottomright")
    cancel_button = gui.Button(main_win, (-1, 260), "CANCEL", "Cancel",
                               widget_pos="bottomleft")

    do_again = CheckBox(main_win, (300, 0), "CB1", "topright")
    dal = gui.Label(main_win, (300-do_again.button.over_width,
                               do_again.button.over_height),
                    "DALabel", "Don't show again: ",
                    widget_pos="bottomright")

    if myConfig.music:
        sfx_select = pygame.mixer.Sound(os.path.join("data", "sfx", "select.ogg"))

        sfx_select.set_volume(myConfig.sound_volume*0.02) 

    while 1:
        for event in app.get_events():
            if event.type == QUIT:
                return "QUIT"
            if event.type == gui.GUI_EVENT:
                if event.name == "MainWindow":
                    event = event.subevent
                    do_again.event(event)
                    if event.widget == gui.Button:
                        if myConfig.music:
                            sfx_select.play()
                    if event.name == "ATTACK" and event.action == gui.GUI_EVENT_CLICK:
                        return True, do_again.state
                    if event.name == "CANCEL" and event.action == gui.GUI_EVENT_CLICK:
                        return False, do_again.state

        screen.blit(bg, (0,0))
        screen.blit(app.render(), (0,0))
        pygame.display.flip()

def move_troops(screen, picktwo, world, myConfig):
    bg = screen.copy()
    app = gui.App(pygame.Surface(screen.get_size()).convert_alpha(), background_color=(0,0,0,0))
    app.theme = gui.make_theme(os.path.join("data", "gui"))

    main_win = gui.Window(app, (-1, -1), "MainWindow", "center", [300, 260],
                          caption="transfer Forces")

    p1_label1 = gui.Label(main_win, (-1, -1), "P1_LABEL1", "Troops:  -",
                          widget_pos="bottomright")
    p1_label2 = gui.Label(main_win, (-1, -1),
                          "P1_LABEL2", "%s/%s   "%(picktwo[0][1].units, picktwo[0][1].max_units),
                          widget_pos="topright")
    p1_label1.theme.label["text-color"] = world.players[picktwo[0][0]].color
    p1_label2.theme.label["text-color"] = world.players[picktwo[0][0]].color
    p1_label1.make_image()
    p1_label2.make_image()

    p2_label1 = gui.Label(main_win, (-1, -1), "P2_LABEL1", ">  Troops:",
                          widget_pos="bottomleft")
    p2_label2 = gui.Label(main_win, (-1, -1), "P2_LABEL2",
                          "   %s/%s"%(picktwo[1][1].units, picktwo[1][1].max_units),
                          widget_pos="topleft")
    p2_label1.theme.label["text-color"] = world.players[picktwo[1][0]].color
    p2_label2.theme.label["text-color"] = world.players[picktwo[1][0]].color
    p2_label1.make_image()
    p2_label2.make_image()


    attack_button = gui.Button(main_win, (-1, 260), "TRANSFER", "Move!",
                               widget_pos="bottomright")
    cancel_button = gui.Button(main_win, (-1, 260), "CANCEL", "Cancel",
                               widget_pos="bottomleft")

    do_again = CheckBox(main_win, (300, 0), "CB1", "topright")
    dal = gui.Label(main_win, (300-do_again.button.over_width,
                               do_again.button.over_height),
                    "DALabel", "Don't show again: ",
                    widget_pos="bottomright")

    if myConfig.music:
        sfx_select = pygame.mixer.Sound(os.path.join("data", "sfx", "select.ogg"))

        sfx_select.set_volume(myConfig.sound_volume*0.02) 

    while 1:
        for event in app.get_events():
            if event.type == QUIT:
                return "QUIT"
            if event.type == gui.GUI_EVENT:
                if event.name == "MainWindow":
                    event = event.subevent
                    do_again.event(event)
                    if event.widget == gui.Button:
                        if myConfig.music:
                            sfx_select.play()
                    if event.name == "TRANSFER" and event.action == gui.GUI_EVENT_CLICK:
                        return True, do_again.state
                    if event.name == "CANCEL" and event.action == gui.GUI_EVENT_CLICK:
                        return False, do_again.state

        screen.blit(bg, (0,0))
        screen.blit(app.render(), (0,0))
        pygame.display.flip()

def gain_troops(screen, player, myConfig):
    bg = screen.copy()
    app = gui.App(pygame.Surface(screen.get_size()).convert_alpha(), background_color=(0,0,0,0))
    app.theme = gui.make_theme(os.path.join("data", "gui"))

    main_win = gui.Window(app, (-1, -1), "MainWindow", "center", [300, 260],
                          caption="Gain Troops")

    p1_label1 = gui.Label(main_win, (-1, -1), "P1_LABEL1", "New Troops: ",
                          widget_pos="midright")
    p1_label2 = gui.Label(main_win, (-1, -1),
                          "P1_LABEL2", "%s"%player.get_terr_holding(),
                          widget_pos="midleft")
    p1_label1.theme.label["text-color"] = player.color
    p1_label2.theme.label["text-color"] = player.color
    p1_label1.make_image()
    p1_label2.make_image()

    cont_button = gui.Button(main_win, (-1, 260), "CONTINUE", "Continue",
                               widget_pos="midbottom")


    do_again = CheckBox(main_win, (300, 0), "CB1", "topright")
    dal = gui.Label(main_win, (300-do_again.button.over_width,
                               do_again.button.over_height),
                    "DALabel", "Don't show again: ",
                    widget_pos="bottomright")

    if myConfig.music:
        sfx_select = pygame.mixer.Sound(os.path.join("data", "sfx", "select.ogg"))

        sfx_select.set_volume(myConfig.sound_volume*0.02) 

    while 1:
        for event in app.get_events():
            if event.type == QUIT:
                return "QUIT"
            if event.type == gui.GUI_EVENT:
                if event.name == "MainWindow":
                    event = event.subevent
                    do_again.event(event)
                    if event.widget == gui.Button:
                        if myConfig.music:
                            sfx_select.play()
                    if event.name == "CONTINUE" and event.action == gui.GUI_EVENT_CLICK:
                        return True, do_again.state

        screen.blit(bg, (0,0))
        screen.blit(app.render(), (0,0))
        pygame.display.flip()

def Options(screen, myConfig):
    app = gui.App(pygame.Surface(screen.get_size()))
    app.theme = gui.make_theme(os.path.join("data", "gui"))

    ol = gui.Label(app, (-1, 0),
                              "GNL", "Options:",
                              widget_pos="midtop")
    ol.theme.font["size"] = 45
    ol.theme.label["text-color"] = (0, 255, 0)
    ol.make_image()

    goback = gui.Button(app, screen.get_size(), "GB", "Return",
                           widget_pos="bottomright")
    goback.theme.font["size"] = 25
    goback.theme.button["text-color"] = (125, 255, 125)
    goback.make_image()

    #make entries...
    entries = []
    boxes = []
    for i in ["fullscreen", "music", "fps_counter",
              "attack_dialog", "move_dialog", "new_unit_dialog"]:
        if not entries:
            if i.find("dialog") != -1:
                x = "disable " + i
            else:
                x = i
            new = gui.Label(app, (15, 60), i, x,
                            widget_pos="topleft")
            entries.append(new)
            do_again = CheckBox(app, (375, 55), i, "topright")
            do_again.set_state(getattr(myConfig, i))
            boxes.append(do_again)
        else:
            if i.find("dialog") != -1:
                x = "disable " + i
            else:
                x = i
            new = gui.Label(app, (15, entries[-1].rect.bottom+15), i, x,
                            widget_pos="topleft")
            entries.append(new)
            do_again = CheckBox(app, (375, entries[-2].rect.bottom+10), i, "topright")
            do_again.set_state(getattr(myConfig, i))
            boxes.append(do_again)

    if myConfig.music:
        sfx_select = pygame.mixer.Sound(os.path.join("data", "sfx", "select.ogg"))

        sfx_select.set_volume(myConfig.sound_volume*0.02) 

    sdlabel = gui.Label(app, (screen.get_width(), 60),
                        "SDLabel", "display: ",
                        widget_pos="topright")
    screendim = gui.MenuList(app, sdlabel.rect.bottomright, "ScreenDim",
                         ["640x480", "800x600", "1024x768"],
                         widget_pos="topright")

    vlabel = gui.Label(app, (screen.get_width(), screendim.rect.bottom + 15),
                       "sound_volume", "sound_volume: ", widget_pos="topright")
    vbar = gui.ScrollBar(app, vlabel.rect.bottomright,
                         "SV_bar", widget_pos="topright",
                         tot_size=[10000, 10], view_size=[100, 10],
                         start_value=0, direction=0)
    vbar.current_value = myConfig.sound_volume * 0.7

    while 1:
        for event in app.get_events():
            if event.type == QUIT:
                return "QUIT"
            if event.type == gui.GUI_EVENT:
                for i in boxes:
                    i.event(event)
                if event.widget == gui.Button:
                    if myConfig.music:
                        sfx_select.play()
                if event.name == "GB":
                    if event.action == gui.GUI_EVENT_CLICK:
                        #prepare config
                        for i in boxes:
                            s = 0
                            if i.state:
                                s = 1
                            setattr(myConfig, i.name, s)
                        setattr(myConfig, "sound_volume", int(vbar.current_value * 1.4))
                        myConfig.save_settings()
                        return "MainMenu"
                if event.name == "ScreenDim":
                    if event.action == gui.GUI_EVENT_CLICK:
                        a = event.entry.split("x")
                        myConfig.screen_width = int(a[0])
                        myConfig.screen_height = int(a[1])

        screen.blit(app.render(), (0,0))
        pygame.display.flip()


def MainMenu(screen, myConfig):
    app = gui.App(pygame.Surface(screen.get_size()))
    app.theme = gui.make_theme(os.path.join("data", "gui"))

    game_name_label = gui.Label(app, (-1, 0),
                              "GNL", "RoboWars",
                              widget_pos="midtop")
    game_name_label.theme.font["size"] = 60
    game_name_label.theme.label["text-color"] = (0, 255, 0)
    game_name_label.make_image()

    play_game = gui.Button(app, (-1, -1), "PlaySingle", "Start Single Player Game",
                           widget_pos="midbottom")
    play_game.theme.font["size"] = 25
    play_game.theme.button["text-color"] = (125, 255, 125)
    play_game.make_image()

    optionsb = gui.Button(app, play_game.rect.midbottom, "OB", "Options",
                           widget_pos="midtop")

    exit_game = gui.Button(app, optionsb.rect.midbottom, "Exit", "Exit",
                           widget_pos="midtop")

    if myConfig.music:
        sfx_select = pygame.mixer.Sound(os.path.join("data", "sfx", "select.ogg"))

        sfx_select.set_volume(myConfig.sound_volume*0.02) 

    while 1:
        for event in app.get_events():
            if event.type == QUIT:
                return "QUIT"
            if event.type == gui.GUI_EVENT:
                if event.widget == gui.Button:
                    if myConfig.music:
                        sfx_select.play()
                if event.name == "PlaySingle":
                    if event.action == gui.GUI_EVENT_CLICK:
                        return "PlaySingle"
                if event.name == "OB":
                    if event.action == gui.GUI_EVENT_CLICK:
                        return "Options"
                if event.name == "Exit":
                    if event.action == gui.GUI_EVENT_CLICK:
                        return "QUIT"

        screen.blit(app.render(), (0,0))
        pygame.display.flip()

def pre_single_game(screen, myConfig):
    app = gui.App(pygame.Surface(screen.get_size()))
    app.theme = gui.make_theme(os.path.join("data", "gui"))

    ol = gui.Label(app, (-1, 0),
                              "GNL", "Game Options:",
                              widget_pos="midtop")
    ol.theme.font["size"] = 45
    ol.theme.label["text-color"] = (0, 255, 0)
    ol.make_image()

    start = gui.Button(app, screen.get_size(), "SG", "Begin Game",
                           widget_pos="bottomright")
    start.theme.font["size"] = 25
    start.theme.button["text-color"] = (125, 255, 125)
    start.make_image()

    goback = gui.Button(app, start.rect.bottomleft, "GB", "Return",
                           widget_pos="bottomright")

    nump = gui.Label(app, (-1, -1),
                        "NumP", "players: 7",
                        widget_pos="midbottom")
    nbar = gui.ScrollBar(app, nump.rect.midright,
                         "NP_bar", widget_pos="midleft",
                         tot_size=[700, 10], view_size=[100, 10],
                         start_value=0, direction=0)
    nbar.current_value = 7 * 10#yields 7
    nbar.max_value = 70
    nbar.min_value = 20

    if myConfig.music:
        sfx_select = pygame.mixer.Sound(os.path.join("data", "sfx", "select.ogg"))

        sfx_select.set_volume(myConfig.sound_volume*0.02) 

    num_ai = gui.Label(app, (-1, -1),
                       "AI", "ai players: 6", widget_pos="midtop")
    vbar = gui.ScrollBar(app, num_ai.rect.midright,
                         "NA_bar", widget_pos="midleft",
                         tot_size=[700, 10], view_size=[100, 10],
                         start_value=0, direction=0)
    vbar.current_value = 6 * 10

    while 1:
        a = int(nbar.current_value/10)
        b = int(vbar.current_value/10)
        if b > a:
            b = a
            vbar.current_value = b*10
        nump.text = "players: %s"%a
        num_ai.text = "ai players: %s"%b
        nump.make_image()
        num_ai.make_image()
        for event in app.get_events():
            if event.type == QUIT:
                return "QUIT"
            if event.type == gui.GUI_EVENT:
                if event.widget == gui.Button:
                    if myConfig.music:
                        sfx_select.play()
                if event.name == "GB":
                    if event.action == gui.GUI_EVENT_CLICK:
                        return "MainMenu"
                if event.name == "SG":
                    if event.action == gui.GUI_EVENT_CLICK:
                        return "PlayGame", a, b

        screen.blit(app.render(), (0,0))
        pygame.display.flip()

def map_loading(screen):
    app = gui.App(pygame.Surface(screen.get_size()))
    app.theme = gui.make_theme(os.path.join("data", "gui"))

    game_name_label = gui.Label(app, (-1, 0),
                              "GNL", "RoboWars",
                              widget_pos="midtop")
    game_name_label.theme.font["size"] = 60
    game_name_label.theme.label["text-color"] = (0, 255, 0)
    game_name_label.make_image()

    message = gui.Label(app, (-1, -1),
                              "GNL", "Map is loading... please wait...",
                              widget_pos="midtop")
    message.theme.font["size"] = 35
    message.theme.label["text-color"] = (255, 0, 0)
    message.make_image()

    screen.blit(app.render(), (0,0))
    pygame.display.flip()
