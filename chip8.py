import sys

import pygame

from cpu import Cpu
from keyboard import Keyboard
from renderer import Renderer
from menu import file_explorer


def main(game_rom, renderer):
    game_rom_again = renderer.menu_bar()
    cpu.load_sprites_into_memory()
    if game_rom_again is None:
        cpu.load_rom(f"{game_rom}", 0x200)
    else:
        cpu.load_rom(f"{game_rom_again}", 0x200)
    while True:
        cpu.cycle()
        pygame_screen(renderer)


def pygame_screen(renderer):
    pygame.time.Clock().tick(90)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keyboard.pygame_key_down(event)
        if event.type == pygame.KEYUP:
            keyboard.pygame_key_up(event)
        if event.type == pygame.VIDEORESIZE:
            renderer.scale_w = int(event.w / renderer.cols)
            renderer.scale_h = int(event.h / renderer.rows)
    pygame.display.update()


if __name__ == "__main__":
    game_rom = file_explorer()
    renderer = Renderer()
    keyboard = Keyboard()
    cpu = Cpu(renderer, keyboard)
    main(game_rom, renderer)
