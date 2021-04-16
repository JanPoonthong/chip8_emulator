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

    def load_rom(self, filename):
        rom_data = open(f"roms/{filename}", "rb").read()
        for index, value in enumerate(rom_data):
            self.memory[0x200 + index] = value

    def cycle(self):
        for i in range(self.speed):
            if not self.pause:
                opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
                self.execute_instruction(opcode)

        if not self.pause:
            self.update_timers()

        self.play_sound()
        self.renderer.render()

    def update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        elif self.sound_timer > 0:
            self.sound_timer -= 1

    def play_sound(self):
        # TODO(jan): Implement this funciton
        pass

    def execute_instruction(self, opcode):
        self.pc += 2

        x = (opcode & 0x0F00) >> 8
        y = (opcode & 0x00F0) >> 4
        print(hex(opcode))

        first_hex = opcode & 0xF000
        if first_hex == 0x0000:
            if opcode == 0x00E0:
                self.renderer.clear()
            if opcode == 0x00EE:
                self.pc = self.stack.pop()
        if first_hex == 0x1000:
            self.pc = opcode & 0xFFF
        if first_hex == 0x2000:
            self.stack.append(self.pc)
            self.pc = opcode & 0xFFF
        if first_hex == 0x3000:
            if self.v[x] == opcode & 0xFF:
                self.pc += 2
        if first_hex == 0x4000:
            if self.v[x] != opcode & 0xFF:
                self.pc += 2
        if first_hex == 0x5000:
            if self.v[x] == self.v[y]:
                self.pc += 2
        if first_hex == 0x6000:
            self.v[x] = opcode & 0xFF
        if first_hex == 0x7000:
            self.v[x] += opcode & 0xFF
        if first_hex == 0x8000:
            last_hex = opcode & 0xF
            if last_hex == 0x0:
                self.v[x] = self.v[y]
            if last_hex == 0x1:
                self.v[x] |= self.v[y]
            if last_hex == 0x2:
                self.v[x] &= self.v[y]
            if last_hex == 0x3:
                self.v[x] ^= self.v[y]
            if last_hex == 0x4:
                # TODO(jan): Something might be wrong here
                total = self.v[x] + self.v[y]
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
            self.i = opcode & 0xFFF
        if first_hex == 0xB000:
            self.pc = (opcode & 0xFFF) + self.v[0]
        if first_hex == 0xC000:
            random_number = random.randint(0x0, 0xFF)
            self.v[x] = random_number & (opcode & 0xFF)
        if first_hex == 0xD000:
            pass
        if first_hex == 0xE000:
            last_two_hex =  opcode & 0xFF
            if last_two_hex == 0x9E:
                pass
            if last_two_hex == 0xA1:
                pass
        if first_hex == 0xF000:
            last_two_hex =  opcode & 0xFF
            if last_two_hex == 0x07:
                pass
            if last_two_hex == 0x0A:
                pass
            if last_two_hex == 0x15:
                pass
            if last_two_hex == 0x18:
                pass
            if last_two_hex == 0x1E:
                pass
            if last_two_hex == 0x29:
                pass
            if last_two_hex == 0x33:
                pass
            if last_two_hex == 0x55:
                pass
            if last_two_hex == 0x65:
                pass
