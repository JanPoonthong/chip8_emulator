import random


class Cpu:
    def __init__(self, renderer, keyboard):
        self.renderer = renderer
        self.keyboard = keyboard
        self.memory = [0] * 4096
        self.v = [0] * 16
        self.i = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.pc = 0x200
        self.stack = []
        self.pause = False
        self.speed = 10

    def load_sprites_into_memory(self):
        sprites = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80   # F
        ]

        for i in range(len(sprites)):
            self.memory[i] = sprites[i]

    def load_rom(self, filename, offset):
        rom_data = open(f"c8games/{filename}", "rb").read()
        for index, value in enumerate(rom_data):
            self.memory[offset + index] = value

    def cycle(self):
        for i in range(self.speed):
            if not self.pause:
                opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
                self.execute_instruction(opcode)

        if not self.pause:
            self.update_timers()

        self.renderer.render()

    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        elif self.sound_timer > 0:
            self.sound_timer -= 1

    def execute_instruction(self, opcode):
        self.pc += 2
        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        first_hex = opcode & 0xF000
        last_two_hex = opcode & 0x00FF

        if first_hex == 0x0000:
            if opcode == 0x00E0:
                self.renderer.clear()
            if opcode == 0x00EE:
                self.pc = self.stack.pop()
        if first_hex == 0x1000:
            self.pc = opcode & 0x0FFF
        if first_hex == 0x2000:
            self.stack.append(self.pc)
            self.pc = opcode & 0x0FFF
        if first_hex == 0x3000:
            if self.v[x] == opcode & 0x00FF:
                self.pc += 2
        if first_hex == 0x4000:
            if self.v[x] != opcode & 0x00FF:
                self.pc += 2
        if first_hex == 0x5000:
            if self.v[x] == self.v[y]:
                self.pc += 2
        if first_hex == 0x6000:
            self.v[x] = opcode & 0x00FF
        if first_hex == 0x7000:
            self.v[x] += opcode & 0x00FF
        if first_hex == 0x8000:
            last_hex = opcode & 0x000F
            if last_hex == 0x0:
                self.v[x] = self.v[y]
            if last_hex == 0x1:
                self.v[x] |= self.v[y]
            if last_hex == 0x2:
                self.v[x] &= self.v[y]
            if last_hex == 0x3:
                self.v[x] ^= self.v[y]
            if last_hex == 0x4:
                self.v[x] += self.v[y]
                total = self.v[x]
                self.v[0xF] = 0
                if total > 0xFF:
                    self.v[0xF] = 1
                self.v[x] = total
            if last_hex == 0x5:
                self.v[0xF] = 0
                if self.v[x] > self.v[y]:
                    self.v[0xF] = 1
                self.v[x] -= self.v[y]
            if last_hex == 0x6:
                self.v[0xF] = self.v[x] & 0x1
                self.v[x] >>= 1
            if last_hex == 0x7:
                self.v[0xF] = 0
                if self.v[y] > self.v[x]:
                    self.v[0xF] = 1
                self.v[x] = self.v[y] - self.v[x]
            if last_hex == 0xE:
                self.v[0xF] = self.v[x] & 0x80
                self.v[x] <<= 1
        if first_hex == 0x9000:
            if self.v[x] != self.v[y]:
                self.pc += 2
        if first_hex == 0xA000:
            self.i = opcode & 0x0FFF
        if first_hex == 0xB000:
            self.pc = (opcode & 0x0FFF) + self.v[0x0]
        if first_hex == 0xC000:
            random_number = random.randint(0x0, 0xFF)
            self.v[x] = random_number & (opcode & 0x00FF)
        if first_hex == 0xD000:
            # Width of the sprite are 8 pixels wide, so it's safe to hardcode
            width = 8
            height = opcode & 0x000F
            self.v[0xF] = 0

            for row in range(height):
                sprite = self.memory[self.i + row]
                for col in range(width):
                    if (sprite & 0x0080) > 0x0:
                        if self.renderer.set_pixel(
                            self.v[x] + col, self.v[y] + row
                        ):
                            self.v[0xF] = 1
                    sprite <<= 1
        if first_hex == 0xE000:
            if last_two_hex == 0x9E:
                if self.keyboard.is_key_pressed(self.v[x]):
                    self.pc += 2
            if last_two_hex == 0xA1:
                if not self.keyboard.is_key_pressed(self.v[x]):
                    self.pc += 2
        if first_hex == 0xF000:
            if last_two_hex == 0x07:
                self.v[x] = self.delay_timer
            if last_two_hex == 0x0A:
                self.pause = True
                self.v[x] = self.keyboard.pygame_key_down()
                self.pc -= 2
                self.pause = False
            if last_two_hex == 0x15:
                self.delay_timer = self.v[x]
            if last_two_hex == 0x18:
                self.sound_timer = self.v[x]
            if last_two_hex == 0x1E:
                self.i += self.v[x]
            if last_two_hex == 0x29:
                self.i = self.v[x] * 0x5
            if last_two_hex == 0x33:
                self.memory[self.i] = self.v[x] // 100
                self.memory[self.i + 1] = (self.v[x] % 100) // 10
                self.memory[self.i + 2] = self.v[x] % 10
            if last_two_hex == 0x55:
                for register_index in range(x):
                    self.memory[self.i + register_index] = self.v[
                        register_index
                    ]

            if last_two_hex == 0x65:
                for register_index in range(x):
                    self.v[register_index] = self.memory[
                        self.i + register_index
                    ]
