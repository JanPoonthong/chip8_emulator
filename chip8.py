import sys

import pygame

from cpu import Cpu
from keyboard import Keyboard
from renderer import Renderer
from menu import file_explorer


def main(game_rom):
    cpu.load_sprites_into_memory()
    cpu.load_rom(f"{game_rom}", 0x200)
    while True:
        game_rom_again = renderer.loading_new_rom()
        reset_game = renderer.reset_rom()
        if game_rom_again is not None:
            cpu.load_rom(f"{game_rom_again}", 0x200)
            if reset_game is True:
                cpu.reset()
                cpu.load_sprites_into_memory()
                cpu.load_rom(f"{game_rom_again}", 0x200)
        if reset_game is True:
            cpu.reset()
            cpu.load_sprites_into_memory()
            cpu.load_rom(f"{game_rom}", 0x200)
        cpu.cycle()
        pygame_screen()


def pygame_screen():
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
    while game_rom is None:
        sys.exit()
        if game_rom is not None:
            break
    renderer = Renderer()
    keyboard = Keyboard()
    cpu = Cpu(renderer, keyboard)
    main(game_rom)
