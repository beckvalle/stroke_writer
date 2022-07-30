#!/usr/bin/python3

import csv
from tkinter import *
from tkinter import ttk
from os.path import exists

# create the main application window
root = Tk()
root.geometry("700x400")

def close_window(window):
    window.destroy()

show_outline_var = BooleanVar()
show_arrows_var = BooleanVar()
stroke_number_var = IntVar()
current_letter_var = StringVar()

show_outline_var.set(True)
show_arrows_var.set(True)
stroke_number_var.set(0)
current_letter_var.set('')

class Stroke_canvas(Canvas):

    def __init__(self, parent, language, height, width, **kwargs):
        super().__init__(parent, **kwargs)
        self.language = language
        self.height = height
        self.width = width
        self.csvfile_name = self.language+'_stk.csv'
        self.fieldnames = ["symbol_name", "strokes"]
        self.letter_loaded = False
        self.point_color = "blue"
        self.stroke_end_id_holder = []
        self.stroke_line_id_holder = []
        self.coords_holder = []
        self.single_stroke_holder = []
        self.loaded_stroke_id_holder = []

        self.setup_language()
        self.draw_vert_grid()
        self.draw_hor_guides()
        # bind mouse movement to draw functions within canvas
        self.bind("<Button-1>", self.save_posn)
        self.bind("<Button-1>", self.change_pt_color_to_red, add='+')
        self.bind("<Button-1>", self.add_circle, add='+')
        self.bind("<B1-Motion>", self.add_line)
        self.bind("<B1-ButtonRelease>", self.change_pt_color_to_red)
        self.bind("<B1-ButtonRelease>", self.add_circle, add='+')
        self.bind("<B1-ButtonRelease>", self.increment_stroke, add='+')

    def save_posn(self, event):
        self.lastx, self.lasty = event.x, event.y
        self.single_stroke_holder.append(str(event.x))
        self.single_stroke_holder.append(str(event.y))

    def add_line(self, event):
        self.stroke_line_id_holder.append(
            self.create_line((self.lastx, self.lasty, event.x, event.y), 
                width=10, fill="red"))
        self.save_posn(event)

    def add_circle(self, event):
        self.stroke_end_id_holder.append(
            self.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, 
                fill=self.point_color, outline=""))

    def increment_stroke(self, event):
        stroke_number_var.set(stroke_number_var.get()+1)
        stroke_num_lbl.config(text="Stroke: "+str(stroke_number_var.get()))
        self.coords_holder.append((';').join(self.single_stroke_holder))
        self.single_stroke_holder = []
        
    def clear_stroke(self):
        self.stroke_end_id_holder = []
        self.stroke_line_id_holder = []
        self.coords_holder = []
        stroke_number_var.set(0)
        stroke_num_lbl.config(text="Stroke: ")

    def clear_written_strokes(self):
        for id in self.stroke_line_id_holder:
            self.delete(id)
        for id in self.stroke_end_id_holder:
            self.delete(id)
        self.clear_stroke()

    def setup_language(self):
        if not (exists(self.csvfile_name)):
            with open(self.csvfile_name, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=self.fieldnames)
                writer.writeheader()

    def handle_stroke_storage(self):
        def store_stroke():
            ret_val = return_val.get()
            with open(self.csvfile_name, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=self.fieldnames)
                writer.writerow({"symbol_name":ret_val, "strokes":('-').join(self.coords_holder)})
            close_window(message_window)
            self.clear_written_strokes()

        message_window = Toplevel(root)
        message_window.grab_set()
        Label(message_window, text= "Enter the letter/symbol name!").grid(row=0, column=0)
        return_val = Entry(message_window)
        return_val.grid(row=1, column=0)
        submit_bttn = ttk.Button(message_window, text="Submit", command=store_stroke).grid(row=2, column=0)
        cancel_bttn = ttk.Button(message_window, text="Cancel", command=lambda: close_window(message_window)).grid(row=2, column=1)

    def set_current_letter(self, in_letter):
        current_letter_var.set(in_letter)
        self.letter_loaded = True
        self.show_outline()

    def load_strokes(self):
        # choose_window = Toplevel(root)
        # choose_bttn = ttk.Button(choose_window, text="A").grid(row=0, column=0)
        self.show_load_options()

        # if (exists(self.csvfile_name)):
        #     pass
        # else:
        #     close_window(choose_window)

    def show_load_options(self):
        choose_window = Toplevel(root)
        col_ct = 0
        row_ct = 0
        button_ids = []
        with open(self.csvfile_name, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                button_letter = row['symbol_name']
                button_id = ttk.Button(choose_window, text=button_letter, command = lambda text=button_letter:self.set_current_letter(text))
                button_ids.append(button_id)

            for bid in button_ids:
                bid.grid(column=col_ct, row=row_ct)
                col_ct +=1
                if col_ct > 4:
                    col_ct = 0
                    row_ct += 1
                
    def show_outline(self):
        if self.letter_loaded:
            clear_canvas()
            if show_outline_var.get():
                with open(self.csvfile_name, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if row['symbol_name'] == current_letter_var.get():
                            hint_lbl['text'] = current_letter_var.get()
                            for stroke in row['strokes'].split('-'):
                                if show_arrows_var.get():
                                    self.create_line(*stroke.split(';'), 
                                        width=3, fill="grey", arrow=LAST, arrowshape=(10, 20, 10))
                                else:
                                    self.create_line(*stroke.split(';'), 
                                        width=3, fill="grey")
                    


    def change_pt_color_to_red(self, event):
        self.point_color = 'red'

    def change_pt_color_to_blue(self, event):
        self.point_color = 'blue'

    def draw_vert_grid(self):
        self.create_line((0, 50, 400, 50), width=3, fill='light grey')
        self.create_line((0, 100, 400, 100), width=3, fill='light grey')
        self.create_line((0, 150, 400, 150), width=3, fill='light grey')
    
    def draw_hor_guides(self):
        self.create_line((150, 0, 150, 400), width=3, fill='light grey',  dash=(10,5))
        self.create_line((250, 0, 250, 400), width=3, fill='light grey',  dash=(10,5))

content = ttk.Frame(root, padding=(3,3,12,12))
name_lbl = ttk.Label(content, text="Prompt: ")
hint_lbl = ttk.Label(content, font=("Arial", 50))
stroke_num_lbl = ttk.Label(content, text="Stroke: ")

sketch = Stroke_canvas(content, language="EN", height=100, width=400)
# sketch.grid(column=0, row=0, columnspan=4, rowspan=2, sticky=(N, W, E, S))
sketch.grid(column=0, row=0, columnspan=4, rowspan=2)
sketch.grid_propagate(0)
# sketch.grid(column=0, row=0, columnspan=4, rowspan=2)

def clear_canvas():
    sketch.delete('all')
    sketch.draw_hor_guides()
    sketch.draw_vert_grid()
    stroke_number_var.set(0)
    stroke_num_lbl.config(text="Stroke: ")
    sketch.clear_stroke()
    hint_lbl['text'] = ''

show_outline_bttn = ttk.Checkbutton(content, text="Outline", 
    variable=show_outline_var, onvalue=True, command=sketch.show_outline)
show_arrows_bttn = ttk.Checkbutton(content, text="Arrows", 
    variable=show_arrows_var, onvalue=True, command=sketch.show_outline)

clear_stroke_bttn = ttk.Button(content, text="Clear Stroke", command=sketch.clear_written_strokes)
clear_bttn = ttk.Button(content, text="Clear All", command=clear_canvas)
load_bttn = ttk.Button(content, text="Load", command=sketch.load_strokes)
store_bttn = ttk.Button(content, text="Store", command=sketch.handle_stroke_storage)
exit_bttn = ttk.Button(content, text="Exit", command=lambda: close_window(root))

name_lbl.grid(column=4, row=0, columnspan=2, sticky=(N, W), padx=5)
hint_lbl.grid(column=4, row=1, columnspan=2, sticky=(N, W), padx=5)
stroke_num_lbl.grid(column=4, row=2, columnspan=2, sticky=(N, W), padx=5)
show_outline_bttn.grid(column=0, row=3)
show_arrows_bttn.grid(column=1, row=3)
clear_stroke_bttn.grid(column=2, row=3)
clear_bttn.grid(column=3, row=3)
load_bttn.grid(column=4, row=3)
store_bttn.grid(column=5, row=3)
exit_bttn.grid(column=6, row=3)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.grid(column=0, row=0)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.columnconfigure(5, weight=1)
content.columnconfigure(6, weight=1)
content.rowconfigure(1, weight=1)

root.mainloop()