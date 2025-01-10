from tkinter import Tk, BOTH, Canvas
from constants import *
from component_def import Window, Cell
from maze import *

def main():
    win = Window(800, 600, "Title1")
    
    maze = Maze(10, 10, 11, 11, 50, 50, win)
    maze._break_entrance_and_exit()
    
    win.wait_for_close()

main()