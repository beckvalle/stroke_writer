#!/usr/bin/python3

# from https://pycad.co/how-to-draw-on-an-image/

import tkinter as tk
from PIL import Image, ImageTk

top = tk.Tk()
# Code to add widgets will go here...

canvas = tk.Canvas(top, bg='black')
canvas.pack(anchor='nw', fill='both', expand=1)

image = Image.open("cat.jpeg")
image = image.resize((400,400), Image.ANTIALIAS)
image = ImageTk.PhotoImage(image)
canvas.create_image(0,0, image=image, anchor='nw')

def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y

def draw_smth(event):
    global lasx, lasy
    canvas.create_line((lasx, lasy, event.x, event.y), 
                      fill='red', 
                      width=2)
    lasx, lasy = event.x, event.y

canvas.bind("<Button-1>", get_x_and_y)
canvas.bind("<B1-Motion>", draw_smth)

top.mainloop()