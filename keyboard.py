import pygame


class Keyboard:
    def __init__(self):
        self.key_map = {
            pygame.K_1: 0x1,  # 1
            pygame.K_2: 0x2,  # 2
            pygame.K_3: 0x3,  # 3
            pygame.K_4: 0xc,  # 4
            pygame.K_q: 0x4,  # Q
            pygame.K_w: 0x5,  # W
            pygame.K_e: 0x6,  # E
            pygame.K_r: 0xD,  # R
            pygame.K_a: 0x7,  # A
            pygame.K_s: 0x8,  # S
            pygame.K_d: 0x9,  # D
            pygame.K_f: 0xE,  # F
            pygame.K_z: 0xA,  # Z
            pygame.K_x: 0x0,  # X
            pygame.K_c: 0xB,  # C
            pygame.K_v: 0xF   # V
        }
        self.key_pressed = pygame.key.get_pressed()
        self.on_next_key_press = None

    def listener(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_map.keys():
                print(event.unicode)
            else:
                print("Invalid key")
