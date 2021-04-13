import pygame


class Keyboard:
    def __init__(self):
        self.keymap = {
            0x1: pygame.K_1,  # 1
            0x2: pygame.K_2,  # 2
            0x3: pygame.K_3,  # 3
            0xc: pygame.K_4,  # 4
            0x4: pygame.K_q,  # Q
            0x5: pygame.K_w,  # W
            0x6: pygame.K_e,  # E
            0xD: pygame.K_r,  # R
            0x7: pygame.K_a,  # A
            0x8: pygame.K_s,  # S
            0x9: pygame.K_d,  # D
            0xE: pygame.K_f,  # F
            0xA: pygame.K_z,  # Z
            0x0: pygame.K_x,  # X
            0xB: pygame.K_c,  # C
            0xF: pygame.K_v  # V
        }
        self.key_pressed = pygame.key.get_pressed()
        self.on_next_key_press = None

    def listener(self, event):
        if event.type == pygame.KEYDOWN:
            print(event.key, event.unicode)
