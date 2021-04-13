import datetime
import sys

import pygame

from keyboard import Keyboard
from renderer import Renderer

renderer = Renderer(scale=25)
keyboard = Keyboard()


def init():
    then = datetime.datetime.now()
    step(then)
    renderer.main()


def step(then):
    now = datetime.datetime.now()
    fps = 1000 / 60
    elapsed = now - then
    # TODO(jan): Fix elapsed
    # if elapsed > fps:
    #     pass


def main():
    init()
    while True:
        pygame_screen()


def pygame_screen():
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        keyboard.listener(event)
    pygame.display.update()


main()
