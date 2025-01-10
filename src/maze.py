from tkinter import Tk, BOTH, Canvas
from constants import *
from component_def import *
import time, random


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win, seed=None):
        self.startx = x1
        self.starty = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = seed
        self._cells = []
        if not seed is None:
            random.seed(seed)

        self._create_cells()

    def _create_cells(self):
        for i in range(self.num_cols):
            column = []
            for j in range(self.num_rows):
                column.append(Cell(self.startx + i * self.cell_size_x, self.starty + j * self.cell_size_x, self.cell_size_x, self.cell_size_y, self.win))
            self._cells.append(column)

        print(self._cells)
        
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

    def _break_entrance_and_exit(self):
        self._cells[0][0].top_wall = False
        self._draw_cell(0,0)
        
        self._cells[-1][-1].bottom_wall = False
        self._draw_cell(-1,-1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        

        while True:
            directions = []
            if i > 0 and not self._cells[i-1][j].visited: directions.append("W")
            if i < self.num_cols - 1 and not self._cells[i+1][j].visited: directions.append("E")
            if j < self.num_rows - 1 and not self._cells[i][j+1].visited: directions.append("S")
            if j > 0 and not self._cells[i][j-1].visited: directions.append("N")

            if not directions:
                break

            direction = random.choice(directions)

            if direction == 'N':
                self._cells[i][j].top_wall = False
                self._cells[i][j - 1].bottom_wall = False
                self._break_walls_r(i, j - 1)

            elif direction == 'S':
                self._cells[i][j].bottom_wall = False
                self._cells[i][j + 1].top_wall = False
                self._break_walls_r(i, j + 1)

            elif direction == 'W':
                self._cells[i][j].left_wall = False
                self._cells[i - 1][j].right_wall = False
                self._break_walls_r(i - 1, j)

            elif direction == 'E':
                self._cells[i][j].right_wall = False
                self._cells[i + 1][j].left_wall = False
                self._break_walls_r(i + 1, j)

        self._draw_cell(i, j)

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False
    

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        # Check if the current cell is the end cell
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        # Possible directions: East, South, West, North
        directions = [("E", i + 1, j), ("S", i, j + 1), ("W", i - 1, j), ("N", i, j - 1)]
        for direction, new_i, new_j in directions:
            if 0 <= new_i < self.num_cols and 0 <= new_j < self.num_rows:
                if not self._cells[new_i][new_j].visited and not self._has_wall(i, j, direction):
                    self._cells[i][j].draw_move(self._cells[new_i][new_j])

                    if self._solve_r(new_i, new_j):
                        return True

                    # Undo move
                    self._cells[i][j].draw_move(self._cells[new_i][new_j], undo=True)

        return False

    def _has_wall(self, i, j, direction):
        if direction == "N":
            return self._cells[i][j].top_wall
        elif direction == "S":
            return self._cells[i][j].bottom_wall
        elif direction == "W":
            return self._cells[i][j].left_wall
        elif direction == "E":
            return self._cells[i][j].right_wall

        return False
