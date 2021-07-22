import pygame


class Keyboard:
    def __init__(self):
        self.key_map = {
            pygame.K_1: 0x1,
            pygame.K_2: 0x2,
            pygame.K_3: 0x3,
            pygame.K_4: 0xC,
            pygame.K_q: 0x4,
            pygame.K_w: 0x5,
            pygame.K_e: 0x6,
            pygame.K_r: 0xD,
            pygame.K_a: 0x7,
            pygame.K_s: 0x8,
            pygame.K_d: 0x9,
            pygame.K_f: 0xE,
            pygame.K_z: 0xA,
            pygame.K_x: 0x0,
            pygame.K_c: 0xB,
            pygame.K_v: 0xF,
        }
        self.key_pressed = [0] * 16

    def pygame_key_down(self, event):
        if event.key in self.key_map.keys():
            key = self.key_map[event.key]
            self.key_pressed[key] = True
            return key

    def pygame_key_up(self, event):
        if event.key in self.key_map.keys():
            key = self.key_map[event.key]
            self.key_pressed[key] = False

    def is_key_pressed(self, key_code):
        return self.key_pressed[key_code]
