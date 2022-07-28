#!/usr/bin/python3

from tkinter import *
from tkinter import ttk

root = Tk()

class Stroke_canvas(Canvas):
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

content = ttk.Frame(root, padding=(3,3,12,12))
# frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
name_lbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)

show_letter_var = BooleanVar()
show_stroke_var = BooleanVar()

show_letter_var.set(True)
show_stroke_var.set(True)

show_letter_bttn = ttk.Checkbutton(content, text="Show letter", 
    variable=show_letter_var, onvalue=True)
show_stroke_bttn = ttk.Checkbutton(content, text="Show stroke", 
    variable=show_stroke_var, onvalue=True)

clear_bttn = ttk.Button(content, text="Clear")
ok_bttn = ttk.Button(content, text="Okay")
cancel_bttn = ttk.Button(content, text="Cancel")

content.grid(column=0, row=0, sticky=(N, S, E, W))

sketch = Stroke_canvas(content)
sketch.grid(column=0, row=0, columnspan=4, rowspan=2, sticky=(N, W, E, S))
sketch.draw_triangle()
sketch.draw_text()

# frame.grid(column=0, row=0, columnspan=4, rowspan=2, sticky=(N, S, E, W))
name_lbl.grid(column=4, row=0, columnspan=2, sticky=(N, W), padx=5)
name.grid(column=4, row=1, columnspan=2, sticky=(N,E,W), pady=5, padx=5)
show_letter_bttn.grid(column=0, row=3)
show_stroke_bttn.grid(column=1, row=3)
clear_bttn.grid(column=2, row=3)
ok_bttn.grid(column=3, row=3)
cancel_bttn.grid(column=4, row=3)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)

root.mainloop()