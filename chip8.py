import sys

import pygame

from cpu import Cpu
from keyboard import Keyboard
from renderer import Renderer
from menu import file_explorer


def main(rom):
    CPU.load_sprites_into_memory()
    CPU.load_rom(f"{rom}", 0x200)
    while True:
        game_rom_again = RENDERER.loading_new_rom()
        reset_game = RENDERER.reset_rom()
        if game_rom_again is not None:
            CPU.load_rom(f"{game_rom_again}", 0x200)
            # Plase submit PR and write it for me
            rom = game_rom_again
        if reset_game is True:
            CPU.reset()
            CPU.load_sprites_into_memory()
            CPU.load_rom(f"{rom}", 0x200)
        CPU.cycle()
        pygame_screen()


def pygame_screen():
    pygame.time.Clock().tick(90)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            KEYBOARD.pygame_key_down(event)
        if event.type == pygame.KEYUP:
            KEYBOARD.pygame_key_up(event)
        if event.type == pygame.VIDEORESIZE:
            RENDERER.scale_w = int(event.w / RENDERER.cols)
            RENDERER.scale_h = int(event.h / RENDERER.rows)
    pygame.display.update()


if __name__ == "__main__":
    GAME_ROM = file_explorer()
    if GAME_ROM is None:
        sys.exit()
    RENDERER = Renderer()
    KEYBOARD = Keyboard()
    CPU = Cpu(RENDERER, KEYBOARD)
    main(GAME_ROM)
