#!/usr/bin/python3

# example from https://tkdocs.com/tutorial/canvas.html

from tkinter import *
from tkinter import ttk

class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.save_posn)
        self.bind("<B1-Motion>", self.add_line)
        
    def save_posn(self, event):
        self.lastx, self.lasty = event.x, event.y

    def add_line(self, event):
        self.create_line((self.lastx, self.lasty, event.x, event.y))
        self.save_posn(event)

    def draw_triangle(self):
        self.create_polygon(10, 10, 200, 50, 10, 50, fill='red', outline='blue')

    def draw_text(self):
        self.create_text(100, 100, text='sample text', 
        anchor='nw', font='TkMenuFont', fill='black')


root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sketch = Sketchpad(root)
sketch.grid(column=0, row=0, sticky=(N, W, E, S))
sketch.draw_triangle()
sketch.draw_text()

root.mainloop()