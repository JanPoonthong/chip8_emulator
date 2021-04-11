import pygame
import sys
import random

pygame.init()
SCREEN = pygame.display.set_mode((640, 320))


class Emulator:
    def __init__(self):
        self.memory = [0] * 4096
        self.register = [0] * 16
        self.sound_timer = 0
        self.delay_timer = 0
        self.program_counter = 0
        self.index = 0
        self.stack = []
        self.speed = 10

    def interpreter(self, instruction):
        self.program_counter += 2
        x = (instruction & 0x0F00) >> 8
        y = (instruction & 0x00F0) >> 4

        first_hex = instruction & 0xF000
        if first_hex == 0x0000:
            if instruction == 0x00E0:
                Output().clear()
            if instruction == 0x0EE:
                self.program_counter = self.stack.pop()
        if first_hex == 0x1000:
            self.program_counter = instruction & 0xFFF
        if first_hex == 0x2000:
            self.stack.append(self.program_counter)
            self.program_counter = instruction & 0xFFF
        if first_hex == 0x3000:
            if self.register[x] == instruction & 0xFF:
                self.program_counter += 2
        if first_hex == 0x4000:
            if self.register[x] != instruction & 0xFF:
                self.program_counter += 2
        if first_hex == 0x5000:
            if self.register[x] == self.register[y]:
                self.program_counter += 2
        if first_hex == 0x6000:
            self.register[x] = instruction & 0xFF
        if first_hex == 0x7000:
            self.register[x] += instruction & 0xFF
        if first_hex == 0x8000:
            last_hex = instruction & 0xF
            if last_hex == 0x0:
                self.register[x] = self.register[y]
            if last_hex == 0x1:
                self.register[x] |= self.register[y]
            if last_hex == 0x2:
                self.register[x] &= self.register[y]
            if last_hex == 0x3:
                self.register[x] ^= self.register[y]
            if last_hex == 0x4:
                # TODO(jan): set VF = carry
                self.register[x] += self.register[y]
            if last_hex == 0x5:
                # TODO(jan): set VF = NOT borrow
                self.register[x] -= self.register[y]
            if last_hex == 0x6:
                self.register[x] >>= 1
                # TODO(jan): least-significant
            if last_hex == 0x7:
                self.register[x] = self.register[y] - self.register[x]
                if self.register[y] > self.register[x]:
                    # TODO(jan): VF is set to 1
                    pass
                else:
                    # TODO(jan): VF is set to 0
                    pass
                self.register[x] -= self.register[y]
            if last_hex == 0xE:
                self.register[x] <<= 1
                # TODO(jan): most-significant
                self.register[x] *= 2
        if first_hex == 0x9000:
            if self.register[x] != self.register[y]:
                self.program_counter += 2
        if first_hex == 0xA000:
            self.index = instruction & 0xFFF
        if first_hex == 0xB000:
            self.program_counter = (instruction & 0xFFF) + self.register[0]
        if first_hex == 0xC000:
            random_bytes = random.randint(0, 255)
            self.register[y] = random_bytes & 0xFF
        if first_hex == 0xD000:
            pass


class Input:
    def __init__(self):
        self.keyboard = [0] * 16


class Rom:
    def __init__(self, filename):
        self.romdata = open(f"c8games/{filename}", "rb").read()

    def load_rom(self, memory):
        for index, val in enumerate(self.romdata):
            memory[0x200 + index] = val


class Output:
    def __init__(self):
        self.column = 640
        self.row = 320
        self.display = [0] * self.column * self.row

    def get_pixel(self, x, y):
        x, y = self.check_border(x, y)
        return self.display[x + (y * self.column)] == 1

    def check_border(self, x, y):
        if x > self.column:
            x -= self.column
        elif x < 0:
            x += self.column

        if y > self.row:
            y -= self.row
        elif y < 0:
            y += self.row

        return x, y

    def set_pixel(self, x, y):
        x, y = self.check_border(x, y)
        self.display[x + (y * self.column)] = 1
        return self.display[x + (y * self.column)]

    def clear(self):
        black = 0, 0, 0
        SCREEN.fill(black)

    def drawing_pixel(self, color):
        for x in range(self.column):
            for y in range(self.row):
                if self.get_pixel(x, y):
                    pygame.draw.rect(SCREEN, color,
                                     (x, y, 10, 10))

    def main(self):
        Rom("INVADERS").load_rom(Emulator().memory)

    def render_pixel(self):
        white = 255, 255, 255
        self.drawing_pixel(white)

    def pygame_display_screen(self):
        pygame.time.Clock().tick(15)
        self.main()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()


while True:
    Output().pygame_display_screen()
