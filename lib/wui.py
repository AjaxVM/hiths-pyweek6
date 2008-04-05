import os

import pygame
from pygame.locals import *

import gui, rules

class CheckBox(object):
    def __init__(self, parent, pos, name, widget_pos="topleft"):
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

    def event(self, event):
        if event.name == self.button.name:
            if event.action == gui.GUI_EVENT_CLICK:
                self.toggle()

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

def do_battle(screen, picktwo, world):
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

    while 1:
        for event in app.get_events():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == gui.GUI_EVENT:
                if event.name == "MainWindow":
                    event = event.subevent
                    do_again.event(event)
                    if event.name == "ATTACK" and event.action == gui.GUI_EVENT_CLICK:
                        return True, do_again.state
                    if event.name == "CANCEL" and event.action == gui.GUI_EVENT_CLICK:
                        return False, do_again.state

        screen.blit(bg, (0,0))
        screen.blit(app.render(), (0,0))
        pygame.display.flip()

def move_troops(screen, picktwo, world):
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

    while 1:
        for event in app.get_events():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == gui.GUI_EVENT:
                if event.name == "MainWindow":
                    event = event.subevent
                    do_again.event(event)
                    if event.name == "TRANSFER" and event.action == gui.GUI_EVENT_CLICK:
                        return True, do_again.state
                    if event.name == "CANCEL" and event.action == gui.GUI_EVENT_CLICK:
                        return False, do_again.state

        screen.blit(bg, (0,0))
        screen.blit(app.render(), (0,0))
        pygame.display.flip()
