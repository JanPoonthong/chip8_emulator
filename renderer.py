import pygame


class Renderer:
    def __init__(self, scale):
        """
        :param scale: the scale for resizing width and height
        """
        pygame.init()
        self.cols = 64
        self.rows = 32
        self.width = self.cols * scale
        self.height = self.rows * scale
        self.scale = scale
        self.display = [0] * (self.cols * self.rows)
        self.screen = pygame.display.set_mode((self.width, self.height))

    def set_pixel(self, x, y):
        """
        :return: returns True, a pixel was erased. If returns False, nothing was
        erased.
        """
        if x > self.cols:
            x -= self.cols
        elif x < 0:
            x += self.cols

        if y > self.rows:
            y -= self.rows
        elif y < 0:
            y += self.rows

        pixel_locate = x + (y * self.cols)
        self.display[pixel_locate] ^= 1
        return not self.display[pixel_locate]

    def clear(self):
        self.display = [0] * (self.cols * self.rows)

    def render(self):
        for i in range(self.cols * self.rows):
            x = (i % self.cols) * self.scale
            y = (i // self.cols) * self.scale

            if self.display[i] == 1:
                white = 255, 255, 255
                pygame.draw.rect(
                    self.screen, white, (x, y, self.scale, self.scale)
                )

    def main(self):
        self.set_pixel(5, 5)
        self.set_pixel(10, 10)
        self.render()
