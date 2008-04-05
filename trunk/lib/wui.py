import os

import pygame
from pygame.locals import *

import gui

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
