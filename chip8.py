import sys

import pygame

from cpu import Cpu
from keyboard import Keyboard
from renderer import Renderer

renderer = Renderer(scale=20)
keyboard = Keyboard()
cpu = Cpu(renderer, keyboard)


def main():
    cpu.load_sprites_into_memory()
    cpu.load_rom("PONG", 0x200)
    while True:
        cpu.cycle()
        pygame_screen()


def pygame_screen():
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keyboard.pygame_key_down(event)
        if event.type == pygame.KEYUP:
            keyboard.pygame_key_up(event)
    pygame.display.update()


main()
