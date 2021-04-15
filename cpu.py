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
