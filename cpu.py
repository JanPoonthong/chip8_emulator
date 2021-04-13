class Cpu:
    def __init__(self):
        self.memory = [0] * 4096
        self.v = [0] * 16
        self.i = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.pc = 0x200
        self.stack = []
        self.pause = False
        self.speed = 10

    @staticmethod
    def load_rom(filename, memory, offset):
        rom_data = open(f"roms/{filename}", "rb").read()
        for index, val in enumerate(rom_data):
            memory[offset + index] = val

