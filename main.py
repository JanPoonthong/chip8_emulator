import pygame
import sys

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

    def interpreter(self, intruction):
        self.program_counter += 2
        x = (intruction & 0x0F00) >> 8
        y = (intruction & 0x00F0) >> 4

        first_hex = intruction & 0xF000
        if first_hex == 0x0000:
            if intruction == 0x00E0:
                Output().clear()


class Input:
    def __init__(self):
        self.keyboard = [0] * 16


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
        self.drawing_pixel(black)

    def drawing_pixel(self, color):
        for x in range(self.column):
            for y in range(self.row):
                if self.get_pixel(x, y):
                    pygame.draw.rect(SCREEN, color,
                                     (x, y, 10, 10))

    def main(self):
        self.set_pixel(5, 5)
        self.set_pixel(500, 500)
        self.render_pixel()
        Emulator().interpreter(0x00E0)

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
