import pygame

from menu import file_explorer


class Renderer:
    def __init__(self):
        pygame.init()
        self.cursor_on_file = None
        self.cursor_on_file_reset = None
        self.cols = 64
        self.rows = 32
        width = self.cols * self.rows
        height = self.rows * self.rows
        self.scale_w = self.rows
        self.scale_h = self.rows
        self.display = [0] * (self.cols * self.rows)
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.color = 255, 255, 255
        self.color_dark = 100, 100, 100
        self.color_light = 170, 170, 170
        self.font = pygame.font.SysFont("Corbel", 20)
        pygame.display.set_caption("Chip-8 emulator")

    def set_pixel(self, x, y):
        """
        :return: returns True, a pixel was erased. If returns False, nothing was
        erased.
        """
        if x >= self.cols:
            x -= self.cols
        elif x < 0:
            x += self.cols

        if y >= self.rows:
            y -= self.rows
        elif y < 0:
            y += self.rows

        pixel_locate = x + (y * self.cols)
        self.display[pixel_locate] ^= 1
        return not self.display[pixel_locate]

    def clear(self):
        self.display = [0] * (self.cols * self.rows)

    def mouse_position(self):
        mouse = pygame.mouse.get_pos()
        self.cursor_on_file = (
            13 / 2 <= mouse[0] <= 13 / 2 + 27
            and 3 / 2 <= mouse[1] <= 3 / 2 + 17
        )
        self.cursor_on_file_reset = (
            98 <= mouse[0] <= 98 + 32 and 3 / 2 <= mouse[1] <= 3 / 2 + 17
        )

    def render(self):
        """
        x goes through width of the screen and y goes through height of the
        screen.
        """
        self.screen.fill((0, 0, 0))
        for i in range(self.cols * self.rows):
            offset = [15, 25]
            x = ((i % self.cols) * self.scale_w) + offset[0]
            y = ((i // self.cols) * self.scale_h) + offset[1]

            if self.display[i] == 1:
                pygame.draw.rect(
                    self.screen,
                    (255, 255, 255),
                    (x, y, self.scale_w, self.scale_h),
                )
        self.menu_bar()
        self.reset_button()

    def menu_bar(self):
        self.mouse_position()
        text = self.font.render("File", True, self.color)
        if self.cursor_on_file:
            pygame.draw.rect(self.screen, self.color_dark, (13, 3, 27, 17))
        else:
            pygame.draw.rect(self.screen, self.color_light, (13, 3, 27, 17))
        self.screen.blit(text, (15, 5))

    def loading_new_rom(self):
        if pygame.mouse.get_pressed()[0] and self.cursor_on_file:
            game_rom = file_explorer()
            return game_rom

    def reset_button(self):
        self.mouse_position()
        text = self.font.render("Rest", True, self.color)
        if self.cursor_on_file_reset:
            pygame.draw.rect(self.screen, self.color_dark, (98, 3, 32, 17))
        else:
            pygame.draw.rect(self.screen, self.color_light, (98, 3, 32, 17))
        self.screen.blit(text, (100, 5))

    def reset_rom(self):
        if pygame.mouse.get_pressed()[0] and self.cursor_on_file_reset:
            self.clear()
            return True
