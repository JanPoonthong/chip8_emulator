import pygame
import sys

from tkinter import *
from tkinter.filedialog import askopenfilename
from renderer import Renderer


def file_explorer():
    root = Tk()
    foo = askopenfilename()
    root.destroy()
    return foo


def menu_bar():
    pygame.init()
    color = (0, 0, 255)
    font = pygame.font.SysFont('Corbel', 35)
    text = font.render('quit', True, color)
    Renderer().screen.blit(text, (100, 100))
    return None
