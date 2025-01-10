from tkinter import Tk, BOTH, Canvas
from constants import *


class Window():
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title(title)
        self.__root.maxsize(width, height)

        self.display = Canvas(self.__root, width=width, height=height)
        self.display.pack()
        self.running = False

    def draw_line(self, line):
        line.draw(self.display)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
        
        
    def close(self):
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Line():
    def __init__(self, point_from, point_to, color='black', width=1):
        self.point_from = point_from
        self.point_to = point_to
        self.fill = color
        self.width = width

    def draw(self, canvas):
        canvas.create_line(
            self.point_from.x, self.point_from.y, self.point_to.x, self.point_to.y, fill=self.fill, width=self.width
        )
        
class Cell():
    def __init__(self, x, y, height, width, window):
        self.left_wall = True
        self.right_wall = True
        self.bottom_wall = True
        self.top_wall = True

        self.__win = window
        self.__x1 = x
        self.__y1 = y
        self.__x2 = x + width
        self.__y2 = x + height

    def draw_move(self, to_cell, undo=False):
        center_x1 = self.__x1 + ((self.__x2 - self.__x1) / 2)
        center_y1 = self.__y1 + ((self.__y2 - self.__y1) / 2)

        center_x2 = to_cell.__x1 + ((to_cell.__x2 - to_cell.__x1) / 2)
        center_y2 = to_cell.__y1 + ((to_cell.__y2 - to_cell.__y1) / 2)
        if undo:
            color = 'gray'
        else:
            color = 'red'
        self.__win.draw_line(
            Line(Point(center_x1, center_y1), Point(center_x2, center_y2), color=color)
        )

    def draw(self):
        if self.left_wall:
            self.__win.draw_line(
                Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2))
            )
        if self.right_wall:
            self.__win.draw_line(
                Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2))
            )
        if self.top_wall:
            self.__win.draw_line(
                Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1))
            )
        if self.bottom_wall:
            self.__win.draw_line(
                Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2))
            )
