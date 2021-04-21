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
            0xf0,
            0x90,
            0x90,
            0x90,
            0xf0,
            0x20,
            0x60,
            0x20,
            0x20,
            0x70,
            0xf0,
            0x10,
            0xf0,
            0x80,
            0xf0,
            0xf0,
            0x10,
            0xf0,
            0x10,
            0xf0,
            0x90,
            0x90,
            0xf0,
            0x10,
            0x10,
            0xf0,
            0x80,
            0xf0,
            0x10,
            0xf0,
            0xf0,
            0x80,
            0xf0,
            0x90,
            0xf0,
            0xf0,
            0x10,
            0x20,
            0x40,
            0x40,
            0xf0,
            0x90,
            0xf0,
            0x90,
            0xf0,
            0xf0,
            0x90,
            0xf0,
            0x10,
            0xf0,
            0xf0,
            0x90,
            0xf0,
            0x90,
            0x90,
            0xe0,
            0x90,
            0xe0,
            0x90,
            0xe0,
            0xf0,
            0x80,
            0x80,
            0x80,
            0xf0,
            0xe0,
            0x90,
            0x90,
            0x90,
            0xe0,
            0xf0,
            0x80,
            0xf0,
            0x80,
            0xf0,
            0xf0,
            0x80,
            0xf0,
            0x80,
            0x80,
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
        x = (opcode & 0x0f00) >> 8
        y = (opcode & 0x00f0) >> 4
        first_hex = opcode & 0xf000
        last_two_hex = opcode & 0x00ff

        if first_hex == 0x0000:
            if opcode == 0x00e0:
                self.renderer.clear()
            if opcode == 0x00ee:
                self.pc = self.stack.pop()
        if first_hex == 0x1000:
            self.pc = opcode & 0x0fff
        if first_hex == 0x2000:
            self.stack.append(self.pc)
            self.pc = opcode & 0x0fff
        if first_hex == 0x3000:
            if self.v[x] == opcode & 0x00ff:
                self.pc += 2
        if first_hex == 0x4000:
            if self.v[x] != opcode & 0x00ff:
                self.pc += 2
        if first_hex == 0x5000:
            if self.v[x] == self.v[y]:
                self.pc += 2
        if first_hex == 0x6000:
            self.v[x] = opcode & 0x00ff
        if first_hex == 0x7000:
            temp = self.v[x] + (opcode & 0x00ff)
            self.v[x] = temp if temp < 256 else temp - 256
        if first_hex == 0x8000:
            last_hex = opcode & 0x000f
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
                self.v[0xf] = 0
                if total > 0xff:
                    self.v[0xf] = 1
                self.v[x] = total & 0x00ff
            if last_hex == 0x5:
                target_reg = self.v[x]
                if self.v[x] > self.v[y]:
                    target_reg -= self.v[y]
                    self.v[0xf] = 1
                else:
                    target_reg = 256 + target_reg - self.v[y]
                    self.v[0xf] = 0
                self.v[x] = target_reg
            if last_hex == 0x6:
                self.v[0xf] = self.v[x] & 0x1
                self.v[x] >>= 1
            if last_hex == 0x7:
                self.v[0xf] = 0
                if self.v[y] > self.v[x]:
                    self.v[0xf] = 1
                self.v[x] = self.v[y] - self.v[x]
            if last_hex == 0xe:
                self.v[0xf] = self.v[x] & 0x80
                self.v[x] <<= 1
        if first_hex == 0x9000:
            if self.v[x] != self.v[y]:
                self.pc += 2
        if first_hex == 0xa000:
            self.i = opcode & 0x0fff
        if first_hex == 0xb000:
            self.pc = (opcode & 0x0fff) + self.v[0x0]
        if first_hex == 0xc000:
            random_number = random.randint(0x0, 0xff)
            self.v[x] = random_number & (opcode & 0x00ff)
        if first_hex == 0xd000:
            width = 8  # 8 pixels wide, so it's safe to hardcode
            height = opcode & 0x000f
            self.v[0xf] = 0

            for row in range(height):
                sprite = self.memory[self.i + row]
                for col in range(width):
                    if (sprite & 0x0080) > 0x0:
                        if self.renderer.set_pixel(
                            self.v[x] + col, self.v[y] + row
                        ):
                            self.v[0xf] = 1
                    sprite <<= 1
        if first_hex == 0xe000:
            if last_two_hex == 0x9e:
                if self.keyboard.is_key_pressed(self.v[x]):
                    self.pc += 2
            if last_two_hex == 0xa1:
                if not self.keyboard.is_key_pressed(self.v[x]):
                    self.pc += 2
        if first_hex == 0xf000:
            if last_two_hex == 0x07:
                self.v[x] = self.delay_timer
            if last_two_hex == 0x0a:
                self.pause = True
                self.v[x] = self.keyboard.pygame_key_down()
                self.pc -= 2
                self.pause = False
            if last_two_hex == 0x15:
                self.delay_timer = self.v[x]
            if last_two_hex == 0x18:
                self.sound_timer = self.v[x]
            if last_two_hex == 0x1e:
                self.i += self.v[x]
            if last_two_hex == 0x29:
                self.i = self.v[x] * 0x5
            if last_two_hex == 0x33:
                self.memory[self.i] = self.v[x] // 100
                self.memory[self.i + 1] = (self.v[x] // 10) % 10
                self.memory[self.i + 2] = self.v[x] % 10
            if last_two_hex == 0x55:
                for register_index in range(x + 1):
                    self.memory[self.i + register_index] = self.v[
                        register_index
                    ]
            if last_two_hex == 0x65:
                for register_index in range(x + 1):
                    self.v[register_index] = self.memory[
                        self.i + register_index
                    ]
