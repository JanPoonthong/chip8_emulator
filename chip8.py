import sys
import argparse

import pygame

from cpu import Cpu
from keyboard import Keyboard
from renderer import Renderer


def main(game_rom, renderer):
    cpu.load_sprites_into_memory()
    cpu.load_rom(f"{game_rom}", 0x200)
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
            renderer.scale_w = event.w / renderer.cols
            renderer.scale_h = event.h / renderer.rows
    pygame.display.update()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Chip-8 is a simple, interpreted,
    programming language which was first used on some do-it-yourself computer
    systems."""
    )
    parser.add_argument("--scale", type=int, help="number of scale")
    parser.add_argument("rom", help="the ROM file to load on startup")
    args = parser.parse_args()
    number_of_scale = args.scale
    game_rom = args.rom
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    renderer = Renderer(scale=number_of_scale)
    keyboard = Keyboard()
    cpu = Cpu(renderer, keyboard)
    main(game_rom, renderer)
