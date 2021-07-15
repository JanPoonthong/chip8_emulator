from tkinter import *
from tkinter.filedialog import askopenfilename


def file_explorer():
    root = Tk()
    foo = askopenfilename()
    root.destroy()
    return foo
