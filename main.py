class Emulator:
    def __init__(self):
        self.memory = [0] * 4096
        self.register = [0] * 16
        self.sound_timer = 0
        self.delay_timer = 0
        self.program_counter = 0
        self.index = 0
        self.stack = []


class Input:
    def __init__(self):
        self.keyboard = [0] * 16


class Output:
    def __init__(self):
        self.column = 64
        self.row = 32
        self.display = [0] * self.column * self.row

    def set_pixel(self, x, y):
        if x > self.column:
            x -= self.column
        elif x < 0:
            x += self.column

        if y > self.row:
            y -= self.row
        elif y < 0:
            y += self.row

        return self.display[x + (y * self.column)] != 1

    def clear(self):
        return self.display
