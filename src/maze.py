from tkinter import Tk, BOTH, Canvas
from constants import *
from component_def import *
import time


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self.startx = x1
        self.starty = y1
        self.num_rows = num_rows
        self.num_cols = num_cols - 1
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []

        self._create_cells()

    def _create_cells(self):
        for i in range(self.num_cols):
            column = []
            for j in range(self.num_rows):
                column.append(Cell(self.startx + i * self.cell_size_x, self.starty + j * self.cell_size_x, self.cell_size_x, self.cell_size_y, self.win))
            self._cells.append(column)
        
        # Draw all the cells
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.002)
